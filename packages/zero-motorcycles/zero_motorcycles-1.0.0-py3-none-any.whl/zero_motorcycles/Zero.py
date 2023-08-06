# SPDX-FileCopyrightText: 2023-present Matt Zuba <matt.zuba@gmail.com>
#
# SPDX-License-Identifier: BSD-3-clause
import base64
from hashlib import md5
import json
import requests.auth
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes


class Zero:
    API_URL = 'https://api-us-cypherstore-prod.zeromotorcycles.com/starcom/v1'

    def __init__(self, username, password):
        self.auth = ZeroAuth(username, password)
        pass

    def get_units(self):
        data = {
            "commandname": "get_units"
        }

        return self._make_request(data).json()

    def get_last_transmit(self, unit):
        data = {
            "unitnumber": unit,
            "commandname": "get_last_transmit"
        }

        return self._make_request(data).json()

    def get_expiration_date(self, unit):
        data = {
            "unitnumber": unit,
            "unittype": 5,
            "commandname": "get_expiration_date"
        }

        return self._make_request(data).json()

    def _make_request(self, data):
        return requests.post(self.API_URL, json=data, auth=self.auth, headers={"User-Agent": "ZeroMoto/1.0"})


class ZeroAuth(requests.auth.AuthBase):
    ENCRYPTION_KEY = "8FA043AADEC92367108D0E25D2C6064F"
    SOURCE = "zero"
    FORMAT = "json"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        return all(
            [
                self.username == getattr(other, "username", None),
                self.password == getattr(other, "password", None),
            ]
        )

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        # Decode and turn the body back into JSON so we can edit it
        data = json.loads(r.body.decode())

        # Add some additional keys to the JSON body
        data["format"] = self.FORMAT
        data["source"] = self.SOURCE
        data["user"] = self.username
        data["pass"] = self.password

        # Encrypt the payload
        encrypted = self._encrypt(json.dumps(data).encode())

        # Set the request body to our newly encrypted value
        r.body = json.dumps({"data": encrypted}).encode()

        return r

    def _encrypt(self, message):
        # from https://stackoverflow.com/a/36780727
        salt = get_random_bytes(8)
        key_iv = self._bytes_to_key(self.ENCRYPTION_KEY.encode(), salt)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message, AES.block_size))).decode()

    @staticmethod
    def _bytes_to_key(data, salt, output=48):
        # from https://stackoverflow.com/a/36780727
        # extended from https://gist.github.com/gsakkis/4546068
        assert len(salt) == 8, len(salt)
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]
