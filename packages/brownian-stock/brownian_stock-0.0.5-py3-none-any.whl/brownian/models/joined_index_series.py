
from typing import Dict, List

import polars as pl

from .. import const
from .abstract_series import AbstractSeries
from .index_series import IndexSeries


class JoinedIndexSeries(AbstractSeries):

    def __init__(self, index_dict: Dict[str, IndexSeries]):
        if len(index_dict) == 0:
            raise ValueError("Length of index_dict must be larger than 0")

        available_keys = []
        df_ls :List[pl.DataFrame] = []
        for key, index in index_dict.items():
            available_keys.append(key)
            df = index._df
            df = df.rename({const.COL_INDEX_VALUE: key})
            df_ls.append(df)

        base_df = df_ls.pop()
        while len(df_ls) > 0:
            poped_df = df_ls.pop()
            base_df = base_df.join(poped_df, on=const.COL_DATE, how="outer")
        base_df = base_df.sort(const.COL_DATE)
        super().__init__(base_df)
        self.available_keys = available_keys