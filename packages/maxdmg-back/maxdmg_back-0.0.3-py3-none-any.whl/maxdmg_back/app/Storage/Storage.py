from copy   import deepcopy

from .                  import Models as M
from .StorageInterface  import StorageInterface
from .Context           import (Context, UserInputStorage, 
                                UserContextStorage, GeneralInfoStorage, 
                                FormsInfoStorage)
from ..Exceptions       import UserNotInDatabase, UserAlreadyInDatabase


class Storage(StorageInterface):
    def __init__(self, 
                 user_input_model : M.UserInput, 
                 general_info     : M.GeneralInfo,
                 forms_info       : M.FormsInfo) -> None:
        self.user_input_model   : M.UserInput   = user_input_model
        self.general_info       : M.GeneralInfo = general_info
        self.forms_info         : M.FormsInfo   = forms_info
        self.main_storage       : M.MainStorage = dict() 

    def HasUser(self, user_id) -> bool:
        if user_id in self.main_storage:
            return True
        return False

    def AssertUser(self, user_id: M.ID) -> None:
        if not self.HasUser(user_id):
            raise UserNotInDatabase(user_id)

    def AddUser(self, user_id: M.ID) -> None:
        if self.HasUser(user_id):
            raise UserAlreadyInDatabase(user_id) 
        new_user_info : M.MainStorageContents = {
            'user_context'    : {
                'current_state_idx' : 0,
                'state_history'     : [self.general_info['start_id'],],
                'rejected_states'   : list(),
            },
            'user_input'      : deepcopy(self.user_input_model),
        }
        self.__NewUser(user_id, new_user_info)

    def ResetUser(self, user_id: M.ID) -> None:
        if not self.HasUser(user_id):
            return
        self.DeleteUser(user_id)
        self.AddUser(user_id)

    def CopyNarrowingFormInfo(self, 
                              old_form_id, 
                              new_form_id,
                              inp_ids):
        fi = self.forms_info[old_form_id]
        pi = fi['possible_inp_ids']
        br = fi['form_branches']
        new_br = list()
        for i in inp_ids:
            for b in br:
                if i in b['req_user_input_ids']:
                    new_br.append(b)
        self.forms_info[new_form_id] = {
            'form_name'         : fi['form_name'], 
            'form_behavior'     : fi['form_behavior'],
            'form_branches'     : new_br,
            'possible_inp_ids'  : inp_ids,
        }

    def DeleteUser(self, user_id: M.ID) -> None:
        if not self.HasUser(user_id):
            return
        self.main_storage.pop(user_id)

    def GetUserContext(self, user_id: M.ID) -> Context:
        return Context( self.__GetUserInput(user_id),
                        self.__GetUserContext(user_id),
                        self.GetGeneralInfoStorage(),
                        self.GetFormsInfoStorage() )

    def __GetUserInput(self, user_id: M.ID) -> UserInputStorage:
        self.AssertUser(user_id)
        return UserInputStorage( 
            self.main_storage[user_id]['user_input'] )

    def __GetUserContext(self, user_id: M.ID) -> UserContextStorage:
        self.AssertUser(user_id)
        return UserContextStorage(  
            self.main_storage[user_id]['user_context'] )

    def GetGeneralInfoStorage(self) -> GeneralInfoStorage:
        return GeneralInfoStorage(self.general_info)

    def GetFormsInfoStorage(self) -> FormsInfoStorage:
        return FormsInfoStorage(self.forms_info)

    def __NewUser(self, user_id: M.ID, contents:M.MainStorageContents):
        self.main_storage[user_id] = contents

