from typing import Callable, Optional
from .client import ITradingClient
from .trade_data import TradeData
from .types import TradingFee
from osmosispy import Coin, utils, Sdk

from osmosis_proto.proto.osmosis.txfees.v1beta1 import (
    query_pb2 as txfees_query,
    query_pb2_grpc as txfees_query_grpc,
)


class OsmosisTradingClient(ITradingClient):
    trader: Sdk

    def __init__(self, trader: Sdk):
        self.trader = trader

    def get_tx_fee(self, symbol: str = "OSMOUSDT") -> Optional[Coin]:
        raise NotImplementedError

    def get_trading_fee(self, symbol: str = "OSMOUSDT") -> Optional[TradingFee]:
        raise NotImplementedError

    def get_price(self, symbol: str = "OSMOUSDT") -> Coin:
        raise NotImplementedError

    def listen_trades(self, cb: Callable[[TradeData], None], symbol: str = "OSMOUSDT"):
        raise NotImplementedError

    def stop_listeners(self) -> None:
        raise NotImplementedError
