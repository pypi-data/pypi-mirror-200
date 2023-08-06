# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    A module of utility methods used for parsing SQL code.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:04:06
    `memberOf`: parse_sql
    `version`: 1.0
    `method_name`: parse_sql
'''


from dataclasses import dataclass,field
import re as _re
import json as _json
import shlex as _shlex
import sqlparse as _sqlparse
import yaml
from typing import Iterable, List, Union as _Union

from pyparsing import And, Suppress,Dict, Word, Literal, Group, Optional, ZeroOrMore, OneOrMore, Regex, restOfLine, alphanums,nums, printables, string, CaselessKeyword,nestedExpr,ParseException,quotedString,removeQuotes,originalTextFor,delimitedList,QuotedString

# import colemen_utilities.dict_utils as _obj
# import colemen_utilities.list_utils as _lu
# import colemen_utilities.string_utils as _csu
# import colemen_utilities.file_utils as _f
import colemen_utilities.sql_utils.sql_utils as _sql
# import colemen_utilities.sql_utils.sql_parse as _parse_sql
# import colemen_utilities.sql_utils as _sql_utils
# import colemen_utilities.console_utils as _console
# import colemen_utilities.sql_utils.KeyStatement as _key_statement
# import colemen_config as _config
# _log = _console.log



# def insert_from_dict(data:dict,table_name,schema_name=None):
#     table = f"`{schema_name}`.`{table_name}`"
#     if schema_name is None:
#         table = f"`{table_name}`"

#     column_string = _sql._gen_column_string(data.keys())

#     value_string = ','.join(['%s' for x in list(range(len(data.keys())))])
#     # for k,v in data.items():
#     sql = f"INSERT INTO {table} ({column_string}) VALUES ({value_string})"
#     return (sql,list(data.values()))

# # statement_types = ["CREATE DATABASE","ALTER DATABASE","CREATE SCHEMA","CREATE INDEX","CREATE TABLE","ALTER TABLE","INSERT INTO","DROP INDEX","DROP TABLE","DELETE","UPDATE","SELECT",]

# @dataclass
# class Query:
#     limit:int = 1000
#     offset:int = 0
#     table_name:str = None
#     schema_name:str = None
#     action:str = "INSERT"
#     data = None
#     insert_group_size = 500
    
#     def __init__(self):
#         pass
    
#     @property
#     def _table_sql_string(self):
#         '''
#             Get this query's _table_sql_string

#             `default`:None


#             Meta
#             ----------
#             `@author`: Colemen Atwood
#             `@created`: 12-06-2022 08:39:57
#             `@memberOf`: query
#             `@property`: _table_sql_string
#         '''
#         value = f"`{self.schema_name}`.`{self.table_name}`"
#         if self.schema_name is None:
#             value = f"`{self.table_name}`"
#         return value
    
#     def _gen_insert(self):
            
            
    
    
    
    