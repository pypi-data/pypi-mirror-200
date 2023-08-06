from .Interface     import FormElem
from .StateHistory  import StateHistory
from .Exceptions    import FormElemSwitchedHistory, WrongDynamicField
from .Storage       import Context, Models as M
from typing         import List, Dict, Union


class RegularTextFormElem(FormElem):
    def __init__(self, field, group: List[FormElem]):
        super().__init__(field, group)
        self.type: str = 'TEXT'

    def AcceptInput(self, input, context: Context):
        pass

    def Reject(self, context: Context) -> None:
        pass

    def IsCompleted(self, context: Context) -> bool:
        return True


class RegularFieldFormElem(FormElem):
    def __init__(self, field, group: List[FormElem]):
        super().__init__(field, group)
        self.type: str = 'FORM'
        
    def AcceptInput(self, input, context: Context) -> None:
        if input['cb'] == '':
            self.Reject(context)
        else:
            super().AcceptInput(input, context)

    def IsGroupCompleted(self, context):
        for groupee in self.group:
            if not groupee.IsCompleted(context):
                return False
        return True

    def ToDict(self, context: Context) -> Dict:
        d = super().ToDict(context)
        t = context.user_input.Read(self.storage_id)
        if t is not None:
            d['text'] = t
        return d


class DynamicFieldFormElem(FormElem):
    SEPARATOR       = ', '
    ADD_BUT_D_ID    = '' 

    def __init__(self, field, group: List[FormElem]):
        super().__init__(field, group)
        self.type: str               = 'D_FORM'
        self.d_id: Union[M.ID, None] = None
        
    def AcceptInput(self, input, context: Context) -> None:
        cb = None 
        if input['d_id'] is not DynamicFieldFormElem.ADD_BUT_D_ID:
            cb = self.__InputToOldDField(input, context)
        else:
            cb = self.__InputToNewDField(input, context)

        if len(cb) == 0:
            super().Reject(context)
        else:
            input['cb'] = cb
            super().AcceptInput(input, context)
        
    def ToDict(self, context: Context) -> List[Dict]:
        my_repr = super().ToDict(context)
        my_repr['d_id'] = DynamicFieldFormElem.ADD_BUT_D_ID 
        ret: List[Dict] = list()
        ret.append(my_repr)
        d_fields_s = context.user_input.Read(self.storage_id)
        if d_fields_s is None: 
            return ret
        d_fields = d_fields_s.split(DynamicFieldFormElem.SEPARATOR)
        for cnt, d_field in enumerate(d_fields):
            ret.append( {
                'id'        : self.id,
                'd_id'      : str(cnt),
                'type'      : 'D_FORM',
                'cb'        : self.cb,
                'text'      : d_field,
                'completed' : True,
            } )
        return ret

    def AddRepr(self, where: List, context: Context) -> None:
        where.extend( self.ToDict(context) )

    def __InputToOldDField(self, input, context: Context) -> str:
        d_fields = context.user_input.Read(self.storage_id).split(
            DynamicFieldFormElem.SEPARATOR)
        d_id = int(input['d_id'])
        if d_id > len(d_fields)-1:
            raise WrongDynamicField(self.id)
        if input['cb'] == '':
            d_fields.pop(d_id)
        else:
            d_fields[d_id] = input['cb']
        return DynamicFieldFormElem.SEPARATOR.join(d_fields).strip()

    def __InputToNewDField(self, input, context: Context) -> str:
        d_fields_s = context.user_input.Read(self.storage_id) 
        if input['cb'] == '':
            if d_fields_s is None:
                return ''
            return d_fields_s.strip()
        if d_fields_s is None:
            d_fields_s = input['cb']
        else:
            d_fields_s += DynamicFieldFormElem.SEPARATOR + input['cb']
        return d_fields_s.strip()        


class ButtonFormElem(FormElem):
    def __init__(self, field, group: List[FormElem]):
        super().__init__(field, group)
        self.type: str = 'BUTTON'

    def AcceptInput(self, input, context: Context) -> None:
        for groupee in self.group:
            groupee.Reject(context)
        input['cb'] = True
        super().AcceptInput(input, context)
        next_id = self.FormElemToNext(context)
        StateHistory.SetNext(next_id, context)
        StateHistory.SwitchToNext(context)
        #raise FormElemSwitchedHistory(self.text) 
    

class SingleChoiceFormElem(FormElem):
    def __init__(self, field, group: List[FormElem]):
        super().__init__(field, group)
        self.type       = 'S_CHOICE'

    def AcceptInput(self, input, context: Context) -> None:
        if self.IsCompleted(context):
            return self.Reject(context)
        for groupee in self.group:
            groupee.Reject(context)
        input['cb'] = True
        return super().AcceptInput(input, context)


class MultiChoiceFormElem(FormElem):
    def __init__(self, field, group: List[FormElem]):
        super().__init__(field, group)
        self.type       = 'M_CHOICE'

    def AcceptInput(self, input, context: Context) -> None:
        if self.IsCompleted(context):
            return self.Reject(context)
        input['cb'] = True
        return super().AcceptInput(input, context)

