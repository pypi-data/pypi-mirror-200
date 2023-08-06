# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
# '''
#     Contains the general methods for manipulating files.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 06-03-2022 10:22:15
#     `memberOf`: rand
#     `version`: 1.0
#     `method_name`: rand
# '''




from dataclasses import dataclass
import json
# import shutil
import time
# import json
# import re
# from pathlib import Path
import time as _time
import json as _json
from datetime import timezone as _timezone
from datetime import datetime
import gzip as _gzip
# import zipfile
import os as _os
import io as _io
import shutil as _shutil
import traceback as _traceback
from threading import Thread as _Thread
import logging as _logging
from pathlib import Path, PureWindowsPath,PurePath

# from isort import file

import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _f
import colemen_utilities.directory_utils as _directory
import colemen_config as _config
from os import scandir, stat
from stat import (
    FILE_ATTRIBUTE_ARCHIVE as A,
    FILE_ATTRIBUTE_SYSTEM as S,
    FILE_ATTRIBUTE_HIDDEN as H,
    FILE_ATTRIBUTE_READONLY as R,
    FILE_ATTRIBUTE_NOT_CONTENT_INDEXED as I,
    FILE_ATTRIBUTE_ENCRYPTED as E,
    FILE_ATTRIBUTE_COMPRESSED as C,
)
from ctypes import WinError, get_last_error


# byte_order = ["archive","system","hidden","readonly","indexed","encrypted","compressed"]

def read_or_write_attribs(
    # https://docs.python.org/3/library/ctypes.html#ctypes.WinDLL
    # kernel32,

    # https://docs.python.org/3/library/os.html#os.DirEntry
    path,

    # archive, system, hidden, readonly, indexed
    a=None, s=None, h=None, r=None, i=None,e=None,c=None,

    # Set to True when you call this function more than once on the same entry.
    update=False
):

    # Get the file attributes as an integer.
    if not update:
        # Fast because we access the stats from the entry
        attrs = _os.stat(path,follow_symlinks=False).st_file_attributes
    else:
        # A bit slower because we re-read the stats from the file path.
        # Notice that this will raise a "WinError: Access denied" on some entries,
        # for example C:\System Volume Information\
        attrs = stat(path, follow_symlinks=False).st_file_attributes

    # Construct the new attributes
    newattrs = attrs
    def setattrib(attr, value):
        nonlocal newattrs
        # Use '{0:032b}'.format(number) to understand what this does.
        if value is True: newattrs = newattrs | attr
        elif value is False: newattrs = newattrs & ~attr
    setattrib(A, a)
    setattrib(S, s)
    setattrib(H, h)
    setattrib(R, r)
    
    # Because this attribute is True when the file is _not_ indexed
    setattrib(I, i if i is None else not i)
    
    setattrib(E, e)
    setattrib(C, c)


    # Optional add more attributes here.
    # See https://docs.python.org/3/library/stat.html#stat.FILE_ATTRIBUTE_ARCHIVE

    # Write the new attributes if they changed
    if newattrs != attrs:
        if not _config.kernel32.SetFileAttributesW(path, newattrs):
            raise WinError(get_last_error())


    data = {
        "archive":bool(newattrs & A),
        "system":bool(newattrs & S),
        "hidden":bool(newattrs & H),
        "readonly":bool(newattrs & R),
        "indexed":bool(newattrs & I),
        "encrypt":bool(newattrs & E),
        "compressed":bool(newattrs & C),

    }
    return data
    # Return an info tuple consisting of bools
    return (
        bool(newattrs & A),
        bool(newattrs & S),
        bool(newattrs & H),
        bool(newattrs & R),
        # Because this attribute is true when the file is _not_ indexed
        not bool(newattrs & I),
        
        bool(newattrs & E),
        bool(newattrs & C),

    )





@dataclass
class File():
    _file_path:str = None
    _name:str = None
    _drive:str = None
    _extension:str = None
    _name_no_ext:str = None
    _dir_path:str = None
    _access_time:int = None
    _modified_time:int = None
    _create:int = None
    _size:int = None
    _is_json:bool = False
    _content:str = None
    
    _archive = None
    _system:bool = None
    _hidden:bool = None
    _readonly:bool = None
    _indexed:bool = None
    _encrypt:bool = None
    _compressed:bool = None
    _attribs:dict = None
    
    _pure_path:PurePath = None
    
    def __init__(self,file_path,args:dict=None):
        self.args = {} if args is None else args
        # self.data = {
        #     "file_path":file_path,
        #     "file_name":None,
        #     "extension":None,
        #     "name_no_ext":None,
        #     "dir_path":None,
        #     "access_time":None,
        #     "modified_time":None,
        #     "create":None,
        #     "size":None,
        #     "is_json":None,
        # }
        self.settings = {}
        if isinstance(args,(dict)):
            _obj.set_attr_from_dict(self,args,set_privates=True)
        self._file_path = file_path
        self._pure_path = PurePath(Path(self._file_path))
        self._file_path = self._pure_path.as_posix()
        # self.data = _obj.set_defaults(self.data,self.args)

    @property
    def to_dict(self):
        '''
            Get this File's data as a dictionary.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:48:25
            `@memberOf`: File
            `@property`: to_dict
        '''
        data = {
            "file_path":self.file_path,
            "name":self.name,
            "extension":self.extension,
            "name_no_ext":self.name_no_ext,
            "dir_path":self.dir_path,
            "access_time":self.accessed,
            "modified_time":self.modified,
            "create":self.created,
            "drive":self.drive,
            "size":self.size,
        }
        return data

    @property
    def file_path(self):
        '''
            Get this File's file_path
            
            The path will use / separators for compatibility.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:37:48
            `@memberOf`: File
            `@property`: file_path
        '''
        return self._file_path
    path = file_path

    @property
    def name(self):
        '''
            Get this File's name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:37:33
            `@memberOf`: File
            `@property`: name
        '''
        value = self._name
        if value is None:
            value = self._pure_path.name
            self._name = value
        return value
    file_name = name


    @property
    def extension(self):
        '''
            Get this File's extension
            This includes the leading period

            `default`:None

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:41:26
            `@memberOf`: File
            `@property`: extension
        '''
        value = self._extension
        if value is None:
            value = self._pure_path.suffix
            self._extension = value
        return value
    ext = extension

    @extension.setter
    def extension(self,value):
        '''
            Set the File's extension property

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:40:40
            `@memberOf`: File
            `@property`: extension
        '''
        oe = _csu.format_extension(self.extension)
        value = _csu.format_extension(value)
        
        if value != oe:
            self._extension = f".{value}"
            new_path = f"{self.dir_path}/{self.name_no_ext}{self._extension}"
            if _f.rename(self.file_path,new_path):
                self._file_path = new_path
                self._pure_path = PurePath(Path(new_path))
        # value = _csu.format_extension(value)
        # self.data['extension'] = f".{value}"

    @property
    def name_no_ext(self):
        '''
            Get this File's name_no_ext

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-24-2023 09:28:27
            `@memberOf`: File
            `@property`: name_no_ext
        '''
        value = self._name_no_ext
        if value is None:
            value = _f.get_name_no_ext(self.file_path)
            self._name_no_ext = value
        return value

    @property
    def dir_path(self):
        '''
            Get this File's dir_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-24-2023 09:28:57
            `@memberOf`: File
            `@property`: dir_path
        '''
        value = self._dir_path
        if value is None:
            # raise TypeError(self.file_path)
            value = _os.path.dirname(self.file_path)
            self._dir_path = value
        return value

    @property
    def drive(self):
        '''
            Get this File's drive

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-25-2022 14:47:02
            `@memberOf`: File
            `@property`: drive
        '''
        value = self._drive
        if value is None:
            value = self._pure_path.drive
            self._drive = value
        return value




    # ---------------------------------------------------------------------------- #
    #                                TIMESTAMP SHIT                                #
    # ---------------------------------------------------------------------------- #



    @property
    def accessed(self):
        '''
            Get this File's accessed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-24-2023 09:29:30
            `@memberOf`: File
            `@property`: accessed
        '''
        value = self._access_time
        if value is None:
            value = _f.get_access_time(self.file_path,rounded=False)
            self._access_time = value
        return value
    access_time = accessed

    @accessed.setter
    def accessed(self,value:float):
        '''
            Set the accessed time for this directory.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:10:50
            `@memberOf`: PostArg
            `@property`: access
        '''
        value = datetime_to_timestamp(value)
        _os.utime(self.file_path, (value,self.modified))
        value = _os.path.getatime(self.file_path)
        self._accessed = value

    @property
    def accessed_mdy(self):
        '''
            Get this dir's accessed_timestamp as m-d-y

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:15:12
            `@memberOf`: file
            `@property`: accessed_pretty
        '''

        value = timestamp_to_pretty(self.accessed,'%m-%d-%Y')
        return value

    @property
    def accessed_datetime(self):
        '''
            Get this dir's accessed timestamp as a datetime object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:16:36
            `@memberOf`: file
            `@property`: accessed_datetime
        '''
        value = datetime.fromtimestamp(self.accessed)
        return value

    @property
    def created(self):
        '''
            Get this File's created

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-24-2023 09:29:30
            `@memberOf`: File
            `@property`: created
        '''
        value = self._create
        if value is None:
            value = _f.get_create_time(self.file_path,rounded=False)
            self._create = value
        return value
    create_time = created

    @property
    def created_mdy(self):
        '''
            Get this dir's createstamp as m-d-y

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:15:12
            `@memberOf`: file
            `@property`: created_pretty
        '''

        value = timestamp_to_pretty(self.created,'%m-%d-%Y')
        return value

    @property
    def created_datetime(self):
        '''
            Get this dir's created timestamp as a datetime object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:16:36
            `@memberOf`: file
            `@property`: created_datetime
        '''
        value = datetime.fromtimestamp(self.created)
        return value

    @property
    def modified(self):
        '''
            Get this File's modified

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@modified`: 02-24-2023 09:29:30
            `@memberOf`: File
            `@property`: modified
        '''
        value = self._modified_time
        if value is None:
            value = _f.get_modified_time(self.file_path,rounded=False)
            self._modified_time = value
        return value
    modified_time = modified

    @modified.setter
    def modified(self,value:float):
        '''
            Set the modified time for this directory.

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:10:50
            `@memberOf`: PostArg
            `@property`: access
        '''
        # print(f"setting modified time: {value}")
        value = datetime_to_timestamp(value)
        _os.utime(self.file_path, (value,value))
        value = _os.path.getmtime(self.file_path)
        self._modified = value

    @property
    def modified_mdy(self):
        '''
            Get this dir's modified_timestamp as m-d-y

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:15:12
            `@memberOf`: file
            `@property`: modified_pretty
        '''

        value = timestamp_to_pretty(self.modified,'%m-%d-%Y')
        return value

    @property
    def modified_datetime(self):
        '''
            Get this dir's modified timestamp as a datetime object.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:16:36
            `@memberOf`: file
            `@property`: modified_datetime
        '''
        value = datetime.fromtimestamp(self.modified)
        return value





    # ---------------------------------------------------------------------------- #
    #                            WINDOWS FILE ATTRIBUTES                           #
    # ---------------------------------------------------------------------------- #

    @property
    def attributes(self):
        '''
            Get this dir's attributes

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:43:15
            `@memberOf`: file
            `@property`: attributes
        '''
        value = self._attribs
        if value is None:
            self._gather_attributes()
            # self._attribs = value
            value = self._attribs
        return value

    def _gather_attributes(self):
        # attribs = read_or_write_attribs(self.file_path)
        self._attribs = read_or_write_attribs(self.file_path)
        # print(f"attribs:{attribs}")
        # _obj.set_attr_from_dict(self,attribs,set_privates=True)
        for k,v in self._attribs.items():
            if hasattr(self,f"_{k}"):
                setattr(self,f"_{k}",v)


    def _set_attributes(self):
        try:
            self._attribs = read_or_write_attribs(
                self.file_path,
                a=self._attribs['archive'],
                s=self._attribs['system'],
                h=self._attribs['hidden'],
                r=self._attribs['readonly'],
                i=not self._attribs['indexed'],
                e=self._attribs['encrypt'],
                c=self._attribs['compressed'],
                update=True
            )
        except PermissionError as e:
            print(e)
        # self._attribs = None
        # print(f"attribs:{attribs}")
        # for k,v in self._attribs.items():
        #     if hasattr(self,f"_{k}"):
        #         setattr(self,f"_{k}",v)

    @property
    def archive(self):
        '''
            Get this file's archive attribute.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: file
            `@property`: archive
        '''
        value = self._archive
        if value is None:
            if self._attribs is None:
                self.attributes
            value = self._attribs['archive']
            self._archive = value
        return value

    # @archive.setter
    # def archive(self,value):
    #     '''
    #         Set the File's archive property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 02-24-2023 10:47:25
    #         `@memberOf`: File
    #         `@property`: archive
    #     '''
    #     self._archive = value
    #     # if self._attribs is None:
    #         # self.attributes
    #     self._attribs['archive'] = value
    #     self._set_attributes()
    #     self._attribs = None

    @property
    def system(self):
        '''
            Get this dir's system

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: file
            `@property`: system
        '''
        value = self._system
        if value is None:
            if self._attribs is None:
                self.attributes
            value = self._attribs['system']
            self._system = value
        return value

    # @system.setter
    # def system(self,value):
    #     '''
    #         Set the File's system property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 02-24-2023 10:47:25
    #         `@memberOf`: File
    #         `@property`: system
    #     '''
    #     self._system = value
    #     # if self._attribs is None:
    #     #     # self._attribs = {}
    #     #     self.attributes
    #     self._attribs['system'] = value
    #     self._set_attributes()
    #     self._attribs = None


    @property
    def hidden(self):
        '''
            Get this dir's hidden

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: file
            `@property`: hidden
        '''
        value = self._hidden
        if value is None:
            if self._attribs is None:
                self.attributes
            value = self._attribs['hidden']
            self._hidden = value
        return value

    # @hidden.setter
    # def hidden(self,value):
    #     '''
    #         Set the File's hidden property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 02-24-2023 10:47:25
    #         `@memberOf`: File
    #         `@property`: hidden
    #     '''
    #     if self._attribs is None:
    #         self.attributes
    #     self._attribs['hidden'] = value
    #     self._set_attributes()
    #     self._hidden = None
    #     self._attribs = None


    @property
    def readonly(self):
        '''
            Get this dir's readonly

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: file
            `@property`: readonly
        '''
        value = self._readonly
        if value is None:
            if self._attribs is None:
                self.attributes
            value = self._attribs['readonly']
            self._readonly = value
        return value

    # @readonly.setter
    # def readonly(self,value):
    #     '''
    #         Set the File's readonly property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 02-24-2023 10:47:25
    #         `@memberOf`: File
    #         `@property`: readonly
    #     '''
    #     self._readonly = value
    #     if self._attribs is None:
    #         self.attributes
    #     self._attribs['readonly'] = value
    #     self._set_attributes()
    #     self._attribs = None

    @property
    def indexed(self):
        '''
            Get this dir's indexed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: file
            `@property`: indexed
        '''
        value = self._indexed
        if value is None:
            if self._attribs is None:
                self.attributes
            value = self._attribs['indexed']
            self._indexed = value
        return value

    # @indexed.setter
    # def indexed(self,value):
    #     '''
    #         Set the File's indexed property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 02-24-2023 10:47:25
    #         `@memberOf`: File
    #         `@property`: indexed
    #     '''
    #     if self._attribs is None:
    #         self.attributes
    #     self._attribs['indexed'] = value
    #     self._set_attributes()
    #     self._attribs = None
    #     self._indexed = None

    @property
    def encrypt(self):
        '''
            Get this dir's encrypt

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: file
            `@property`: encrypt
        '''
        value = self._encrypt
        if value is None:
            if self._attribs is None:
                self.attributes
            value = self._attribs['encrypt']
            self._encrypt = value
        return value

    # @encrypt.setter
    # def encrypt(self,value):
    #     '''
    #         Set the File's encrypt property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 02-24-2023 10:47:25
    #         `@memberOf`: File
    #         `@property`: encrypt
    #     '''
    #     if self._attribs is None:
    #         self.attributes
    #     self._attribs['encrypt'] = value
    #     self._set_attributes()
    #     self._attribs = None
    #     self._encrypt = None


    @property
    def compressed(self):
        '''
            Get this dir's compressed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: file
            `@property`: compressed
        '''
        value = self._compressed
        if value is None:
            if self._attribs is None:
                self.attributes
            value = self._attribs['compressed']
            self._compressed = value
        return value

    # @compressed.setter
    # def compressed(self,value):
    #     '''
    #         Set the File's compressed property

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 02-24-2023 10:47:25
    #         `@memberOf`: File
    #         `@property`: compressed
    #     '''
    #     # self._compressed = value
    #     if self._attribs is None:
    #         self.attributes
    #     self._attribs['compressed'] = value
    #     self._set_attributes()
    #     self._compressed = None
    #     self._attribs = None





    # ---------------------------------------------------------------------------- #
    #                             ADDITIONAL ATTRIBUTES                            #
    # ---------------------------------------------------------------------------- #




    @property
    def size(self):
        '''
            Get this File's size in bytes

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-24-2023 09:32:51
            `@memberOf`: File
            `@property`: size
        '''
        value = self._size
        if value is None:
            value = _os.path.getsize(self.file_path)
            self._size = value
        return value

    @property
    def exists(self):
        '''
            Confirm that the actual file exists.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-24-2023 09:33:26
            `@memberOf`: File
            `@property`: exists
        '''
        return _os.path.isfile(self.file_path)

    @property
    def _is_json(self):
        '''
            Get this File's _is_json

            If the is_json argument was not provided, this will check the file extension.

            If the extension is not json or jsonc, it will return False.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:37:53
            `@memberOf`: File
            `@property`: _is_json
        '''
        value = self._is_json
        # @Mstep [IF] if the property is not currenty set
        if value is None:
            value = False
            if self.extension in ['.json','.jsonc']:
                value = True
            if self.content is not None:
                result = _f.as_json(self.content)
                if result is not False:
                    value = True
                    self.content = result
            self._is_json = value
        return value



    @property
    def content(self):
        '''
            Get this File's content

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-24-2023 09:52:25
            `@memberOf`: File
            `@property`: content
        '''
        value = self._content
        if value is None:
            if self.exists is True:
                value = _f.readr(self.path)
                self._content = value
        return value

    def content_to_string(self,value):
        value = self.content
        if isinstance(value,(str)) is True:
            return value
        if isinstance(value,(dict,list)):
            # TODO []: add error catching.
            value = json.encode(value)
            return value

    @content.setter
    def content(self,value='',save=True):
        '''
            Set the File's content

            `default`:''


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-15-2022 09:33:56
            `@memberOf`: File
            `@property`: contents
        '''
        self._content = value
        if save == True:
            _f.write(self.path,self._content)

    def save(self):
        _f.write(self.path,self.content)

    def delete(self,shred:bool=False)->bool:
        return _f.delete(self.file_path,shred=shred)

    def append(self,new_contents):
        _f.append(self.path,new_contents)
        # @Mstep [IF] if the contents have already been read.
        if self._content is not None:
            # @Mstep [] set the contents to None
            self._content = None
            # @Mstep [] read the file again.
            _ = self.content

def file_from_path(file_path,**kwargs):
    
    args = {
        "is_json":_obj.get_kwarg(['is_json','json'],None,(bool),**kwargs),
    }
    return File(file_path,args)





def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

def timestamp_to_pretty(timestamp,format_string:str=None):
    if format_string is None:
        format_string = "%m-%d-%Y %H:%M:%S:%f"
    return datetime.fromtimestamp(timestamp).strftime(format_string)

def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple()) + dt.microsecond/1e6