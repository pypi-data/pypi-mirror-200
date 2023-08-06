import asyncio
import copy
import pickle
import time
import random

import ceylon


class Processor:
    def __init__(self, name, func, filters=None, accept_agent_type=None):
        if filters is None:
            filters = []
        self.agent = None
        self.name = name
        self.func = func
        self.filters = filters
        self.accept_agent_type = accept_agent_type

    def set_agent(self, agent):
        self.agent = agent

    async def __call__(self, message):
        for f in self.filters:
            if not await f(message):
                return None
        if self.accept_agent_type and message.sender_type != self.accept_agent_type:
            return None
        return await self.func(self.agent, message.data)


class Background:
    def __init__(self, agent, name, func):
        self.agent = agent
        self.name = name
        self.func = func

    async def __call__(self, *args, **kwargs):
        return await self.func(self.agent, *args, **kwargs)


class Message:
    def __init__(self, agent_id, agent_type, agent_name, data, _id=None):
        self.id = _id if _id else agent_id + "/" + str(time.time())
        self.sender_id = agent_id
        self.sender_name = agent_name
        self.sender_type = agent_type
        self.data = data

    @staticmethod
    def decode(data):
        try:
            data = pickle.loads(data)
            if "id" in data and "data" in data:
                return Message(
                    _id=data["id"],
                    agent_id=data["sender_id"],
                    agent_name=data["sender_name"],
                    agent_type=data["sender_type"],
                    data=data["data"]
                )
        except Exception as e:
            return None

    def encode(self):
        return pickle.dumps({
            "id": self.id,
            "data": self.data,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "sender_type": self.sender_type
        })


class AgentWrapper:
    def __init__(self, agent, agent_stack_name, name, agent_index, background_processors, message_processors=None):
        if message_processors is None:
            message_processors = {}
        pubsub = ceylon.ceylon.PubSub()
        self.agent = agent
        self.agent.name = name
        self.agent.agent_stack_name = agent_stack_name
        self.agent.index = agent_index
        self.agent.id = pubsub.get_node_id()
        self.pubsub = pubsub
        self.background_processors = background_processors
        self.message_processors = {}
        for name, processor in message_processors.items():
            processor.set_agent(self.agent)
            self.message_processors[name] = processor

        self.agent.send = self.send
        # self.agent.send = self.send

    def send(self, topic, message):
        msg_data = Message(self.agent.id, self.agent.agent_stack_name, self.agent.name, message)
        res = self.pubsub.publish(f"{self.agent.id}/{topic}", msg_data.encode())
        return message

    async def __subscribe_to_pubsub__(self, debug=False):
        # async def process_message(agent_name, data, status):
        async def process_message(data, status, sender_id, publisher_id, topic, *args, **kwargs):
            if debug:
                ceylon.log.info(f"{self.agent.id}/{self.agent.name} Agent callback received: {data}")
            message: Message = Message.decode(data)
            # print(f"{self.agent.id}/{self.agent.name} Agent callback received")
            if message is not None:
                processors = [asyncio.create_task(processor(message)) for processor in
                              self.message_processors.values()]
                await asyncio.sleep(0.00000000001)
                await asyncio.gather(*processors)

        self.pubsub.subscribe("agent_topic", self.agent.id, self.agent.name, process_message)
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

    def register(self, name=None, number_of_agents=1):
        def decorator(cls):
            self.number_of_agents = number_of_agents
            self.__agent__name = name or cls.__name__
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

    def processor(self, name=None, filters=None, agent_type=None):
        def decorator(func):
            _name = name or func.__name__
            self.__message_processors[_name] = Processor(_name, func, filters=filters, accept_agent_type=agent_type)
            return func

        return decorator

    def build_agent(self, agent_index=0) -> AgentWrapper:
        agent_class = self.__agent__cls()
        message_processors = self.__message_processors
        background_processors = self.__background_processors
        agent_type = self.__agent__name
        agent_name = f"{agent_type}-{agent_index}"
        agent_index = f"{agent_index}"
        agent = AgentWrapper(agent_class, agent_type, agent_name, int(agent_index),
                             background_processors,
                             copy.deepcopy(message_processors))
        return agent

    def run(self):
        agents = [self.build_agent(i) for i in range(self.number_of_agents)]
        if len(agents) > 1:
            ceylon.log.warning("We are not supporting multiple agents from here please use the CeylonAI class")
        agent = agents[0]
        run_agent(agent)


def run_agent(agent: AgentWrapper):
    asyncio.run(agent.run(debug=False))
