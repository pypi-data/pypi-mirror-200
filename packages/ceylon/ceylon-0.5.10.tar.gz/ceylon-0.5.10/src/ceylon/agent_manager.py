import asyncio
import copy

from ceylon.agent_wrapper import AgentWrapper


class CeylonAI:

    def __init__(self):
        self._agents = {}

    def register(self, name, number_of_agents=1):
        # agent_data: AgentWrapper = AgentWrapper(name)
        agent_list = [AgentWrapper(f"{name}-{i}") for i in range(number_of_agents)]

        def decorator(cls):
            for agent_data in agent_list:
                agent_data.set_agent(cls)
                self._agents[agent_data.name] = agent_data
            return cls

        def init(func):
            for agent_data in agent_list:
                agent_data.set_init(copy.copy(func))
            return func

        decorator.init = init

        def processor(name):
            def _decorator(func):
                for agent_data in agent_list:
                    agent_data.add_processor(name, copy.copy(func))
                return func

            return _decorator

        decorator.processor = processor

        def background(name):
            def _decorator(func):
                for agent_data in agent_list:
                    agent_data.add_background(name, copy.copy(func))
                return func

            return _decorator

        decorator.background = background

        return decorator

    async def __start__(self):
        agents_tsk = [asyncio.create_task(agent_data.start_agent()) for agent_data in self._agents.values()]
        await asyncio.gather(*agents_tsk)

    async def __finish__(self):
        print("finish")

    def start(self):
        try:
            # your code here
            asyncio.run(self.__start__())
        except KeyboardInterrupt:
            asyncio.run(self.__finish__())
        finally:
            print("finally")
