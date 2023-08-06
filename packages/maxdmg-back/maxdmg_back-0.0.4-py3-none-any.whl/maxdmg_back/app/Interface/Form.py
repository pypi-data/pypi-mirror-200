class FormContext():
    def __init__(self, context, branches):
        self.state_history = context.state_history
        self.branches      = branches
        self.storage       = context.storage

