from pydantic import BaseSettings as Settings



class Config(Settings):
    """
        Config is main the configuration to be passed client object.

        endpoint_url: To connect crawler service
        token: To authenticate crawler service securely
    """

    endpoint_url: str
    token: str

