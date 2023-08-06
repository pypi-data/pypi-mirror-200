from dataclasses import dataclass
from osmosispy import Coin


@dataclass
class TradeData:
    price: Coin
    quantity: Coin
