from .          import Models as M
from .Context   import Context


class StorageInterface():
    def __init__(self):
        pass
    def HasUser(self, user_id: M.ID) -> bool: 
        return NotImplemented
    def AssertUser(self, user_id: M.ID) -> None:
        raise NotImplementedError
    def AddUser(self, user_id: M.ID) -> None:
        raise NotImplementedError
    def DeleteUser(user_id: M.ID) -> None:
        raise NotImplementedError
    def GetUserContext(self, user_id: M.ID) -> Context:
        raise NotImplementedError

