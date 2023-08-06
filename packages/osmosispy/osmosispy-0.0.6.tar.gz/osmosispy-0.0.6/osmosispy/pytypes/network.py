"""
The network class allows the user to defines the network the sdk interface should connect to.

There are some default values set for devnet, testnet, mainet and localnet, but the user cna also define its own
network by setting the values of the Network data class.

"""
import dataclasses
import enum
import os
from typing import Dict, List, Optional


class NetworkType(enum.Enum):
    """Enum class for the available network types. E.g. 'testnet' and 'devnet'."""

    LOCALNET = "localnet"
    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet"


@dataclasses.dataclass
class Network:
    lcd_endpoint: str
    grpc_endpoint: str
    tendermint_rpc_endpoint: str
    chain_id: str
    env: str = "custom"

    @property
    def is_insecure(self) -> bool:
        return not ("https" in self.tendermint_rpc_endpoint)

    @classmethod
    def devnet(cls) -> "Network":
        """
        **NOT IMPLEMENTED YET**
        """
        raise NotImplementedError

    @classmethod
    def testnet(cls) -> "Network":
        """
        **NOT IMPLEMENTED YET**
        """
        raise NotImplementedError

    @classmethod
    def mainnet(cls) -> "Network":
        return cls(
            lcd_endpoint=f'https://lcd.osmosis.zone',
            grpc_endpoint=f'grpc.osmosis.zone:9090',
            tendermint_rpc_endpoint=f'https://rpc.osmosis.zone',
            chain_id=f'osmosis-1',
            env=NetworkType.MAINNET.value,
        )

    @classmethod
    def localnet(cls) -> "Network":
        """
        Localnet is the network you would expect to connect to if you run `make localnet` from the osmosis repository.
        It allows you to update locally the golang codebase to checkout the behavior of the chain with different changes
        applied.

        Returns:
            Network: The updated Network object.
        """
        return cls(
            lcd_endpoint=f'http://localhost:1317',
            grpc_endpoint=f'localhost:9090',
            tendermint_rpc_endpoint=f'http://localhost:26657',
            chain_id=f'osmosis-1',
            env=NetworkType.LOCALNET.value,
        )

    def string(self) -> str:
        """
        Returns the current environment the network was initialized with. Will return `custom` if a custom network
        was created

        Returns:
            str: The name of the current environment.
        """
        return self.env
