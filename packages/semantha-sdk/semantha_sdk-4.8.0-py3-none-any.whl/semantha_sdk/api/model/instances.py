from semantha_sdk.rest.rest_client import RestClient


class InstancesEndpoint:
    def __init__(self, session: RestClient, api_endpoint: str):
        self.__session = session
        self.__api_endpoint = api_endpoint

    def get(self):
        """ (Not yet implemented) """
        raise NotImplementedError("Not yet implemented!")
        return self.__session.get(self.__api_endpoint).execute()

    def post(self, body: dict):
        """ (Not yet implemented) """
        raise NotImplementedError("Not yet implemented!")
        return self.__session.post(self.__api_endpoint, ).execute()
