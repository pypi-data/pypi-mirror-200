from ..Form     import Form
from ..Storage  import Context, Models as M
from .          import FormElemFactory

from ..Types    import FormBehavior
from typing     import Dict

from copy       import deepcopy


class FormPrototypeFactory():
    prototypes: Dict[M.ID, Form] = dict()
    fields  = None
    storage = None

    @staticmethod
    def INIT(states, fields, storage):
        FormPrototypeFactory.fields = fields
        for state in states.values():
            fields = \
                FormPrototypeFactory.__FieldsToFormElems(state['forms_ids'])
            FormPrototypeFactory.prototypes[state['id']] = \
                Form(state['id'], fields)
            FormPrototypeFactory.storage = storage

    @staticmethod
    def Make(form_id: M.ID) -> Form:
        from copy import deepcopy
        # THIS ONE IS NOT WORKING NOW
        # I know, I know, should've deleted it
        return deepcopy( FormPrototypeFactory.Get(form_id) )

    @staticmethod
    def Get(form_id: M.ID, context : Context) -> Form:
        form  = FormPrototypeFactory.prototypes[form_id]
        behav = context.forms_info.Read(form_id)['form_behavior']
        if behav == FormBehavior.REGULAR:
            return form

        ids   = form.GetFieldsIds()
        inps  = context.user_input.ReadAll()
        ids.extend([
            k for k,v in inps.items() if isinstance(v, str)
        ])
        fields = FormPrototypeFactory.__FieldsToFormElems(ids)

        return Form(form.id, fields)

    @staticmethod
    def CopyNarrowing(form_id: M.ID, context: Context) -> Form:
        inp = context.user_input.ReadAll()
        fi  = context.forms_info.Read(form_id)['possible_inp_ids']
        empty_inp = {
            k: inp[k] for k in fi if inp[k] is None
        }
        h = hash( tuple( sorted( empty_inp.keys() )))
        if h not in FormPrototypeFactory.prototypes:
            fields = \
                FormPrototypeFactory.__FieldsToFormElems(empty_inp.keys())
            FormPrototypeFactory.prototypes[h] = \
                Form(h, fields)
            FormPrototypeFactory.storage.CopyNarrowingFormInfo(
                    form_id, h, list( empty_inp.keys() ) )

        return FormPrototypeFactory.prototypes[h]

    @staticmethod
    def __FieldsToFormElems(fields_ids):
        pt      = None 
        fields  = list()
        for id in fields_ids:
            f, pt = FormElemFactory.Make(
                FormPrototypeFactory.fields[id],
                pt)
            fields.append(f)
        return fields

