import multiprocessing

from ceylon import CeylonAIAgent, run_agent


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
            agent_tx = []
            for agent in agent_objects:
                task = multiprocessing.Process(target=run_agent, args=(agent,))
                task.start()
                agent_tx.append(task)

            for task in agent_tx:
                task.join()
        except KeyboardInterrupt:
            print("Bye Bye")
            exit(0)
