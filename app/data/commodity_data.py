from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class CommodityInfo:
    name: str
    ticker: str


class Commodity(Enum):
    BRENTOIL = CommodityInfo(name="Brent Oil", ticker="BZ=F")
    CRUDEOIL = CommodityInfo(name="Crude Oil", ticker="CL=F")
    GOLD = CommodityInfo(name="Gold", ticker="GC=F")
    SILVER = CommodityInfo(name="Silver", ticker="SI=F")
    COPPER = CommodityInfo(name="Copper", ticker="HG=F")
    NATURALGAS = CommodityInfo(name="Natural Gas", ticker="NG=F")
    NIKEL = CommodityInfo(name="Nikel", ticker="-")
    COAL = CommodityInfo(name="Coal", ticker="-")
    ALUMINIUM = CommodityInfo(name="Aluminium", ticker="-")
    BAUXITE = CommodityInfo(name="Bauxite", ticker="-")
    CONSUMENT_SERVICE = CommodityInfo(name="Consument Service", ticker="-")

    @classmethod
    def from_name(cls, name):
        for c in cls:
            if c.value.name.lower() == name.lower():
                return c
        raise ValueError(f"Unknown commodity: {name}")
