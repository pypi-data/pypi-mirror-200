from collections    import OrderedDict
import json

from .Interface     import FormElem
from .StateHistory  import StateHistory
from .Exceptions    import FormElemSwitchedHistory
from .Storage       import Context, Models as M

from typing         import Dict, List, Union
from .Types         import BranchTypes


class Form():
    def __init__(self, form_id: M.ID, fields):
        self.id             = form_id 
        self.fields         = OrderedDict()

        for f in fields: 
            self.fields[f.id] = f

        self.next_b_tpl     = {
            'id'        : 'next',
            'type'      : 'BUTTON',
            'cb'        : 'next',
            'text'      : 'СОХРАНИТЬ И ПРОДОЛЖИТЬ',
            'completed' : False,
        }
        self.prev_b_tpl     = {
            'id'        : 'prev',
            'type'      : 'BUTTON',
            'cb'        : 'prev',
            'text'      : 'НАЗАД',
            'completed' : False,
        }
        self.done_b_tpl     = {
            'id'        : 'done',
            'type'      : 'BUTTON',
            'cb'        : 'done',
            'text'      : 'ЗАВЕРШИТЬ РАБОТУ',
            'completed' : False,
        }

    def IsCompleted(self, context: Context) -> bool:
        for field in self.fields:
            if not field.IsCompleted(context):
                return False
        return True

    def IsFieldCompleted(self, field_id: M.ID) -> bool:
        return self.fields[field_id].IsCompleted()

    def AcceptInput(self, input, context: Context) -> None:
        field = self.fields[input['field_id']]
        field.AcceptInput(input, context)

    def Reject(self, context: Context) -> None:
        for field in self.fields.values():
            field.Reject(context)

    def ToDict(self, context: Context) -> List[Dict]:
        next_id = self.DetermineNextState(context)
        StateHistory.SetNext(next_id, context)
        repr: List[Dict] = list()
        for field in self.fields.values():
            field.AddRepr(repr, context)
        if   StateHistory.CanSwitchToPrev(context):
            repr.append(self.prev_b_tpl)
        if   StateHistory.CanSwitchToNext(context):
            repr.append(self.next_b_tpl)
        elif StateHistory.AtEnd(context):
            repr.append(self.done_b_tpl)
        return repr

    def DetermineNextState(self, context: Context) -> Union[M.ID, None]:
        cur_id   = StateHistory.GetCurrent(context)
        branches = context.forms_info.Read(cur_id)['form_branches']
        u_input  = context.user_input
        all_inps = context.forms_info.Read(cur_id)['possible_inp_ids']

        for branch in branches:
            match branch['type'].value:
                case BranchTypes.CONDITIONAL:
                    for inp in branch['req_user_input_ids']:
                        if not self.fields[inp].IsCompleted(
                                context):
                            break
                    else:
                        return branch['resulting_state_id']
                case BranchTypes.UNCONDITIONAL:
                    return branch['resulting_state_id']
                case BranchTypes.STRICT:
                    for inp in all_inps:
                        if not self.fields[inp].IsGroupCompleted(
                                context):
                            break
                    else:
                        return branch['resulting_state_id']
        return None

    def GetFieldsIds(self):
        return list( self.fields.keys() )

    def ToJson(self, context) -> str:
        return json.dumps( self.ToDict(context) )

