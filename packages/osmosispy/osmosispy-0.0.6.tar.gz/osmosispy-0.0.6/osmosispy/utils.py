from google.protobuf import message
from typing import Dict, List, Optional, Union
import collections
from typing import Any,  Dict, Iterable, List, Optional, Union
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf import any_pb2
from osmosis_proto.proto.osmosis.gamm.pool_models.stableswap import stableswap_pool_pb2
from osmosis_proto.proto.osmosis.gamm.pool_models.balancer import balancerPool_pb2

# number of decimal places
PRECISION = 18


def from_sdk_dec(dec_str: str) -> float:
    if dec_str is None or dec_str == '':
        return 0

    if '.' in dec_str:
        raise TypeError(
            f'expected a decimal string but got {dec_str} containing \'.\'')

    try:
        int(dec_str)
    except ValueError as err:
        raise ValueError(f'failed to convert {dec_str} to a number') from err

    neg = False
    if dec_str[0] == '-':
        neg = True
        dec_str = dec_str[1:]

    input_size = len(dec_str)
    bz_str = ''
    # case 1, purely decimal
    if input_size <= PRECISION:
        # 0. prefix
        bz_str = '0.'

        # set relevant digits to 0
        bz_str += '0' * (PRECISION - input_size)

        # set final digits
        bz_str += dec_str
    else:
        # inputSize + 1 to account for the decimal point that is being added
        dec_point_place = input_size - PRECISION

        bz_str = dec_str[:dec_point_place]  # pre-decimal digits
        bz_str += '.'  # decimal point
        bz_str += dec_str[dec_point_place:]  # pre-decimal digits

    if neg:
        bz_str = '-' + bz_str

    return float(bz_str)


def from_sdk_int(int_str: str) -> int:
    return int(int_str)


def dict_keys_must_match(dict_: dict, keys: List[str]):
    """Asserts that two iterables have the same elements, the same number of
    times, without regard to order.
    Alias for the 'element_counts_are_equal' function.

    dict_keys_must_match(dict_, keys)

    Example:
    - [0, 1, 1] and [1, 0, 1] compare equal.
    - [0, 0, 1] and [0, 1] compare unequal.

    """
    assert element_counts_are_equal(dict_.keys(), keys)


def element_counts_are_equal(
    first: Iterable[Any], second: Iterable[Any]
) -> Optional[bool]:
    """Asserts that two iterables have the same elements, the same number of
    times, without regard to order.

    Args:
        first (Iterable[Any])
        second (Iterable[Any])

    Returns:
        Optional[bool]: "passed" status. If this is True, first and second share
            the same element counts. If they don't the function will raise an
            AssertionError and return 'None'.
    """
    first_seq, second_seq = list(first), list(second)

    passed: Union[bool, None]
    try:
        first = collections.Counter(first_seq)
        second = collections.Counter(second_seq)
    except TypeError:
        # Handle case with unhashable elements
        differences = _count_diff_all_purpose(first_seq, second_seq)
    else:
        if first == second:
            passed = True
            return passed
        differences = _count_diff_hashable(first_seq, second_seq)

    if differences:
        standardMsg = "Element counts were not equal:\n"
        lines = ["First has %d, Second has %d:  %r" %
                 diff for diff in differences]
        diffMsg = "\n".join(lines)
        msg = "\n".join([standardMsg, diffMsg])
        passed = False
        assert passed, msg


_Mismatch = collections.namedtuple("Mismatch", "actual expected value")


def _count_diff_all_purpose(actual, expected):
    "Returns list of (cnt_act, cnt_exp, elem) triples where the counts differ"
    # elements need not be hashable
    s, t = list(actual), list(expected)
    m, n = len(s), len(t)
    NULL = object()
    result = []
    for i, elem in enumerate(s):
        if elem is NULL:
            continue
        cnt_s = cnt_t = 0
        for j in range(i, m):
            if s[j] == elem:
                cnt_s += 1
                s[j] = NULL
        for j, other_elem in enumerate(t):
            if other_elem == elem:
                cnt_t += 1
                t[j] = NULL
        if cnt_s != cnt_t:
            diff = _Mismatch(cnt_s, cnt_t, elem)
            result.append(diff)

    for i, elem in enumerate(t):
        if elem is NULL:
            continue
        cnt_t = 0
        for j in range(i, n):
            if t[j] == elem:
                cnt_t += 1
                t[j] = NULL
        diff = _Mismatch(0, cnt_t, elem)
        result.append(diff)
    return result


def _count_diff_hashable(actual, expected):
    "Returns list of (cnt_act, cnt_exp, elem) triples where the counts differ"
    # elements must be hashable
    s, t = collections.Counter(actual), collections.Counter(expected)
    result = []
    for elem, cnt_s in s.items():
        cnt_t = t.get(elem, 0)
        if cnt_s != cnt_t:
            diff = _Mismatch(cnt_s, cnt_t, elem)
            result.append(diff)
    for elem, cnt_t in t.items():
        if elem not in s:
            diff = _Mismatch(0, cnt_t, elem)
            result.append(diff)
    return result


PROTOBUF_MSG_BASE_ATTRS: List[str] = (
    dir(message.Message)
    + ['Extensions', 'FindInitializationErrors', '_CheckCalledFromGeneratedFile']
    + ['_extensions_by_name', '_extensions_by_number']
)
"""PROTOBUF_MSG_BASE_ATTRS (List[str]): The default attributes and methods of
an instance of the 'protobuf.message.Message' class.
"""


def camel_to_snake(camel: str):
    return ''.join(
        ['_' + char.lower() if char.isupper() else char for char in camel]
    ).lstrip('_')


def dict_keys_from_camel_to_snake(d):
    """
    Transform all keys from the dictionary from camelcase to snake case.

    Args:
        d (dict): The dictionary to transform

    Returns:
        dict: The dictionary transformed
    """
    if isinstance(d, list):
        return [
            dict_keys_from_camel_to_snake(
                i) if isinstance(i, (dict, list)) else i
            for i in d
        ]
    return {
        camel_to_snake(a): dict_keys_from_camel_to_snake(b)
        if isinstance(b, (dict, list))
        else b
        for a, b in d.items()
    }


def deserialize(pb_msg: message.Message, no_sdk_transformation: bool = False) -> dict:
    """Deserializes a proto message into a dictionary.

    - sdk.Dec values are converted to floats.
    - sdk.Int values are converted to ints.
    - Missing fields become blank strings.

    Args:
        pb_msg (protobuf.message.Message)
        no_sdk_transformation (bool): Wether to bypass the sdk transformation. Default to False

    Returns:
        dict: 'pb_msg' as a JSON-able dictionary.
    """

    if isinstance(pb_msg, any_pb2.Any):
        return pb_msg

    if not isinstance(pb_msg, message.Message):
        return pb_msg

    custom_dtypes: Dict[str, bytes] = {
        str(field[1]): field[0].GetOptions().__getstate__().get("serialized", None)
        for field in pb_msg.ListFields()
    }
    serialized_output = {}
    expected_fields: List[str] = list(pb_msg.DESCRIPTOR.fields_by_name.keys())

    for _, attr in enumerate(expected_fields):
        attr_search = pb_msg.__getattribute__(attr)
        custom_dtype = custom_dtypes.get(str(attr_search))

        if custom_dtype is not None:
            if "sdk/types.Dec" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = float(
                        pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = from_sdk_dec(
                        pb_msg.__getattribute__(attr)
                    )
            elif "sdk/types.Int" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = int(
                        pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = from_sdk_int(
                        pb_msg.__getattribute__(attr)
                    )
            elif "Int" in str(custom_dtype):  # Used for sdk.Coin message normalization
                serialized_output[str(attr)] = int(
                    pb_msg.__getattribute__(attr))
            else:
                val = pb_msg.__getattribute__(attr)
                if hasattr(val, '__len__') and not isinstance(val, str):
                    updated_vals = []
                    for v in val:
                        updated_vals.append(deserialize(v))
                    serialized_output[str(attr)] = updated_vals
                else:
                    serialized_output[str(attr)] = deserialize(val)
        elif custom_dtype is None and not attr_search:
            if str(attr_search) == "[]":
                serialized_output[str(attr)] = []
            else:
                serialized_output[str(attr)] = attr_search
        else:
            serialized_output[str(attr)] = deserialize(
                pb_msg.__getattribute__(attr))

    return serialized_output


def deserialize_pool(pool: any_pb2.Any):
    """
    Deserialize different pool types from Any type

    TODO: make this more generic and automate the process
    """
    if pool.Is(stableswap_pool_pb2.Pool.DESCRIPTOR):
        pool_obj = stableswap_pool_pb2.Pool()
    elif pool.Is(balancerPool_pb2.Pool.DESCRIPTOR):
        pool_obj = balancerPool_pb2.Pool()
    else:
        raise ValueError("Unknown pool type", pool.type_url)

    pool_obj.ParseFromString(pool.value)
    return deserialize(pool_obj)
