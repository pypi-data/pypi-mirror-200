import pickle
import time


class Processor:
    def __init__(self, agent, name, func):
        self.agent = agent
        self.name = name
        self.func = func

    async def __call__(self, message):
        return await self.func(self.agent, message)


class Background:
    def __init__(self, agent, name, func):
        self.agent = agent
        self.name = name
        self.func = func

    async def __call__(self, *args, **kwargs):
        return await self.func(self.agent, *args, **kwargs)


class Message:
    def __init__(self, agent_id, message):
        self.id = agent_id + "/" + str(time.time())
        self.message = message

    @staticmethod
    def decode(data):
        try:
            data = pickle.loads(data)
            if "id" in data and "message" in data:
                return Message(data["id"], data["message"])
        except Exception as e:
            return None

    def encode(self):
        return pickle.dumps({"id": self.id, "message": self.message})
