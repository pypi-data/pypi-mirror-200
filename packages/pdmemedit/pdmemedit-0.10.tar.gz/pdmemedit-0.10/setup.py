from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Edit/read/observe memory with pymem and pandas"

# Setting up
setup(
    name="pdmemedit",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/pdmemedit',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_dillpickle', 'a_pandas_ex_fastloc', 'a_pandas_ex_numexpr', 'get_consecutive_filename', 'numexpr', 'numpy', 'pandas', 'PrettyColorPrinter', 'psutil', 'Pymem', 'regex', 'tolerant_isinstance', 'useful_functions_easier_life'],
    keywords=['pymem', 'pandas', 'assembly', 'hacking', 'low-level', 'cheat engine'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_dillpickle', 'a_pandas_ex_fastloc', 'a_pandas_ex_numexpr', 'get_consecutive_filename', 'numexpr', 'numpy', 'pandas', 'PrettyColorPrinter', 'psutil', 'Pymem', 'regex', 'tolerant_isinstance', 'useful_functions_easier_life'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*