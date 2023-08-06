from enum import Enum


class TempCodeTriggers(Enum):
    EmailActivation = 'EA'
    PwdReset = 'PR'


class JWTTokenTypes(Enum):
    access = 'access'
    refresh = 'refresh'
