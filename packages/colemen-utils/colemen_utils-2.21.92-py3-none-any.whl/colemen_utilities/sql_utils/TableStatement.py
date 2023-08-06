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

import colemen_utilities.dict_utils as _obj
import colemen_utilities.list_utils as _lu
import colemen_utilities.string_utils as _csu
import colemen_utilities.file_utils as _f
import colemen_utilities.sql_utils.sql_parse as _parse_sql
import colemen_utilities.sql_utils as _sql_utils
import colemen_utilities.console_utils as _console
import colemen_utilities.sql_utils.KeyStatement as _key_statement
# import colemen_config as _config
_log = _console.log







@dataclass
class TableStatement:
    raw_statement:str = None
    '''The raw (unmodified) SQL statement for the table.'''
    raw_column_lines:str = None
    '''The contents of a create statement'''
    action:str = None
    '''The action that this table statement performs [CREATE,DROP]'''
    test:str = None
    schema_name:str = None
    '''The name of the schema this table belongs to.'''
    comment:str = None
    '''The SQL comment if one is found.'''
    
    _keys = None
    _constraints = None
    _indexes = None

    def __init__(self,raw_statement):
        self.raw_statement = raw_statement
        self._keys = []
        self._constraints = []
        self._indexes = []



    @property
    def summary(self):
        '''
            Get this TableStatement's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 11-30-2022 11:49:43
            `@memberOf`: TableStatement
            `@property`: summary
        '''
        value = {
            "raw_statement":self.raw_statement,
            "raw_column_lines":self.raw_column_lines,
            "action":self.action,
            "test":self.test,
            "schema_name":self.schema_name,
            "comment":self.comment,
            "keys":[x.summary for x in self._keys],
            "constraints":[x.summary for x in self._constraints],
            "indexes":[x.summary for x in self._indexes],
        }
        
        return value

    def parse(self):
        if isinstance(self.raw_statement,(str)) is False:
            raise Exception("No raw_statement provided.")
        _parse_table_statement(self,self.raw_statement)

    def add_key(self,key:_key_statement.KeyStatement):
        if key.is_constraint:
            self._constraints.append(key)
        if key.is_index:
            self._indexes.append(key)
        self._keys.append(key)

def _parse_table_statement(table:TableStatement,value:_Union[None,str]=None)->_Union[TableStatement,None]:
    '''
        Parse a table SQL statement.

        ----------

        Arguments
        -------------------------
        `value` {str,None}
            The SQL string to parse.

        Return {dict,None}
        ----------------------
        The statement data dictionary if it can be parsed, None otherwise.

        {
            `action`: "create",
            `test`: "if not exists",
            `schema_name`: "idealech_Equari_Management_Database",
            `table_name`: "faq_categories",
            `raw_statement`: "Original and Unmodified Create Statement Goes here.",
            `columns`: [
                {
                    "name": "faq_category_id",
                    "type": "int",
                    "allow_nulls": false,
                    "default": null,
                    "comment": null,
                    "is_primary_key": false,
                    "primary_key": true
                },
                ...
            ],
            `primary_keys`: [
                "faq_category_id"
            ],
            `keys`: [
                {
                    "key_name": "FK_FaqCategories_FaqCategoryID",
                    "foreign_col_name": [
                        "parent_faq_category_id"
                    ]
                }
            ],
            `constraints`: [
                {
                    "constraint_name": "FK_FaqCategory_Parent_FaqCategory",
                    "foreign_key": "FK_FaqCategories_FaqCategoryID",
                    "local_col_name": "parent_faq_category_id",
                    "schema_name": "idealech_Equari_Management_Database",
                    "table_name": "faq_categories",
                    "foreign_col_name": "faq_category_id",
                    "on_delete": "CASCADE",
                    "on_update": "CASCADE"
                }
            ],
            `name`: "faq_categories"
        }



        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 20:30:22
        `memberOf`: sql_parse
        `version`: 1.0
        `method_name`: parse_table_statement
        * @xxx [06-05-2022 20:34:11]: documentation for parse_table_statement
    '''
    # _log("sql_parse.parse_table_statement")
    # value = _re.sub(r"COLLATE\s?(?:utf8_unicode_ci)"," ",value)
    value = _re.sub(r"\s?AUTO_INCREMENT=[0-9]*","",value)
    value = _re.sub(r"\s?ENGINE=[a-zA-Z0-9_]*","",value)
    value = _re.sub(r"\s?DEFAULT CHARSET=[a-zA-Z0-9_]*","",value)
    value = _re.sub(r"\s?COLLATE=[a-zA-Z0-9_]*","",value)
    value = value.replace(" DEFAULT NULL"," NULL DEFAULT NULL")
    value = _re.sub(r"[ \t]{2,}"," ",value)
    
    
    # @Mstep [] capture the comment if it is found in the line.
    value,comment_value = _parse_sql._parse_statement_comment(value)
    


    _tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
    _quote = (_tick|_double_quote|_single_quote)
    # _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    # paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    quoted_word = _quote + Word(alphanums + "_") + _quote


    keys = CaselessKeyword("table")
    create_statement = CaselessKeyword("create").setResultsName('action') + keys
    drop_statement = CaselessKeyword("drop").setResultsName('action') + keys
    action = drop_statement | create_statement


    exists = Optional(CaselessKeyword("if exists") | CaselessKeyword("if not exists")).setResultsName('test')
    table_name = Optional(quoted_word.setResultsName('schema_name') + _period) + quoted_word.setResultsName('table_name')


    grammar = action + exists + table_name
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']
        defaults = {
            "raw_statement":value,
            "action":None,
            "test":None,
            "schema_name":None,
            "table_name":None,
            "comment":comment_value,
        }
        new_data = {}
        # @Mstep [LOOP] iterate the data dictionary.
        for k,v in data.items():
            # @Mstep [IF] if the value is a list.
            if isinstance(v,(list)):
                # @Mstep [] assign the first item to the new_data dict.
                new_data[k] = v[0]
                continue
            # @Mstep [ELSE] assign the value directly to the new_data dict.
            new_data[k] = v
        new_data = _obj.set_defaults(defaults,new_data)
        # @Mstep [LOOP] iterate the new_data dictionary.
        for k,v in new_data.items():
            # @Mstep [IF] if the table has a matching attribute
            if hasattr(table,k):
                # @Mstep [] assign the attribute value.
                setattr(table,k,v)


        if table.action == "create":
            cols = _capture_create_table_columns(value)
            table.raw_column_lines = cols
            # new_data['column_data'] = _obj.strip_list_nulls([parse_column_data(x) for x in cols])
            d = _parse_table_column_lines(table)
            new_data = {**new_data,**d}

            new_data["comment"] = comment_value
        # print(new_data)
        output = new_data

    return output


def _capture_create_table_columns(sql)->Iterable[str]:
    '''
        Used by parse_table_statement to capture the column area of the statement.

        ----------

        Arguments
        -------------------------
        `sql` {str}
            The create table statement to parse.

        Return {list}
        ----------------------
        A list of column declarations upon success.
        The list is empty if nothing is found.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 08:48:11
        `memberOf`: parse_sql
        `version`: 1.0
        `method_name`: _capture_create_table_columns
        @xxx [06-01-2022 08:50:01]: documentation for _capture_create_table_columns
    '''

    output = []
    # @Mstep [] capture everything in the parentheses
    scanner = originalTextFor(nestedExpr('(',')'))
    # @Mstep [LOOP] iterate the matched values.
    for match in scanner.searchString(sql):
        # @Mstep [] strip parentheses from the beginning and end of the string.
        val = _csu.strip(match[0],["(",")"])
        # @Mstep [] escape quoted characters in the value.
        val = _sql_utils.escape_quoted_chars(val,True,['__%0A__'])
        # @Mstep [] split the value by new lines.
        output = val.split("\n")
    # @Mstep [RETURN] return the output
    return output




def _parse_table_column_lines(table:TableStatement):
    data = {
        "columns":[],
        "primary_keys":[],
        "indexes":[],
        "unique_keys":[],
        "keys":[],
        "constraints":[],
    }
    # keys = []
    
    for line in table.raw_column_lines:
        if len(line) == 0:
            continue
        line = _csu.strip(line,[" "])
        # print(f"line: {line}")

        if _sql_utils.is_line_key(line):
            # print(f"key found: {line} {parse_key(line)}")
            key = _key_statement.KeyStatement(line)
            key.parse()
            table.add_key(key)
        #     data['keys'] = _lu.append(data['keys'],parse_key(line))

        #     ft = parse_fulltext_key(line)
        #     if ft is not None:
        #         data['indexes'].append(ft)

        #     uk = parse_unique_key(line)
        #     if uk is not None:
        #         # print(f"Unique Key Found: {uk}")
        #         data['indexes'].append(uk)
        #         data['unique_keys'].append(uk)
        #         # data['unique_keys'] = _lu.append(data['unique_keys'],uk['unique_key'])

        #     pk = parse_primary_key(line)
        #     if pk is not None:
        #         data['indexes'].append(pk)
        #         data['primary_keys'] = _lu.append(data['primary_keys'],pk['primary_key'])
        #     # data['primary_keys'] = _lu.append(data['primary_keys'],parse_primary_key(line))

        # if _sql_utils.is_line_constraint(line):
        #     data['constraints'] = _lu.append(data['constraints'],parse_constraint(line))


    #     data['columns'] = _lu.append(data['columns'],parse_column_data(line))

    # for c in data['columns']:
    #     c['is_primary_key'] = False
    #     if c['name'] in data['primary_keys']:
    #         c['is_primary_key'] = True



    return data







