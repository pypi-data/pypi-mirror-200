import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from .cq_config import Config, load_all_config
from .cq_receive import Receive, run_receive_server
from .cq_send import Send
from .type_insert import Insert
from .type_plugin import load_all_plugin
from ._ciallo import schedule

__all__ = "run",



class CoreOfInsert:
    nonparametric_insert_type = ['init', 'insert']
    parametric_insert_type = ['private', 'group', 'notice', 'request']
    __slots__ = ("insert_type", "to_run",)

    def __init__(self, _insert_type:str, _component_list:list):
        self.insert_type = _insert_type
        self.to_run = self.get_to_run(_component_list)
        # to_run:list[function] for parametric_insert_type
        # to_run:dict{'bot_qq':list[function]} for nonparametric_insert_type

    def get_to_run(self, _component_list:list):
        """
        Retuens:
        ```
            to_run:list[function]
            to_run:dict{'bot_qq':list[function]}
        ```
        """
        if self.insert_type in self.nonparametric_insert_type:
            return [_ for _ in _component_list if _.__alive__]
        elif self.insert_type in self.parametric_insert_type:
            to_run_dict:dict = {_:[] for _ in Config.cfginfo.keys()}
            for _ in _component_list:
                if [] == _.__dev__:
                    to_run_dict = {
                        v.append(_) or k:v for k,v in to_run_dict.items()
                    }
                else:
                    for dev in _.__dev__:
                        dev = str(dev)
                        dev_to_list:list = to_run_dict.get(dev, [])
                        dev_to_list.append(_)
                        to_run_dict.update({dev:dev_to_list})
            return to_run_dict

    async def _run_core(self, _rev:dict = {}):
        if self.insert_type in self.nonparametric_insert_type:
            if [] != self.to_run:
                await asyncio.gather(*[_() for _ in self.to_run])
        elif self.insert_type in self.parametric_insert_type:
            to_run_list:list = self.to_run.get(str(_rev.get("self_id")), [])
            to_run_list = [
                _ for _ in to_run_list if (
                    [] == _.__group__ or _rev.get('group_id') in _.__group__
                )
            ]
            to_run_list = sorted(
                to_run_list, key = lambda x:x.__num__, reverse = False
            )
            if [] != to_run_list:
                await asyncio.gather(*[_(_rev) for _ in to_run_list])
    def run(self, _rev:dict = {}): asyncio.run(self._run_core(_rev))

def _run_core():
    core_private_list:list = Insert.manage_component_dict.get("private", [])
    core_group_list:list = Insert.manage_component_dict.get("group", [])
    core_notice_list:list = Insert.manage_component_dict.get("notice", [])
    core_request_list:list = Insert.manage_component_dict.get("request", [])
    core_private = CoreOfInsert("private", core_private_list)
    core_group = CoreOfInsert("group", core_group_list)
    core_notice = CoreOfInsert("notice", core_notice_list)
    core_request = CoreOfInsert("request", core_request_list)
    core_private.run({'message':None})
    core_group.run({'message':None})
    while True:
        if Receive.rev_list != []: rev:dict = Receive.rev_list.pop(0)
        else: continue
        if all((rev != {}, rev.get('post_type','meta_event') != 'meta_event')):
            schedule.send_rev(rev)
            post_type:str = rev['post_type'] if 'post_type' in rev else ''
            msg_type:str = rev['message_type'] if 'message_type' in rev else ''
            if msg_type == 'private':
                private_bool:bool =all((
                    rev.get('user_id') not in Config(rev).blackqq_list,
                ))
                if private_bool:
                    threading.Thread(target=core_private.run, args=(rev,)).start()
            elif msg_type == 'group':
                group_bool:bool = all((
                    rev.get('group_id') in Config(rev).group_list,
                    rev.get('user_id') not in Config(rev).blackqq_list,
                ))
                if group_bool:
                    threading.Thread(target=core_group.run, args=(rev,)).start()
            elif post_type == 'notice':
                notice_bool:bool = all((
                    any((
                        rev.get('user_id') not in Config(rev).blackqq_list,
                        rev.get('user_id',None) == None,
                    )),
                    any((
                        rev.get('group_id') in Config(rev).group_list,
                        rev.get('group_id',None) == None,
                    )),
                ))
                if notice_bool:
                    threading.Thread(target=core_notice.run, args=(rev,)).start()
            elif post_type == 'request':
                request_bool:bool = all((
                    any((
                        rev.get('user_id') not in Config(rev).blackqq_list,
                        rev.get('user_id',None) == None,
                    )),
                    any((
                        rev.get('group_id') in Config(rev).group_list,
                        rev.get('group_id',None) == None,
                    )),
                ))
                if request_bool:
                    threading.Thread(target=core_request.run, args=(rev,)).start()

def cq_is_alive() -> bool:
    for _ in list(Config.cfginfo.keys()):
        try:
            result = Send(_).get_status()
            if not 'data' in result and result['data']['online']:
                return cq_is_alive()
        except:
            time.sleep(1)
            return cq_is_alive()
    else:
        return True

def _run(_yoshino:str = "~~~ciallo~~~"):
    load_all_config()
    load_all_plugin()
    cq_is_alive()
    core_init_list:list = Insert.manage_component_dict.get("init", [])
    coro_insert_list:list = Insert.manage_component_dict.get("insert", [])
    core_init = CoreOfInsert("init", core_init_list)
    coro_insert = CoreOfInsert("insert", coro_insert_list)
    core_init.run()
    with ThreadPoolExecutor() as executor:
        executor.submit(coro_insert.run)
        executor.submit(run_receive_server)
        executor.submit(_run_core)
        print(_yoshino)
    print("~~~少女祈祷中~~~")


def run(_yoshino:str = "~~~ciallo~~~"):
    """run yoshino bot
    Args:
    ```
        _yoshino:str = "~~~ciallo~~~"
    ```
    Usages:
    ```
        if __name__ == "__main__":
            fnbot.run()
    ```
    """
    return _run(_yoshino)


