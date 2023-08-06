from dataclasses import dataclass


@dataclass
class TradingFee:
    maker_commision: float
    taker_commision: float
