import asyncio
import copy
import logging
import multiprocessing
import os
import random
import time

import ceylon.ceylon
from art import text2art

from .agent_wrapper import Message

my_art = text2art("Ceylon-AI", font='tarty1')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("ceylon.ai", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("version 0.2.5", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("RAKUN-MAS")

from .ceylon import *

__doc__ = ceylon.__doc__
if hasattr(ceylon, "__all__"):
    __all__ = ceylon.__all__

from .agentdecorator import AgentDecorator


# from .agent_manager import CeylonAI


def run_agent(agent):
    asyncio.run(agent.run(debug=False))


class AgentWrapper:
    def __init__(self, agent, name, agent_index, background_processors, message_processors):
        pubsub = ceylon.ceylon.PubSub()
        self.agent = agent
        self.agent.name = name
        self.agent.index = agent_index
        self.agent.id = pubsub.get_node_id()
        self.pubsub = pubsub
        self.background_processors = background_processors
        self.message_processors = message_processors

        self.agent.send = self.send
        # self.agent.send = self.send

    def send(self, topic, message):
        msg_data = Message(self.agent.id, message)
        msg = ceylon.python_string_to_vec_u8(msg_data.encode())
        res = self.pubsub.publish(f"{self.agent.id}/{topic}", msg)
        return message

    async def __subscribe_to_pubsub__(self, debug=False):
        async def process_message(data):
            if debug:
                log.info(f"{self.agent.id}/{self.agent.name} Agent callback received: {data}")
            message: Message = Message.decode(data)
            if message is not None:
                processors = [asyncio.create_task(processor(self.agent, message.message)) for processor in
                              self.message_processors.values()]
                await asyncio.gather(*processors)

        self.pubsub.subscribe("agent_topic", process_message)
        await self.pubsub.start()

    async def run(self, debug=False):
        sleep_duration = random.uniform(0.5, 2.5)
        await asyncio.sleep(sleep_duration)
        if hasattr(self.agent, "setup_method") and self.agent.setup_method is not None:
            await self.agent.setup_method()

        sub_tx = asyncio.create_task(self.__subscribe_to_pubsub__(debug=debug))

        background_tasks = []
        for name, processor in self.background_processors.items():
            background_tasks.append(asyncio.create_task(processor(self.agent)))

        await asyncio.gather(sub_tx, *background_tasks)


class CeylonAIAgent:

    def __init__(self, order=0):
        self.__agent__cls = None
        self.__agent_initial_method = None
        self.__message_processors = {}
        self.__background_processors = {}
        self.number_of_agents = 1
        self.__agent__name = None
        self.order = order

    def register(self, name, number_of_agents=1):
        def decorator(cls):
            self.number_of_agents = number_of_agents
            self.__agent__name = name
            self.__agent__cls = cls
            self.__agent__cls.setup_method = self.__agent_initial_method
            return cls

        return decorator

    def init(self):
        def decorator(func):
            self.__agent_initial_method = func
            return func

        return decorator

    def background(self, name=None):
        def decorator(func):
            _name = name or func.__name__
            self.__background_processors[_name] = func
            return func

        return decorator

    def processor(self, name=None):
        def decorator(func):
            _name = name or func.__name__
            self.__message_processors[_name] = func
            return func

        return decorator

    def build_agent(self, agent_index=0) -> AgentWrapper:
        agent_class = self.__agent__cls()
        message_processors = self.__message_processors
        background_processors = self.__background_processors
        agent_name = self.__agent__name
        agent_name = f"{agent_name}-{agent_index}"
        agent_index = f"{agent_index}"
        agent = AgentWrapper(agent_class, agent_name, int(agent_index), background_processors,
                             message_processors)
        return agent

    def run(self):
        agents = [self.build_agent(i) for i in range(self.number_of_agents)]
        if len(agents) > 1:
            log.warning("We are not supporting multiple agents from here please use the CeylonAI class")
        agent = agents[0]
        run_agent(agent)


class CeylonAI:

    def __init__(self):
        self.__agents: [CeylonAIAgent] = []

    def agent(self, order=0):
        agent = CeylonAIAgent(order=order)
        temp_agents = [agent, *self.__agents]
        self.__agents = reversed(sorted(temp_agents, key=lambda x: x.order))
        return agent

    def register_agent(self, agent):
        self.__agents.append(agent)

    def run(self, debug=False):
        try:

            agent_objects = []
            for agent in self.__agents:
                agent: CeylonAIAgent = agent
                _number_of_agents = agent.number_of_agents
                for i in range(_number_of_agents):
                    agent_objects.append(agent.build_agent(i))
            print("Starting Agents")
            print("=====================================")
            agent_tx = []
            for agent in agent_objects:
                print(f"Create {agent} {agent.agent} Agent")
                task = multiprocessing.Process(target=run_agent, args=(agent,))
                task.start()
                agent_tx.append(task)

            for task in agent_tx:
                task.join()
        except KeyboardInterrupt:
            print("Bye Bye")
            exit(0)
