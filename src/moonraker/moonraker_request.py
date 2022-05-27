from typing import Callable
from attr import dataclass

@dataclass
class MoonrakerRequest():
    response_received_callback : Callable[[dict], None] = None
    request_was_send_callback : Callable = None
    request : dict = None