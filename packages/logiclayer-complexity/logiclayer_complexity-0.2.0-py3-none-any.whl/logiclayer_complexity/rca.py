from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import economic_complexity
import pandas as pd
from tesseract_olap import DataRequest, DataRequestParams


@dataclass
class RcaParameters:
    cube: str
    activity: str
    location: str
    measure: str
    year: int
    locale: Optional[str]
    threshold: Dict[str, Tuple[str, int]]
    aliases: Dict[str, str]

    @property
    def query(self) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": [self.location, self.activity],
            "measures": [self.measure],
            "cuts_include": {
                "Year": [str(self.year)],
            },
        }

        if self.locale is not None:
            params["locale"] = self.locale

        return DataRequest.new(self.cube, params)

    def apply_threshold(self, df: pd.DataFrame):
        measure = self.measure

        for level, condition in self.threshold.items():
            column_id = f"{level} ID"
            # From data, group rows by `level` dimension and get the sum of `measure`
            measure_sum = df[[column_id, measure]].groupby(by=[column_id]).sum()
            # Apply threshold condition and get rows that comply
            sum_to_drop = measure_sum.loc[series_compare(measure_sum[measure], *condition)]
            # Drop complying rows from summed dataframe (leaving non-complying only)
            measure_sum.drop(sum_to_drop.index, inplace=True)
            # Get indexes of non-complying rows
            data_to_drop = df.loc[df[column_id].isin(measure_sum.index)].index
            # ...and drop them from the original data
            df.drop(data_to_drop, inplace=True)

            del measure_sum, sum_to_drop, data_to_drop

    def _calculate(self, df: pd.DataFrame):
        """Execute RCA calculations.
        """
        index = self.location
        columns = self.activity
        values = self.measure

        # Guess ID column names
        index_id = f"{index} ID"
        index_id = index_id if index_id in df.columns else index
        columns_id = f"{columns} ID"
        columns_id = columns_id if columns_id in df.columns else columns

        # pivot the table and remove NAs
        tbl = pd.pivot_table(df, index=index_id, columns=columns_id, values=values)
        tbl.dropna(axis=1, how="all", inplace=True)
        tbl.fillna(0, inplace=True)

        # perform RCA calculation
        result = economic_complexity.rca(tbl.astype(float))

        def unpivot():
            # unpivot the table
            result.reset_index(inplace=True)
            rca = pd.melt(result, id_vars=[index_id], value_name=f"{values} RCA")

            # at this point the table only contains the ID columns and the RCA values

            # restore index labels
            if index != index_id:
                df_index = df[[index_id, index]].set_index(index_id)
                dict_index = df_index[index].to_dict()
                rca[index] = rca[index_id].map(dict_index)

            # restore columns labels
            if columns != columns_id:
                df_columns = df[[columns_id, columns]].set_index(columns_id)
                dict_columns = df_columns[columns].to_dict()
                rca[columns] = rca[columns_id].map(dict_columns)

            return rca

        return result, unpivot

    def calculate(self, df: pd.DataFrame, unpivot: bool = True) -> pd.DataFrame:
        df_rca, do_unpivot = self._calculate(df)
        if unpivot:
            df_rca = do_unpivot()
        del do_unpivot
        return df_rca


def series_compare(series: pd.Series, operator: str, value: int):
    if operator == "lt":
        return series.lt(value)
    if operator == "lte":
        return series.le(value)
    if operator == "gt":
        return series.gt(value)
    if operator == "gte":
        return series.ge(value)
    if operator == "eq":
        return series.eq(value)
    if operator == "neq":
        return series.ne(value)

    raise ValueError(f"Invalid comparison operator '{operator}'")
