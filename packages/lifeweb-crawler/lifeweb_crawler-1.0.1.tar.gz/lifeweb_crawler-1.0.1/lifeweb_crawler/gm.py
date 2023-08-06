import os

class Config:
    EDGE_SERVER = os.getenv("EDGE_SERVER")

    def __init__(self, **kwargs):

        pass


connection = Config()
