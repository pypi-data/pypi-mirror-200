from ..Storage  import ActiveUsers
from ..Storage  import StorageInterface
from typing     import Union


class ActiveUsersFactory():
    storage: StorageInterface

    @staticmethod
    def INIT(storage: StorageInterface) -> None:
        ActiveUsersFactory.storage = storage

    @staticmethod
    def Make() -> ActiveUsers:
        return ActiveUsers(ActiveUsersFactory.storage)

