from flask import url_for
from error import NotInstanciatedError

class EndPoints:
    _context = None
    _instance = None

    home = None
    search = None
    browse = None
    select = None
    multimedia = None
    get_multimedia = None
    download = None
    error = None

    def __init__(self, context) -> None:
        EndPoints._context = context
        EndPoints._instance = self

    @staticmethod
    def getInstance():
        if EndPoints._instance != None:
            return EndPoints._instance
        else:
            raise NotInstanciatedError()