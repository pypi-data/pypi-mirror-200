from .Exceptions    import CantSwitch
from .Storage       import Models as M
from .Storage       import Context 
from typing         import Union


class StateHistory():
    FormFactory = None

    @staticmethod
    def INIT(FormFactoryClass):
        StateHistory.FormFactory = FormFactoryClass

    @staticmethod
    def GetCurrent(context: Context) -> M.ID:
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        return hst[idx]

    @staticmethod
    def GetNext(context: Context) -> M.ID:
        idx = context.user_context.Read('current_state_idx') + 1
        hst = context.user_context.Read('state_history')
        return hst[idx]

    @staticmethod
    def SetNext(next_id, context: Context) -> None:
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        if len(hst)-1 > idx and hst[idx+1]==next_id:
            return
        reject = hst[idx+1:-1]
        context.user_context.Write('rejected_states', reject)
        hst = hst[0:idx+1]
        if next_id in hst:
            form = StateHistory.FormFactory.CopyNarrowing(
                    next_id, context)
            next_id = form.id
        if next_id:
            hst.append(next_id)
        context.user_context.Write('state_history', hst)

    @staticmethod
    def AtEnd(context: Context) -> bool:
        cur_id   = StateHistory.GetCurrent(context)
        end_ids  = context.general_info.Read('end_ids')
        return cur_id in end_ids
        #branches = context.general_info.Read('branches')[cur_id]
        #return len(branches) == 0

    @staticmethod
    def CanSwitchToNext(context: Context) -> bool:
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        return len(hst)-1 > idx

    @staticmethod
    def CanSwitchToPrev(context: Context) -> bool:
        idx = context.user_context.Read('current_state_idx')
        return idx > 0

    @staticmethod
    def SwitchToNext(context: Context) -> None:
        if StateHistory.CanSwitchToNext(context):
            idx = context.user_context.Read('current_state_idx')
            context.user_context.Write('current_state_idx', idx + 1)
        else:
            raise CantSwitch("No next!")

    @staticmethod
    def SwitchToPrev(context: Context) -> None:
        if StateHistory.CanSwitchToPrev(context):
            idx = context.user_context.Read('current_state_idx')
            context.user_context.Write('current_state_idx', idx - 1)
        else:
            raise CantSwitch("No prev!")

