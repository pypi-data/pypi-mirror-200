"""
Classes:
    TxClient: A client for building, simulating, and broadcasting transactions.
    Transaction: Transactions trigger state changes based on messages. Each message
        must be cryptographically signed before being broadcasted to the network.
"""
import json
import logging
from copy import deepcopy
from numbers import Number
from typing import Any, Callable, Iterable, List, Tuple, Union

from google.protobuf import any_pb2, message
from google.protobuf.json_format import MessageToDict
from osmosis_proto.proto.cosmos.base.abci.v1beta1 import abci_pb2 as abci_type
from osmosis_proto.proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from osmosis_proto.proto.cosmos.base.v1beta1.coin_pb2 import Coin
from osmosis_proto.proto.cosmos.tx.signing.v1beta1 import signing_pb2 as tx_sign
from osmosis_proto.proto.cosmos.tx.v1beta1 import tx_pb2 as cosmos_tx_type

from osmosispy import pytypes as pt
from osmosispy import wallet
from osmosispy.exceptions import SimulationError, TxError
from osmosispy.grpc_client import GrpcClient


class TxClient:
    """
    The `TxClient` ia s class provided by the SDK to allow developers to build,
    simulate, and broadcast transactions on the blockchain.
    """

    def __init__(
        self,
        priv_key: wallet.PrivateKey,
        network: pt.Network,
        client: GrpcClient,
        config: pt.TxConfig,
    ):
        self.priv_key = priv_key
        self.network = network
        self.client = client
        self.address = None
        self.config = config

    def execute_tx(
        self, tx: "Transaction", gas_estimate: float, **kwargs
    ) -> abci_type.TxResponse:
        conf: pt.TxConfig = self.get_config(**kwargs)

        def compute_gas_wanted() -> float:
            # Related to https://github.com/cosmos/cosmos-sdk/issues/14405
            # TODO We should consider adding the behavior mentioned by tac0turtle.
            gas_wanted = gas_estimate * 1.25  # apply gas multiplier
            if conf.gas_wanted > 0:
                gas_wanted = conf.gas_wanted
            elif conf.gas_multiplier > 0:
                gas_wanted = gas_estimate * conf.gas_multiplier
            return gas_wanted

        gas_wanted = compute_gas_wanted()
        gas_price = pt.GAS_PRICE if conf.gas_price <= 0 else conf.gas_price

        fee = [
            cosmos_base_coin_pb.Coin(
                amount=str(int(gas_price * gas_wanted)),
            )
        ]
        logging.info(
            "Executing transaction with fee: %s and gas_wanted: %d", fee, gas_wanted
        )
        tx = (
            tx.with_gas_limit(gas_wanted)
            .with_fee(fee)
            .with_memo("")
            .with_timeout_height(self.client.timeout_height)
        )
        tx_raw_bytes = tx.get_signed_tx_data()

        return self._send_tx(tx_raw_bytes, conf.tx_type)

    def _send_tx(self, tx_raw_bytes: bytes, tx_type: pt.TxType) -> abci_type.TxResponse:
        broadcast_fn: Callable[[bytes], abci_type.TxResponse]

        if tx_type == pt.TxType.SYNC:
            broadcast_fn = self.client.send_tx_sync_mode
        elif tx_type == pt.TxType.ASYNC:
            broadcast_fn = self.client.send_tx_async_mode
        else:
            broadcast_fn = self.client.send_tx_block_mode

        return broadcast_fn(tx_raw_bytes)

    def build_tx(
        self,
        msgs: Union[pt.PythonMsg, List[pt.PythonMsg]],
        get_sequence_from_node: bool = False,
    ) -> Tuple["Transaction", wallet.Address]:
        if not isinstance(msgs, list):
            msgs = [msgs]

        pb_msgs = [msg.to_pb() for msg in msgs]

        self.client.sync_timeout_height()
        address: wallet.Address = self.get_address_info()
        sequence: int = address.get_sequence(
            from_node=get_sequence_from_node,
            lcd_endpoint=self.network.lcd_endpoint,
        )
        tx = (
            Transaction()
            .with_messages(pb_msgs)
            .with_sequence(sequence)
            .with_account_num(address.get_number())
            .with_chain_id(self.network.chain_id)
            .with_signer(self.priv_key)
        )
        return tx, address

    def simulate(self, tx: "Transaction") -> abci_type.SimulationResponse:
        """
        Simulate a transaction to estimate gas usage, validate the transaction parameters and determine if the transaction would be executed successfully.

        Args:
            tx (Transaction): The transaction object to be simulated.

        Returns:
            SimulationResponse: The simulation response, containing information about the simulated transaction.

        Raises:
            SimulationError: If there was an error while simulating the transaction.
        """
        sim_tx_raw_bytes: bytes = tx.get_signed_tx_data()

        sim_res: abci_type.SimulationResponse
        success: bool
        sim_res, success = self.client.simulate_tx(sim_tx_raw_bytes)
        if not success:
            raise SimulationError(sim_res)

        return sim_res

    def get_address_info(self) -> wallet.Address:
        """
        Get the address information of the account associated with the private key.

        Returns:
            Address: The address information of the account associated with the private key.
        """
        if self.address is None:
            pub_key: wallet.PublicKey = self.priv_key.to_public_key()
            self.address = pub_key.to_address()
            self.address = self.address.init_num_seq(self.network.lcd_endpoint)

        return self.address

    def get_config(self, **kwargs) -> pt.TxConfig:
        """
        Get the transaction configuration.

        Returns:
            TxConfig: The transaction configuration.
        """
        config: pt.TxConfig = deepcopy(self.config)
        prop_names = dir(config)
        for k, v in kwargs.items():
            if k in prop_names:
                setattr(config, k, v)
            else:
                logging.warning(
                    "%s is not a supported config property, ignoring", k)

        return config


class Transaction:
    """
    The state of a system changes when a `Transaction` is executed with one or
    more messages ('msgs'). In order for a message to be valid, it must be signed
    by an authorized account and then broadcasted to the network. Once the message
    is received by the network, it undergoes a validation process to ensure that
    it is secure and complies with the consensus rules of the network. Only after
    successful validation, it can be included in a block and added to the blockchain.

    Attributes:
        msgs (Tuple[Message]): The messages to be executed in the transaction.
        account_num (int): The number of the account in the state.
        sequence (int): Each transaction must have a unique sequence number
            that serves as a security measure to prevent replay attacks.
            The sequence number must be unique each time a transaction is
            broadcasted to the network.
        chain_id (str): The chain ID of the network.
        fee (List[Coin]): The fee to be paid for the transaction.
        gas_limit (int): The maximum amount of gas that can be used to execute
            the transaction.
        priv_key (wallet.PrivateKey): The private key of the account that will
            sign the transaction.
        memo (str): A note or description to be added to the transaction.
        timeout_height (int): The block height after which the transaction will
            be rejected.
    """

    def __init__(
        self,
        msgs: Tuple[message.Message, ...] = None,
        account_num: int = None,
        priv_key: wallet.PrivateKey = None,
        sequence: int = None,
        chain_id: str = None,
        fee: List[Coin] = None,
        gas_limit: int = 0,
        memo: str = "",
        timeout_height: int = 0,
    ):
        self.msgs = self.__convert_msgs(msgs) if msgs is not None else []
        self.account_num = account_num
        self.priv_key = priv_key
        self.sequence = sequence
        self.chain_id = chain_id
        self.fee = cosmos_tx_type.Fee(amount=fee, gas_limit=gas_limit)
        self.gas_limit = gas_limit
        self.memo = memo
        self.timeout_height = timeout_height

    @staticmethod
    def __convert_msgs(msgs: List[message.Message]) -> List[any_pb2.Any]:
        any_msgs: List[any_pb2.Any] = []
        for msg in msgs:
            any_msg = any_pb2.Any()
            any_msg.Pack(msg, type_url_prefix="")
            any_msgs.append(any_msg)
        return any_msgs

    def with_messages(self, msgs: Iterable[message.Message]) -> "Transaction":
        self.msgs.extend(self.__convert_msgs(msgs))
        return self

    def with_sender(self, client: GrpcClient, sender: str) -> "Transaction":
        if len(self.msgs) == 0:
            raise IndexError(
                "messsage is empty, please use with_messages at least 1 message"
            )
        account = client.get_account(sender)
        if account:
            self.account_num = account.account_number
            self.sequence = account.sequence
            return self
        raise KeyError("Account doesn't exist")

    def with_signer(self, priv_key: wallet.PrivateKey):
        self.priv_key = priv_key
        return self

    def with_account_num(self, account_num: int) -> "Transaction":
        self.account_num = account_num
        return self

    def with_sequence(self, sequence: int) -> "Transaction":
        self.sequence = sequence
        return self

    def with_chain_id(self, chain_id: str) -> "Transaction":
        self.chain_id = chain_id
        return self

    def with_fee(self, fee: List[Coin]) -> "Transaction":
        self.fee = cosmos_tx_type.Fee(amount=fee, gas_limit=self.fee.gas_limit)
        return self

    def with_gas_limit(self, gas: Number) -> "Transaction":
        self.fee.gas_limit = int(gas)
        return self

    def with_memo(self, memo: str) -> "Transaction":
        if len(memo) > pt.MAX_MEMO_CHARACTERS:
            raise ValueError("memo is too large")
        self.memo = memo
        return self

    def with_timeout_height(self, timeout_height: int) -> "Transaction":
        self.timeout_height = timeout_height
        return self

    def __generate_info(self, public_key: wallet.PublicKey = None) -> Tuple[str, str]:
        body = cosmos_tx_type.TxBody(
            messages=self.msgs, memo=self.memo, timeout_height=self.timeout_height
        )

        body_bytes = body.SerializeToString()
        mode_info = cosmos_tx_type.ModeInfo(
            single=cosmos_tx_type.ModeInfo.Single(
                mode=tx_sign.SIGN_MODE_DIRECT)
        )

        if public_key:
            any_public_key = any_pb2.Any()
            any_public_key.Pack(
                public_key.to_public_key_proto(), type_url_prefix="")
            signer_info = cosmos_tx_type.SignerInfo(
                mode_info=mode_info, sequence=self.sequence, public_key=any_public_key
            )
        else:
            signer_info = cosmos_tx_type.SignerInfo(
                mode_info=mode_info, sequence=self.sequence
            )

        auth_info = cosmos_tx_type.AuthInfo(
            signer_infos=[signer_info], fee=self.fee)
        auth_info_bytes = auth_info.SerializeToString()

        return body_bytes, auth_info_bytes

    def get_sign_doc(
        self, public_key: wallet.PublicKey = None
    ) -> cosmos_tx_type.SignDoc:
        if len(self.msgs) == 0:
            raise ValueError("message is empty")

        if self.account_num is None:
            raise RuntimeError("account_num should be defined")

        if self.sequence is None:
            raise RuntimeError("sequence should be defined")

        if self.chain_id is None:
            raise RuntimeError("chain_id should be defined")

        body_bytes, auth_info_bytes = self.__generate_info(public_key)

        return cosmos_tx_type.SignDoc(
            body_bytes=body_bytes,
            auth_info_bytes=auth_info_bytes,
            chain_id=self.chain_id,
            account_number=self.account_num,
        )

    def get_tx_data(
        self, signature: bytes, public_key: wallet.PublicKey = None
    ) -> bytes:
        body_bytes, auth_info_bytes = self.__generate_info(public_key)

        tx_raw = cosmos_tx_type.TxRaw(
            body_bytes=body_bytes,
            auth_info_bytes=auth_info_bytes,
            signatures=[signature],
        )
        return tx_raw.SerializeToString()

    def get_signed_tx_data(self) -> bytes:
        if self.priv_key is None:
            raise RuntimeError("priv_key should be defined")

        pub_key = self.priv_key.to_public_key()
        sign_doc = self.get_sign_doc(pub_key)
        sig = self.priv_key.sign(sign_doc.SerializeToString())
        return self.get_tx_data(sig, pub_key)
