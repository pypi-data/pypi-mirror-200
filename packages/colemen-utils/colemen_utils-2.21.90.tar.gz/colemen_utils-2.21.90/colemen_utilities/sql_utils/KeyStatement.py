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


from dataclasses import dataclass
import re as _re
import json as _json
import shlex as _shlex
import sqlparse as _sqlparse
import yaml
from typing import Iterable, Union as _Union

from pyparsing import And, Suppress,Dict, Word, Literal, Group, Optional, ZeroOrMore, OneOrMore, Regex, restOfLine, alphanums,nums, printables, string, CaselessKeyword,nestedExpr,ParseException,quotedString,removeQuotes,originalTextFor,delimitedList,QuotedString

import colemen_utilities.dict_utils as _obj
import colemen_utilities.list_utils as _lu
import colemen_utilities.string_utils as _csu
import colemen_utilities.file_utils as _f
# import colemen_utilities.parse_sql as _parse_sql
import colemen_utilities.sql_utils as _sql_utils
import colemen_utilities.console_utils as _console
# import colemen_config as _config
_log = _console.log



_tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
_quote = (_tick|_double_quote|_single_quote)
_open_paren,_close_paren = [Suppress(x) for x in list('()')]
quoted_word = _quote + Word(alphanums + "_") + _quote
'''Matches [`"']ALPHA_NUM[`"']'''
paren_word_list = _open_paren + Word(alphanums + "_,'\"` ") + _close_paren
paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren


@dataclass
class KeyStatement:
    raw_statement:str = None
    '''The raw (unmodified) SQL statement for the key.'''
    key_name:str = None
    '''The name of the key.'''
    key_type:str = None
    '''The type of key [fulltext,unique,primary]'''
    is_index:bool = False
    '''True if the key is an index.'''
    index_type:str = None
    '''The type of index this key represents. [fulltext,primary_key]'''
    is_constraint:bool = False
    '''True if this key is a constraint.'''
    constraint_type:str = None
    '''The type of constraint this key represents. [unique]'''
    comment:str = None
    '''The SQL comment if one is found.'''
    foreign_col_name = None
    '''The name(s) of the foreign key if one is found'''
    columns = None
    '''The column names associated to this key'''
    
    local_col_name:str = None
    '''The name of the local column used in a foreign key constraint'''
    foreign_col_name:str = None
    '''The name of the foreign column used in a foreign key constraint'''
    schema_name:str = None
    '''The name of the foreign tables schema used in a foreign key constraint'''
    on_delete:str = None
    '''The action to perform on delete used in a foreign key constraint'''
    on_update:str = None
    '''The action to perform on an update used in a foreign key constraint'''

    def __init__(self,raw_statement):
        self.raw_statement = raw_statement

    @property
    def summary(self):
        '''
            Get this KeyStatement's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 11-30-2022 12:08:05
            `@memberOf`: KeyStatement
            `@property`: summary
        '''
        value = {
            "raw_statement":self.raw_statement,
            "key_name":self.key_name,
            "key_type":self.key_type,
            "is_index":self.is_index,
            "index_type":self.index_type,
            "is_constraint":self.is_constraint,
            "constraint_type":self.constraint_type,
            "comment":self.comment,
            "foreign_col_name":self.foreign_col_name,
            "columns":self.columns,
            "local_col_name":self.local_col_name,
            "foreign_col_name":self.foreign_col_name,
            "schema_name":self.schema_name,
            "on_delete":self.on_delete,
            "on_update":self.on_update,
        }
        return value

    def parse(self):
        if isinstance(self.raw_statement,(str)) is False:
            raise Exception("No raw_statement provided.")
        _parse_key(self,self.raw_statement)
        _parse_fulltext_key(self)
        _parse_unique_key(self)
        _parse_primary_key(self)
        _parse_constraint(self)

def _parse_key(key:KeyStatement,value=None):

    if 'key' not in value.lower():
        return None

    # value ="KEY `FK_ActivityLogs_ActivityTypeID` (`activity_type_id`, `activity_type_hash_id`),"
    # _tick,_double_quote,_single_quote,_comma = [Suppress(x) for x in list('`"\',')]
    # _quote = (_tick|_double_quote|_single_quote)
    # _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    # paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    # quoted_word = _quote + Word(alphanums + "_") + _quote

    # paren_word_list = _open_paren + Word(alphanums + "_,'\"` ") + _close_paren

    # KEY `FK_ActivityLogs_RequestLogID`
    key_name = Optional(CaselessKeyword('unique')) + Suppress(CaselessKeyword('KEY')) + quoted_word.setResultsName('key_name')

    foreign_col_name = paren_word_list.setResultsName('foreign_col_name').setParseAction(_sql_utils.parse_list)

    grammar = key_name + foreign_col_name
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']
        new_data = {}
        for k,v in data.items():
            if k == "foreign_col_name":
                new_data[k] = v.split(",")
                continue
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v

        # print(new_data)
        output = new_data

    
    if output is not None:
        for k,v in output.items():
            if hasattr(key,k):
                setattr(key,k,v)
    
    return output



def _parse_primary_key(key:KeyStatement):
    value = key.raw_statement
    if 'primary key' not in value.lower():
        return None
    # value = "PRIMARY KEY (`activity_log_id`)"
    # value = "PRIMARY KEY (`activity_type_id`, `activity_type_hash_id`),"
    # _tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
    # _quote = (_tick|_double_quote|_single_quote)
    # _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    # paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    # quoted_word = _quote + Word(alphanums + "_") + _quote
    # paren_word_list = _open_paren + Word(alphanums + "_,'\"` ") + _close_paren
    primary_key = paren_word_list.setResultsName('primary_key').setParseAction(_sql_utils.parse_list)
    grammar = Suppress(CaselessKeyword('primary key')) + primary_key
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']
        new_data = {
            "is_index":True,
            "index_type":"primary_key"
        }
        for k,v in data.items():
            if k == "primary_key":
                new_data[k] = v.split(",")
                continue
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v

        # print(new_data)
        output = new_data

    if output is not None:
        for k,v in output.items():
            if hasattr(key,k):
                setattr(key,k,v)

    return output


def _parse_unique_key(key:KeyStatement):
    value = key.raw_statement
    if 'unique key' not in value.lower():
        return None
    # UNIQUE KEY `Unique_barnBlocks_barnID_userID_3006` (`user_id`, `barn_id`) COMMENT 'Unique constraint to ensure a barn cannot block the same user multiple times.',

    _tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
    _quote = (_tick|_double_quote|_single_quote)
    _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    # paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    quoted_word = _quote + Word(alphanums + "_") + _quote


    paren_word_list = _open_paren + Word(alphanums + "_,'\"` ") + _close_paren
    unique_key = paren_word_list.setResultsName('columns').setParseAction(_sql_utils.parse_list)
    key_name = quoted_word.setResultsName('key_name')

    comment = None
    match = _re.findall(r"comment\s*'([^']*)",value,_re.IGNORECASE)
    if isinstance(match,(list)) and len(match) > 0:
        comment = match[0]

    grammar = Suppress(CaselessKeyword('unique key')) + key_name + unique_key
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']

        new_data = {
            "is_index":True,
            "is_constraint":True,
            "index_type":"unique",
            "comment":comment,
        }
        for k,v in data.items():
            if k == "columns":
                new_data[k] = v.split(",")
                continue
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v
        # print(f"Unique Key Data: {new_data}")
        # print(new_data)
        output = new_data
    if output is not None:
        for k,v in output.items():
            if hasattr(key,k):
                setattr(key,k,v)
        
    return output

def _parse_fulltext_key(key:KeyStatement):
    value = key.raw_statement
    # value = "FULLTEXT KEY `FullText_regAss_name_3079` (`name`) COMMENT 'A fullText Index on the registration association name for searching.'"

    value = _re.sub(r'full[^a-z]*text[^a-z]*key','fulltext key',value,_re.IGNORECASE)
    if 'fulltext key' not in value.lower():
        return None

    value,comment_value = _sql_utils._parse_statement_comment(value)
    # print(f"after comment: {value}")

    # FULLTEXT KEY `FullText_regAss_name_3079` (`name`) COMMENT 'A fullText Index on the registration association name for searching.'

    # _tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
    # _quote = (_tick|_double_quote|_single_quote)
    # _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    # paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren

    # matches : `FullText_regAss_name_3079`
    # quoted_word = _quote + Word(alphanums + "_") + _quote


    # paren_word_list = _open_paren + Word(alphanums + "_,'\"` ") + _close_paren
    column_list = paren_word_list.setResultsName('columns').setParseAction(_sql_utils.parse_list)
    key_name = quoted_word.setResultsName('constraint_name')

    # comment = None
    # match = _re.findall(r"comment\s*'([^']*)",value,_re.IGNORECASE)
    # if isinstance(match,(list)) and len(match) > 0:
    #     comment = match[0]

    grammar = Suppress(CaselessKeyword('fulltext key')) + key_name + column_list
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']

        new_data = {
            "is_index":True,
            "index_type":"fulltext",
            "comment":comment_value,
        }


        for k,v in data.items():
            if k == "columns":
                new_data[k] = v.split(",")
                continue
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v
        # print(f"fulltext Key Data: {new_data}")
        # print(new_data)
        output = new_data

    if output is not None:
        for k,v in output.items():
            if hasattr(key,k):
                setattr(key,k,v)

    return output

def _parse_constraint(key:KeyStatement=None):
    '''
        Parse constraint data from the string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to parse.

        Return {dict,None}
        ----------------------
        The constraint data dictionary if successful, None otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 20:20:57
        `memberOf`: sql_parse
        `version`: 1.0
        `method_name`: parse_constraint
        * @xxx [06-05-2022 20:26:05]: documentation for parse_constraint
    '''
    # CONSTRAINT `FK_users_files_profileImageID_KyOEqngrNiZd` FOREIGN KEY (`profile_image_id`) REFERENCES `files` (`file_id`) ON DELETE SET NULL ON UPDATE CASCADE
    # CONSTRAINT `FK_User_ProfileImageID_File` FOREIGN KEY `fkIdx_910` (`profile_image_id`) REFERENCES `idealech_Equari_Content_Database`.`files` (`file_id`) ON DELETE CASCADE ON UPDATE CASCADE
    value = key.raw_statement
    if _sql_utils.is_line_constraint(value) is False:
        return None
    # _tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
    # _quote = (_tick|_double_quote|_single_quote)
    # _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    # paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    # quoted_word = _quote + Word(alphanums + "_") + _quote

    constraint_conditions = (CaselessKeyword('RESTRICT') | CaselessKeyword('CASCADE') | CaselessKeyword('SET NULL') | CaselessKeyword('NO ACTION') | CaselessKeyword('SET DEFAULT'))

    # MATCHES = CONSTRAINT `FK_users_files_profileImageID_KyOEqngrNiZd` 
    constraint_name = Suppress(CaselessKeyword('CONSTRAINT')) + quoted_word.setResultsName('constraint_name')

    # MATCHES = FOREIGN KEY (`profile_image_id`)
    foreign_key_name = Suppress(CaselessKeyword('FOREIGN KEY')) + Optional(quoted_word.setResultsName('foreign_key')) | Suppress(CaselessKeyword('FOREIGN KEY'))
    # foreign_key_name = Suppress(CaselessKeyword('FOREIGN KEY')) + Optional(quoted_word.setResultsName('foreign_key'))
    local_col_name = paren_word.setResultsName('local_col_name')
    
    
    foreign_table = Suppress(CaselessKeyword('REFERENCES')) + Optional(quoted_word.setResultsName('schema_name') + _period) + quoted_word.setResultsName('table_name')
    # foreign_table = Suppress(CaselessKeyword('REFERENCES')) + Optional(quoted_word.setResultsName('schema_name') + _period) + quoted_word.setResultsName('table_name')
    foreign_col_name = paren_word.setResultsName('foreign_col_name')

    on_delete = Suppress(CaselessKeyword('ON DELETE')) + constraint_conditions.setResultsName('on_delete')
    on_update = Suppress(CaselessKeyword('ON UPDATE')) + constraint_conditions.setResultsName('on_update')
    constraints = ZeroOrMore(on_delete | on_update)

    grammar = constraint_name + foreign_key_name + local_col_name + foreign_table + foreign_col_name + constraints
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    comment = None
    match = _re.findall(r"comment\s*'([^']*)",value,_re.IGNORECASE)
    if isinstance(match,(list)) and len(match) > 0:
        comment = match[0]

    if len(res) > 0:
        data = res.as_dict()['data']
        key.is_constraint = True
        new_data = {
            "comment":comment
        }
        for k,v in data.items():
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v

        # print(new_data)
        output = new_data
        
    if output is not None:
        for k,v in output.items():
            if hasattr(key,k):
                setattr(key,k,v)
        
    return output






