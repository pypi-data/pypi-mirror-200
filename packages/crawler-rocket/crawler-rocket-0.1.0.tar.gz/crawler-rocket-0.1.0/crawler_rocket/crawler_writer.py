from __future__ import annotations
from typing import Callable, Sequence, Hashable, Literal, TypeVar
import pandas as pd
from pandas import DataFrame
from pandas._typing import (
    FilePath,
    ReadCsvBuffer,
    WriteBuffer,
    Scalar,
    AnyArrayLike,
    IndexLabel,
    Suffixes,
)

from .logger import CH_LOGGER


class CrawlerWriter(object):
    def __init__(
        self,
        key: str,
        column_list: list[str] | None = None,
        df: DataFrame | None = None,
    ) -> None:
        self._key = key
        if column_list is None and df is None:
            CH_LOGGER.error("one of ``column_list`` and ``df`` must be set")
        self._data: DataFrame = pd.DataFrame(data=df, columns=column_list)

    def read_csv(
        self,
        filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str],
        sep: str | None = ...,
        delimiter: str | None = None,
        # Column and Index Locations and Names
        header: int | Sequence[int] | None | Literal["infer"] = "infer",
        names: list[str] | None = None,
        index_col: int | str | Sequence[int | str] | Literal[False] | None = None,
    ):
        """
        Read a comma-separated values (csv) file into CrawlerWriter.

        Parameters
        ----------
        filepath_or_buffer : str, path object or file-like object
            Any valid string path is acceptable. The string could be a URL. Valid
            URL schemes include http, ftp, s3, gs, and file. For file URLs, a host is
            expected. A local file could be: file://localhost/path/to/table.csv.

            If you want to pass in a path object, pandas accepts any ``os.PathLike``.

            By file-like object, we refer to objects with a ``read()`` method, such as
            a file handle (e.g. via builtin ``open`` function) or ``StringIO``.
        sep : str, default {_default_sep}
            Delimiter to use. If sep is None, the C engine cannot automatically detect
            the separator, but the Python parsing engine can, meaning the latter will
            be used and automatically detect the separator by Python's builtin sniffer
            tool, ``csv.Sniffer``. In addition, separators longer than 1 character and
            different from ``'\\s+'`` will be interpreted as regular expressions and
            will also force the use of the Python parsing engine. Note that regex
            delimiters are prone to ignoring quoted data. Regex example: ``'\r\t'``.
        delimiter : str, default ``None``
            Alias for sep.
        header : int, list of int, None, default 'infer'
            Row number(s) to use as the column names, and the start of the
            data.  Default behavior is to infer the column names: if no names
            are passed the behavior is identical to ``header=0`` and column
            names are inferred from the first line of the file, if column
            names are passed explicitly then the behavior is identical to
            ``header=None``. Explicitly pass ``header=0`` to be able to
            replace existing names. The header can be a list of integers that
            specify row locations for a multi-index on the columns
            e.g. [0,1,3]. Intervening rows that are not specified will be
            skipped (e.g. 2 in this example is skipped). Note that this
            parameter ignores commented lines and empty lines if
            ``skip_blank_lines=True``, so ``header=0`` denotes the first line of
            data rather than the first line of the file.
        names : array-like, optional
            List of column names to use. If the file contains a header row,
            then you should explicitly pass ``header=0`` to override the column names.
            Duplicates in this list are not allowed.
        index_col : int, str, sequence of int / str, or False, optional, default ``None``
        Column(s) to use as the row labels of the ``Dataframe``, either given as
        string name or column index. If a sequence of int / str is given, a
        MultiIndex is used.
        """
        self._data = pd.read_csv(
            filepath_or_buffer,
            sep=sep,
            delimiter=delimiter,
            header=header,
            names=names,
            index_col=index_col,
        )

    def save_to_csv(
        self,
        path_or_buf: FilePath | WriteBuffer[bytes] | WriteBuffer[str] | None = None,
        sep: str = ",",
        na_rep: str = "",
        float_format: str | Callable | None = None,
        columns: list[Hashable] | None = None,
        header: bool | list[str] = True,
        index: bool = False,
    ):
        """Write object to a comma-separated values (csv) file."""
        self._data.to_csv(
            path_or_buf,
            sep=sep,
            na_rep=na_rep,
            float_format=float_format,
            columns=columns,
            header=header,
            index=index,
        )

    def read_excel(
        self,
        io,
        sheet_name: str | int | None = 0,
        header: int | Sequence[int] | None = 0,
        names: list[str] | None = None,
        index_col: int | Sequence[int] | None = None,
        usecols: Sequence[int] | Sequence[str] | Callable[[str], bool] | None = None,
    ):
        """
        Read an Excel file into a pandas DataFrame.

        Supports `xls`, `xlsx`, `xlsm`, `xlsb`, `odf`, `ods` and `odt` file extensions
        read from a local filesystem or URL. Supports an option to read
        a single sheet or a list of sheets.

        Parameters
        ----------
        io : str, bytes, ExcelFile, xlrd.Book, path object, or file-like object
            Any valid string path is acceptable. The string could be a URL. Valid
            URL schemes include http, ftp, s3, and file. For file URLs, a host is
            expected. A local file could be: ``file://localhost/path/to/table.xlsx``.

            If you want to pass in a path object, pandas accepts any ``os.PathLike``.

            By file-like object, we refer to objects with a ``read()`` method,
            such as a file handle (e.g. via builtin ``open`` function)
            or ``StringIO``.
        sheet_name : str, int, list, or None, default 0
            Strings are used for sheet names. Integers are used in zero-indexed
            sheet positions (chart sheets do not count as a sheet position).
            Lists of strings/integers are used to request multiple sheets.
            Specify None to get all worksheets.

            Available cases:

            * Defaults to ``0``: 1st sheet as a `DataFrame`
            * ``1``: 2nd sheet as a `DataFrame`
            * ``"Sheet1"``: Load sheet with name "Sheet1"
            * ``[0, 1, "Sheet5"]``: Load first, second and sheet named "Sheet5"
            as a dict of `DataFrame`
            * None: All worksheets.

        header : int, list of int, default 0
            Row (0-indexed) to use for the column labels of the parsed
            DataFrame. If a list of integers is passed those row positions will
            be combined into a ``MultiIndex``. Use None if there is no header.
        names : array-like, default None
            List of column names to use. If file contains no header row,
            then you should explicitly pass header=None.
        index_col : int, list of int, default None
            Column (0-indexed) to use as the row labels of the DataFrame.
            Pass None if there is no such column.  If a list is passed,
            those columns will be combined into a ``MultiIndex``.  If a
            subset of data is selected with ``usecols``, index_col
            is based on the subset.

            Missing values will be forward filled to allow roundtripping with
            ``to_excel`` for ``merged_cells=True``. To avoid forward filling the
            missing values use ``set_index`` after reading the data instead of
            ``index_col``.
        usecols : str, list-like, or callable, default None
            * If None, then parse all columns.
            * If str, then indicates comma separated list of Excel column letters
            and column ranges (e.g. "A:E" or "A,C,E:F"). Ranges are inclusive of
            both sides.
            * If list of int, then indicates list of column numbers to be parsed
            (0-indexed).
            * If list of string, then indicates list of column names to be parsed.
            * If callable, then evaluate each column name against it and parse the
            column if the callable returns ``True``.

        Returns a subset of the columns according to behavior above.
        """
        self._data = DataFrame(
            pd.read_excel(
                io,
                sheet_name=sheet_name,
                header=header,
                names=names,
                index_col=index_col,
                usecols=usecols,
            )
        )

    def save_to_excel(
        self,
        excel_writer,
        sheet_name: str = "Sheet1",
        na_rep: str = "",
        float_format: str | None = None,
        columns: Sequence[str] | None = None,
        header: list[str] | bool = True,
        index: bool = False,
        index_label: str | Sequence[str] | None = None,
    ):
        """Write object to an Excel sheet."""
        self._data.to_excel(
            excel_writer=excel_writer,
            sheet_name=sheet_name,
            na_rep=na_rep,
            float_format=float_format,
            columns=columns,
            header=header,
            index=index,
            index_label=index_label,
        )

    def columns(self) -> list[str]:
        """Return the columns list"""
        return self._data.columns.values.tolist()

    def head(self) -> str:
        """Return the first n rows."""
        if self._data.empty:
            CH_LOGGER.error("crawler writer has no data")
        return self._data.head().to_string()

    def lines(self) -> int:
        """Return the lines of data"""
        return len(self._data.index)

    def data(self) -> DataFrame:
        """Return dataframe of the crawler writer"""
        return self._data

    def set_data(self, data: DataFrame) -> None:
        """Set data for the crawler writer"""
        self._data = data

    def tail(self) -> str:
        """Return the last n rows."""
        if self._data.empty:
            CH_LOGGER.error("crawler writer has no data")
        return self._data.tail().to_string()

    def find(self, line: int, column: Hashable) -> Scalar:
        """
        Get data at line=``line`` column=``column``.

        Parameters
        ----------
        line: int
            The index of the data
        column: Hashable
            Use column index or column name to locate
        """
        if type(column) == int:
            return self._data.iat[line, column]
        else:
            return self._data.at[line, column]

    def write(self, line: int, column: Hashable, data: Scalar):
        """Write info at line=``line`` column=``column``."""
        if not data:
            CH_LOGGER.error("write() takes at least 3 arguments (2 given)")
        if type(column) == int:
            self._data.iat[line, column] = data
        else:
            self._data.at[line, column] = data

    def write_line(self, **datas):
        """Write info to next line."""
        if not datas:
            CH_LOGGER.error("write() takes at least 1 arguments (0 given)")
        line = self.lines()
        for col in datas.keys():
            self._data.at[line, col] = datas[col]
        self._data = self._data

    def write_line_at(self, line: int, **datas):
        """Write info to the line ``line``."""
        max_line = self.lines()
        if line > max_line:
            CH_LOGGER.error(f"the max line can reach is {max_line}")
        elif not datas:
            CH_LOGGER.error("write() takes at least 1 arguments (0 given)")
        for col in datas.keys():
            self._data.at[line, col] = datas[col]
        self._data = self._data

    def delete_line(self, line: int) -> None:
        """Delete info at line=``line``."""
        self._data = self._data.drop(line).reset_index(drop=True)

    def append_column(
        self,
        index: int,
        column_name: Hashable,
        value: Scalar | AnyArrayLike | None = None,
        allow_duplicates=False,
    ) -> None:
        """
        Append a new column.
        Parameters
        ----------
        index : int
            Insertion index. Must verify 0 <= loc <= len(columns).
        column : str, number, or hashable object
            Label of the inserted column.
        value : Scalar, Series, or array-like
        allow_duplicates : bool, optional, default lib.no_default
        """
        self._data.insert(index, column_name, value, allow_duplicates=allow_duplicates)

    def delete_column(
        self, column_name: Hashable | None, column_index: int | None, inplace=True
    ) -> DataFrame | None:
        """Delete a new column."""
        if column_name is None and column_index is None:
            CH_LOGGER.error("One of column_name and column_index must be set.")
        elif column_name != None:
            return self._data.drop(column_name, axis="columns", inplace=inplace)
        else:
            return self._data.drop(index=column_index, axis="columns", inplace=inplace)

    def apply(
        self,
        column_index: int,
        func,
        *args,
        **kwargs,
    ):
        """
        Invoke function on values of one column of the data.
        Can be ufunc (a NumPy function that applies to the entire Series)
        or a Python function that only works on single values.
        Parameters
        ----------
        column_index: int
            The column you want to apply the func.
        func : function
            Python function or NumPy ufunc to apply.
        args : tuple
            Positional arguments passed to func after the series value.
        **kwargs
            Additional keyword arguments passed to func.
        """
        s = self._data.iloc[:, column_index]
        self._data[self._data.columns[column_index]] = s.apply(
            func, convert_dtype=True, *args, **kwargs
        )

    def append(
        self,
        other: CrawlerWriter,
        join="inner",
        ignore_index: bool = True,
    ) -> CrawlerWriter:
        """
        Append rows of other to the end of caller.
        Return a new CrawlerWriter.
        """
        df = pd.concat(
            [self._data, other.data()], axis=0, join=join, ignore_index=ignore_index  # type: ignore
        )
        return CrawlerWriter(self._key, None, df)

    def merge(
        self,
        right: CrawlerWriter,
        how: str = "inner",
        on: IndexLabel | None = None,
        left_on: IndexLabel | None = None,
        right_on: IndexLabel | None = None,
        left_index: bool = False,
        right_index: bool = False,
        sort: bool = False,
        suffixes: Suffixes = ("_x", "_y"),
        copy: bool = True,
        indicator: bool = False,
        validate: str | None = None,
    ) -> CrawlerWriter:
        """
        Merge another data source. Just like the sql Join,
        return a new CrawlerWriter.
        """
        df = self._data.merge(
            right.data(),
            how=how,  # type: ignore
            on=on,
            left_on=left_on,
            right_on=right_on,
            left_index=left_index,
            right_index=right_index,
            sort=sort,
            suffixes=suffixes,
            copy=copy,
            indicator=indicator,
            validate=validate,
        )
        return CrawlerWriter(self._key, None, df)
