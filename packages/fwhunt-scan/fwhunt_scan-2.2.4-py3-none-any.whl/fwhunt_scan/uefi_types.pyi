from _typeshed import Incomplete
from typing import Optional

class UefiService:
    name: Incomplete
    address: Incomplete
    def __init__(self, name: str, address: int) -> None: ...
    @property
    def __dict__(self): ...

class UefiGuid:
    value: Incomplete
    name: Incomplete
    def __init__(self, value: str, name: str) -> None: ...
    @property
    def bytes(self) -> bytes: ...
    @property
    def __dict__(self): ...

class UefiProtocol(UefiGuid):
    address: Incomplete
    guid_address: Incomplete
    service: Incomplete
    def __init__(self, name: str, address: int, value: str, guid_address: int, service: str) -> None: ...
    @property
    def __dict__(self): ...

class UefiProtocolGuid(UefiGuid):
    address: Incomplete
    def __init__(self, name: str, address: int, value: str) -> None: ...
    @property
    def __dict__(self): ...

class NvramVariable:
    name: Incomplete
    guid: Incomplete
    service: Incomplete
    def __init__(self, name: str, guid: str, service: UefiService) -> None: ...
    @property
    def __dict__(self): ...

class SmiHandler:
    address: Incomplete
    def __init__(self, address: int) -> None: ...
    @property
    def __dict__(self): ...

class SwSmiHandler(SmiHandler):
    sw_smi_input_value: Incomplete
    def __init__(self, sw_smi_input_value: Optional[int], address: int) -> None: ...
    @property
    def __dict__(self): ...

class ChildSwSmiHandler(SmiHandler):
    handler_guid: Incomplete
    def __init__(self, handler_guid: Optional[str], address: int) -> None: ...
    @property
    def __dict__(self): ...
