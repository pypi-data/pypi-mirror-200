from typing import IO, BinaryIO

from ..api.tool_identity import ToolIdentity
from ..rpc import RPCClient


class Programmer:
    "A Programmer"

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._rpc = rpc
        self._tool_id = ToolIdentity(tool_id=tool_id)

    def reset_target(self) -> None:
        "Reset the target connected to the device"
        self._rpc.tools_programmer_reset_target(self._tool_id)

    def flash_file(self, src: IO[bytes]) -> None:
        "Flash the target with the given file"

        if not isinstance(src, BinaryIO):
            raise TypeError("flash_file expects objects with type BinaryIO")

        self._rpc.tools_programmer_flash(self._tool_id, src)
