# ==== StateHistory Exceptions

class CantSwitch(Exception):
    def __init__(self, where):
        self.message = 'Cannot switch state history:'
        self.where   = where

        super(CantSwitch, self).__init__( 
            (self.message, self.where) )

    def __reduce__(self):
        return (CantSwitch, (self.message, self.where))


# ==== StateHistory Exceptions

class UserNotInDatabase(Exception):
    def __init__(self, user_id):
        self.message = 'User is not in the database:'
        self.user_id = user_id

        super(UserNotInDatabase, self).__init__( 
            (self.message, self.user_id) )

    def __reduce__(self):
        return (UserNotInDatabase, (self.message, self.user_id))


class UserAlreadyInDatabase(Exception):
    def __init__(self, user_id):
        self.message = 'User is already in the database:'
        self.user_id = user_id

        super(UserAlreadyInDatabase, self).__init__( 
            (self.message, self.user_id) )

    def __reduce__(self):
        return (UserAlreadyInDatabase, (self.message, self.user_id))


# ==== Context Exceptions

class OperationIsNotSupported(Exception):
    def __init__(self, op):
        self.message = 'Operation is not supported:'
        self.op      = op

        super(OperationIsNotSupported, self).__init__( 
            (self.message, self.op) )

    def __reduce__(self):
        return (OperationIsNotSupported, (self.message, self.op))


# ==== Branching Exceptions

class BranchHasNoCondition(Exception):
    def __init__(self, cond):
        self.message = 'Operation is not supported:'
        self.cond    = cond

        super(BranchHasNoCondition, self).__init__( 
            (self.message, self.cond) )

    def __reduce__(self):
        return (BranchHasNoCondition, (self.message, self.cond))


# ==== FormElem Exceptions

class WrongDynamicField(Exception):
    def __init__(self, cond):
        self.message = 'No dynamic field:'
        self.id      = id

        super(WrongDynamicField, self).__init__( 
            (self.message, self.id) )

    def __reduce__(self):
        return (WrongDynamicField, (self.message, self.id))

class UnsupportedFormElemType(Exception):
    def __init__(self, t):
        self.message = 'No dynamic field:'
        self.type    = t

        super(UnsupportedFormElemType, self).__init__( 
            (self.message, self.type) )

    def __reduce__(self):
        return (UnsupportedFormElemType, (self.message, self.type))


class FormElemSwitchedHistory(Exception):
    def __init__(self, form_elem_name):
        self.message = 'Form Element switched history to next state!'
        self.name    = form_elem_name

        super(FormElemSwitchedHistory, self).__init__( 
            (self.message, self.name) )

    def __reduce__(self):
        return (FormElemSwitchedHistory, (self.message, self.name))


# ==== Messaging Exceptions
class UserDone(Exception):
    pass

