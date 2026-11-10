#!/bin/python
import hashlib
import os
import random


def mine_block(k, prev_hash, transactions):
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'

    block_hash = hashlib.sha256()
    block_hash.update(prev_hash)

    for transaction in transactions:
        block_hash.update(transaction.encode())

    mask = (1 << k) - 1
    counter = 0

    while True:
        nonce = str(counter).encode()

        candidate_hash = block_hash.copy()
        candidate_hash.update(nonce)

        digest = candidate_hash.digest()

        if int.from_bytes(digest, byteorder='big') & mask == 0:
            break

        counter += 1

    assert isinstance(nonce, bytes)
    return nonce


def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given. 
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())

    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines


if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take to long
    diff = 20

    transactions = get_random_lines(filename, num_lines)
    nonce = mine_block(diff, transactions)
    print(nonce)
