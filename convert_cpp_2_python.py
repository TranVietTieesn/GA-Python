from dataclasses import dataclass
from typing import List

@dataclass
class phancong:
    lop: str
    mon: str
    gv: str
    so_tiet: int
    len_: int
    muc_uu_tien: int
    ttpc: bool
    
@dataclass
class tlop:
    mon: str
    gv: str
    
@dataclass
class tklop:
    lop: str
    tiet: List[tlop]
