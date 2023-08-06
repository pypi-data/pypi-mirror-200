import json
import os
from contextlib import asynccontextmanager
from typing import TypeVar, AsyncContextManager

import redis.asyncio as redis
from redis.commands.json.path import Path

from moontour_common.database.rabbitmq import notify_room
from moontour_common.models import BaseRoom

_RoomType = TypeVar('_RoomType', bound=BaseRoom)

ROOM_KEY_PREFIX = 'room:'

_host = os.getenv('REDIS_HOST', 'redis')
redis_client = redis.Redis(host=_host)


def get_room_key(room_id: str) -> str:
    return f'{ROOM_KEY_PREFIX}{room_id}'


@asynccontextmanager
async def room_lock(room_id: str):
    async with redis_client.lock(f'room-{room_id}'):
        yield


async def create_room(room: _RoomType):
    await set_room(room)


def delete_room(room_id: str):
    redis_client.json().delete(get_room_key(room_id), Path.root_path())


async def get_room(room_id: str, model: type[_RoomType]) -> _RoomType:
    room_raw = await redis_client.execute_command('JSON.GET', get_room_key(room_id), Path.root_path())
    return model.parse_raw(room_raw)


async def set_room(room: _RoomType):
    await redis_client.execute_command('JSON.SET', get_room_key(room.id), Path.root_path(), room.json())


@asynccontextmanager
async def modify_room(
        room_id: str,
        model: type[_RoomType] = BaseRoom,
        notify: bool = True
) -> AsyncContextManager[_RoomType]:
    assert model.get_mode() is not None  # Modifying abstract models will lead to unexpected results

    async with room_lock(room_id):
        room = await get_room(room_id, model)
        try:
            yield room
        except Exception:
            raise
        else:
            await set_room(room)

            if notify:
                await notify_room(room)
