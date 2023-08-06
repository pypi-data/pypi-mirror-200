from typing import Callable, Optional
from .trade_data import TradeData
from .types import TradingFee
from osmosispy import Coin
import re


class ITradingClient:
    """
    Interface for trading clients
    """

    @classmethod
    def split_symbol(cls, symbol: str) -> tuple[str, str]:
        """
        Splits the symbol into the two assets

        Args:
            symbol (str): The symbol to split

        Returns:
            tuple[str, str]: The two assets
        """

        v = re.split(r"([A-Z]+)(BTC|ETH|USDT|BNB|PAX|USDC|USDS)", symbol)

        return v[1], v[2]

    def get_trading_fee(self, symbol: str = "OSMOUSDT") -> Optional[TradingFee]:
        """
        Get the current trading fee for the symbol

        Args:
            symbol (str, optional): The pair to get the trading fee for. Defaults to "OSMOUSDT".

        Returns:
            Optional[TradingFee]: The trading fee for the pair. None if the there is no trades or fee info for the pair.
        """
        raise NotImplementedError

    def get_price(self, symbol: str = "OSMOUSDT") -> Coin:
        """
        Get the current price in the pair

        Args:
            symbol (str, optional): The pair to get the price in. Defaults to "OSMOUSDT".

        Returns:
            Coin: The price of the first asset in the pair
        """
        raise NotImplementedError

    def listen_trades(self, cb: Callable[[TradeData], None], symbol: str = "OSMOUSDT"):
        """
        Listen to trades for the pair

        Args:
            cb (`TradeData`) -> None: The callback to call when a trade is made
            symbol (str, optional): The pair to listen to. Defaults to "OSMOUSDT".

        Example:
        ```
        # Listen to trades for 60 seconds
        def cb(trade_data: TradeData):
            print(trade_data)

        client.listen_trades(cb)

        sleep(60)

        client.stop_ws()
        """
        raise NotImplementedError

    def stop_listeners(self) -> None:
        """
        Stops all listeners
        """
        raise NotImplementedError
