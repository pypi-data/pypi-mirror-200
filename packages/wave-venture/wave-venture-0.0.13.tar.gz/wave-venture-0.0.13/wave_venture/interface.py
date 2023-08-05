import ssl
import json
import uuid
import typing
import urllib.parse

import tqdm
import loguru
import certifi
import requests
import websockets

from wave_venture import utils
from wave_venture import config
from wave_venture import serializer


class ServerError(Exception):
    pass


def _send(action, kwargs):
    response = requests.post(
        url=(config.url + "/" + action),
        json=kwargs,
        headers={"Authorization": f"Bearer {config.auth_token}"},
    )
    response.raise_for_status()
    body = response.json(object_hook=serializer.decoder)
    if body["error"]:
        if trace := body["error"].get("stack_trace"):
            loguru.logger.error(trace)
        raise ServerError(body["error"]["dev_message"])
    return body["result"]


async def _send_progress(action, kwargs, *, progress_title):
    url = urllib.parse.urlparse(config.url)
    secure = url.scheme == "https"
    scheme = "wss" if secure else "ws"
    url = url._replace(scheme=scheme)
    url = urllib.parse.urlunparse(url)

    request_uid = uuid.uuid4().hex
    ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    ssl_ctx = secure if secure else None
    headers = {"Authorization": f"Bearer {config.auth_token}"}

    connection = websockets.connect(
        uri=url,
        extra_headers=headers,
        ssl=ssl_ctx,
        max_size=config.websocket_max_size,
        max_queue=config.websocket_max_queue,
        read_limit=config.websocket_read_limit,
        write_limit=config.websocket_write_limit,
        close_timeout=config.websocket_close_timeout,
        ping_interval=config.websocket_ping_interval,
        ping_timeout=config.websocket_ping_timeout,
    )

    async with connection as ws:
        payload = json.dumps(
            {
                "uid": request_uid,
                "action": action,
                "kwargs": kwargs,
            },
        )
        await ws.send(payload)

        progress_bar = tqdm.tqdm(
            total=100,
            desc=progress_title,
            bar_format="{l_bar}{bar}",
        )
        while True:
            msg = await ws.recv()
            msg = json.loads(msg, object_hook=serializer.decoder)

            if msg["error"]:
                if trace := msg["error"].get("stack_trace"):
                    loguru.logger.error(trace)
                raise ServerError(msg["error"]["dev_message"])

            assert msg["uid"] == request_uid

            if (
                msg["result"] is not None
                and msg["result"].get("_type") == "progress"
            ):
                # progress_bar.set_description(msg["result"]["message"])
                update = (msg["result"]["progress"] * 100) - progress_bar.n
                progress_bar.update(int(update))
                yield msg["result"]
            else:
                progress_bar.set_description("complete")
                progress_bar.update(100 - progress_bar.n)
                break

        progress_bar.clear()
        progress_bar.close()

    yield msg["result"]


# @utils.assert_call_signature
def new(
    *,
    name: str,
    prescript: str = None,
    tags_pre: typing.List[str] = None,
) -> dict:
    result = _send(
        action="document.insert",
        kwargs={
            "name": name,
            "prescript": prescript,
            "tags_pre": tags_pre,
        },
    )
    return result["instance"]


def load(*, uid: str) -> dict:
    result = _send(
        action="document.select",
        kwargs={"uid": uid},
    )
    return result["instance"]


def clone(
    *,
    uid: str,
    name: str,
    prescript: str = None,
    tags_pre: typing.List[str] = None,
    trim_errors: bool = False,
) -> dict:
    result = _send(
        action="document.clone",
        kwargs={
            "previous_uid": uid,
            "new_name": name,
            "new_prescript": prescript,
            "new_tags_pre": tags_pre,
            "trim_errors": trim_errors,
        },
    )
    return result["instance"]


@utils.serial
async def run(doc: dict):
    action = "document.update"
    kwargs = {"uid": doc["uid"], "finalised": True}
    runner = _send_progress(action, kwargs, progress_title="running")

    async for result in runner:
        pass

    return result["instance"]


# @utils.assert_call_signature
def add(
    metatype: str,
    doc: dict,
    /,
    *,
    name: str,
    **kwargs,
) -> dict:
    result = _send(
        action="prototype.insert",
        kwargs={
            "doc_uid": doc["uid"],
            "instance": {
                "name": name,
                "_metatype": metatype,
                **kwargs,
            },
        },
    )
    return result["instance"]


@utils.serial
async def resolve(
    doc,
    results_paths,
) -> typing.Union[typing.List[dict], dict]:
    result = _send(
        action="document.select",
        kwargs={
            "uid": doc["uid"],
            "include": ["uid", "finalised"],
        },
    )
    doc = result["instance"]

    if doc["finalised"]:
        permutations = _send(
            action="permutation.select",
            kwargs={
                "doc_uid": doc["uid"],
            },
        )
        uids = [p["uid"] for p in permutations if p["success"] is True]
    else:
        uids = [doc["uid"]]

    results_paths = [
        segment.strip()
        for line in results_paths.split("\n")
        for segment in line.split(" ")
        if segment
    ]
    results_paths = ["uid", *results_paths]

    action = "resolve"
    kwargs = {"uids": uids, "paths": results_paths}
    runner = _send_progress(action, kwargs, progress_title="resolving")

    results = {}

    async for result in runner:
        if result and result.get("_type") == "progress":
            uid = result["chunk"]["uid"]
            path = result["chunk"]["path"]
            value = result["chunk"]["value"]
            results.setdefault(uid, {})[path] = value

    return list(results.values())
