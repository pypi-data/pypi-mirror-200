import uuid

from ..API          import API
from .Messages      import *
from ..Exceptions   import UserDone


class MonoAPI(API):
    def __init__(self, active_users, general_info, 
                 forms_info, state_machine):
        super().__init__()
        self.active_users  = active_users
        self.state_machine = state_machine
        self.general_info  = general_info
        self.forms_info    = forms_info

    def RegisterFrontendAPI(self, api):
        fi = self.forms_info.ReadAll()
        forms_names = {
            id: fi[id]['form_name'] for id in fi.keys()
        }
        contents = {
            'start_id'        : self.general_info.Read('start_id'),
            'end_ids'         : self.general_info.Read('end_ids'),
            'always_open_ids' : self.general_info.Read('always_open_ids'),
            'states_names'    : forms_names,
        }
        return {
            'user_id'   : None,
            'type'      : MessageType.FrontAccepted,
            'contents'  : contents,
        }

    def NewUser(self) -> str:
        user_id = uuid.uuid4()
        self.active_users.AddUser(user_id)
        return user_id

    def DeleteUser(self, back_id) -> None:
        self.active_users.DeleteUser(back_id)

    def AcceptInput(self, message: Message) -> Message:
        user_id = message['user_id']

        if message['contents'] is None:
            self.active_users.ResetUser(user_id)

        context = self.active_users.GetUserContext(user_id)

        try:
            form = self.state_machine.Go(context, 
                                         message['contents'])
            return {
                'user_id'   : user_id,
                'type'      : MessageType.FormOut,
                'contents'  : form,
            }
        except UserDone:
            tags = context.general_info.Read('tags_by_field_id')
            inps = context.user_input.ReadAll()

            tags_inps = dict()
            for f_id, tgs in tags.items():
                if not tgs:
                    continue
                for t in tgs.split(','):
                    tag = t.strip()
                    if not tags_inps.get(tag) or not tags_inps[tag]:
                        tags_inps[tag] = inps[f_id]

            contents = {
                'tags'      : tags_inps,
            }

            return {
                'user_id'   : user_id,
                'type'      : MessageType.DocInfoOut,
                'contents'  : contents,
            }

