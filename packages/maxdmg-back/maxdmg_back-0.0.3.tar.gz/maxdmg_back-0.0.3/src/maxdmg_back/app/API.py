from .Factories import APIFactory


class API():
    def __init__(self):
        pass

    def RegisterFrontendAPI(self, api):
        pass

    def NewUser(self):
        pass

    def AcceptInput(self, input):
        pass


def Get():
    return APIFactory.Make()

