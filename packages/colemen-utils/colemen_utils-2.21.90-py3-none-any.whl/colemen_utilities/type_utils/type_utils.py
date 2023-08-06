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
from typing import Union
import json
import colemen_utilities.dict_utils as _obj


_BOOL_TRUE_SYNONYMS = ["TRUE", "true", "True", "yes", "y", "1","sure","correct","affirmative"]
_BOOL_FALSE_SYNONYMS = ["FALSE", "false", "False", "no", "n", "0","wrong","incorrect","nope","negative"]

_VALID_PYTHON_TYPES = {
    "str":["string","str","text","varchar"],
    "int":["integer","number","int"],
    "float":["float","double"],
    "list":["list","array"],
    "tuple":["tuple","set"],
    "set":["set"],
    "dict":["dictionary","dict"],
    "boolean":["boolean","bool"]
}
_VALID_PHP_TYPES = {
    "string":["string","str","text","varchar","mediumtext","tinytext","longtext","char",],
    "int":["integer","number","int","tinyint","mediumint","smallint","bigint","dec",],
    "float":["float","double","decimal"],
    "array":["list","array","dictionary","dict","tuple","set"],
    "bool":["boolean","bool"],
    "null":["null","none"],
}


# _sql_data_types = [
#     "mediumblob",
#     "varbinary",
#     "timestamp",
#     "tinyblob",
#     "longblob",
#     "datetime",
#     "binary",
#     "year",
#     "time",
#     "enum",
#     "date",
#     "blob",
#     "set",
#     "dec",
#     "bit",
# ]


def type_to_php(value:str)->str:
    value = value.lower()
    for k,v in _VALID_PHP_TYPES.items():
        if value in v:
            return k
    return None

def determine_boolean(value:str, def_val=None)->bool:
    '''
        Attempts to determine a boolean value from a string using synonyms

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to parse for a boolean value.

        [`def_val`=None] {mixed}
            The value to return if a boolean cannot be determined

        Return {bool|None|Mixed}
        ----------------------
        True if the value contains a True synonym.
        False if the value contains a False synonym.
        def_val [None] if no boolean value can be determined.


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:10:55
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: determine_boolean
    '''
    result = def_val
    if value in _BOOL_TRUE_SYNONYMS:
        result = True
    if value in _BOOL_FALSE_SYNONYMS:
        result = False
    return result

def python_type_name(value):
    '''
        Attempts to determine the type name of the value provided.
        It checks if the value is a synonym of a known python type.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The value to test.

        Return {string|None}
        ----------------------
        The type if it can be determined, None otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-21-2022 12:03:11
        `version`: 1.0
        `method_name`: python_type_name
        # @TODO []: documentation for python_type_name
    '''

    results = []
    if isinstance(value,(str)):
        value = [value]
    else:
        return None

    for test_val in value:
        test_val = test_val.lower()
        for type_name,val in _VALID_PYTHON_TYPES.items():
            if test_val in val:
                results.append(type_name)
    results = list(set(results))
    if len(results) == 0:
        return None
    if len(results) == 1:
        return results[0]
    return results

def to_string(value,convert_values=False,bools_to_ints=False):
    '''
        Convert the value to a string.
        ----------

        Arguments
        -------------------------
        `value` {type}
            The value to convert

        [`convert_values`=False] {bool}
            If True and the value is a list/dict, it will convert all values to strings.
            Otherwise, it will jsonify the entire value.

        [`bools_to_ints`=False] {bool}
            if True, bools will be a string integer "1" for True and "0" for False.

        Return {str}
        ----------------------
        The value converted to a string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-09-2023 07:49:07
        `memberOf`: type_utils
        `version`: 1.0
        `method_name`: to_string
        * @xxx [03-09-2023 07:51:21]: documentation for to_string
    '''
    if isinstance(value,(bool)):
        return bool_to_string(value,number=bools_to_ints)
    if isinstance(value,(int,float)):
        return str(value)
    if isinstance(value,(dict,list)):
        if convert_values is True:
            if isinstance(value,(dict)):
                nv = {}
                for k,v in value.items():
                    nv[k] = to_string(v)
                return nv
            if isinstance(value,(list)):
                nv = []
                for v in value:
                    nv.append(to_string(v))
                return nv
        else:
            return json.dumps(value)

    return value

def bool_to_string(value:bool,number=False):
    '''
        Converts a boolean value to a string representation.

        ----------

        Arguments
        -------------------------
        `value` {bool}
            The boolean to convert

        [`number`=False] {bool}
            if True, the result will be a string integer "1" for True and "0" for False.

        Return {string|None}
        ----------------------
        ("true"|"1") if the boolean is True, ("false"|"0") if it is False.

        None otherwise

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:57:03
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: bool_to_string
    '''


    # number = _obj.get_kwarg(["number"], False, (bool), **kwargs)
    result = None
    if value is True:
        result = "true"
        if number is True:
            result = "1"
    if value is False:
        result = "false"
        if number is True:
            result = "0"
    return result

def bool_to_int(value,default=0):
    '''
        Convert a boolean value to its integer equivalent.

        ----------

        Arguments
        -------------------------
        `value` {bool}
            The boolean to convert
        [`default`=0] {any}
            The default value to return if a boolean cannot be determined.



        Return {int}
        ----------------------
        The integer equivalent

        True = 1
        False = 0

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 13:46:56
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: bool_to_int
        * @xxx [06-01-2022 13:48:26]: documentation for bool_to_int
    '''


    if isinstance(value,(bool)) is False:
        return default

    if value is True:
        return 1
    if value is False:
        return 0

def to_bool(value,default=False,null_default=False):
    '''
        Convert a string to its boolean equivalent.

        ----------

        Arguments
        -------------------------
        `value` {str}
            the value to convert.

        [`default`=False] {any}
            The default value to return if a boolean cannot be determined.

        [`null_default`=False] {any}
            The default value to return if the value is null.

        Return {bool}
        ----------------------
        The boolean equivalent if successful, the default value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 13:40:42
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: to_bool
        * @xxx [06-01-2022 13:42:09]: documentation for to_bool
    '''
    if value is None:
        return null_default

    if isinstance(value,(bool)):
        return value

    True_syns =["yes","y","sure","correct","indeed","right","affirmative","yeah","ya","true","1"]
    False_syns =["no","n","wrong","incorrect","false","negative","0"]
    if str(value).lower() in True_syns:
        return True
    if str(value).lower() in False_syns:
        return False

    return default

def is_scalar(value:any,exclude_bool=False)->bool:
    '''
        Determine if the value provided is scalar.

        Scalar includes:
        - string
        - integer
        - float
        - bool

        ----------

        Arguments
        -------------------------
        `value` {any}
            The value to test.

        [`exclude_bool`=False] {bool}
            If True, bool is not considered a scalar.


        Return {bool}
        ----------------------
        True if the value is scalar False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:56:10
        `memberOf`: objectUtils
        `version`: 1.0
        `method_name`: is_scalar
        * @xxx [06-03-2022 07:57:32]: documentation for is_scalar
    '''
    scalar = (str,int,float,bool)
    if exclude_bool is True:
        scalar = (str,int,float)


    if isinstance(value,scalar):
        return True
    return False

def is_list_of_dicts(value:any)->bool:
    '''
        Determine if the value is a list of dictionaries.
        ----------

        Arguments
        -------------------------
        `value` {any}
            The value to test.


        Return {bool}
        ----------------------
        True if the ALL items in the value are dictionaries, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-06-2022 08:47:05
        `memberOf`: type_utils
        `version`: 1.0
        `method_name`: is_list_of_dicts
        * @xxx [12-06-2022 08:47:59]: documentation for is_list_of_dicts
    '''
    output = False
    if isinstance(value,(list)):
        result = True

        for itm in value:
            if isinstance(itm,(dict)) is False:
                result = False
        if result is True:
            output = True
    return output

def to_number(value:Union[str,int,float],default=None):
    from colemen_utilities.validate_utils.general import is_float,is_integer
    if isinstance(value,(int,float)):
        return value
    if isinstance(value,(str)):
        if is_float(value):
            return float(value)
        if is_integer(value):
            return int(value)
    return default









