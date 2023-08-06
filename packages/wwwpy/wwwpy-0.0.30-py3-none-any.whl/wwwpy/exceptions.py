class WwwpyException(Exception):
    pass


class RemoteException(WwwpyException):
    """When user defined server code fails"""
    pass


class RemoteError(WwwpyException):
    """When network/wwwpy infrastructure fails"""
    pass
