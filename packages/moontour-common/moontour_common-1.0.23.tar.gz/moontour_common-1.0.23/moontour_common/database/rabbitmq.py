import os

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue, ExchangeType

from moontour_common.models import BaseRoom

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
ROOMS_EXCHANGE_NAME = 'rooms'

_channel: AbstractChannel | None = None


async def get_rabbitmq_client() -> AbstractChannel:
    global _channel
    if _channel is None:
        connection = await aio_pika.connect_robust(host=RABBITMQ_HOST)
        _channel = await connection.channel()
    return _channel


async def get_rooms_exchange() -> AbstractExchange:
    client = await get_rabbitmq_client()
    return await client.declare_exchange(name=ROOMS_EXCHANGE_NAME, type=ExchangeType.TOPIC)


async def declare_player_queue(room_id: str, user_id: str) -> AbstractQueue:
    client = await get_rabbitmq_client()
    queue_name = f'{room_id}.{user_id}'
    queue = await client.declare_queue(name=queue_name, auto_delete=True)
    exchange = await get_rooms_exchange()
    await queue.bind(exchange, routing_key=f'{room_id}.*')
    return queue


async def notify_room(room: BaseRoom):
    exchange = await get_rooms_exchange()
    await exchange.publish(
        message=Message(body=room.json().encode()),
        routing_key=f'{room.id}.*',
    )
