from typing import Union, List, Optional, Dict
# ! Локальные импорты
#from . import tree
from . import units

# ! Константы
LINUX_BYTES_NAMES: Dict[str, int] = {
    "KiB": 1024,
    "MiB": 1048576,
    "GiB": 1073741824
}

# Функции редактирования
def removes(l: list, ldv: list) -> list:
    for value in ldv:
        for i in range(0, l.count(value)):
            l.remove(value)
    return l

def replaces(s: str, d: Dict[str, str]) -> str:
    for i in d.items():
        try: s = s.replace(i[0], i[1])
        except: pass
    return s

def startswiths(string: str, sl: List[str]) -> bool:
    for i in sl:
        if string.startswith(i):
            return True
    return False

# ! Convert Functions
def to_bool(string: str) -> Optional[bool]:
    try: return bool(str(string).replace(" ", "").title())
    except: pass

def to_int(string: Optional[str]) -> Optional[int]:
    try: return int(str(string).lower().replace(" ", ""))
    except: pass

def to_float(string: Optional[str]) -> Optional[float]:
    try: return float(replaces(str(string).lower(), {" ": "", ",": "."}))
    except: pass

def from_csv(data: str, *, header: Optional[List[str]]=None, sep=",", end="\r\r\n") -> List[Dict[str, str]]:
    dt: List[List[str]] = [i.split(sep) for i in removes(data.split(end), [""])]
    head, out = header or dt[0], []
    if header is None: dt = dt[1:]
    for d in dt:
        l = {}
        for idx, i in enumerate(head):
            l[i] = d[idx]
        out.append(l)
    return out

"""
def from_tcpu_data(s: str) -> tree.Tree:
    t, slines = tree.Tree(), removes(s.split("\r\n"), [""])
    for sline in slines:
        *keys, value = str(sline).replace(" ", "_").lower().split(":")
        if (data:=to_float(value)) is not None: value = data
        elif (data:=to_int(value)) is not None: value = data
        elif value.replace("_","") == "": value = None
        t.set(".".join(keys), value)
    return t
"""

def linux_bytes(string: Optional[Union[str, int]]) -> Optional[int]:
    if not isinstance(string, int):
        if string is not None:
            ls = string.split(' ')
            try:
                return int(ls[0]) * LINUX_BYTES_NAMES[ls[1]]
            except:
                pass
    return string

# ! Функции проверки
def sn(string: Optional[str]) -> Optional[str]:
    if string is not None:
        if not startswiths(string, units.NONE_TYPE_EXCEPTIONS):
            return string
