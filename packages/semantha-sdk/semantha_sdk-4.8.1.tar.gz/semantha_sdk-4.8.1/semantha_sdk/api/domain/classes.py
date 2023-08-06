from semantha_sdk import RestClient
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model import Class
from semantha_sdk.response import SemanthaPlatformResponse


class ClassEndpoint(SemanthaAPIEndpoint):
    """ Endpoint for a specific class.

        Allows for accessing class instances.
    """

    def __init__(self, session: RestClient, parent_endpoint: str, classid: str):
        super().__init__(session, parent_endpoint)
        self.__classid = classid

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self.__classid}"

    def get_instance(self):
        """ (Not yet implemented) Get all instances of the class """
        raise NotImplementedError("Not  yet implemented!")
        return self.__sesssion.get(self._endpoint).execute()

    def delete_instance(self):
        """ (Not yet implemented) Delete all instances of the class """
        raise NotImplementedError("Not  yet implemented!")
        return self.__sesssion.delete(self._endpoint).execute()


class ClassesEndpoint(SemanthaAPIEndpoint):
    """ Endpoint for the classes in a domain.

        References: Specific api for specific classes

    """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/classes"

    def get_classes(self) -> SemanthaPlatformResponse:
        """ (Not yet implemented) Get all classes """
        raise NotImplementedError("Not  yet implemented!")
        return self._session.get(self._endpoint).execute()

    def post_classes(self, classes: list[Class]) -> SemanthaPlatformResponse:
        """ (Not yet implemented) Create one or more classes """
        raise NotImplementedError("Not  yet implemented!")
        body = [_class.data for _class in classes]
        return self._session.post(self._endpoint, ).execute()

    def delete_classes(self) -> SemanthaPlatformResponse:
        """ (Not yet implemented) Delete all classes """
        raise NotImplementedError("Not  yet implemented!")
        return self._session.delete(self._endpoint).execute()

    def get_class(self, classid: str):
        """ (Not yet implemented) Get a specific class by id """
        raise NotImplementedError("Not  yet implemented!")
        return ClassEndpoint(self._session, self._endpoint, classid)

    def put_class(self, _class: Class):
        """ (Not yet implemented) Add a given class """
        raise NotImplementedError("Not  yet implemented!")
        body = _class.data
        return self._session.put(self._endpoint, body).execute()

    def delete_class(self, classid: str):
        """ (Not yet implemented) Delete a class given its class id """
        raise NotImplementedError("Not  yet implemented!")
        return self._session.delete(self._endpoint + f"/{classid}").execute()
