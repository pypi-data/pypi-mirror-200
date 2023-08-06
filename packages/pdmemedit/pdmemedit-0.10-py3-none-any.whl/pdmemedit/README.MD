# Edit/read/observe memory with pymem and pandas DataFrames

## pip install pdmemedit

### Tested against Windows 10 / Python 3.10 / Anaconda 

#### Why not use the best libraries for organizing Big Data to organize Big Data?

```python
# Here is an example
# start a separate Python process and get the pid
from time import sleep
import os

tu = (
    6666,
    77777554,
    "b1abvababubux",
    b"b1abvababubux",
    "b1abvababubux".encode("utf-16-le"),
)
print(os.getpid())
while True:
    print(f"{tu=}\t{id(tu)=}")

    for v in tu:
        print(f"{v=}\t{id(v)=}")
        sleep(5)

    # output:
    # tu=(6666, 77777554, 'b1abvababubux', b'b1abvababubux', b'b\x001\x00a\x00b\x00v\x00a\x00b\x00a\x00b\x00u\x00b\x00u\x00x\x00')	id(tu)=1784089644304
    # v=6666	id(v)=1784088602128
    # v=77777554	id(v)=1784088604816
    # v='b1abvababubux'	id(v)=1784089580144
    # v=b'b1abvababubux'	id(v)=1784089556480
    # v=b'b\x001\x00a\x00b\x00v\x00a\x00b\x00a\x00b\x00u\x00b\x00u\x00x\x00'	id(v)=1784089244720

```







```python
import pymem
import numpy as np
from pdmemedit import Pdmemory
# pass either pid or filename, but not both
pdme = Pdmemory(
    pid=21956, filename=None  # pid of the Python process we have just created
)

# memory to DataFrame
pdme.update_region_df(
    limitfunction=lambda x: True,
    dtypes=(
        "S1",
        np.int8,
        np.uint8,
        np.int16,
        np.uint16,
        np.int32,
        np.uint32,
        np.int64,
        np.uint64,
        np.float32,
        np.float64,
    ),
    allowed_protections=(
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_WRITECOPY,
        # pymem.ressources.structure.MEMORY_PROTECTION.PAGE_NOACCESS,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_WRITECOPY,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_GUARD,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_NOCACHE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_WRITECOMBINE,
    ),
)
regiondf = pdme.get_regiondf()
print(regiondf)

```
![](https://github.com/hansalemaos/screenshots/blob/main/memedit/regiondf.png?raw=true)




```python

###################################################################
# Search for a string
# Don't forget to get a memory dump by calling pdme.update_region_df before you search for a string
pdme.search_string("b1abvababubux")
stringresultsdf = pdme.get_searchstringdf()
print(stringresultsdf)
```
![](https://github.com/hansalemaos/screenshots/blob/main/memedit/stringresultsdf.png?raw=true)




```python
###################################################################
# Search for a number
# Don't forget to get a memory dump by calling pdme.update_region_df before you search for a number
pdme.search_number(
    numexprquery=f"(a == 77777554)",  # numexpr.evaluate string, name of 'a' can't be changed
    dtypes=(
        np.int8,
        np.uint8,
        np.int16,
        np.uint16,
        np.int32,
        np.uint32,
        np.int64,
        np.uint64,
        # np.float32,
        # np.float64,
    ),
)
numberresults = pdme.get_searchnumberdf()
print(numberresults)

```
![](https://github.com/hansalemaos/screenshots/blob/main/memedit/numberresults.png?raw=true)



```python

###################################################################
# Call pdme.search_number first, edit the DataFrame (self.numbersearchdf) until it serves your needs
# and call pdme.observe_numbers to see how the value changes
pdme.observe_numbers(  # ctrl+c to break
    keepcondition="(new >= old)",  # numexpr.evaluate string, names of 'new/old' can't be changed
    sleep_between_scans=1,
    savefolder=None,
    printoutputlimit=100,
)
observedvalues = pdme.get_observerdf()
print(observedvalues)


```
![](https://github.com/hansalemaos/screenshots/blob/main/memedit/observedvalues.png?raw=true)




```python

###################################################################
# How to edit the memory
numberresults.ff_write.apply(lambda x: x(99999999)) # Overwrites results with 99999999
stringresultsdf.ff_write_str.apply(
    lambda x: x("B")
)  # binary/utf-8/utf-16-le... conversation should work automatically - overwrites each single letter

# Output after calling numberresults.ff_write/stringresultsdf.ff_write_str
# tu=(6666, 99999999, 'BBBBBBBBBBBBB', b'BBBBBBBBBBBBB', b'B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00')	id(tu)=1784089644304
# v=6666	id(v)=1784088602128
# v=99999999	id(v)=1784088604816
# v='BBBBBBBBBBBBB'	id(v)=1784089580144
# v=b'BBBBBBBBBBBBB'	id(v)=1784089556480
# v=b'B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00B\x00'	id(v)=1784089244720


```


```python


###################################################################

# Use this with care, and limit the area of interest as much as possible, this method might use a lot of memory and get really slow, since
# it dumps the memory of the whole process and compares every single byte with the last memory dump.
# You can stop recording by pressing Ctrl+C
pdme.record_all_changing_values(  # might get very slow and use a lot of memory
    limitfunc=lambda x: True,
    dtype=np.uint32,
    allowed_protections=(
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
    ),
)
pdme.get_differencesdf()

```