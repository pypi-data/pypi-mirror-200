"""The Roborock api."""

from __future__ import annotations

import asyncio
import base64
import binascii
import hashlib
import hmac
import json
import logging
import math
import secrets
import struct
import time
from typing import Any

import aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from roborock.exceptions import (
    RoborockException,
)
from .code_mappings import WASH_MODE_MAP, DUST_COLLECTION_MAP, RoborockDockType, \
    RoborockDockDustCollectionType, RoborockDockWashingModeType
from .containers import (
    UserData,
    HomeDataDevice,
    Status,
    CleanSummary,
    Consumable,
    DNDTimer,
    CleanRecord,
    HomeData,
    MultiMapsList,
    SmartWashParameters,

)
from .typing import (
    RoborockDeviceProp,
    RoborockCommand,
    RoborockDockSummary,
)

_LOGGER = logging.getLogger(__name__)
QUEUE_TIMEOUT = 4
MQTT_KEEPALIVE = 60


def md5hex(message: str) -> str:
    md5 = hashlib.md5()
    md5.update(message.encode())
    return md5.hexdigest()


def md5bin(message: str) -> bytes:
    md5 = hashlib.md5()
    md5.update(message.encode())
    return md5.digest()


def encode_timestamp(_timestamp: int) -> str:
    hex_value = f"{_timestamp:x}".zfill(8)
    return "".join(list(map(lambda idx: hex_value[idx], [5, 6, 3, 7, 1, 2, 0, 4])))


class PreparedRequest:
    def __init__(self, base_url: str, base_headers: dict = None) -> None:
        self.base_url = base_url
        self.base_headers = base_headers or {}

    async def request(
            self, method: str, url: str, params=None, data=None, headers=None
    ) -> dict | list:
        _url = "/".join(s.strip("/") for s in [self.base_url, url])
        _headers = {**self.base_headers, **(headers or {})}
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method,
                    _url,
                    params=params,
                    data=data,
                    headers=_headers,
            ) as resp:
                return await resp.json()


class RoborockClient():

    def __init__(self, endpoint: str, device_localkey: dict[str, str], prefixed=False) -> None:
        self.device_localkey = device_localkey
        self._seq = 1
        self._random = 4711
        self._id_counter = 10000
        self._salt = "TXdfu$jyZ#TZHsg4"
        self._endpoint = base64.b64encode(md5bin(endpoint)[8:14]).decode()
        self._nonce = secrets.token_bytes(16)
        self._prefixed = prefixed

    def _decode_msg(self, msg: bytes, local_key: str) -> dict[str, Any]:
        if self._prefixed:
            msg = msg[4:]
        if msg[0:3] != "1.0".encode():
            raise RoborockException("Unknown protocol version")
        if len(msg) == 17:
            [version, _seq, _random, timestamp, protocol] = struct.unpack(
                "!3sIIIH", msg[0:17]
            )
            return {
                "version": version,
                "timestamp": timestamp,
                "protocol": protocol,
            }
        crc32 = binascii.crc32(msg[0: len(msg) - 4])
        [version, _seq, _random, timestamp, protocol, payload_len] = struct.unpack(
            "!3sIIIHH", msg[0:19]
        )
        [payload, expected_crc32] = struct.unpack_from(f"!{payload_len}sI", msg, 19)
        if crc32 != expected_crc32:
            raise RoborockException(f"Wrong CRC32 {crc32}, expected {expected_crc32}")

        aes_key = md5bin(encode_timestamp(timestamp) + local_key + self._salt)
        decipher = AES.new(aes_key, AES.MODE_ECB)
        decrypted_payload = unpad(decipher.decrypt(payload), AES.block_size)
        return {
            "version": version,
            "timestamp": timestamp,
            "protocol": protocol,
            "payload": decrypted_payload,
        }

    def _get_msg_raw(self, device_id, protocol, timestamp, payload, prefix='') -> bytes:
        local_key = self.device_localkey[device_id]
        aes_key = md5bin(encode_timestamp(timestamp) + local_key + self._salt)
        cipher = AES.new(aes_key, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(payload, AES.block_size))
        encrypted_len = len(encrypted)
        values = [
            "1.0".encode(),
            self._seq,
            self._random,
            timestamp,
            protocol,
            encrypted_len,
            encrypted
        ]
        if self._prefixed:
            values = [prefix] + values
        msg = struct.pack(
            f"!{'I' if self._prefixed else ''}3sIIIHH{encrypted_len}s",
            *values
        )
        crc32 = binascii.crc32(msg[4:] if self._prefixed else msg)
        msg += struct.pack("!I", crc32)
        return msg

    def _get_payload(
            self, method: RoborockCommand, params: list = None
    ):
        timestamp = 1680196427
        request_id = self._id_counter
        self._id_counter += 1
        inner = {
            "id": request_id,
            "method": method,
            "params": params or [],
            "security": {
                "endpoint": self._endpoint,
                "nonce": self._nonce.hex().upper(),
            },
        }
        payload = bytes(
            json.dumps(
                {
                    "t": timestamp,
                    "dps": {"101": json.dumps(inner, separators=(",", ":"))},
                },
                separators=(",", ":"),
            ).encode()
        )
        return request_id, timestamp, payload

    async def send_command(
            self, device_id: str, method: RoborockCommand, params: list = None
    ):
        raise NotImplementedError

    async def get_status(self, device_id: str) -> Status:
        status = await self.send_command(device_id, RoborockCommand.GET_STATUS)
        if isinstance(status, dict):
            return Status(status)

    async def get_dnd_timer(self, device_id: str) -> DNDTimer:
        dnd_timer = await self.send_command(device_id, RoborockCommand.GET_DND_TIMER)
        if isinstance(dnd_timer, dict):
            return DNDTimer(dnd_timer)

    async def get_clean_summary(self, device_id: str) -> CleanSummary:
        clean_summary = await self.send_command(
            device_id, RoborockCommand.GET_CLEAN_SUMMARY
        )
        if isinstance(clean_summary, dict):
            return CleanSummary(clean_summary)
        elif isinstance(clean_summary, bytes):
            return CleanSummary({"clean_time": clean_summary})

    async def get_clean_record(self, device_id: str, record_id: int) -> CleanRecord:
        clean_record = await self.send_command(
            device_id, RoborockCommand.GET_CLEAN_RECORD, [record_id]
        )
        if isinstance(clean_record, dict):
            return CleanRecord(clean_record)

    async def get_consumable(self, device_id: str) -> Consumable:
        consumable = await self.send_command(device_id, RoborockCommand.GET_CONSUMABLE)
        if isinstance(consumable, dict):
            return Consumable(consumable)

    async def get_washing_mode(self, device_id: str) -> RoborockDockWashingModeType:
        washing_mode = await self.send_command(device_id, RoborockCommand.GET_WASH_TOWEL_MODE)
        return WASH_MODE_MAP.get(washing_mode['wash_mode'])

    async def get_dust_collection_mode(self, device_id: str) -> RoborockDockDustCollectionType:
        dust_collection = await self.send_command(device_id, RoborockCommand.GET_DUST_COLLECTION_MODE)
        return DUST_COLLECTION_MAP.get(dust_collection['mode'])

    async def get_mop_wash_mode(self, device_id: str) -> SmartWashParameters:
        mop_wash_mode = await self.send_command(device_id, RoborockCommand.GET_SMART_WASH_PARAMS)
        if isinstance(mop_wash_mode, dict):
            return SmartWashParameters(mop_wash_mode)

    async def get_dock_summary(self, device_id: str, dock_type: RoborockDockType) -> RoborockDockSummary:
        collection_mode = await self.get_dust_collection_mode(device_id)
        mop_wash = None
        washing_mode = None
        if dock_type == RoborockDockType.EMPTY_WASH_FILL_DOCK:
            [mop_wash, washing_mode] = await asyncio.gather(
                *[self.get_mop_wash_mode(device_id), self.get_washing_mode(device_id)])

        return RoborockDockSummary(collection_mode, washing_mode, mop_wash)

    async def get_prop(self, device_id: str) -> RoborockDeviceProp:
        [status, dnd_timer, clean_summary, consumable] = await asyncio.gather(
            *[
                self.get_status(device_id),
                self.get_dnd_timer(device_id),
                self.get_clean_summary(device_id),
                self.get_consumable(device_id),
            ]
        )
        last_clean_record = None
        if clean_summary and clean_summary.records and len(clean_summary.records) > 0:
            last_clean_record = await self.get_clean_record(
                device_id, clean_summary.records[0]
            )
        dock_summary = None
        if status.dock_type != RoborockDockType.NO_DOCK:
            dock_summary = await self.get_dock_summary(device_id, status.dock_type)
        if any([status, dnd_timer, clean_summary, consumable]):
            return RoborockDeviceProp(
                status, dnd_timer, clean_summary, consumable, last_clean_record, dock_summary
            )

    async def get_multi_maps_list(self, device_id) -> MultiMapsList:
        multi_maps_list = await self.send_command(
            device_id, RoborockCommand.GET_MULTI_MAPS_LIST
        )
        if isinstance(multi_maps_list, dict):
            return MultiMapsList(multi_maps_list)

    async def get_map_v1(self, device_id):
        return await self.send_command(device_id, RoborockCommand.GET_MAP_V1)


class RoborockApiClient:
    def __init__(self, username: str, base_url=None) -> None:
        """Sample API Client."""
        self._username = username
        self._default_url = "https://euiot.roborock.com"
        self.base_url = base_url
        self._device_identifier = secrets.token_urlsafe(16)

    async def _get_base_url(self) -> str:
        if not self.base_url:
            url_request = PreparedRequest(self._default_url)
            response = await url_request.request(
                "post",
                "/api/v1/getUrlByEmail",
                params={"email": self._username, "needtwostepauth": "false"},
            )
            if response.get("code") != 200:
                raise RoborockException(response.get("error"))
            self.base_url = response.get("data").get("url")
        return self.base_url

    def _get_header_client_id(self):
        md5 = hashlib.md5()
        md5.update(self._username.encode())
        md5.update(self._device_identifier.encode())
        return base64.b64encode(md5.digest()).decode()

    async def request_code(self) -> None:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()
        code_request = PreparedRequest(base_url, {"header_clientid": header_clientid})

        code_response = await code_request.request(
            "post",
            "/api/v1/sendEmailCode",
            params={
                "username": self._username,
                "type": "auth",
            },
        )

        if code_response.get("code") != 200:
            raise RoborockException(code_response.get("msg"))

    async def pass_login(self, password: str) -> UserData:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()

        login_request = PreparedRequest(base_url, {"header_clientid": header_clientid})
        login_response = await login_request.request(
            "post",
            "/api/v1/login",
            params={
                "username": self._username,
                "password": password,
                "needtwostepauth": "false",
            },
        )

        if login_response.get("code") != 200:
            raise RoborockException(login_response.get("msg"))
        return UserData(login_response.get("data"))

    async def code_login(self, code) -> UserData:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()

        login_request = PreparedRequest(base_url, {"header_clientid": header_clientid})
        login_response = await login_request.request(
            "post",
            "/api/v1/loginWithCode",
            params={
                "username": self._username,
                "verifycode": code,
                "verifycodetype": "AUTH_EMAIL_CODE",
            },
        )

        if login_response.get("code") != 200:
            raise RoborockException(login_response.get("msg"))
        return UserData(login_response.get("data"))

    async def get_home_data(self, user_data: UserData) -> HomeData:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()
        rriot = user_data.rriot
        home_id_request = PreparedRequest(
            base_url, {"header_clientid": header_clientid}
        )
        home_id_response = await home_id_request.request(
            "get",
            "/api/v1/getHomeDetail",
            headers={"Authorization": user_data.token},
        )
        if home_id_response.get("code") != 200:
            raise RoborockException(home_id_response.get("msg"))
        home_id = home_id_response.get("data").get("rrHomeId")
        timestamp = math.floor(time.time())
        nonce = secrets.token_urlsafe(6)
        prestr = ":".join(
            [
                rriot.user,
                rriot.password,
                nonce,
                str(timestamp),
                hashlib.md5(("/user/homes/" + str(home_id)).encode()).hexdigest(),
                "",
                "",
            ]
        )
        mac = base64.b64encode(
            hmac.new(rriot.h_unknown.encode(), prestr.encode(), hashlib.sha256).digest()
        ).decode()
        home_request = PreparedRequest(
            rriot.reference.api,
            {
                "Authorization": f'Hawk id="{rriot.user}", s="{rriot.password}", ts="{timestamp}", nonce="{nonce}", '
                                 f'mac="{mac}"',
            },
        )
        home_response = await home_request.request("get", "/user/homes/" + str(home_id))
        if not home_response.get("success"):
            raise RoborockException(home_response)
        home_data = home_response.get("result")
        return HomeData(home_data)
