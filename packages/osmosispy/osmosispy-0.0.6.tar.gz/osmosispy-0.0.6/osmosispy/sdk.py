"""
The fundamental gateway to the blockchain is the "Sdk" - an essential library that requires authorization
with a wallet/signer for each "Sdk" object.

The "Sdk" provides two crucial clients - a transaction client for signing and broadcasting transactions,
and a query client for sending gRPC queries. The functionalities offered by the "Sdk" are highly dependent
on the user's network and transaction configurations.

To configure the "Sdk" object, users can utilize the Network and TxConfig classes provided by the
osmosispy/pytypes package. These classes ensure seamless integration and optimized performance with
the desired network and transaction settings.
"""
import logging
from .pytypes import Network, TxConfig
from .grpc_client import GrpcClient
from .tx import TxClient
from .wallet import PrivateKey


class Sdk:
    """
    The Sdk class acts as an intermediary that facilitates the signing and sending of transactions or
    query execution from a node.

    It is associated with several crucial components, including a wallet or signer that can either be
    newly generated or recovered from an existing mnemonic. Additionally, the network that the node will
    connect to and an optional configuration defining how to behave and the gas configuration for each
    transaction are specified.

    Any method that starts with with_ will replace the existing Sdk object with a new version that has
    the defined behavior. This approach ensures flexibility and allows users to customize the Sdk object
    to suit their specific requirements.

    The Sdk class has the following essential attributes: priv_key, query, tx, network, and tx_config.

    Here's an example of how to use the Sdk class to create a new object with specific configurations:

    ```python
    sdk = (
        Sdk.authorize(val_mnemonic)
        .with_config(tx_config)
        .with_network(network)
    )
    ```

    By leveraging this code snippet, you can authorize a new Sdk object,
    configure it with a specific tx_config and network,
    and use it to execute your desired transactions or queries.
    """

    query: GrpcClient
    network: Network
    tx: TxClient
    tx_config: TxConfig
    mnemonic: str

    def __init__(self, _error_do_not_use_init_directly=None) -> None:
        """Unsupported, please use from_mnemonic to initialize."""
        if not _error_do_not_use_init_directly:
            raise TypeError(
                "Please use PrivateKey.from_mnemonic() to construct me")
        self.priv_key: PrivateKey = None
        self.query = None
        self.tx = None
        self.network = None
        self.tx_config = TxConfig()

    @classmethod
    def authorize(cls, key: str = None) -> "Sdk":
        """
        The Authorize method enables users to generate or recover a wallet and register it as an Sdk object.
        In the case of wallet recovery, users need to provide the mnemonic phrase via the key argument
        If the key argument is not provided, a new wallet is created automatically.

        Args:
            key (str, optional): The mnemonic phrase to recover the wallet. Ceating a new wallet if not provided.

        Returns:
            Sdk: The updated sdk object, which includes the registered wallet.

        By leveraging this method, users can quickly and efficiently generate or recover a wallet and register
        it as an Sdk object.
        """
        self = cls(_error_do_not_use_init_directly=True)
        if key is None:
            (mnemonic, pk) = PrivateKey.generate()
            logging.warning(
                "The mnemonic used for the newly generated key is: \n%s", mnemonic
            )
            logging.warning(
                "Please write down this key, it will NOT be recoverable otherwise"
            )
        elif len(key.split(" ")) > 1:
            pk = PrivateKey.from_mnemonic(key)
        elif len(key) > 0:
            pk = PrivateKey.from_hex(key)

        self._with_priv_key(pk)
        self.mnemonic = mnemonic if key is None else key

        return self

    def with_network(
        self, network: Network
    ) -> "Sdk":
        """
        `with_network` method allows users to modify the network configuration of the Sdk object to connect to a specified network.

        Args:
            network (Network): A network object that specifies the desired network configuration.

        Returns:
            Sdk: The updated sdk object with the new network configuration.

        By utilizing this method, users can seamlessly switch between different networks and enjoy optimal performance and security.
        """
        self.network = network
        self._with_query_client(
            GrpcClient(network, True)
        )
        return self

    def with_config(self, config: TxConfig) -> "Sdk":
        """
        Change the configuration for trasnactions for the sdk to the specified config.

        Args:
            config (TxConfig): A transaction configuration object

        Returns:
            Sdk: The updated sdk object
        """
        self.tx_config = config
        tx_client = TxClient(
            client=self.query,
            network=self.network,
            priv_key=self.priv_key,
            config=self.tx_config,
        )
        self._with_tx_client(tx_client)
        return self

    @property
    def address(self) -> str:
        """
        Public address of the wallet.

        Returns:
            str: The public address of the wallet
        """
        pub_key = self.priv_key.to_public_key()
        return pub_key.to_address().to_acc_bech32()

    # Private methods
    def _with_query_client(self, client: GrpcClient) -> "Sdk":
        self.query = client
        tx_client = TxClient(
            client=self.query,
            network=self.network,
            priv_key=self.priv_key,
            config=self.tx_config,
        )
        self._with_tx_client(tx_client)
        return self

    def _with_tx_client(self, tx_client: TxClient) -> "Sdk":
        self.tx = tx_client
        return self

    def _with_priv_key(self, priv_key: PrivateKey) -> "Sdk":
        self.priv_key = priv_key
        return self
