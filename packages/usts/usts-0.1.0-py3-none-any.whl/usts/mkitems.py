from .item import Item
from .utils import *

def make_str(value: str):
    execute = lambda: value
    return Item(execute, periodic=-1)

def make_time(timestrf: str="%m/%d/%Y %H:%M:%S", periodic: float=1.0) -> Item:
    try: import datetime
    except: raise ImportError("datetime module not found!")

    execute = lambda: datetime.datetime.now().strftime(timestrf)   
    return Item(execute, periodic)

def make_cpu_usage(str_format: str="CPU: {data}%", periodic: float=1.0) -> Item:
    try: import psutil
    except: raise ImportError("psutil module not found!")
    
    execute = lambda: str_format.replace("{data}", 
        str(psutil.cpu_percent())
    )

    return Item(execute, periodic)

def make_memory_usage(str_format: str="RAM: {data}",
                      data_type: str="percent", data_format: str="%", 
                      periodic: float=1.0) -> Item:
    try: import psutil
    except: raise ImportError("psutil module not found!")
    
    str_format += data_format
    execute = lambda: str_format.replace("{data}", 
        str(format_bytes(
            psutil.virtual_memory().__getattribute__(data_type),
            data_format)
        ))
    
    return Item(execute, periodic)

def make_cryptocurrency(str_format: str="Monero: {data}$", coin: str="monero",
                        currency: str="usd", periodic: float=60.0) -> Item:
    try: import requests
    except: raise ImportError("requests module not found!")

    request_url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}'
    execute = lambda: str_format.replace("{data}", 
        str(requests.get(request_url).json()[coin][currency]))
    
    return Item(execute, periodic)



