from porcupine.base import Serializer


class LogEntrySerializer:
    class Base(Serializer):
        id: int
        message: str = None
        status_code: int = None
        request_body: dict = None
        username: str = None
        level: str
        module: str
        function: str
        filename: str
