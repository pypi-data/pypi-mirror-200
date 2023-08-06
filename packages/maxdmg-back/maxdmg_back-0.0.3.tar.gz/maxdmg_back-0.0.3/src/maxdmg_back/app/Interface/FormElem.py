from ..StateHistory     import StateHistory
from ..Storage          import Context, Models as M
from ..Exceptions       import BranchHasNoCondition
from typing             import List, Dict

import json


class FormElem():
    def __init__(self, field, group: List):
        self.id: M.ID           = field['id']
        self.storage_id: M.ID   = field['id']

        self.text: str = field['text'] 
        self.desc: str = ''
        self.cb: str   = str(field['id'])

        self.group: List[FormElem] = group
        self.group.append(self)

        self.is_completed = False

        self.type: str = 'INTERFACE'

    def AcceptInput(self, input, context: Context) -> None:
        context.user_input.Write(self.storage_id, input['cb'])
        self.is_completed = True

    def Reject(self, context: Context) -> None:
        context.user_input.Delete(self.storage_id)
        self.is_completed = False

    def IsCompleted(self, context: Context) -> bool:
        #return self.is_completed
        return True if context.user_input.Contains(self.storage_id) else False

    def IsGroupCompleted(self, context):
        for groupee in self.group:
            if groupee.IsCompleted(context):
                return True
        return False

    def ToDict(self, context: Context) -> Dict:
        return {
            'id'        : self.id,
            'type'      : self.type,
            'cb'        : self.cb,
            'text'      : self.text,
            'completed' : self.IsCompleted(context),
        }

    def ToJson(self, context: Context) -> str:
        return json.dumps( self.ToDict(context) )

    def AddRepr(self, where: List, context: Context) -> None:
        where.append( self.ToDict(context) )

    def FormElemToNext(self, context: Context) -> M.ID:
        cur_id = StateHistory.GetCurrent(context)
        branches = context.general_info.Read('branches')[cur_id]
        for branch in branches:
            for user_input_id in branch['req_user_input_ids']:
                if user_input_id == self.storage_id:
                    return branch['resulting_state_id']
        raise BranchHasNoCondition(self.storage_id)

