"""Economic Complexity adapter for use in LogicLayer.

Contains a module to enable endpoints which return economic complexity
calculations, using a Tesseract OLAP server as data source.
"""

from typing import Dict, List, Optional, Tuple

import pandas as pd
from fastapi import Depends, HTTPException
from logiclayer import LogicLayerModule, route
from tesseract_olap import DataRequest, OlapServer
from tesseract_olap.backend.exceptions import BackendError
from tesseract_olap.query.exceptions import QueryError

from .__version__ import __title__, __version__
from .complexity import ComplexityParameters
from .dependencies import parse_filter, prepare_complexity_params, prepare_rca_params
from .rca import RcaParameters
from .wdi import WdiParameters, WdiReference, WdiReferenceSchema, parse_wdi


class EconomicComplexityModule(LogicLayerModule):
    """Economic Complexity calculations module class for LogicLayer."""

    server: "OlapServer"
    wdi: Optional["WdiReference"]

    def __init__(
        self,
        server: "OlapServer",
        wdi: Optional["WdiReferenceSchema"] = None,
    ):
        """Setups the server for this instance."""
        super().__init__()

        if server is None:
            raise ValueError(
                "EconomicComplexityModule requires a tesseract_olap.OlapServer instance"
            )
        self.server = server

        if wdi is not None:
            self.wdi = WdiReference(**wdi)

    async def fetch_data(self, query: DataRequest):
        """Retrieves the data from the backend, and handles related errors."""
        try:
            res = await self.server.execute(query)
        except QueryError as exc:
            raise HTTPException(status_code=400, detail=exc.message) from None
        except BackendError as exc:
            raise HTTPException(status_code=500, detail=exc.message) from None

        return pd.DataFrame([item async for item in res])

    async def apply_wdi_threshold(
        self,
        df: pd.DataFrame,
        wdi_params: WdiParameters,
        location: str,
    ):
        if self.wdi is None:
            raise HTTPException(500, "WDI reference is not configured")

        wdi_location = self.wdi.level_mapper.get(location, location)
        wdi_query = self.wdi.build_query(wdi_params, wdi_location)
        wdi_data = await self.fetch_data(wdi_query)
        wdi_members = wdi_data[f"{wdi_location} ID"].to_list()

        # WDI works the same as threshold, but using remote data
        data_to_drop = df.loc[~df[f"{location} ID"].isin(wdi_members)]
        df.drop(data_to_drop.index, inplace=True)

        del wdi_data, data_to_drop

    @route("GET", "/")
    def route_root(self):
        return {
            "module": __title__,
            "version": __version__,
            "wdi": "disabled" if self.wdi is None else "enabled",
        }

    @route("GET", "/rca")
    async def route_rca(
        self,
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        rca: RcaParameters = Depends(prepare_rca_params),
        wdi: List[WdiParameters] = Depends(parse_wdi),
    ):
        """RCA calculation endpoint."""
        df = await self.fetch_data(rca.query)

        rca.apply_threshold(df)
        for item in wdi:
            await self.apply_wdi_threshold(df, item, rca.location)

        rca_df = rca.calculate(df, unpivot=True)

        apply_filters(rca_df, filters)
        apply_aliases(rca_df, rca.aliases)

        return {
            "data": rca_df.to_dict("records"),
        }

    @route("GET", "/eci")
    async def route_eci(
        self,
        cmplx: ComplexityParameters = Depends(prepare_complexity_params),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        wdi: List[WdiParameters] = Depends(parse_wdi),
    ):
        """ECI calculation endpoint."""
        df = await self.fetch_data(cmplx.query)

        cmplx.apply_threshold(df)
        for item in wdi:
            await self.apply_wdi_threshold(df, item, cmplx.location)

        eci = cmplx.calculate(df, "ECI", unpivot=True)

        apply_filters(eci, filters)
        apply_aliases(eci, cmplx.aliases)

        return {
            "data": eci.to_dict("records"),
        }

    @route("GET", "/pci")
    async def route_pci(
        self,
        cmplx: ComplexityParameters = Depends(prepare_complexity_params),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        wdi: List[WdiParameters] = Depends(parse_wdi),
    ):
        """PCI calculation endpoint."""
        df = await self.fetch_data(cmplx.query)

        cmplx.apply_threshold(df)
        for item in wdi:
            await self.apply_wdi_threshold(df, item, cmplx.location)

        pci = cmplx.calculate(df, "PCI", unpivot=True)

        apply_filters(pci, filters)
        apply_aliases(pci, cmplx.aliases)

        return {
            "data": pci.to_dict("records"),
        }


def apply_filters(df: pd.DataFrame, filters: Dict[str, Tuple[str, ...]]):
    # filter which members will be sent in the response
    for key, values in filters.items():
        column_id = f"{key} ID"
        dropping = df.loc[~df[column_id].isin(values)].index
        df.drop(dropping, inplace=True)
        del dropping


def apply_aliases(df: pd.DataFrame, aliases: Dict[str, str]):
    df.rename(columns=aliases, inplace=True)
