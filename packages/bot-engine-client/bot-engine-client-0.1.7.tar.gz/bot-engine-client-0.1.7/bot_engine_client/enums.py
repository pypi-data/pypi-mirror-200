from enum import Enum


class BotType(str, Enum):
    """"""

    Intraday = "Intraday"
    Position = "Position"


class TradingPlatform(str, Enum):
    """"""

    XQ = "XQ"
    MultiCharts = "MultiCharts"
    MultiChartsNET = "MultiCharts.NET"
    TradeStation = "TradeStation"
    NinjaTrader = "NinjaTrader"
    cTrader = "cTrader"
    WealthLab = "WealthLab"
    Quantower = "Quantower"
    QuantConnect = "QuantConnect"
    NeighNa = "VeighNa"


class TradeType(str, Enum):
    """"""

    Buy = "Buy"
    Sell = "Sell"
