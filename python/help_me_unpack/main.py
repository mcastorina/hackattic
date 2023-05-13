import recast
import requests
import base64
import os

challenge = 'https://hackattic.com/challenges/help_me_unpack'
token = os.environ['TOKEN']

req = requests.get(f'{challenge}/problem?access_token={token}').json()['bytes']
raw_bytes = base64.b64decode(req)
v1 = recast.bytes2int(raw_bytes[0:4])
v2 = recast.bytes2uint(raw_bytes[4:8])
v3 = recast.bytes2short(raw_bytes[8:10])
v4 = recast.bytes2float(raw_bytes[12:16])
v5 = recast.bytes2double(raw_bytes[16:24])
v6 = recast.bytes2double(raw_bytes[24:32], byteorder='big')
payload = {'int': v1, 'uint': v2, 'short': v3,
           'float': v4, 'double': v5, 'big_endian_double': v6}
result = requests.post(
    f'{challenge}/solve?access_token={token}&playground=1', json=payload).json()

print(result)
