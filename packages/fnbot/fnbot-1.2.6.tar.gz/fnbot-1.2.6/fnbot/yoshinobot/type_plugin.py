import os
import importlib

from ._bot import _plugin

from .cq_config import *

__all__ = (
    "insert_plugin", "insert_plugins_dir", "insert_the_plugin",
)



class Plugin(_plugin):
    """
    Class Properties:
    ```
        all_plugin_name: list[str]
        inserted_plugins: dict
    ```
    """
    all_plugin_name:list = []
    """`list[str]`"""
    inserted_plugins:dict = {}
    __slots__ = ('plugin_name_list', 'relative_path_str',)

    def __init__(self, _plugin_name_list:list, _relative_path_str:str):
        self.plugin_name_list = _plugin_name_list
        self.relative_path_str = _relative_path_str

    def _relative_to_absolute(self) -> str:
        """
        Returns:
        ```
            str: absolute path of self.relative_path_str
        ```
        """
        absolute_path:str = (
            Config.path_pybot + "/" + self.relative_path_str.lstrip("./").rstrip("/")
        )
        return absolute_path

    def _to_import_name(self, _name:str) -> str:
        """
        Returns:
        ```
            str: the name to be imported
        ```
        """
        import_name:str = self.relative_path_str.lstrip("./").rstrip("/")
        import_name =  ".".join(import_name.split("/")) + f".{_name}"
        if import_name.endswith(".py"): import_name = import_name.rstrip(".py")
        return import_name

    def _is_legal_plugin(self, _plugin:str) -> bool:
        """
        Args:
        ```
            _plugin_str:str    :debug_file, debug.py, debug_dir
        ```
        Returns:
        ```
            bool: Is it a plugin name that can be imported?
        ```
        """
        if any((_plugin.startswith('_'),)): return False
        absolute_plugin_path:str = self._relative_to_absolute() + '/' + _plugin
        return any((
            os.path.isfile(absolute_plugin_path),
            os.path.isfile(absolute_plugin_path + '.py'),
            all((
                os.path.isdir(absolute_plugin_path),
                os.path.isfile(absolute_plugin_path + '/__init__.py'),
            )),
        ))

    def _insert_plugin(self, _name:str):
        plugin_list = os.listdir(self._relative_to_absolute())
        if _name in plugin_list or _name + '.py' in plugin_list:
            self.all_plugin_name.append(self._to_import_name(_name))
        else:
            raise RuntimeError(f"Not found {_name}!!!")


    def insert_plugins_dir(self, _exc_plugins_list:list = []):
        plugin_dir_list:list = os.listdir(self._relative_to_absolute())
        plugin_dir_list = [_ for _ in plugin_dir_list if self._is_legal_plugin(_)]
        plugin_dir_list = [_ for _ in plugin_dir_list if _ not in _exc_plugins_list]
        if plugin_dir_list == []: raise RuntimeError("Not found any plugin!!!")
        for _ in plugin_dir_list: self._insert_plugin(_)

    def insert_plugin_self(self):
        plugin_list = [_ for _ in self.plugin_name_list if self._is_legal_plugin(_)]
        for _ in plugin_list: self._insert_plugin(_)

    def insert_the_plugin(self):
        for _ in self.plugin_name_list: self._insert_plugin(_)



def insert_plugin(_plugin, _relative_path:str):
    """
    Args:
    ```
        _plugin: str | list
        _relative_path: str | None = None
    ```
    Usages:
    ```
        fnbot.insert_plugin("debug", "./plugins")
    ```
    """
    assert isinstance(_plugin, (str, list))
    assert isinstance(_relative_path, str)
    if isinstance(_plugin, str): _plugin = [_plugin]
    plugin = Plugin(_plugin, _relative_path)
    return plugin.insert_plugin_self()

def insert_the_plugin(_plugin, _relative_path:str):
    """contain _plugin

    Args:
    ```
        _plugin: str | list
        _relative_path: str | None = None
    ```
    Usages:
    ```
        fnbot.insert_plugin("_debug", "./plugins")
    ```
    """
    assert isinstance(_plugin, (str, list))
    assert isinstance(_relative_path, str)
    if isinstance(_plugin, str): _plugin = [_plugin]
    plugin = Plugin(_plugin, _relative_path)
    return plugin.insert_the_plugin()

def insert_plugins_dir(_relative_path_dir:str, _exc_plugins_list:list = []):
    """
    Args:
    ```
        _relative_path_dir:str
        _exc_plugins_list:list[str] = []
    ```
    Usages:
    ```
        fnbot.insert_plugins_dir("./plugins")
    ```
    """
    assert isinstance(_relative_path_dir, str)
    assert isinstance(_exc_plugins_list, list)
    plugin = Plugin([], _relative_path_dir)
    return plugin.insert_plugins_dir(_exc_plugins_list)

def load_all_plugin():
    for _ in Plugin.all_plugin_name:
        module = importlib.import_module(_)
        Plugin.inserted_plugins.update({str(module):_})


