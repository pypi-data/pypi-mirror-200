from .StorageInterface  import StorageInterface
from .                  import Models as M
from .Context           import Context
from typing             import Dict


class ActiveUsers(StorageInterface):
    def __init__(self, storage: StorageInterface):
        self.storage : StorageInterface = storage
        self.user_context_cache : Dict[M.ID, Context] = dict()

    def HasUser(self, user_id: M.ID) -> bool: 
        return self.storage.HasUser(user_id)

    def AssertUser(self, user_id: M.ID) -> None: 
        self.storage.AssertUser(user_id)

    def AddUser(self, user_id: M.ID) -> None: 
        return self.storage.AddUser(user_id)
    
    def DeleteUser(self, user_id: M.ID) -> None:
        if user_id in self.user_context_cache:
            self.user_context_cache.pop(user_id)
        self.storage.DeleteUser(user_id)

    def ResetUser(self, user_id: M.ID) -> None:
        if user_id in self.user_context_cache:
            self.user_context_cache.pop(user_id)
        self.storage.ResetUser(user_id)

    def GetUserContext(self, user_id: M.ID) -> Context: 
        if user_id not in self.user_context_cache:
            self.user_context_cache[user_id] =\
                self.storage.GetUserContext(user_id)
        return self.user_context_cache[user_id]

