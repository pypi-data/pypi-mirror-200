# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=bare-except
# pylint: disable=line-too-long
'''
    Utility methods for compressing and zipping directories.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 10:34:00
    `memberOf`: directory_utils
'''


from datetime import datetime
import os
import shutil as _shutil
from typing import Union
import colemen_utilities.string_utils as _scu
import colemen_utilities.file_utils as _f
import colemen_utilities.dict_utils as _obj
import colemen_utilities.directory_utils as _dir

# logger = logging.getLogger(__name__)

def create_zip(
    src,
    dst,
    delete_after:bool=False,
    overwrite:bool=True,
    timestamps:bool=True)->Union[str,bool]:
    '''
        Create a zip archive of the directory provided.

        ----------

        Arguments
        -------------------------
        `src` {string}
            The file path to the directory to be archived.

        `dst` {str}
            The file path to the zip file to be created.\
            `WITHOUT AN EXTENSION`

        [`delete_after`=False] {bool}
            If True, the source directy will be deleted after the zip is created.

        [`overwrite`=True] {bool}
            If False, it will skip creating the archive.

        [`timestamps`=True] {bool}
            If False, the zip file's modified & accessed times will be the current time, otherwise it will use the source's modified timestamp.

        Return {bool,string}
        ----------------------
        The zip file path if successful, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03\26\2022 11:15:20
        `memberOf`: dir_compression
        `version`: 1.0
        `method_name`: create_zip
        # @xxx [03\26\2022 11:31:44]: documentation for create_zip
    '''

    # delete_after = _obj.get_kwarg(["delete after"], False, (bool), **kwargs)
    # overwrite = _obj.get_kwarg(["overwrite"], True, (bool), **kwargs)

    if _f.exists(dst):
        if overwrite is False:
            return True

    try:
        result = _shutil.make_archive(dst, 'zip', src)
    except:
        print("Failed to create zip archive.")
        return False
    else:
        result_no_ext = _scu.file_path(result,url=True).replace(_f.get_ext(result),'')
        dst = _scu.file_path(dst,url=True)
        if timestamps:
            modified_unix = os.path.getmtime(src)
            os.utime(result, (modified_unix, modified_unix))
        # access_unix = os.path.getatime(src)
        # os.utime(result, (access_unix))


        if result_no_ext == dst:
            if delete_after:
                _dir.delete(src)
        return result
    return False