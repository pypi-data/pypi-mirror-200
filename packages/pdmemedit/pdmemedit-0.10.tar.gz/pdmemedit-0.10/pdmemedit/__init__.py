import binascii
import inspect
import os
import sys
import time
from copy import deepcopy
import functools
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()

from get_consecutive_filename import get_free_filename
from useful_functions_easier_life import ignore_exceptions_decorator
import psutil
import pymem
import pandas as pd
import numpy as np

from collections import defaultdict
from tolerant_isinstance import isinstance_tolerant
from regex import regex

from a_pandas_ex_numexpr import pd_add_numexpr

pd_add_numexpr()
import numexpr
from PrettyColorPrinter import add_printer

add_printer(True)

from a_pandas_ex_fastloc import (
    pd_add_fastloc,
)

pd_add_fastloc()
nested_dict = lambda: defaultdict(nested_dict)
from a_pandas_ex_dillpickle import pd_add_dillpickle

pd_add_dillpickle()

from typing import Any, Tuple, Optional

try:
    from collections import Iterable
except Exception as fe:
    pass
from functools import reduce
import math


bytedivmult = {
    "aa_dump_numpy_int8": 8,
    "aa_dump_numpy_uint8": 8,
    "aa_dump_numpy_int16": 4,
    "aa_dump_numpy_uint16": 4,
    "aa_dump_numpy_int32": 2,
    "aa_dump_numpy_uint32": 2,
    "aa_dump_numpy_int64": 1,
    "aa_dump_numpy_uint64": 1,
    "aa_dump_numpy_float32": 2,
    "aa_dump_numpy_float64": 1,
}


numpydtypes = {
    np.int8: "aa_dump_numpy_int8",
    np.uint8: "aa_dump_numpy_uint8",
    np.int16: "aa_dump_numpy_int16",
    np.uint16: "aa_dump_numpy_uint16",
    np.int32: "aa_dump_numpy_int32",
    np.uint32: "aa_dump_numpy_uint32",
    np.int64: "aa_dump_numpy_int64",
    np.uint64: "aa_dump_numpy_uint64",
    np.float32: "aa_dump_numpy_float32",
    np.float64: "aa_dump_numpy_float64",
    np.string_: "aa_dump_numpy_uint8",
}


def checkiter(x):
    try:
        _ = isinstance(x, Iterable)
        if _:
            return True
    except Exception:
        pass
    try:
        _ = iter(x)
        return True
    except TypeError:
        return False


def float_check_nan(num):
    if float("-inf") < float(num) < float("inf"):
        return False
    else:
        return True


def is_nan(
    x: Any,
    emptyiters: bool = False,
    nastrings: bool = False,
    emptystrings: bool = False,
    emptybytes: bool = False,
) -> bool:
    """
    Check if a value is NaN (not a number).

    Parameters:
        x (Any): The value to check.
        emptyiters (bool): If True, empty iterables are considered NaN (default False).
        nastrings (bool): If True, a list of string representations of NaN values are considered NaN (default False).
        emptystrings (bool): If True, empty strings are considered NaN (default False).
        emptybytes (bool): If True, empty bytes objects are considered NaN (default False).

    Returns:
        bool: True if the value is NaN, False otherwise.
    """
    # useful when you read a csv file and the missing data is not converted correctly to nan
    nastringlist = [
        "<NA>",
        "<NAN>",
        "<nan>",
        "np.nan",
        "NoneType",
        "None",
        "-1.#IND",
        "1.#QNAN",
        "1.#IND",
        "-1.#QNAN",
        "#N/A N/A",
        "#N/A",
        "N/A",
        "n/a",
        "NA",
        "#NA",
        "NULL",
        "null",
        "NaN",
        "-NaN",
        "nan",
        "-nan",
    ]
    if isinstance(x, type(None)):
        return True
    try:
        if np.isnan(x):
            return True
    except Exception:
        pass
    try:
        if pd.isna(x):
            return True
    except Exception:
        pass
    try:
        if pd.isnull(x):
            return True
    except Exception:
        pass
    try:
        if math.isnan(x):
            return True
    except Exception:
        pass
    try:
        if x != x:
            return True
    except Exception:
        pass
    try:
        if not isinstance(x, str):
            if float_check_nan(x) is True:
                return True
    except Exception:
        pass
    if emptystrings is True:
        if isinstance(x, str):
            try:
                if x == "":
                    return True
            except Exception:
                pass
    if emptybytes is True:
        if isinstance(x, bytes):
            try:
                if x == b"":
                    return True
            except Exception:
                pass
    if nastrings is True:
        if isinstance(x, str):
            try:
                if x in nastringlist:
                    return True
            except Exception:
                pass
    if emptyiters is True:
        if isinstance(x, (str, bytes)):
            pass
        else:
            if checkiter(x):
                try:
                    if not np.any(x):
                        return True
                except Exception:
                    pass
                if isinstance(x, (pd.Series, pd.DataFrame)):
                    try:
                        if x.empty:
                            return True
                    except Exception:
                        pass
                try:
                    if not any(x):
                        return True
                except Exception:
                    pass

                try:
                    if not x:
                        return True
                except Exception:
                    pass
                try:
                    if len(x) == 0:
                        return True
                except Exception:
                    pass
    return False


def groupBy(key, seq):
    # https://stackoverflow.com/a/60282640/15096247
    return reduce(
        lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list)
    )


def hex2bin(pattern):
    r"""
    a5=hex2bin(pattern='\\x00')
    b'\x00'
    """
    pattern = pattern.lower()
    pattern = pattern.replace("\\x", "")
    pattern = pattern.replace('"', "")
    pattern = pattern.replace("'", "")
    return b"".join(
        [binascii.a2b_hex(i + j) for i, j in zip(pattern[0::2], pattern[1::2])]
    )


def string_to_utf16_byte(word):
    r"""
    word, wordlist = string_to_utf16_byte(word='hahc&oiü')

    word
    b'hahc&oi\xfc'
    wordlist
    [b'h', b'a', b'h', b'c', b'&', b'o', b'i', b'\xfc']


    """
    wordlist_b = [hex2bin(hex(x)[2:]) for x in word.encode("utf-16-le")]
    word = b"".join(wordlist_b)
    wordlist = [xd for xd in wordlist_b if xd != b""]
    return word, wordlist


def scan_pattern_page(
    handle,
    address,
    bufferdty=None,
    regbytes=True,
    allowed_protections=(
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
    ),
):
    mbi = pymem.memory.virtual_query(handle, address)
    next_region = mbi.BaseAddress + mbi.RegionSize

    if (
        mbi.state != pymem.ressources.structure.MEMORY_STATE.MEM_COMMIT
        or mbi.protect not in allowed_protections
    ):
        return next_region, None
    if not regbytes:
        return next_region, None
    page_bytes = pymem.memory.read_bytes(handle, address, mbi.RegionSize)
    if not isinstance_tolerant(bufferdty, None):
        va = np.frombuffer(page_bytes, dtype=bufferdty)
    else:
        va = page_bytes

    return next_region, va


def attach_to_process(pid=None, filename=None):
    """
    Attach to a running process using its PID or executable filename and set up configurations
    for reading and writing memory in different data types.

    Args:
        pid (int, None): PID of the process to attach to.
        filename (str, None): Name of the executable file of the process to attach to.

    Raises:
        ValueError: If both pid and filename are None.

    Returns:
        None
    """
    if is_nan(pid) and is_nan(filename):
        raise ValueError("pid and filename can't be both None!")
    if not is_nan(filename):
        npid = 0
        for p in psutil.process_iter():
            if p.name().lower() == filename.lower():
                npid = p.pid
                break
    else:
        npid = int(pid)
    pm = pymem.Pymem(npid)
    bytediv = {
        "aa_dump_numpy_int8": 1,
        "aa_dump_numpy_uint8": 1,
        "aa_dump_numpy_int16": 2,
        "aa_dump_numpy_uint16": 2,
        "aa_dump_numpy_int32": 4,
        "aa_dump_numpy_uint32": 4,
        "aa_dump_numpy_int64": 8,
        "aa_dump_numpy_uint64": 8,
        "aa_dump_numpy_float32": 4,
        "aa_dump_numpy_float64": 8,
    }

    byteread = {
        "aa_dump_numpy_int8": lambda addi: functools.partial(
            np.frombuffer, pm.read_bytes(int(addi), 1), dtype=np.int8
        )[0],
        "aa_dump_numpy_uint8": pm.read_uchar,
        "aa_dump_numpy_int16": pm.read_short,
        "aa_dump_numpy_uint16": pm.read_ushort,
        "aa_dump_numpy_int32": pm.read_int,
        "aa_dump_numpy_uint32": pm.read_uint,
        "aa_dump_numpy_int64": pm.read_longlong,
        "aa_dump_numpy_uint64": pm.read_ulonglong,
        "aa_dump_numpy_float32": pm.read_float,
        "aa_dump_numpy_float64": pm.read_double,
    }

    bytewrite = {
        "aa_dump_numpy_int8": pm.write_short,  # maybe not working!!
        "aa_dump_numpy_uint8": pm.write_uchar,
        "aa_dump_numpy_int16": pm.write_short,
        "aa_dump_numpy_uint16": pm.write_ushort,
        "aa_dump_numpy_int32": pm.write_int,
        "aa_dump_numpy_uint32": pm.write_uint,
        "aa_dump_numpy_int64": pm.write_longlong,
        "aa_dump_numpy_uint64": pm.write_ulonglong,
        "aa_dump_numpy_float32": pm.write_float,
        "aa_dump_numpy_float64": pm.write_double,
    }
    return pm, bytediv, byteread, bytewrite


def get_dfs_from_regions(
    configs,
    limitfunc=lambda x: True,
    bufferdtype=(
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
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
    ),
):
    """
    Retrieve information about memory regions and modules in the current process.

    Parameters:
    -----------
    limitfunc : callable, optional
        A function that takes a memory region base address as input and returns
        a byte string representing the pattern to search for in that region.
        The default is a lambda function that always returns True.
    bufferdtype : tuple or list, optional
        A sequence of NumPy data types that can be used to interpret the memory
        buffer returned by the Windows API. The default is a tuple containing
        various integer and floating point types.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame with information about memory regions and modules, including
        their start and end addresses, names, base addresses, filenames, entry
        points, sizes, and process handles.

    Notes:
    ------
    This function uses the `scan_pattern_page` and `nested_dict` functions to
    scan memory regions for the specified pattern and store the results in a
    nested dictionary. The dictionary is then converted to a pandas DataFrame,
    which is used to extract information about the loaded modules in the current
    process. The resulting DataFrame is then returned.
    """
    if isinstance_tolerant(bufferdtype, tuple):
        bufferdtype = list(bufferdtype)
    next_region = 0
    allareas = nested_dict()
    if not isinstance_tolerant(bufferdtype, list):
        bufferdtype = [bufferdtype]
    user_space_limit = 0x7FFFFFFF0000 if sys.maxsize > 2**32 else 0x7FFF0000
    cpo = 0
    while next_region < user_space_limit:
        oldregion = next_region
        regbytes = limitfunc(oldregion)
        next_region, va = scan_pattern_page(
            configs.pm.process_handle,
            oldregion,
            bufferdty=None,
            regbytes=regbytes,
            allowed_protections=allowed_protections,
        )
        for bufferdty in bufferdtype:
            try:
                va1 = np.frombuffer(va, bufferdty)
            except Exception as fe:
                va1 = None

            allareas[cpo][f"aa_start_{bufferdty}"] = oldregion
            allareas[cpo][f"aa_end_{bufferdty}"] = next_region
            allareas[cpo][f"aa_dump_{bufferdty}"] = va1
        cpo += 1
    dfareas = pd.DataFrame(allareas).T
    moduleinfos = []
    for k in configs.pm.list_modules():
        a = k.name
        b = k.lpBaseOfDll
        c = k.filename
        d = k.EntryPoint
        e = k.SizeOfImage
        f = k.process_handle
        for bufferdty in bufferdtype:
            dafa = dfareas.loc[dfareas[f"aa_start_{bufferdty}"] == k.lpBaseOfDll]
            if not dafa.empty:
                moduleinfos.append((dafa.index[0], a, b, c, d, e, f))
    dfmo = pd.DataFrame.from_records(moduleinfos).set_index(0).sort_index()
    dfmo.columns = [
        "aa_name",
        "aa_lpBaseOfDll",
        "aa_filename",
        "aa_EntryPoint",
        "aa_SizeOfImage",
        "aa_process_handle",
    ]
    df3 = pd.concat([dfareas, dfmo[~dfmo.index.duplicated(keep="first")]], axis=1)
    df3 = df3.dropna(subset=df3.columns[2]).reset_index(drop=True)
    df3.columns = [
        regex.sub(r"[\W_]+", "_", x).replace("_class_", "_").strip("_")
        for x in df3.columns
    ]
    df3 = df3.drop(
        columns=[
            x
            for x in df3.columns[2:]
            if str(x).startswith("aa_start_") or str(x).startswith("aa_end_")
        ]
    )
    df3.columns = ["aa_start", "aa_end"] + df3.columns[2:].to_list()
    df3["aa_memstate"] = df3.aa_start.ds_apply_ignore(
        pd.NA, lambda x: pymem.memory.virtual_query(configs.pm.process_handle, int(x))
    )
    df3["aa_rights"] = df3.aa_memstate.ds_apply_ignore(pd.NA, lambda x: x.protect.name)
    df3["aa_type"] = df3.aa_memstate.ds_apply_ignore(pd.NA, lambda x: x.type.name)
    df3["aa_state"] = df3.aa_memstate.ds_apply_ignore(pd.NA, lambda x: x.state.name)

    return df3


def read_str_ex(configs, aa_abs_address, aa_max_byt_distance):
    try:
        return configs.pm.read_string(
            address=aa_abs_address, length=aa_max_byt_distance
        )
    except Exception:
        return pd.NA


def write_str_ex(
    configs,
    aa_abs_address,
    aa_max_byt_distance,
    aa_char,
):
    try:
        if aa_max_byt_distance == 2:
            configs.pm.write_bytes(
                address=aa_abs_address,
                value=str(aa_char).encode("utf-16-le"),
                length=aa_max_byt_distance,
            )
        else:
            configs.pm.write_bytes(
                address=aa_abs_address,
                value=str(aa_char).encode(),
                length=aa_max_byt_distance,
            )
        return True
    except Exception as fe:
        print(fe, aa_abs_address, aa_char)
        return False


def search_string(configs, df, wordsearch, concurrent=True, partial=True):
    """
    Search for a string pattern in a DataFrame column containing binary data.

    Args:
        df (pd.DataFrame): The DataFrame to search in.
        wordsearch (str): The string pattern to search for.
        concurrent (bool, optional): Whether to use concurrent regex matching. Defaults to True.
        partial (bool, optional): Whether to allow partial matches. Defaults to True.

    Returns:
        Tuple[pd.DataFrame, List[List[Tuple[int, bool]]]]: A tuple containing the DataFrame with the search results and a list of start/end positions of each partial match found.


    """
    try:
        allres = []
        startend_partial = []
        for lele in range(len(df)):
            ma = df.iloc[lele].aa_dump_S1.__array__()
            word, wordlist = string_to_utf16_byte(wordsearch)
            susu = "".join([f"(ma=={repr(x)})|" for x in (set(wordlist))]).strip("|")
            positive = numexpr.evaluate(susu)
            wherepositive = np.nonzero(positive)[0]
            rightletters = ma[wherepositive]
            startend_ = [
                (x.spans()[0], x.partial if hasattr(x, "partial") else False)
                for x in (
                    regex.finditer(
                        word,
                        b"".join(rightletters),
                        concurrent=concurrent,
                        partial=True,
                    )
                )
            ]
            startend_partial.append(startend_.copy())
            startend = [x[0] for x in startend_]
            posmatches = [wherepositive[x[0] : x[1]] for x in startend]
            allshapes = np.max([q.shape[0] for q in posmatches])
            adjustedarrays = [
                np.pad(x, (0, allshapes - len(x)), "constant", constant_values=-1)
                for x in posmatches
            ]
            resultdf = [
                (
                    pd.concat(
                        [
                            pd.DataFrame([g := df.aa_dump_S1.iloc[lele][x]]),
                            pd.DataFrame([x]),
                        ],
                        ignore_index=True,
                    ).T
                )
                .rename(columns={0: "aa_letter", 1: "aa_pos"})
                .assign(aa_word=b"".join(g), aa_matchid=ini)
                for ini, x in enumerate(adjustedarrays)
            ]

            resultdf = (
                pd.concat(resultdf)
                .reset_index()
                .rename(columns={"index": "aa_letterindex"})
            )
            resultdf["aa_start_block"] = df.iloc[lele].aa_start
            resultdf["aa_end_block"] = df.iloc[lele].aa_end
            allres.append(resultdf)
        allres = [x[1].assign(aa_blockid=x[0]) for x in enumerate(allres)]

        dfra = pd.concat(allres)
        dfra = dfra.dropna().reset_index(drop=True)
        dfra = dfra.loc[dfra.aa_pos != -1].reset_index(drop=True)

        newgroups = []
        for name, group in dfra.groupby(["aa_blockid", "aa_matchid"]):
            newdi = tuple(np.diff(group.aa_pos).tolist())
            newgroups.append(
                group.copy().assign(
                    aa_bytediff=[newdi] * len(group),
                    aa_bytedifflen=len(set(newdi)),
                )
            )

        dfra = pd.concat(newgroups).reset_index(drop=True)
        dfra["aa_max_byt_distance"] = dfra.aa_bytediff.ds_apply_ignore(
            -1, lambda x: max(x) if x else -1
        )
        dfra["aa_min_byt_distance"] = dfra.aa_bytediff.ds_apply_ignore(
            -1, lambda x: min(x) if x else -1
        )
        dfra["aa_len_seq"] = dfra.aa_word.ds_apply_ignore(0, len)
        if not partial:
            dfra = dfra.loc[
                (dfra.aa_min_byt_distance.isin([1, 2]))
                & (dfra.aa_len_seq == len(wordsearch))
                & (dfra.aa_max_byt_distance.isin([1, 2]))
                & (dfra.aa_bytedifflen == 1)
            ].reset_index(drop=True)

        dfra["aa_abs_address"] = dfra.aa_start_block + dfra.aa_pos
        dfra["ff_read_str"] = dfra.ds_apply_ignore(
            pd.NA,
            lambda x: FlexiblePartialOwnName(
                read_str_ex,
                f"",
                True,
                configs,
                int(x.aa_abs_address),
                int(x.aa_max_byt_distance),
            ),
            axis=1,
        )
        dfra["ff_write_str"] = dfra.ds_apply_ignore(
            pd.NA,
            lambda x: FlexiblePartialOwnName(
                write_str_ex,
                f"",
                True,
                configs,
                int(x.aa_abs_address),
                int(x.aa_max_byt_distance),
            ),
            axis=1,
        )
        return dfra, startend_partial
    except Exception as fe:
        print(fe)
        return (
            pd.DataFrame(
                columns=[
                    "aa_letterindex",
                    "aa_letter",
                    "aa_pos",
                    "aa_word",
                    "aa_matchid",
                    "aa_start_block",
                    "aa_end_block",
                    "aa_blockid",
                    "aa_bytediff",
                    "aa_bytedifflen",
                    "aa_max_byt_distance",
                    "aa_min_byt_distance",
                    "aa_len_seq",
                    "aa_abs_address",
                    "ff_read_str",
                    "ff_write_str",
                ]
            ),
            [],
        )


def get_ts(sep="_"):
    tnow = time.time()
    return (
        time.strftime(f"h%H{sep}m%M{sep}s%S_ms")
        + (str(tnow).split(".")[-1] + "0" * 10)[:6]
    ) + f'__{str(tnow).replace(".", "_")}'


def copy_func(f):
    if callable(f):
        if inspect.ismethod(f) or inspect.isfunction(f):
            g = lambda *args, **kwargs: f(*args, **kwargs)
            t = list(filter(lambda prop: not ("__" in prop), dir(f)))
            i = 0
            while i < len(t):
                setattr(g, t[i], getattr(f, t[i]))
                i += 1
            return g
    dcoi = deepcopy([f])
    return dcoi[0]


class FlexiblePartialOwnName:
    r"""
    FlexiblePartial(
            remove_file,
            "()",
            True,
            fullpath_on_device=x.aa_fullpath,
            adb_path=adb_path,
            serialnumber=device,
        )

    """

    def __init__(
        self, func, funcname: str, this_args_first: bool = True, *args, **kwargs
    ):
        self.this_args_first = this_args_first
        self.funcname = funcname
        try:
            self.f = copy_func(func)
        except Exception:
            self.f = func
        try:
            self.args = copy_func(list(args))
        except Exception:
            self.args = args

        try:
            self.kwargs = copy_func(kwargs)
        except Exception:
            try:
                self.kwargs = kwargs.copy()
            except Exception:
                self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newdic = {}
        newdic.update(self.kwargs)
        newdic.update(kwargs)
        if self.this_args_first:
            return self.f(*self.args, *args, **newdic)

        else:
            return self.f(*args, *self.args, **newdic)

    def __str__(self):
        return self.funcname

    def __repr__(self):
        return self.funcname


def search_number(configs, df11, columns, numexprstr):
    """
    Search for a number in a DataFrame.

    Args:
        df11 (pd.DataFrame): The DataFrame to search.
        columns (list, optional): The columns to search. Defaults to None.
        numexprstr (str): The number to search for.

    Returns:
        pd.DataFrame: The results of the search.
    """
    if is_nan(columns, emptyiters=True):
        numcolumns = df11.columns.to_list()[3:-6]
    else:
        numcolumns = columns

    reaa = pd.concat(
        [
            df11[x].ds_apply_ignore(
                np.array([], dtype=np.uint64),
                lambda a: np.nonzero(numexpr.evaluate(numexprstr))[0].astype(np.uint64)
                * configs.bytediv[x],
            )
            for x in numcolumns
        ],
        axis=1,
        ignore_index=True,
    )
    reaa.columns = numcolumns
    dfa = pd.concat(
        [
            reaa[x]
            .loc[reaa[x].ds_apply_ignore(False, lambda x: len(x) > 0)]
            .reset_index()
            .assign(aa_dtype=x)
            .explode(x)
            .rename(columns={x: "aa_relativeaddress", "index": "aa_blockindex"})
            for x in reaa.columns
        ],
        ignore_index=True,
    )
    dfa["aa_blockstart"] = dfa.aa_blockindex.map(df11.aa_start)
    dfa["aa_absaddress"] = dfa.aa_blockstart + dfa.aa_relativeaddress
    dfa["aa_absaddress"] = dfa["aa_absaddress"].astype("Int64")
    dfa["aa_absaddress_hex"] = dfa["aa_absaddress"].ds_apply_ignore(
        "", lambda x: hex(x)
    )
    dfa["aa_value"] = numexprstr
    dfa["ff_read"] = dfa.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            ignore_exceptions_decorator(
                functools.partial(configs.byteread[x.aa_dtype]),
                exception_value=pd.NA,
                disable=False,
                print_exception=True,
            ),
            "",
            True,
            int(x.aa_absaddress),
        ),
        axis=1,
    )

    dfa["ff_write"] = dfa.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            ignore_exceptions_decorator(
                functools.partial(configs.bytewrite[x.aa_dtype]),
                exception_value=pd.NA,
                disable=False,
                print_exception=True,
            ),
            "",
            True,
            int(x.aa_absaddress),
        ),
        axis=1,
    )
    colna = get_ts(sep="_")
    dfa[colna] = dfa.ff_read.ds_apply_ignore(pd.NA, lambda x: x())
    indfilt = dfa.aa_blockstart.to_list()
    meminfo = (
        df11.set_index("aa_start")
        .loc[indfilt][
            [
                x
                for x in df11.columns
                if "aa_dump" not in x and x not in ["aa_start", "aa_end"]
            ]
        ]
        .reset_index(drop=True)
    )
    dfa = pd.concat([dfa, meminfo], axis=1)

    return dfa


def observe_all_values(
    configs,
    dty: type = np.int8,
    limitfunc=lambda x: True,
    allowed_protections=(
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_WRITECOPY,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_NOACCESS,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_WRITECOPY,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_GUARD,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_NOCACHE,
        pymem.ressources.structure.MEMORY_PROTECTION.PAGE_WRITECOMBINE,
    ),
):
    isstring = False
    if dty == np.string_:
        isstring = True
        dty = np.uint8
    check_differences = [numpydtypes[dty]]
    extradty = []
    if numpydtypes[dty] != "aa_dump_numpy_int64":
        check_differences.append("aa_dump_numpy_int64")
        extradty.append(np.int64)
    co = -1
    df11 = get_dfs_from_regions(
        configs=configs,
        limitfunc=limitfunc,
        bufferdtype=[dty, *extradty],
        allowed_protections=allowed_protections,
    )
    allfinalresults = []
    while True:
        try:
            df12 = get_dfs_from_regions(
                configs=configs,
                limitfunc=limitfunc,
                bufferdtype=[dty, *extradty],
                allowed_protections=allowed_protections,
            )

            difference1 = []
            difference2 = []
            for x in list(set(df11.aa_start) & set(df12.aa_start)):
                a = df11.loc[df11.aa_start == x].aa_dump_numpy_int64.iloc[0]
                b = df12.loc[df12.aa_start == x].aa_dump_numpy_int64.iloc[0]
                gotexc = False
                y = x
                try:
                    c = np.nonzero(~numexpr.evaluate("a==b"))[0]
                    d = c.copy()
                except Exception as fe:
                    lenche = min(a.shape[0], b.shape[0]) - 1
                    lenchemax = max(a.shape[0], b.shape[0])
                    ax = a[:lenche]
                    bx = b[:lenche]
                    c = np.nonzero(~numexpr.evaluate("ax==bx"))[0]
                    gotexc = True
                    an_array = np.empty((lenchemax,))
                    an_array[:] = np.NaN
                    cc = c.copy()
                    c = np.concatenate([cc, np.arange(a.shape[0])[a.shape[0] :]])
                    d = np.concatenate([cc, np.arange(b.shape[0])[b.shape[0] :]])

                if np.any(c) or np.any(d):
                    difference1.append(
                        (
                            x,
                            c,
                            *[
                                df11.loc[df11.aa_start == x][q].iloc[0][
                                    c * configs.bytedivmult[q]
                                ]
                                for q in check_differences
                            ],
                        )
                    )
                    difference2.append(
                        (
                            y,
                            d,
                            *[
                                df12.loc[df12.aa_start == y][q].iloc[0][
                                    d * configs.bytedivmult[q]
                                ]
                                for q in check_differences
                            ],
                        )
                    )
            dfdiff1 = pd.DataFrame(
                difference1, columns=["aa_start", "aa_index64", *check_differences]
            )
            dfdiff2 = pd.DataFrame(
                difference2, columns=["aa_start", "aa_index64", *check_differences]
            )
            t1flat = []
            t2flat = []
            for checkcol in check_differences:
                if checkcol == "aa_dump_numpy_int64" and dty != np.int64:
                    continue
                for _ in range(2):
                    if _ == 0:
                        checktmpdf = dfdiff1
                        appender = t1flat
                        checktmpdfbig = df11
                    else:
                        checktmpdf = dfdiff2
                        appender = t2flat
                        checktmpdfbig = df12
                    t1 = pd.concat(
                        checktmpdf.apply(
                            lambda x: pd.DataFrame(
                                np.c_[
                                    x["aa_index64"].__array__(), x[checkcol].__array__()
                                ]
                            )
                            .rename(columns={0: "aa_index64", 1: "aa_value"})
                            .assign(
                                aa_start=x.aa_start,
                                aa_index64=lambda qq: qq["aa_index64"]
                                * configs.bytedivmult[checkcol],
                            )
                            .assign(
                                aa_absaddress=lambda qq: qq["aa_start"]
                                + qq["aa_index64"],
                                aa_dtype=checkcol,
                            ),
                            axis=1,
                        ).to_list()
                    )
                    t1 = pd.concat(
                        [
                            t1,
                            t1.apply(
                                lambda m: (
                                    checktmpdfbig.loc[
                                        checktmpdfbig["aa_start"] == m.aa_start,
                                        m.aa_dtype,
                                    ].iloc[0][
                                        [
                                            int(m.aa_index64 + x)
                                            for x in range(
                                                configs.bytedivmult[m.aa_dtype]
                                            )
                                        ]
                                    ],
                                    [
                                        int(m.aa_index64 + x)
                                        for x in range(configs.bytedivmult[m.aa_dtype])
                                    ],
                                    [
                                        int(
                                            m.aa_absaddress
                                            + (
                                                x
                                                * (8 // configs.bytedivmult[m.aa_dtype])
                                            )
                                        )
                                        for x in range(configs.bytedivmult[m.aa_dtype])
                                    ],
                                ),
                                axis=1,
                                result_type="expand",
                            ),
                        ],
                        axis=1,
                    )
                    appender.append(t1.copy())

            co = co + 1
            allfla1 = []
            for t11 in t1flat:
                allfatemp = []
                for t111 in range(len(t11)):
                    t1111 = (
                        pd.DataFrame(t11.iloc[t111][[0, 1, 2]].to_list())
                        .T.reset_index(drop=True)
                        .rename(
                            columns={0: "aa_value", 1: "aa_index64", 2: "aa_absaddress"}
                        )
                        .assign(
                            aa_start=t11.aa_start.iloc[0], aa_dtype=t11.aa_dtype.iloc[0]
                        )
                    )
                    allfatemp.append(t1111)
                allfla1.append(pd.concat(allfatemp).assign(aa_checkindex=co))
            co = co + 1
            allfla2 = []
            for t11 in t2flat:
                allfatemp = []
                for t111 in range(len(t11)):
                    t1111 = (
                        pd.DataFrame(t11.iloc[t111][[0, 1, 2]].to_list())
                        .T.reset_index(drop=True)
                        .rename(
                            columns={0: "aa_value", 1: "aa_index64", 2: "aa_absaddress"}
                        )
                        .assign(
                            aa_start=t11.aa_start.iloc[0], aa_dtype=t11.aa_dtype.iloc[0]
                        )
                    )
                    allfatemp.append(t1111)
                allfla2.append(pd.concat(allfatemp).assign(aa_checkindex=co))

            differencedfs = []
            for no in range(len(allfla1)):
                differencedfs.append(pd.concat([allfla1[no], allfla2[no]]).dropna())
            finalresult = pd.concat(differencedfs)

            allfinalresults.append(finalresult.copy())
            df11 = df12.copy()
        except KeyboardInterrupt:
            break
        except Exception as fa:
            # print(fa)

            continue

    try:
        allfa = (
            pd.concat(allfinalresults)
            .reset_index(drop=True)
            .sort_values(by=["aa_absaddress", "aa_checkindex"])
            .reset_index(drop=True)
        )
    except Exception as fe:
        print(fe)
        return pd.DataFrame(
            columns=[
                "aa_value",
                "aa_index64",
                "aa_absaddress",
                "aa_start",
                "aa_dtype",
                "aa_checkindex",
            ]
        )
    if isstring:
        allfa.aa_value = allfa.aa_value.__array__().view("S8").copy()
    return allfa


def observe_values(
    df, numexprfilter=None, sleeptime=1.0, savefolder=None, printoutputlimit=200
):
    """
    Continuously observes the values in a Pandas DataFrame and performs several optional operations.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to observe.
    numexprfilter : str, optional
        A NumExpr filter to apply to the DataFrame before processing.
    sleeptime : int, optional
        The number of seconds to sleep between observations.
    savefolder : str, optional
        The folder path to save the DataFrame to as a pickle file.
    printoutputlimit : int, optional
        The maximum number of rows to print to the console.

    Returns:
    --------
    pandas.DataFrame
        A copy of the original DataFrame with any modifications applied.
    """
    dfa = df.copy()
    lastcol = [x for x in dfa.columns if x.startswith("h")][-1]
    try:
        while True:
            try:
                colna = get_ts(sep="_")
                dfa[colna] = dfa.ff_read.ds_apply_ignore(pd.NA, lambda x: x())
                if not is_nan(numexprfilter, emptystrings=True):
                    new = dfa[colna].__array__()
                    old = dfa[lastcol].__array__()
                    dfa = dfa.loc[numexpr.evaluate(numexprfilter)]
                    lastcol = colna
                if not is_nan(savefolder):
                    if not os.path.exists(savefolder):
                        os.makedirs(savefolder)
                    fname = get_free_filename(
                        folder=savefolder, fileextension=".pkl", leadingzeros=5
                    )
                    dfa.to_dillpickle(fname)
                    print(fname)
                if not is_nan(printoutputlimit):
                    dfa[: int(printoutputlimit)].ds_color_print_all()

                time.sleep(sleeptime)
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        pass

    return dfa


class ConfigsDeb:
    def __init__(self, pid=None, filename=None):
        self.pm, self.bytediv, self.byteread, self.bytewrite = attach_to_process(
            pid, filename
        )
        self.pid = pid
        self.filename = filename


class Pdmemory:
    def __init__(self, pid=None, filename=None):
        self.configs = ConfigsDeb(pid=pid, filename=filename)
        self.regiondf = pd.DataFrame()
        self.stringsearchdf = pd.DataFrame()
        self.numbersearchdf = pd.DataFrame()
        self.observerdf = pd.DataFrame()
        self.differencesdf = pd.DataFrame()

    def record_all_changing_values(
        self,
        limitfunc: callable = lambda x: True,
        dtype: type = np.uint32,
        allowed_protections: tuple = (
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
        ),
    ) -> "Pdmemory":
        """Record all changing values in the process memory.

        Args:
            limitfunc (callable): A function to limit which regions to search.
            dtype (type): The data type of the memory values to search.
            allowed_protections (tuple): The allowed memory protections to search.

        Returns:
            self (Pdmemory): The current instance of Pdmemory.
        """
        print("Press ctrl+c to stop the recording")
        self.differencesdf = observe_all_values(
            configs=self.configs,
            dty=dtype,
            limitfunc=limitfunc,
            allowed_protections=allowed_protections,
        )
        return self

    def search_string(
        self,
        str_: str,
        concurrent: bool = True,
        partial: bool = False,
    ) -> "Pdmemory":
        """
        Searches for a string in the target process.

        Args:
            str_: The string to search for.
            concurrent: A boolean indicating whether the search should be concurrent.
            partial: A boolean indicating whether partial results are allowed.

        Returns:
            The current instance of Pdmemory.
        """
        self.stringsearchdf, _ = search_string(
            self.configs, self.regiondf, str_, concurrent=concurrent, partial=partial
        )
        return self

    def observe_numbers(
        self,
        keepcondition: str = "(new == old)",
        sleep_between_scans: float = 1,
        savefolder: Optional[str] = None,
        printoutputlimit: Optional[int] = 100,
    ) -> "Pdmemory":
        """
        Continuously observe changes in memory addresses that match the `keepcondition` expression,
        comparing the current value with the previous value in a loop, with a pause of `sleep_between_scans`
        seconds between each loop. The results are saved to a CSV file in `savefolder`, if specified.
        Results are saved to `self.observerdf`

        Args:
            keepcondition: A boolean expression string to filter the values to observe (evaluated through numexpr).
                The default
                expression is "(new == old)", which means it will drop all values that have changed.
            sleep_between_scans: Number of seconds to wait between each scan. Default is 1 second.
            savefolder: A folder path to save the observed values to a CSV file. Default is None, which
                means the results will not be saved.
            printoutputlimit: Maximum number of rows to display when printing the observed values. Default
                is 100. If None, nothing will be printed

        Returns:
            The current instance of Pdmemory.

        Raises:
            KeyboardInterrupt: If the user presses Ctrl+C during the observation, this exception is raised
                to stop the observation.
        """
        print("Press ctrl+c to stop the observation")
        self.observerdf = observe_values(
            df=self.numbersearchdf,
            numexprfilter=keepcondition,
            sleeptime=sleep_between_scans,
            savefolder=savefolder,
            printoutputlimit=printoutputlimit,
        )
        return self

    def search_number(
        self,
        numexprquery: str,
        dtypes: Tuple[type, ...] = (
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
    ) -> "Pdmemory":
        """
        Search for numerical values that match the `numexprquery` expression in memory regions that contain
        the specified data types in `dtypes`. The results are saved in `self.numbersearchdf`.

        Args:
            numexprquery: A Numexpr expression string to filter the values to search for.
            dtypes: A tuple of Numpy data types to specify the columns to search in memory regions. Default
                data types are (int8, uint8, int16, uint16, int32, uint32, int64, uint64, float32, float64).

        Returns:
            The current instance of Pdmemory.
        """
        dtypessearch = {
            np.int8: "aa_dump_numpy_int8",
            np.uint8: "aa_dump_numpy_uint8",
            np.int16: "aa_dump_numpy_int16",
            np.uint16: "aa_dump_numpy_uint16",
            np.int32: "aa_dump_numpy_int32",
            np.uint32: "aa_dump_numpy_uint32",
            np.int64: "aa_dump_numpy_int64",
            np.uint64: "aa_dump_numpy_uint64",
            np.float32: "aa_dump_numpy_float32",
            np.float64: "aa_dump_numpy_float64",
        }
        columns = []
        for d in dtypes:
            columns.append(dtypessearch[d])
        self.numbersearchdf = search_number(
            self.configs,
            self.regiondf,
            columns=columns,
            numexprstr=numexprquery,
        )
        return self

    def update_region_df(
        self,
        limitfunction: callable = lambda x: True,
        dtypes: tuple = (
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
        allowed_protections: tuple = (
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READ,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_EXECUTE_WRITECOPY,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READONLY,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_READWRITE,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_WRITECOPY,
            # pymem.ressources.structure.MEMORY_PROTECTION.PAGE_NOACCESS,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_GUARD,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_NOCACHE,
            pymem.ressources.structure.MEMORY_PROTECTION.PAGE_WRITECOMBINE,
        ),
    ) -> "Pdmemory":
        """
        Updates the region DataFrame based on the current process.

        :param limitfunction: A function used to limit which regions are included in the DataFrame. By default, includes all regions.
        :type limitfunction: function, optional
        :param dtypes: A tuple of numpy data types used to filter the memory regions based on their data type. By default, includes 'S1', np.int8, np.uint8, np.int16, np.uint16, np.int32, np.uint32, np.int64, np.uint64, np.float32, and np.float64.
        :type dtypes: tuple, optional
        :param allowed_protections: A tuple of pymem.ressources.structure.MEMORY_PROTECTION flags used to filter the memory regions based on their protection status. By default, includes PAGE_EXECUTE_READ, PAGE_EXECUTE_READWRITE, PAGE_EXECUTE_WRITECOPY, PAGE_READONLY, PAGE_READWRITE, PAGE_WRITECOPY, PAGE_GUARD, PAGE_NOCACHE, and PAGE_WRITECOMBINE.
        :type allowed_protections: tuple, optional
        :return: The updated region DataFrame.
        :rtype: The current instance of Pdmemory.

        """
        self.regiondf = get_dfs_from_regions(
            configs=self.configs,
            limitfunc=limitfunction,
            bufferdtype=dtypes,
            allowed_protections=allowed_protections,
        )
        return self

    def get_regiondf(self):
        return self.regiondf

    def get_searchstringdf(self):
        return self.stringsearchdf

    def get_searchnumberdf(self):
        return self.numbersearchdf

    def get_observerdf(self):
        return self.observerdf

    def get_differencesdf(self):
        return self.differencesdf


