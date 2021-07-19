"""
Ethereum Logs Bloom
^^^^^^^^^^^^^^^^^^^

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Logs Bloom related functionalities used in Ethereum.
"""

from typing import List

from ethereum.base_types import Uint
from ethereum.crypto import keccak256

from .eth_types import Bloom, Log


def add_to_bloom(bloom: Bloom, bloom_entry: bytes) -> Bloom:
    """
    Add a bloom entry to the bloom filter (`bloom`).

    Parameters
    ----------
    bloom :
        The bloom filter.
    bloom_entry :
        An entry which is to be added to bloom filter.

    Returns
    -------
    logs_bloom : `Bloom` or `Bytearray256`
        The logs bloom obtained which is 256 bytes with some bits set as per
        the bloom entry.
    """
    # TODO: This functionality hasn't been tested rigorously yet.
    hash = keccak256(bloom_entry)

    for idx in (0, 2, 4):
        # Obtain the least significant 11 bits from the pair of bytes
        # (16 bits), and set this bit in bloom bytearray.
        # The obtained bit is 0-indexed in the bloom filter from the least
        # significant bit to the most significant bit.
        bit_to_set = Uint.from_be_bytes(hash[idx : idx + 2]) & 2047
        # Below is the index of the bit in the bytearray (where 0-indexed
        # byte is the most significant byte)
        bit_index = 2047 - bit_to_set

        byte_index = bit_index // 8
        bit_value = 1 << (7 - (bit_index % 8))
        bloom[byte_index] = bloom[byte_index] | bit_value

    return bloom


def logs_bloom(logs: List[Log]) -> Bloom:
    """
    Obtain the logs bloom from a list of log entries.

    Parameters
    ----------
    logs :
        List of logs for which the logs bloom is to be obtained.

    Returns
    -------
    logs_bloom : `Bloom` or `Bytearray256`
        The logs bloom obtained which is 256 bytes with some bits set as per
        the caller address and the log topics.
    """
    # TODO: Logs bloom functionality hasn't been tested rigorously yet. The
    # required test cases need `CALL` opcode to be implemented.
    bloom: Bloom = bytearray(b"\x00" * 256)

    for log in logs:
        bloom = add_to_bloom(bloom, log.address)
        for topic in log.topics:
            bloom = add_to_bloom(bloom, topic)

    return bloom
