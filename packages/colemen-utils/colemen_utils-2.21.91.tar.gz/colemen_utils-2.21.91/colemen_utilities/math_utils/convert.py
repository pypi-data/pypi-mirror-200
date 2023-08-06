# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    A module of utility methods used for parsing and converting python types.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: type_utils
'''
import re
from typing import Union
import colemen_utilities.string_utils as _csu
# import colemen_utilities.dict_utils as _obj


_digital_storage = {
    "bytes":"b",
    "kilobytes":"KB",
    "megabytes":"MB",
    "gigabytes":"GB",
    "terabytes":"TB",
}

def pretty_bytes(value,decimals:int=None,left_pad:int=None):
    
    # print(f"value: {value}")
    if value < 1000:
        value= f"{value}{_digital_storage['kilobytes']}"
    elif 1000 < value < 1000000:
        value= bytes_to_kilobytes(value,pretty=True,decimal=decimals)
        # return f"{round(value,decimals)}{_digital_storage['kilobytes']}"
    elif 1000000 < value < 1000000000:
        value= bytes_to_megabytes(value,pretty=True,decimal=decimals)
        # return f"{round(value,decimals)}{_digital_storage['megabytes']}"
    elif 1000000000 < value < 1000000000000:
        value= bytes_to_gigabytes(value,pretty=True,decimal=decimals)
        # return f"{round(value,decimals)}{_digital_storage['gigabytes']}"
    elif 1000000000000 < value < 1000000000000:
        value= bytes_to_terabytes(value,pretty=True,decimal=decimals)
        # return f"{round(value,decimals)}{_digital_storage['terabytes']}"
    if left_pad is not None:
        value = _csu.leftPad(value,left_pad," ")
    return value

def to_bytes(value:str):
    # abbrevs = sorted(_digital_storage, key=lambda k: len(_digital_storage[k]), reverse=True)
    sorted_items = sorted(_digital_storage.items(), key = lambda item : len(item[1]),reverse=True)
    newd = dict(sorted_items)
    # print(newd)
    for k,v in newd.items():
        # print(f"    {k},{v}")
    # for k,v in reversed(_digital_storage.items()):
        if value.lower().endswith(v.lower()):
            # print(f"        Type Found: {k}")
            num_val = _csu.string_to_number(value)
            method_name = f"{k}_to_bytes"
            # print(f"        method_name:{method_name}")
            if method_name in globals():
            # if callable(method_name):
                # print(f"        method exists:{method_name}")
                return globals()[method_name](num_val)
            break
    return value

def bytes_to_kilobytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['kilobytes']}"
    return value

def bytes_to_megabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['megabytes']}"
    return value

def bytes_to_gigabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['gigabytes']}"
    return value

def bytes_to_terabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000000000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['terabytes']}"
    return value

def kilobytes_to_bytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['bytes']}"
    return value

def kilobytes_to_megabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['megabytes']}"
    return value

def kilobytes_to_gigabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['gigabytes']}"
    return value

def kilobytes_to_terabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['terabytes']}"
    return value

def megabytes_to_bytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['bytes']}"
    return value

def megabytes_to_kilobytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['kilobytes']}"
    return value

def megabytes_to_gigabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['gigabytes']}"
    return value

def megabytes_to_terabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['terabytes']}"
    return value

def gigabytes_to_bytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['bytes']}"
    return value

def gigabytes_to_kilobytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['kilobytes']}"
    return value

def gigabytes_to_megabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['megabytes']}"
    return value

def gigabytes_to_terabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value / 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['terabytes']}"
    return value

def terabytes_to_bytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000000000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['bytes']}"
    return value

def terabytes_to_kilobytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['kilobytes']}"
    return value

def terabytes_to_megabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['megabytes']}"
    return value

def terabytes_to_gigabytes(value:Union[int,float],pretty:bool=False,decimal:int=None)->Union[int,float]:
    value = value * 1000
    if decimal is not None:
        value = round(value,decimal)
    if pretty is True:
        return f"{value}{_digital_storage['gigabytes']}"
    return value


