import json as _json
import os as _os


import colemen_utilities.dict_utils as _obj



def write(
    file_path:str,
    contents=None,
    to_json:bool=False,
    size:int=None,
    append:bool=False,
    prepend:bool=False,
    write_mode:str="w",
    ):
    '''
        Writes the contents to a file path.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path to the file...

        [`contents`=None] {any}
            The contents to write to the file.

        [`to_json`=None] {bool}
            If True, the content will be converted to a JSON string.
            This will happen automatically if the content is not a string.

        [`size`=None] {int}
            Write a file of this size in kilobytes

        [`append`=False] {bool}
            If True, the contents will be appended to the file_path.
            If the file does not already exist, it will be created.

        [`prepend`=False] {bool}
            If True, the contents will be prepended to the file_path.
            If the file does not already exist, it will be created.

        [`write_mode`="w"] {str}
            The write mode of the file.



        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-24-2023 05:42:15
        `memberOf`: file_write
        `version`: 1.0
        `method_name`: write
        * @xxx [02-24-2023 05:55:56]: documentation for write
    '''


    if size is not None:
        of_size(file_path, size)
        return

    is_json = to_json
    if is_json is not False or isinstance(contents,(str)) is False:
        write_to_json(file_path, contents)
        return

    if append is True:
        append(file_path, contents)
        return

    if prepend is True:
        prepend(file_path, contents)
        return

    f = open(file_path, write_mode)
    f.write(contents)
    f.close()

def prepend(file_path, contents):
    '''
        appends the contents to the file_path.
        if the content provided is not a string, it is converted to JSON.
    '''
    if isinstance(contents, str) is False:
        contents = _json.dumps(contents, indent=4)

    if _os.path.isfile(file_path) is True:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                o_content= file.read()
                contents = o_content + contents
            except UnicodeDecodeError:
                print(f"read_file - file_path UnicodeDecodeError: {file_path}")

    f = open(file_path, "w")
    f.write(contents)
    f.close()

def append(file_path, contents):
    '''
        appends the contents to the file_path.
        if the content provided is not a string, it is converted to JSON.
    '''
    if isinstance(contents, str) is False:
        contents = _json.dumps(contents, indent=4)

    # @Mstep [if] if the file does not exist
    if _os.path.isfile(file_path) is False:
        # @Mstep [] write the file normally.
        write(file_path,contents)
        return

    f = open(file_path, "a")
    f.write(contents)
    f.close()

def of_size(file_path, kb_size):
    '''
        Write a file that is of a specific size.
        @param {string} file_path - The path to the file to write.
        @param {int} kb_size - The size of the file to write in kilobytes
    '''
    # kb_size = size
    # kb_size = size * (1024 * 1024)
    with open(file_path, "wb") as out:
        out.truncate(kb_size)

def to_json(file_path, content, indent=4):
    '''
        Write or append to a json file.
        @function to_json

        @param {string} file_path - The path to the file to write.
        @param {mixed} content - The content to be written to the json file
        @param {int} [indent=4] - The pretty print indent setting for the JSON output.
    '''

    json_str = _json.dumps(content, indent=indent)
    f = open(file_path, "w")
    f.write(json_str)
    f.close()
write_to_json = to_json