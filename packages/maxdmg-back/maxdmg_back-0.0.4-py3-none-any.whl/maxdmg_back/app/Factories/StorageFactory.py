from ..Storage  import Storage, Models
from typing     import Dict


class StorageFactory():
    graph = None
    forms: Dict
    docs : Dict

    @staticmethod
    def INIT(graph, forms, docs) -> None:
        StorageFactory.graph = graph
        StorageFactory.forms = forms
        StorageFactory.docs  = docs

    @staticmethod
    def Make() -> Storage:
        g = StorageFactory.graph

        user_input_model : Models.UserInput = dict()
        tags_by_field_id : Models.Tags      = dict()

        for field in StorageFactory.forms.values():
            if field['type'] == 'TEXT':
                continue
            user_input_model[field['id']] = None
            tags_by_field_id[field['id']] = field['tags']

        forms_info  : Models.FormsInfo = { }
        forms_names            : Models.FormsNames             = dict()
        forms_behaviors        : Models.FormsBehavior          = dict()
        forms_branches_storage : Models.StatesBranchesStorage  = dict()
        possible_inp_ids       : Models.PossibleInpIds         = dict()

        for s_id, state in g.states.items():
            branches : Models.StateBranches = list()
            for tr_id in state['out_transitions_ids']:
                branch : Models.Branch = {
                    'type'               :
                        g.transitions[tr_id]['type'],
                    'req_user_input_ids' : 
                        g.transitions[tr_id]['form_elem_ids'],
                    'resulting_state_id' :
                        g.transitions[tr_id]['target_id'],
                }
                branches.append(branch)
            form : Models.Form = {
                'form_name'             : state['name'],
                'form_behavior'         : state['behavior'].value,
                'form_branches'         : branches,
                'possible_inp_ids'      : state['forms_ids'],
            }
            forms_info[s_id] = form 

        docs = [
            {'tag' : doc['tag'], 'name' : doc['name']} for\
                doc in StorageFactory.docs.values()
        ]
        
        general_info : Models.GeneralInfo = {
            # info for navigation 
            'start_id'          : g.start_node_id,
            'end_ids'           : g.end_node_ids,
            'always_open_ids'   : g.always_open_ids,
            # info for docgen
            'tags_by_field_id'  : tags_by_field_id,
            'documents'         : docs
        }

        return Storage(user_input_model, general_info, forms_info)

