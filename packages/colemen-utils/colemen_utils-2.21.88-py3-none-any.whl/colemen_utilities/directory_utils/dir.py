# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=bare-except
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    Contains the directory class

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 10:44:23
    `memberOf`: directory_utils
'''


from datetime import datetime
import json

import colemen_config as _config
import colemen_utilities.directory_utils.dir_compression as _comp
import colemen_utilities.directory_utils.dir_delete as _del
import colemen_utilities.directory_utils.dir_read as _del
# from colemen_utilities.directory_utils.dir_read import exists as _exists
import colemen_utilities.file_utils as _f
import colemen_utilities.dict_utils as _obj
import colemen_utilities.string_utils as _csu

# logger = _logging.getLogger(__name__)
from dataclasses import dataclass
import os
from typing import Iterable, Union
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
        attrs = os.stat(path,follow_symlinks=False).st_file_attributes
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
class Directory:
    file_path:str = None
    '''The path to this directory'''
    name:str = None
    '''The name of this directory.'''
    dir_path:str = None
    '''The path to the directory that contains this directory.'''
    _drive:str = None
    '''The drive that this directory belongs to.'''
    _modified = None
    _accessed = None
    _created = None
    _size = None
    _archive = None
    _system:bool = None
    _hidden:bool = None
    _readonly:bool = None
    _indexed:bool = None
    _encrypt:bool = None
    _compressed:bool = None
    _attribs:dict = None
    _files:list = None

    def __init__(self,file_path:str) -> None:
        self.file_path = file_path
        self.dir_path = os.path.dirname(file_path)
        self.name = os.path.basename(file_path)
        self._drive = _f.get_drive(self.file_path)


    # ---------------------------------------------------------------------------- #
    #                                TIMESTAMP SHIT                                #
    # ---------------------------------------------------------------------------- #

    @property
    def modified(self):
        '''
            Get this dir's modified

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-22-2023 16:39:24
            `@memberOf`: dir
            `@property`: modified
        '''
        value = self._modified
        if value is None:
            value = os.path.getmtime(self.file_path)
            self._modified = value
        return value

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
        os.utime(self.file_path, (value,value))
        value = os.path.getmtime(self.file_path)
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
            `@memberOf`: dir
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
            `@memberOf`: dir
            `@property`: modified_datetime
        '''
        value = datetime.fromtimestamp(self.modified)
        return value



    @property
    def accessed(self):
        '''
            Get this dir's accessed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-22-2023 16:39:24
            `@memberOf`: dir
            `@property`: accessed
        '''
        value = self._accessed
        if value is None:
            value = os.path.getatime(self.file_path)
            self._accessed = value
        return value

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
        os.utime(self.file_path, (self.accessed,value))
        value = os.path.getmtime(self.file_path)
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
            `@memberOf`: dir
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
            `@memberOf`: dir
            `@property`: accessed_datetime
        '''
        value = datetime.fromtimestamp(self.accessed)
        return value


    @property
    def created(self):
        '''
            Get this dir's created

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-22-2023 16:39:24
            `@memberOf`: dir
            `@property`: created
        '''
        value = self._created
        if value is None:
            value = os.path.getmtime(self.file_path)
            self._created = value
        return value

    @property
    def created_mdy(self):
        '''
            Get this dir's created_timestamp as m-d-y

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:15:12
            `@memberOf`: dir
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
            `@memberOf`: dir
            `@property`: created_datetime
        '''
        value = datetime.fromtimestamp(self.created)
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
            `@memberOf`: dir
            `@property`: attributes
        '''
        value = self._attribs
        if value is None:
            self._gather_attributes()
            value = self._attribs
        return value

    def _gather_attributes(self):
        self._attribs = read_or_write_attribs(self.file_path)
        # print(f"attribs:{attribs}")
        for k,v in self._attribs.items():
            if hasattr(self,f"_{k}"):
                setattr(self,f"_{k}",v)

    @property
    def archive(self):
        '''
            Get this dir's archive

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: dir
            `@property`: archive
        '''
        value = self._archive
        if value is None:
            self.attributes
            value = self._attribs['archive']
        return value

    @property
    def system(self):
        '''
            Get this dir's system

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: dir
            `@property`: system
        '''
        value = self._system
        if value is None:
            self.attributes
            value = self._attribs['system']
        return value

    @property
    def hidden(self):
        '''
            Get this dir's hidden

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: dir
            `@property`: hidden
        '''
        value = self._hidden
        if value is None:
            self.attributes
            value = self._attribs['hidden']
        return value

    @property
    def readonly(self):
        '''
            Get this dir's readonly

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: dir
            `@property`: readonly
        '''
        value = self._readonly
        if value is None:
            self.attributes
            value = self._attribs['readonly']
        return value

    @property
    def indexed(self):
        '''
            Get this dir's indexed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: dir
            `@property`: indexed
        '''
        value = self._indexed
        if value is None:
            self.attributes
            value = self._attribs['indexed']
        return value

    @property
    def encrypt(self):
        '''
            Get this dir's encrypt

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: dir
            `@property`: encrypt
        '''
        value = self._encrypt
        if value is None:
            self.attributes
            value = self._attribs['encrypt']
        return value

    @property
    def compressed(self):
        '''
            Get this dir's compressed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:15:24
            `@memberOf`: dir
            `@property`: compressed
        '''
        value = self._compressed
        if value is None:
            self.attributes
            value = self._attribs['compressed']
        return value





    # ---------------------------------------------------------------------------- #
    #                             ADDITIONAL ATTRIBUTES                            #
    # ---------------------------------------------------------------------------- #

    @property
    def exists(self):
        '''
            Get this dir's exists

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 12:58:27
            `@memberOf`: dir
            `@property`: exists
        '''
        value = os.path.isdir(self.file_path)
        return value

    @property
    def size(self):
        '''
            Get this dir's size in bytes

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 09:02:37
            `@memberOf`: dir
            `@property`: size
        '''
        value = self._size
        # if value is None:
        size = 0
        for path, dirs, files in os.walk(self.file_path):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)

        value = size
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
        # value = _obj.get_arg(self.data,['drive'],None,(str))
        # # @Mstep [IF] if the property is not currenty set
        # if value is None:
        #     value = _f.get_drive(self.file_path)
        #     self.data['drive'] = value
        
        return self._drive


    def create_zip(self,file_name:str = None,delete_after:bool=False,
                overwrite:bool=True):
        '''
            Convert this directory to a zip file.

            ----------

            Arguments
            -------------------------
            `file_name` {str}
                The name of the zip file.
                If not provided, the directory name will be used.

            [`delete_after`=False] {bool}
                Delete the original directory after the zip file is made.

            [`overwrite`=True] {bool}
                If False, it will skip creating the archive.


            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-22-2023 16:44:53
            `memberOf`: dir
            `version`: 1.0
            `method_name`: create_zip
            * @xxx [02-22-2023 16:47:06]: documentation for create_zip
        '''
        if file_name is None:
            file_name = self.name
        dst = f"{self.dir_path}/{self.name}"

        return _comp.create_zip(self.file_path,dst,delete_after=delete_after,overwrite=overwrite)

    def delete(self,shred:bool=False):
        '''
            Delete this directory
            ----------

            Arguments
            -------------------------
            [`shred`=False] {bool}
                If True the contents will be securely shredded and deleted.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-23-2023 12:53:22
            `memberOf`: dir
            `version`: 1.0
            `method_name`: delete
            * @xxx [02-23-2023 12:54:02]: documentation for delete
        '''
        if shred is True:
            for f in _f.get_files(self.file_path,recursive=True):
                _f.delete(f['file_path'],shred=True)
        _del.delete(self.file_path)

    @property
    def content_hash(self):
        '''
            Get this dir's content_hash

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 14:10:35
            `@memberOf`: dir
            `@property`: content_hash
        '''
        data = []
        files = _f.get_files_obj(self.file_path,recursive=True)
        for file in files:
            data.append(file.to_dict)
        value = _csu.to_hash(json.dumps(data))
        return value

    def gen_content_summary(self):
        summary_path = f"{self.file_path}/.dircache"
        contents = []
        most_recent_modification = 0
        for f in _f.get_files_obj(self.file_path,recursive=True,exclude=[".dircache"]):
            fhash = _csu.to_hash(f"{f.size}_{f.modified_time}")
            line = f"{f.file_path} ---hash:{fhash}"
            if f.modified_time > most_recent_modification:
                most_recent_modification = f.modified_time
            contents.append(line)
        omod = self.modified
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(contents))
        # _f.write(summary_path,'\n'.join(contents))
        self.modified = omod
        return most_recent_modification

    @property
    def has_changed(self):
        '''
            Get this dir's has_changed

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 14:57:18
            `@memberOf`: dir
            `@property`: has_changed
        '''
        most_recent_modification = 0
        summary_path = f"{self.file_path}/.dircache"
        if _f.exists(summary_path):
            content = _f.readr(summary_path)
            if content is None:
                most_recent_modification = self.gen_content_summary()
                return (False,most_recent_modification)
            if "---hash:" not in content:
                _f.delete(summary_path)
                most_recent_modification = self.gen_content_summary()
                return (False,most_recent_modification)
            content_lines = content.split("\n")
            for line in content_lines:
                path,fhash = line.split("---hash:")
                if _f.exists(path):
                    f = _f.get_file(path)
                    current_hash = _csu.to_hash(f"{f.size}_{f.modified_time}")
                    if most_recent_modification < f.modified_time:
                        most_recent_modification = f.modified_time
                    if fhash != current_hash:
                        most_recent_modification = self.gen_content_summary()
                        return (True,most_recent_modification)
                else:
                    self.gen_content_summary()
                    return (True,most_recent_modification)
            for f in _f.get_files_obj(self.file_path,exclude=[".dircache"],recursive=True):
                if f.file_path not in content:
                    if most_recent_modification < f.modified_time:
                        most_recent_modification = f.modified_time
                    most_recent_modification = self.gen_content_summary()
                    return (True,most_recent_modification)
        else:
            most_recent_modification = self.gen_content_summary()
        return (False,most_recent_modification)


    @property
    def most_recent_modification(self):
        '''
            Get this dir's most_recent_modification

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 14:16:27
            `@memberOf`: dir
            `@property`: most_recent_modification
        '''
        value = 0
        files = _f.get_files_obj(self.file_path,recursive=True,exclude=[".dircache"])
        for f in files:
            mod = os.path.getmtime(f.file_path)
            if mod > value:
                value = mod
        # value = self.most_recent_modification
        return value


    @property
    def files(self)->Iterable[_config._file_type]:
        '''
            Get this dir's files

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-23-2023 08:34:16
            `@memberOf`: dir
            `@property`: files
        '''
        value = self._files
        if value is None:
            value = self.get_files()
        # value = _f.get_files(self.file_path,recursive=False)
        return self._files




    # @property
    def get_files(
        self,
        recursive:bool=False,
        exclude:Union[str,list]=None,
        include:Union[str,list]=None,
        extensions:Union[str,list]=None,
        )->Iterable[_config._file_type]:
        '''
            Get all files/data from this directory.

            ----------

            Keyword Arguments
            -----------------
                [`search_path`=cwd] {str|list}
                    The search path or list of paths to iterate.

                [`recursive`=False] {boolean}
                    If True the path is iterated recursively

                [`exclude`=[]] {str|list}
                    A term or list or terms to ignore if the file path contains any of them.

                [`extensions|ext|extension`=[]] {str|list}
                    An extension or list of extensions that the file must have.\n
                    Can have leading periods or not.\n
                    if equal to "images" it will automatically search for these extensions:
                        bmp,dds,dib,eps,gif,icns,ico,im,jpg,jpeg,jpeg 2000,msp,pcx,png,ppm,sgi,spider,tga,tiff,webp,xbm

            return
            ----------
            `return` {list}
                A list of file instances.
        '''

        value = _f.get_files_obj(
            self.file_path,
            recursive=recursive,
            exclude=exclude,
            include=include,
            extensions=extensions,
        )
        self._files:Iterable[_config._file_type] = value
        return value

    def has_file(self,file_name)->Union[_config._file_type,bool]:
        '''
            Check if this directory contains a file with a matching name.
            ----------

            Arguments
            -------------------------
            `file_name` {str}
                The name to search for it must match exactly.
                The extension is not required, but obviously can cause issues if there are multiple
                files with the same name and different extensions.

            Return {file,bool}
            ----------------------
            The file object if the file exists, False otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-01-2023 08:39:45
            `memberOf`: dir
            `version`: 1.0
            `method_name`: has_file
            * @xxx [03-01-2023 08:42:31]: documentation for has_file
        '''
        ext = _f.get_ext(file_name)
        for f in self.files:
            if ext is False:
                if f.name_no_ext == file_name:
                    return f
            else:
                if f.name == file_name:
                    return f
        if _f.exists(f"{self.file_path}/{file_name}"):
            return _f.get_file(f"{self.file_path}/{file_name}")
        return False

    # def get_file(self,file_name)->_config._file_type:
    #     '''
    #         Retrieve a file object from this directory
    #         ----------

    #         Arguments
    #         -------------------------
    #         `arg_name` {type}
    #             arg_description

    #         Keyword Arguments
    #         -------------------------
    #         `arg_name` {type}
    #             arg_description

    #         Return {type}
    #         ----------------------
    #         return_description

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 03-01-2023 08:42:39
    #         `memberOf`: dir
    #         `version`: 1.0
    #         `method_name`: get_file
    #         * @TODO []: documentation for get_file
    #     '''
    #     result = None
    #     if self.has_file(file_name) is True:
    #         result = _f.get_file(f"{self.file_path}/{file_name}")
    #     return result




def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

def timestamp_to_pretty(timestamp,format_string:str=None):
    if format_string is None:
        format_string = "%m-%d-%Y %H:%M:%S:%f"
    return datetime.fromtimestamp(timestamp).strftime(format_string)
