


from dataclasses import dataclass
import os
import re
from typing import Iterable
import colemen_utils as c


# buildutils: auto_generate_init
# This will cause the compiler to gather all sub packages and modules and import them into this
# __init__ file.



@dataclass
class Package:
    dir_path:str = None
    package_name:str = None
    name:str = None
    init_path:str = None

    auto_generate_init:bool = False
    parent_asterisk_import:bool = False
    parent_named_import:bool = True
    no_import:bool = False
    parent_import_privately:bool = False


    _init_content:str = None
    _modules = None
    _packages = None
    _imports = None
    _orig_imports = None
    first_empty_line:int = None
    first_import_line:int = None

    def __init__(self,data) -> None:
        self.dir_path = c.string.file_path(data['file_path'],url=True)
        self.package_name = data['dir_name']
        self.name = data['dir_name']
        self.init_path = f"{self.dir_path}/__init__.py"
        if c.file.exists(self.init_path):
            # print(f"self.init_path:{self.init_path}")
            self._init_content = c.file.readr(self.init_path)

        else:
            c.file.write(self.init_path,"# buildutils: auto_generate_init\n\n\n\n")
        _ = self.options


    def _determine_import_idx(self):
        if self._init_content is not None:
            content = self._init_content.split("\n")
            

    def _capture_imports(self)->list:
        if self._orig_imports is None:
            
            imports = []
            if self._init_content is not None:
                content = self._init_content.split("\n")
                within_docblock = False
                for idx,line in enumerate(content):
                    if line.startswith("'''")or line.startswith('"""'):
                        within_docblock = not within_docblock
                    if len(line) == 0 and self.first_empty_line is None:
                        # be sure that the first empty line is not within the module docblock
                        if within_docblock is False:
                            self.first_empty_line = idx
                        # self.first_import_line = idx
                    if line.startswith("#") is False and "import" in line:
                    # if line.startswith("import") or line.startswith("from"):
                        if self.first_import_line is None:
                            self.first_import_line = idx
                        imports.append(line)
            self._orig_imports = imports
        if self.first_import_line is None:
            self.first_import_line = self.first_empty_line
        return self._orig_imports

    def _capture_build_comments(self)->list:
        # comments = []
        # content = self._init_content.split("\n")
        match = re.findall(r'#\s*build.?utils.?\s*([^\n]*)',self._init_content)
        value = [c.string.to_snake_case(x) for x in match]
        return value

    @property
    def init_data(self):
        '''
            Get this init_compiler's init_data

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 14:04:11
            `@memberOf`: init_compiler
            `@property`: init_data
        '''
        _ = self.options
        _ = self._capture_imports()

    @property
    def options(self):
        '''
            Get this init_compiler's options

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:22:26
            `@memberOf`: init_compiler
            `@property`: options
        '''
        if self._init_content is None:
            return None
        comments = self._capture_build_comments()
        for option in comments:
            # print(f"option: {option}")
            if option == "auto_generate_init":
                self.auto_generate_init = True
            if option == "parent_asterisk_import":
                self.parent_asterisk_import = True
            if option == "parent_named_import":
                self.parent_named_import = True
            if option == "parent_import_privately":
                self.parent_import_privately = True
            if option == "no_import":
                self.no_import = True
                self.parent_asterisk_import = False
                self.parent_named_import = False

        value = {
            "auto_generate_init":self.auto_generate_init,
            "parent_asterisk_import":self.parent_asterisk_import,
            "parent_named_import":self.parent_named_import,
            "no_import":self.no_import,
            "parent_import_privately":self.parent_import_privately,
        }
        return value

    @property
    def modules(self):
        '''
            Get this init_compiler's modules

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:18:40
            `@memberOf`: init_compiler
            `@property`: modules
        '''
        value = self._modules
        if value is None:
            value = c.file.get_files(self.dir_path,recursive=False,ignore=["__init__","- Copy",".pyc","__pycache__"])
            value = [Module(self,x) for x in value]

            self._modules = value
            # dirs = c.dirs.get_folders(f"{os.getcwd()}/apricity/objects",recursive=False)
        return value

    @property
    def packages(self):
        '''
            Get this init_compiler's packages

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 14:30:13
            `@memberOf`: init_compiler
            `@property`: packages
        '''
        value = self._packages
        if value is None:
            value = []
            dirs = c.dirs.get_folders(self.dir_path,recursive=False,exclude=["__pycache__"])
            for pkg in dirs:
                # print(f"instantiating: {pkg['dir_name']} package")
                package = Package(pkg)
                value.append(package)
            self._packages = value
        return value

    @property
    def original_imports(self):
        '''
            Get this init_compiler's original_imports

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:57:41
            `@memberOf`: init_compiler
            `@property`: original_imports
        '''
        value = self._capture_imports()
        return value

    @property
    def imports(self):
        '''
            Get this init_compiler's imports

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:47:37
            `@memberOf`: init_compiler
            `@property`: imports
        '''
        value = self._imports
        if value is None:
            value = []
            for pkg in self.packages:
                print(f"{self.name}=>{pkg.name}.no_import: {pkg.no_import}")
                if pkg.no_import is True:
                    print(f"{pkg.name}.no_import = True")

                    if pkg.asterisk_import in self.original_imports:
                        print(f"    {pkg.name}.{pkg.asterisk_import} Found in init")
                        self._init_content = self._init_content.replace(pkg.asterisk_import,'')
                    ni = pkg.named_import
                    ni = re.sub(r'\s*as[^\n]','',ni)
                    print(f"ni:{ni}")
                    for oi in self.original_imports:
                        if ni in oi:
                    # if pkg.named_import in self.original_imports:
                            print(f"    {pkg.name}.{pkg.named_import} Found in init")
                            self._init_content = self._init_content.replace(pkg.named_import,'')
                    continue
                else:
                    if pkg.asterisk_import not in self.original_imports:
                        if pkg.named_import not in self.original_imports:
                            value.append(pkg.import_statement)

            for mod in self.modules:
                # print(f"{mod.name}.no_import:{mod.no_import}")
                # print(f"{mod.name}.asterisk_import:{mod.asterisk_import}")
                # print(f"{mod.name}.named_import:{mod.named_import}")
                if mod.no_import is True:
                    print(f"{mod.name}.no_import = True")

                    if mod.asterisk_import in self.original_imports:
                        print(f"    {mod.name}.{mod.asterisk_import} Found in init")
                        self._init_content = self._init_content.replace(mod.asterisk_import,'')

                    if mod.named_import in self.original_imports:
                        print(f"    {mod.name}.{mod.named_import} Found in init")
                        self._init_content = self._init_content.replace(mod.named_import,'')
                    continue
                else:
                    skip = False
                    
                    # Remove the alias from the import and check if it is already in the file.
                    ni = mod.named_import
                    ni = re.sub(r'\s*as[^\n]*','',ni)
                    # print(f"ni:{ni}")
                    for oi in self.original_imports:
                        if ni in oi:
                            skip = True

                    if skip is True:
                        # Skip this import because it is alread imported
                        continue
                    
                    if mod.asterisk_import not in self.original_imports:
                        if mod.named_import not in self.original_imports:
                            value.append(mod.import_statement)
            self._imports = value
        return value

    def save(self):
        _=self.init_data
        _=self.imports
        _ = [x.save() for x in self.packages]
        if self.auto_generate_init is True:
            c.con.log(f"Auto generating init for: {self.package_name}")
            # imports = []
            lines = self._init_content.split("\n")
            for imp in self.imports:
                # imports.append(mod.import_statement)
                lines.insert(self.first_import_line,imp)
            # import_string = '\n'.join(imports)
            c.file.write(self.init_path,'\n'.join(lines))




    @property
    def import_path(self):
        '''
            Get this init_compiler's import_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:40:00
            `@memberOf`: init_compiler
            `@property`: import_path
        '''
        value = self.dir_path.replace(f"{c.string.file_path(os.getcwd(),url=True)}","")
        
        value = value.replace("/",".")
        value = c.string.strip(value,["."])
        return value

    @property
    def asterisk_import(self):
        '''
            Get this init_compiler's asterisk_import

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:43:28
            `@memberOf`: init_compiler
            `@property`: asterisk_import
        '''
        value = f"from {self.import_path} import *"
        return value

    @property
    def named_import(self):
        '''
            Get this init_compiler's named_import

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:43:39
            `@memberOf`: init_compiler
            `@property`: named_import
        '''
        value = f"import {self.import_path} as {self.name}"
        if self.parent_import_privately:
            value = f"import {self.import_path} as _{self.name}"

        return value
    

    @property
    def import_statement(self):
        '''
            Get this init_compiler's import_statement

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:41:11
            `@memberOf`: init_compiler
            `@property`: import_statement
        '''
        _=self.options
        # print(f"{self.name}.parent_asterisk_import")
        value = self.named_import
        if self.parent_asterisk_import is True:
            value = self.asterisk_import

        return value







@dataclass
class Module:
    package:Package = None
    file_path:str = None
    dir_path:str = None
    package_name:str = None
    file_name:str = None


    auto_generate_init:bool = False
    parent_asterisk_import:bool = False
    parent_named_import:bool = True
    no_import:bool = False
    parent_import_privately:bool = False

    _init_content:str = None
    _modules = None

    def __init__(self,package,data) -> None:
        self.package = package

        self.file_name = data['file_name']
        self.name = data['name_no_ext']
        self.file_path = c.string.file_path(data['file_path'],url=True)
        self.dir_path = c.string.file_path(data['file_path'],url=True)

        self._init_content = c.file.readr(self.file_path)
        
        _=self.options

    def _capture_build_comments(self)->list:
        # comments = []
        # content = self._init_content.split("\n")
        match = re.findall(r'#\s*build.?utils.?\s*([^\n]*)',self._init_content)
        value = [c.string.to_snake_case(x) for x in match]
        return value

    @property
    def options(self):
        '''
            Get this init_compiler's options

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:22:26
            `@memberOf`: init_compiler
            `@property`: options
        '''
        if self._init_content is None:
            return None
        comments = self._capture_build_comments()
        for option in comments:
            # print(f"option: {option}")
            if option == "auto_generate_init":
                self.auto_generate_init = True
            if option == "parent_asterisk_import":
                self.parent_asterisk_import = True
                self.parent_named_import = False
            if option == "parent_named_import":
                self.parent_named_import = True
            if option == "parent_import_privately":
                self.parent_import_privately = True
            if option == "no_import":
                self.no_import = True
                self.parent_asterisk_import = False
                self.parent_named_import = False

        value = {
            "auto_generate_init":self.auto_generate_init,
            "parent_asterisk_import":self.parent_asterisk_import,
            "parent_named_import":self.parent_named_import,
            "no_import":self.no_import,
            "parent_import_privately":self.parent_import_privately,
        }
        return value

    @property
    def import_path(self):
        '''
            Get this init_compiler's import_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:40:00
            `@memberOf`: init_compiler
            `@property`: import_path
        '''
        value = self.file_path.replace(f"{c.string.file_path(os.getcwd(),url=True)}","")
        value = value.replace(self.file_name,self.name)
        value = value.replace("/",".")
        value = c.string.strip(value,["."])
        return value

    @property
    def asterisk_import(self):
        '''
            Get this init_compiler's asterisk_import

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:43:28
            `@memberOf`: init_compiler
            `@property`: asterisk_import
        '''
        value = f"from {self.import_path} import *"
        return value

    @property
    def named_import(self):
        '''
            Get this init_compiler's named_import

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:43:39
            `@memberOf`: init_compiler
            `@property`: named_import
        '''
        value = f"import {self.import_path} as {self.name}"
        if self.parent_import_privately:
            value = f"import {self.import_path} as _{self.name}"

        return value

    @property
    def import_statement(self):
        '''
            Get this init_compiler's import_statement

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-20-2023 13:41:11
            `@memberOf`: init_compiler
            `@property`: import_statement
        '''
        _=self.options
        # print(f"{self.name}.parent_asterisk_import")
        value = self.named_import
        if self.parent_asterisk_import is True:
            value = self.asterisk_import

        return value


def compile_inits(root_path:str):
    imports = []
    dirs = c.dirs.get_folders(root_path,recursive=False)
    for pkg in dirs:
        package = Package(pkg)
        package.save()
        imports.append(package.import_statement)



if __name__ == '__main__':
    compile_inits()
    # list_py_modules()
    # compile_objects_init()
    # compile_susurrus_init()
    # compile_objects_init()
    # compile_settings_init()