# # pylint: disable=missing-function-docstring
# # pylint: disable=missing-class-docstring
# # pylint: disable=line-too-long
# # pylint: disable=unused-wildcard-import
# # pylint: disable=wildcard-import
# # pylint: disable=unused-import
# '''
#     A module of utility methods used for parsing SQL code.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 06-03-2022 10:04:06
#     `memberOf`: parse_sql
#     `version`: 1.0
#     `method_name`: parse_sql
# '''


# from dataclasses import dataclass
# import re as _re
# import json as _json
# import shlex as _shlex
# import sqlparse as _sqlparse
# import yaml
# from typing import Union as _Union

# from pyparsing import And, Suppress,Dict, Word, Literal, Group, Optional, ZeroOrMore, OneOrMore, Regex, restOfLine, alphanums,nums, printables, string, CaselessKeyword,nestedExpr,ParseException,quotedString,removeQuotes,originalTextFor,delimitedList,QuotedString

# import colemen_utilities.dict_utils as _obj
# import colemen_utilities.list_utils as _lu
# import colemen_utilities.string_utils as _csu
# import colemen_utilities.file_utils as _f
# import colemen_utilities.sql_utils as _sql
# import colemen_utilities.console_utils as _console
# # import colemen_config as _config
# _log = _console.log







# @dataclass
# class ColumnDeclaration:
#     column_name:str = None
#     column_type:str = None
#     character_maximum_length:int = None
#     is_nullable:bool = False
#     _default:bool = False
#     column_comment:str = None

#     @property
#     def summary(self):
#         '''
#             Get this ColumnDeclaration's summary

#             `default`:None


#             Meta
#             ----------
#             `@author`: Colemen Atwood
#             `@created`: 11-30-2022 10:31:24
#             `@memberOf`: ColumnDeclaration
#             `@property`: summary
#         '''
#         value = {
#             "column_name":self.column_name,
#             "column_type":self.column_type,
#             "character_maximum_length":self.character_maximum_length,
#             "is_nullable":self.is_nullable,
#             "_default":self._default,
#             "column_comment":self.column_comment,
#         }
#         return value

#     @property
#     def default(self)->str:
#         '''
#             Get the default value.

#             `default`:None


#             Meta
#             ----------
#             `@author`: Colemen Atwood
#             `@created`: 11-30-2022 10:28:44
#             `@memberOf`: PostArg
#             `@property`: default
#         '''
#         value = self._default
#         return value

#     @default.setter
#     def default(self,value:str):
#         '''
#             Set the default value.

#             Meta
#             ----------
#             `@author`: Colemen Atwood
#             `@created`: 11-30-2022 10:28:44
#             `@memberOf`: PostArg
#             `@property`: default
#         '''
#         if value == "NULL":
#             value = None
#         self._default = value
