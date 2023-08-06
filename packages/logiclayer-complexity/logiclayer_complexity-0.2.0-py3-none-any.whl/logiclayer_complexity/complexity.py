from dataclasses import dataclass, field
from typing import Optional, Union, overload
from typing_extensions import Literal

import economic_complexity
import pandas as pd

from .rca import RcaParameters


@dataclass
class ComplexityParameters:
    rca_params: RcaParameters
    iterations: int
    cutoff: float
    rank: bool = field(default=False)
    sort_ascending: Optional[bool] = None

    def __getattr__(self, _name: str):
        return getattr(self.rca_params, _name)

    def _calculate(self, df: pd.DataFrame):
        cutoff = self.cutoff
        iterations = self.iterations
        rank = self.rank
        sort_ascending = self.sort_ascending

        location = self.rca_params.location
        activity = self.rca_params.activity
        measure = self.rca_params.measure

        rca, _ = self.rca_params._calculate(df)

        rca[rca >= cutoff] = 1
        rca[rca < cutoff] = 0

        eci, pci = economic_complexity.complexity(rca, iterations=iterations)

        def unpivot(ds: pd.Series, name: Literal["ECI", "PCI"]) -> pd.DataFrame:
            if sort_ascending is not None:
                ds = ds.sort_values(ascending=sort_ascending)

            dfci = ds.to_frame(name=f"{measure} {name}").reset_index()

            if rank or sort_ascending is not None:
                dfci[f"{measure} {name} Ranking"] = dfci[f"{measure} {name}"].rank(ascending=False)

            index = location if name == "ECI" else activity
            index_id = f"{index} ID"
            index_id = index_id if index_id in df.columns else index

            if index != index_id:
                df_index = df[[index_id, index]].set_index(index_id)
                dict_index = df_index[index].to_dict()
                dfci[index] = dfci[index_id].map(dict_index)

            return dfci

        return eci, pci, unpivot

    @overload
    def calculate(
        self, df: pd.DataFrame, name: Literal["ECI", "PCI"], *, unpivot: Literal[False],
    ) -> pd.Series: ...

    @overload
    def calculate(
        self, df: pd.DataFrame, name: Literal["ECI", "PCI"], *, unpivot: Literal[True],
    ) -> pd.DataFrame: ...

    @overload
    def calculate(
        self, df: pd.DataFrame, name: Literal["ECI", "PCI"]
    ) -> pd.DataFrame: ...

    def calculate(
        self,
        df: pd.DataFrame,
        name: Literal["ECI", "PCI"],
        *,
        unpivot: bool = True,
    ) -> Union[pd.DataFrame, pd.Series]:
        eci, pci, do_unpivot = self._calculate(df)

        if name == "ECI":
            return do_unpivot(eci, name) if unpivot else eci
        elif name == "PCI":
            return do_unpivot(pci, name) if unpivot else pci
        else:
            raise ValueError(
                "Complexity calculation must intend to retrieve 'ECI' or 'PCI'"
            )
