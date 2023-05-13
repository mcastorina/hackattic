import recast
import requests
import base64
import os

CHALLENGE = 'help_me_unpack'
HACK_ATTIC = f'https://hackattic.com/challenges/{CHALLENGE}'
TOKEN = os.environ['TOKEN']


def get_challenge(**kwargs):
    kwargs['access_token'] = TOKEN
    return requests.get(f'{HACK_ATTIC}/problem', params=kwargs).json()


def solve(j, **kwargs):
    kwargs['access_token'] = TOKEN
    return requests.post(f'{HACK_ATTIC}/solve', params=kwargs, json=j).json()


raw_bytes = base64.b64decode(get_challenge()['bytes'])
v1 = recast.bytes2int(raw_bytes[0:4])
v2 = recast.bytes2uint(raw_bytes[4:8])
v3 = recast.bytes2short(raw_bytes[8:10])
v4 = recast.bytes2float(raw_bytes[12:16])
v5 = recast.bytes2double(raw_bytes[16:24])
v6 = recast.bytes2double(raw_bytes[24:32], byteorder='big')
payload = {'int': v1, 'uint': v2, 'short': v3,
           'float': v4, 'double': v5, 'big_endian_double': v6}
print(solve(payload, playground=1))
