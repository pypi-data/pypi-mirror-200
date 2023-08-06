from ..FormElems    import *
from ..Interface    import FormElem
from ..Types        import FormType
from ..Exceptions   import UnsupportedFormElemType
from typing         import List


class FormElemFactory():
    current_group: List[FormElem] = list()

    def Make(graph_field, prev_field_type) -> FormElem:
        pt = prev_field_type
        if graph_field['type'] != pt:
            pt = graph_field['type']
            FormElemFactory.current_group   = list()
        g = FormElemFactory.current_group

        match graph_field['type'].value:
            case FormType.REGULAR_TEXT:
                form = RegularTextFormElem(graph_field, g)
            case FormType.REGULAR_FIELD:
                form = RegularFieldFormElem(graph_field, g)
            case FormType.DYNAMIC_FIELD:
                form = DynamicFieldFormElem(graph_field, g)
            case FormType.BUTTON:
                form = ButtonFormElem(graph_field, g)
            case FormType.SINGLE_CHOICE:
                form = SingleChoiceFormElem(graph_field, g)
            case FormType.MULTI_CHOICE:
                form = MultiChoiceFormElem(graph_field, g)
            case _:
                raise UnsupportedFormElemType(\
                    graph_field['type'].value)
        return form, pt

