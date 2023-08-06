from .Factories      import (
    FormPrototypeFactory, 
    StorageFactory, 
    ActiveUsersFactory, 
    APIFactory
)
from .StateMachine   import StateMachine 
from .StateHistory   import StateHistory 


class Assembly():
    storage         = None
    active_users    = None
    api             = None

    graph           = None
    forms           = None
    docs            = None

    @staticmethod
    def Assemble(loader):
        graph = loader['graph']
        forms = loader['forms']
        docs  = loader['docs']
        Assembly.graph = graph
        Assembly.forms = forms
        Assembly.docs  = docs

        StorageFactory.INIT(graph, forms, docs)
        Assembly.storage = StorageFactory.Make()

        ActiveUsersFactory.INIT(Assembly.storage)
        Assembly.active_users = ActiveUsersFactory.Make()

        FormPrototypeFactory.INIT(
                graph.states, 
                forms,
                Assembly.storage) 

        StateHistory.INIT(FormPrototypeFactory)

        APIFactory.INIT(Assembly.active_users, 
                        Assembly.storage.GetGeneralInfoStorage(),
                        Assembly.storage.GetFormsInfoStorage(),
                        StateMachine())
        Assembly.api = APIFactory.Make()

    @staticmethod
    def __PrintFormPrototypes():
        graph = Assembly.graph

        print('\nForms are:')
        for form in FormPrototypeFactory.prototypes.values():
            print('- ', graph.states[form.id]['name'], form.fields, '\n')

