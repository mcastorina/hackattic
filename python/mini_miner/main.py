import requests
import hashlib
import json
import os

CHALLENGE = 'mini_miner'
HACK_ATTIC = f'https://hackattic.com/challenges/{CHALLENGE}'
TOKEN = os.environ['TOKEN']


def get_challenge(**kwargs):
    kwargs['access_token'] = TOKEN
    return requests.get(f'{HACK_ATTIC}/problem', params=kwargs).json()


def solve(j, **kwargs):
    kwargs['access_token'] = TOKEN
    return requests.post(f'{HACK_ATTIC}/solve', params=kwargs, json=j).json()


def hash(j):
    s = json.dumps(j, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(s.encode()).digest()


def leading_zero_bits(byte_string):
    def leading_bits(b):
        for shift in range(9):
            mask = ~((1 << shift) - 1)
            if b & mask == 0:
                return 8 - shift
        return 0
    count = 0
    for b in byte_string:
        c = leading_bits(b)
        count += c
        if c != 8:
            break
    return count


challenge = get_challenge()
difficulty = challenge['difficulty']
block = challenge['block']

nonce = -1
while leading_zero_bits(hash(block)) < difficulty:
    nonce += 1
    block['nonce'] = nonce

print(solve({'nonce': nonce}, playground=1))
