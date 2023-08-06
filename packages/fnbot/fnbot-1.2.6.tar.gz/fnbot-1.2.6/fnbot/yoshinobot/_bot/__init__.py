"""
yoshino bot
"""

__all__ = (
    "_ciallo",
    "_config", "_receive", "_send",
    "_insert", "_message", "_plugin",
)



class _ciallo:
    def __init__(self, self_id = ...):
        """
        Args:
        ```
            self_id: '_message' | dict | int | str | None
        ```
        """
        assert isinstance(self_id, (
            _message, dict, int, str, type(None), type(Ellipsis),
        ))
        if isinstance(self_id, (str, int)):
            self.self_id = str(self_id)
        elif isinstance(self_id, dict):
            self.self_id = str(self_id.get('self_id', None))
        elif isinstance(self_id, (_message,)):
            self.self_id = str(getattr(self_id, 'self_id', None))
        else:
            self.self_id = None

class _config(_ciallo):
    def __init__(self, _id = None):
        super(_config, self).__init__(_id)
class _receive(_ciallo):
    def __init__(self, _id = None):
        super(_receive, self).__init__(_id)
class _send(_ciallo):
    def __init__(self, _id = None):
        super(_send, self).__init__(_id)

class _insert(type):
    def __new__(cls, _name:str, _bases:tuple, _dict:dict):
        return type.__new__(cls, _name, _bases, _dict)
    def __init__(self, _name:str, _bases:tuple, _dict:dict):
        return type.__init__(self, _name, _bases, _dict)
class _message:
    def __init__(self):
        super(_message, self).__init__()
class _plugin:
    def __init__(self):
        super(_plugin, self).__init__()


