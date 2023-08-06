from ..utils import format_bytes
from ..module import Module

try: import psutil 
except: print("ModuleRAM: psutil module not found!")

class ModuleRAM(Module):

    def __init__(self,  str_format: str="RAM: {data}",
                        data_type: str="percent", data_format: str="%",      
                        periodic: float=1.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format     = str_format
        self.data_type      = data_type
        self.data_format    = data_format

    def execute(self) -> str:
        raw_ram = psutil.virtual_memory().__getattribute__(self.data_type)
        ram     = str(format_bytes(raw_ram, self.data_format))
        return self.str_format.replace("{data}", ram)

