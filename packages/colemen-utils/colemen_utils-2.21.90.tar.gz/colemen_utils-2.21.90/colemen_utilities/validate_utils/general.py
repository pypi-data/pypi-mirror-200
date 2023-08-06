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
import re as _re
from typing import Union
import colemen_utilities.dict_utils as _obj
import colemen_utilities.string_utils as _csu
import colemen_utilities.list_utils as _arr
import colemen_utilities.type_utils as _type

def is_email(value:str)->bool:
    '''
        Determine if the value is an email address.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to validate

        Return {bool}
        ----------------------
        True if it is an email, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:53:20
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_email
        * @xxx [01-06-2023 09:54:06]: documentation for is_email
    '''
    if isinstance(value,(str)) is False:
        return False
    if _re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',value) is None:
        return False
    return True

def alpha_only(value:str)->bool:
    return False if _re.match(r'^[a-zA-Z]*$',value) is None else True

def alphanumeric_only(value:str)->bool:
    return False if _re.match(r'^[a-zA-Z0-9]*$',value) is None else True

def is_integer(value:Union[str,int],negatives=True):
    '''
        Determine if the value provided is an integer.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.

        Return {bool}
        ----------------------
        True if the value is an integer or string containing an integer, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:38:36
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_integer
        * @xxx [01-06-2023 09:39:49]: documentation for is_integer
    '''

    if isinstance(value,(int)):
        if negatives is False:
            if value < 0:
                return False
        return True

    # @Mstep [] determine the appropriate regex to use.
    reg = r'^[0-9]*$'

    if negatives is True:
        reg = r'^[0-9-]*$'


    # @Mstep [IF] if the value is a string.
    if isinstance(value,(str)):
        # @Mstep [] strip leading and trailing spaces.
        value = _csu.strip(value,[" "])
        return False if _re.match(reg,value) is None else True

def is_float(value:Union[str,float],negatives=True):
    '''
        Determine if the value provided is a float.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.

        Return {bool}
        ----------------------
        True if the value is an float or string containing an float, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:38:36
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_float
        * @xxx [01-06-2023 09:39:49]: documentation for is_float
    '''

    if isinstance(value,(int)):
        if negatives is False:
            if value < 0:
                return False
        return True

    if isinstance(value,(str)):

        # @Mstep [] determine the appropriate regex to use.
        reg = r'^[0-9]*\.[0-9]*$'

        if negatives is True:
            reg = r'^[0-9-]*\.[0-9]*$'

        # @Mstep [] strip leading and trailing spaces.
        value = _csu.strip(value,[" "])
        return False if _re.match(reg,value) is None else True
    return isinstance(value,(int))

def numeric_only(value:str,negatives=True)->bool:
    '''
        Determine if the value is an integer or float.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.


        Return {bool}
        ----------------------
        True if the value contains an integer or float, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:48:24
        `memberOf`: general
        `version`: 1.0
        `method_name`: numeric_only
        * @xxx [01-06-2023 09:49:15]: documentation for numeric_only
    '''
    if isinstance(value,(str)):
        value = _csu.strip(value,[" "])
        if len(value) == 0:
            return False

    if is_integer(value,negatives):
        return True
    if is_float(value,negatives):
        return True
    return False

def phone_number(value:str)->bool:
    return False if _re.match(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',value) is None else True

def ip_address(value:Union[str,int])->bool:
    import ipaddress
    try:
        ipaddress.ip_address(value)
        # print("Valid IP Address")
        return True
    except ValueError:
        pass
        # print("Invalid IP Address")
    return False

def future_unix(value:int)->bool:
    '''
        Determine if the value provided is a unix timestamp set in the future.
        ----------


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-05-2022 13:58:56
        `memberOf`: cerberus
        `version`: 1.0
        `method_name`: future_unix
        * @TODO []: documentation for future_unix
    '''
    import time
    return False if value <= time.time() else True

def past_unix(value:int)->bool:
    '''
        Determine if the value provided is a unix timestamp set in the past.
        ----------


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-05-2022 13:58:56
        `memberOf`: cerberus
        `version`: 1.0
        `method_name`: past_unix
        * @TODO []: documentation for past_unix
    '''
    import time
    return False if value >= time.time() else True

def to_hash_id(value:str,prefix:str):
    if prefix not in value:
        value= f"{prefix}_{value}"

def crud_type(value:str):
    aliases = {
        "create":["create","c","1","cr","cre","crea","creat"],
        "read":["read","r","2","re","rea"],
        "update":["update","u","3","up","upd","upda","updat"],
        "delete":["delete","d","4","de","del","dele","delet"],
    }
    if isinstance(value,(str,int)) is False:
        return False
    if isinstance(value,(int)):
        value = str(value)

    value = _csu.strip(value,[" "])
    value = value.lower()

    for k,v in aliases.items():
        if value in v:
            return k
    return False
    valids = ["create","read","update","delete"]
    if value.lower() not in valids:
        return False
    return True

def request_method(value:str)->Union[str,bool]:
    '''
        Validate that the value is an HTTP request method.
        
        This will match partial names as well.
        ----------

        Arguments
        -------------------------
        `value` {str}
            The value to test

        Return {str,bool}
        ----------------------
        The request name if successful, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-15-2023 11:48:27
        `memberOf`: general
        `version`: 1.0
        `method_name`: request_method
        * @xxx [03-15-2023 11:49:30]: documentation for request_method
    '''
    if isinstance(value,(str)) is False:
        return False
    valids = {
        "options":["options","o","op","opt","opti","optio","option"],
        "connect":["connect","c","co","con","conn","conne","connec"],
        "delete":["delete","d","de","del","dele","delet"],
        "patch":["patch","pa","pat","patc"],
        "trace":["trace","t","tr","tra","trac"],
        "head":["head","h","he","hea"],
        "post":["post","po","pos"],
        "get":["get","g","ge","get"],
        "put":["put","pu","put"],
    }
    # valids = ["connect","delete","get","head","options","patch","post","put","trace"]
    for k,v in valids.items():
        if value.lower() in v:
            return k

    return False

def required_keys(required:list,data:dict)->Union[list,None]:
    '''
        Confirm that the data contains all of the required keys.
        ----------

        Arguments
        -------------------------
        `required` {list}
            The list of required keys
        `data` {dict}
            The dictionary to test.

        Return {list}
        ----------------------
        A list of missing keys if there are any, None otherwise

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-27-2023 12:59:52
        `version`: 1.0
        `method_name`: required_keys
        * @xxx [02-27-2023 13:01:22]: documentation for required_keys
    '''
    missing_keys = []
    for rq in required:
        if rq not in data:
            missing_keys.append(rq)
    if len(missing_keys) == 0:
        missing_keys = None
    return missing_keys

def data_type(
    value,
    data_type:Union[list,str],
    allow_nulls:bool=False,
    coerce_bools:bool=True
    )->bool:
    '''
        Validate that the value provided belongs to one to the types provided.
        ----------

        Arguments
        -------------------------
        `value` {any}
            The value to test
        `data_type` {str,list}
            A data type name or list of names to test for.
        [`allow_nulls`=False] {bool}
            If True the value is allowed to be None or any of the data_types provided.


        Return {bool}
        ----------------------
        True if the data type is matched, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-27-2023 13:24:20
        `memberOf`: general
        `version`: 1.0
        `method_name`: data_type
        * @xxx [02-27-2023 13:26:11]: documentation for data_type
    '''
    data_type = _arr.force_list(data_type)
    data_type = [_type.python_type_name(x) for x in data_type]
    if allow_nulls is True and value is None:
        return True
    if "boolean" in data_type and coerce_bools is True:
        data_type.append("bool")
        # print(f"data_type:{data_type}")
        tmp = _type.to_bool(value,None)
        # print(f"tmp: {tmp}")
        if tmp is not None:
            value = tmp

    val_type = type(value).__name__
    # print(f"val_type:{val_type}")
    
    if val_type not in data_type:
        return False
    return True

def value_length(
    value:str,
    min_len:Union[int,float]=None,
    max_len:Union[int,float]=None,
    inclusive:bool=True
    )->Union[tuple,bool]:
    result = True
    if isinstance(value,(int,float)):
        value = str(value)

    val_len = len(value)
    if min_len is not None and max_len is None:
        result = (val_len,min_len,None)
        if inclusive is True:
            if min_len <= val_len:
                result = True
        else:
            if min_len < val_len:
                result = True

    if min_len is not None and max_len is not None:
        result = (val_len,min_len,max_len)
        if inclusive is True:
            if min_len <= val_len <= max_len:
                result = True
        else:
            if min_len < val_len < max_len:
                result = True

    if min_len is None and max_len is not None:
        result = (val_len,None,max_len)
        if inclusive is True:
            if val_len <= max_len:
                result = True
        else:
            if val_len < max_len:
                result = True


    return result

def value_count(
    value:str,
    min_val:Union[int,float]=None,
    max_val:Union[int,float]=None,
    inclusive:bool=True
    )->Union[tuple,bool]:
    result = True
    if isinstance(value,(int,float)) is False:
        return True

    
    if min_val is not None and max_val is None:
        result = (value,min_val,None)
        if inclusive is True:
            if min_val <= value:
                result = True
        else:
            if min_val < value:
                result = True

    if min_val is not None and max_val is not None:
        result = (value,min_val,max_val)
        if inclusive is True:
            if min_val <= value <= max_val:
                result = True
        else:
            if min_val < value < max_val:
                result = True

    if min_val is None and max_val is not None:
        result = (value,None,max_val)
        if inclusive is True:
            if value <= max_val:
                result = True
        else:
            if value < max_val:
                result = True


    return result


