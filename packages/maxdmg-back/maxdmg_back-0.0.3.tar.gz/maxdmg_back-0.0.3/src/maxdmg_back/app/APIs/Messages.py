from ..Storage  import Models as M
from typing     import TypedDict, Dict, List, Union


class MessageType():
    Input           = 'input'
    FormOut         = 'form'
    DocInfoOut      = 'doc_info'
    FrontAccepted   = 'fron_ok'


class Form(TypedDict):
    id        : M.ID
    type      : MessageType
    cb        : str 
    text      : str
    completed : bool


class Input(TypedDict):
    field_type  : str
    field_id    : M.ID
    cb          : str


class OutForm(TypedDict):
    form        : Form


Tag = str 
Inp = str
class OutInfoForDocgen(TypedDict):
    tags        : Dict[Tag, Inp]
    docs        : M.Documents


class OutFrontAccepted(TypedDict):
    start_id        : str 
    end_ids         : List[str]
    always_open_ids : List[str]
    states_names    : List[str]


Contents = Union[Input, 
                 OutForm, 
                 OutInfoForDocgen, 
                 OutFrontAccepted, 
                 None]


class Message(TypedDict):
    user_id     : Union[M.ID, None]
    type        : str
    contents    : Contents

