# Build Utitilities

## Whats it all about?
I got sick of updating the setup.py file with the modules it should include and creating the __init__.py files.
So that is why build utils was added.


## How do I use it?
In the setup.py file, import colemen_utils then you have a few options of how to proceed.



## Methods:

---

### purge_dist
A really simple method, this will clear out all files in the dist folder.

```python
import colemen_utils as c

c.purge_dist()

# Setting up
setup(
    name="something",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=['stuff'],
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'colemen_utils'
    ],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
```

### list_py_modules
This method will iterate the paths provided to collect all of the modules into a list that can be used by the setup method for building the package.

The paths can point to a single 

```python
import colemen_utils as c

PY_MODULES = c.build_utils.list_py_modules(f"{os.getcwd()}/apricity/objects")

# Setting up
setup(
    name="something",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=['stuff'] + PY_MODULES,
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'colemen_utils'
    ],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
```
