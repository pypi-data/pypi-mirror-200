from typing     import TypedDict, Dict, List, Union
from ..Types    import BranchTypes, FormBehavior


ID = str

UserInput = Dict[ID, Union[str, None]]

class UserContext(TypedDict):
    current_state_idx   : int 
    state_history       : List[ID]
    rejected_states     : List[ID] 

class Branch(TypedDict):
    type                : BranchTypes
    req_user_input_ids  : List[ID] 
    resulting_state_id  : ID

FormsBranches = List[Branch]

FormsBranchesStorage = Dict[ID, FormsBranches]

class MainStorageContents(TypedDict):
    user_context        : UserContext
    user_input          : UserInput

MainStorage = Dict[ID, MainStorageContents]

PossibleInpIds = Dict[ID, List[ID]]

class Document(TypedDict):
    tag         : str
    doc_name    : str

Documents       = List[Document] 
Tags            = Dict[ID, Union[List[str], None]]
FormsNames      = Dict[ID, str]
FormsBehaviors  = Dict[ID, str]

class GeneralInfo(TypedDict):
    start_id            : ID
    end_ids             : ID
    always_open_ids     : ID
    tags_by_field_id    : Tags
    documents           : Documents

class Form(TypedDict):
    form_name           : str
    form_behavior       : str
    form_branches       : FormsBranches
    possible_inp_ids    : List[ID]

FormsInfo = Dict[ID, Form]

