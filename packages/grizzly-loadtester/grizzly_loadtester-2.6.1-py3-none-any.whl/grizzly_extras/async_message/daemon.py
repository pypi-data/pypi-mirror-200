from typing import List, Optional, Union, cast
from types import FrameType
from uuid import uuid4
from json import loads as jsonloads, dumps as jsondumps
from threading import Thread
from urllib.parse import urlparse
from signal import signal, SIGTERM, SIGINT, Signals
from time import sleep

import setproctitle as proc

import zmq.green as zmq

from . import (
    ThreadLogger,
    AsyncMessageRequest,
    AsyncMessageResponse,
    AsyncMessageHandler,
    LRU_READY,
    SPLITTER_FRAME,
)

from grizzly_extras.transformer import JsonBytesEncoder


run: bool = True


def signal_handler(signum: Union[int, Signals], frame: Optional[FrameType]) -> None:
    global run
    if run:
        run = False


signal(SIGTERM, signal_handler)
signal(SIGINT, signal_handler)


def router() -> None:
    logger = ThreadLogger('router')
    proc.setproctitle('grizzly-async-messaged')  # set appl name on ibm mq
    logger.debug('starting')

    context = zmq.Context(1)
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.ROUTER)
    frontend.bind('tcp://127.0.0.1:5554')
    backend.bind('inproc://workers')

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    worker_threads: List[Thread] = []

    def spawn_worker() -> None:
        identity = str(uuid4())

        thread = Thread(target=worker, args=(context, identity, ))
        thread.daemon = True
        worker_threads.append(thread)
        thread.start()
        logger.info(f'spawned worker {identity} ({thread.ident})')

    workers_available: List[str] = []

    spawn_worker()

    while run:
        socks = dict(poller.poll(timeout=1000))

        if not socks:
            continue

        logger.debug("i'm alive!")

        if socks.get(backend) == zmq.POLLIN:
            logger.debug('polling backend')
            try:
                backend_response = backend.recv_multipart(flags=zmq.NOBLOCK)
            except zmq.Again:
                sleep(0.1)
                continue

            if not backend_response:
                continue

            reply = backend_response[2:]
            if reply[0] != LRU_READY.encode():
                frontend.send_multipart(reply)
            else:
                worker_id = backend_response[0]
                logger.info(f'worker {worker_id.decode()} ready')
                workers_available.append(worker_id)

        if socks.get(frontend) == zmq.POLLIN:
            logger.debug('polling frontend')
            try:
                msg = frontend.recv_multipart(flags=zmq.NOBLOCK)
            except zmq.Again:
                sleep(0.1)
                continue

            request_id = msg[0]
            payload = jsonloads(msg[-1].decode())

            worker_id = payload.get('worker', None)

            if worker_id is None:
                worker_id = workers_available.pop()
                payload['worker'] = worker_id.decode()
                logger.info(f'assigning worker {payload["worker"]}')
                request = jsondumps(payload).encode()
                if len(workers_available) == 0:
                    logger.debug('spawning an additional worker, for next client')
                    spawn_worker()
            else:
                worker_id = worker_id.encode()
                request = msg[-1]

            backend_request = [worker_id, SPLITTER_FRAME, request_id, SPLITTER_FRAME, request]
            backend.send_multipart(backend_request)

    logger.info('stopping')
    for worker_thread in worker_threads:
        logger.debug(f'waiting for {worker_thread.ident}')
        worker_thread.join()

    try:
        context.destroy()
    except:
        logger.error('failed to destroy zmq context', exc_info=True)

    logger.info('stopped')


def worker(context: zmq.Context, identity: str) -> None:
    logger = ThreadLogger(f'worker::{identity}')
    worker = context.socket(zmq.REQ)

    worker.setsockopt_string(zmq.IDENTITY, identity)
    worker.connect('inproc://workers')
    worker.send_string(LRU_READY)

    integration: Optional[AsyncMessageHandler] = None

    while run:
        try:
            request_proto = worker.recv_multipart(flags=zmq.NOBLOCK)
        except zmq.Again:
            sleep(0.1)
            continue

        logger.debug(f"i'm alive! {run=}")

        if not request_proto:
            logger.error('empty msg')
            continue

        request = cast(
            AsyncMessageRequest,
            jsonloads(request_proto[-1].decode()),
        )

        if request['worker'] != identity:
            logger.error(f'got {request["worker"]}, expected {identity}')
            continue

        response: Optional[AsyncMessageResponse] = None
        if integration is None:
            try:
                integration_url = request.get('context', {}).get('url', None)
                if integration_url is None:
                    raise RuntimeError('no url found in request context')

                parsed = urlparse(integration_url)

                if parsed.scheme in ['mq', 'mqs']:
                    from .mq import AsyncMessageQueueHandler
                    integration = AsyncMessageQueueHandler(identity)
                elif parsed.scheme == 'sb':
                    from .sb import AsyncServiceBusHandler
                    integration = AsyncServiceBusHandler(identity)
                else:
                    raise RuntimeError(f'integration for {str(parsed.scheme)}:// is not implemented')

            except Exception as e:
                response = {
                    'worker': identity,
                    'response_time': 0,
                    'success': False,
                    'message': str(e),
                }

        if response is None and integration is not None:
            logger.debug('send request to handler')
            response = integration.handle(request)
            logger.debug('got response from handler')

            if request.get('action', None) in ['DISCONNECT', 'DISC']:
                integration.close()
                integration = None

        response_proto = [
            request_proto[0],
            SPLITTER_FRAME,
            jsondumps(response, cls=JsonBytesEncoder).encode(),
        ]

        worker.send_multipart(response_proto)

    logger.debug(f"i'm going to die! {run=}")
    logger.info('stopping')
    if integration is not None:
        logger.debug(f'closing {integration.__class__.__name__}')
        try:
            integration.close()
        except:  # pragma: no cover
            logger.error('failed to close integration', exc_info=True)

    try:
        worker.close()
    except:  # pragma: no cover
        logger.error('failed to close worker', exc_info=True)
    logger.debug('stopped')


def main() -> int:
    try:
        router()
        return 0
    except KeyboardInterrupt:
        return 1
