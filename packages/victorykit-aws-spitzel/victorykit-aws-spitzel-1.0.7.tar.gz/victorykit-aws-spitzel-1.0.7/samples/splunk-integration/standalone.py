#!/usr/bin/env python3
"""Sample Implementation of a Standalone AWS Spitzel Splunk HEC source

This uses nothing more than aws-spitzel and the Python standard library to
forward CloudTrail events to Splunk.

Extend it as needed (e.g. adding client certificate support, etc.).

Use it as a you use aws-spitzel, but additionally you will have to provide
some more flags. Check out ``--help`` for more information.

What you will have to do when running this in production? Running this on 
dual-core intel i5 makes it drop a few connections, or not be able to connect
at all. Since the Splunk server is run as a Docker container on the same 
machine it is difficult to determine the root cause probably. Probably throttle 
the creation of threads, so that less socket file descriptors are open.

This can also serve as a basis for an AWS Lambda implementation.
"""
from typing import Generator, Optional
import json
import http.client
from ssl import SSLContext, PROTOCOL_SSLv23
from dataclasses import dataclass, asdict, fields, field
from urllib.parse import urlunparse
from threading import Thread
from time import sleep
from datetime import datetime
from queue import Queue

import aws_spitzel
from aws_spitzel.cli import get_parser, main as cli_main

@dataclass
class ProgramContext:

    hostname: str
    token: str
    ssl: SSLContext 
    username: Optional[str] = 'Splunk'
    scheme: Optional[str] = 'https'
    port: Optional[int] = 443
    path: Optional[str] = 'services/collector'
    max_threads: Optional[str] = 200


def send_event(
    event: dict,
    context: ProgramContext,
    scontext: aws_spitzel.ProgramContext,
    signal_queue: Queue
) -> None:

    retries = 0

    response = None

    connection = None

    err = None

    while retries < 10:

        try:
            connection = http.client.HTTPSConnection(
                context.hostname,
                port=context.port,
                context=context.ssl
            )

            connection.request(
                method="POST",
                url=f'/{context.path}',
                headers={
                    'Authorization': f'{context.username} {context.token}'
                },
                body=json.dumps({
                    'event': event,
                    'time': int(datetime.strptime(event['eventTime'], "%Y-%m-%dT%H:%M:%SZ").timestamp()),
                    'source': event['eventSource']
                })
            )

            response = connection.getresponse()

            err = None

            break
        except Exception as _err:

            sleep(3)

            err = str(_err)

            retries += 1

    if err is not None:

        url = urlunparse((context.scheme, f'{context.hostname}:{context.port}', 
                          context.path, None, None, False))

        raise Exception(f'unable to post {url}: {err}')
    elif response.status != 200:

        raise Exception(f'{response.reason} [{response.status}]: '
                        '%s' % response.read())

    connection.close()

    print(f"done: {event['eventID']}")


def safe_send_event(
    event: dict,
    context: ProgramContext,
    scontext: aws_spitzel.ProgramContext,
    signal_queue: Queue
) -> None:

    try:

        send_event(event, context, scontext, signal_queue)
    except Exception as err:

        raise err from err

    signal_queue.put(None)


def main(context: ProgramContext, scontext: aws_spitzel.ProgramContext):
    """
    """

    signal_queue = Queue()

    worker_threads = []
    active_threads = 0

    index = 0;

    for match in aws_spitzel.main(scontext):

        print(f"do #{index}: {match['eventID']} ({match['eventTime']})")

        thread = Thread(
            target = safe_send_event,
            args = [match, context, scontext, signal_queue]
        )

        worker_threads.append(thread)

        thread.start()

        active_threads += 1

        index += 1

        if active_threads >= context.max_threads:

            print(f'throttling: {active_threads} active; {context.max_threads} max')

            signal_queue.get()

            active_threads -= 1


    for thread in worker_threads:

        thread.join()


if __name__ == '__main__':

    parser = get_parser()

    parser.add_argument('--splunk-hec-hostname',
        metavar = 'HOSTNAME',
        dest = 'hostname',
        help="Splunk HEC HTTP endpoint hostname",
        type=str,
        required=True
    )
    
    parser.add_argument('--splunk-hec-port',
        metavar = 'PORT',
        dest = 'port',
        help="Splunk HEC HTTP endpoint port",
        type=int,
        default=ProgramContext.port
    )

    parser.add_argument('--splunk-hec-path',
        metavar = 'PATH',
        dest = 'path',
        help="Splunk HEC HTTP endpoint path",
        type=str,
        default=ProgramContext.path
    )

    parser.add_argument('--splunk-hec-scheme',
        metavar = 'SCHEME',
        help="Splunk HEC HTTP endpoint scheme",
        dest = 'scheme',
        type=str,
        default=ProgramContext.scheme
    )

    parser.add_argument('--splunk-hec-username',
        metavar = 'NAME',
        help="Splunk HEC user name",
        dest = 'username',
        type=str,
        default='Splunk'
    )

    parser.add_argument('--splunk-hec-token',
        metavar = 'TOKEN',
        help="Splunk HEC token",
        type=str,
        dest='token',
        required=True
    )

    parser.add_argument('--max-threads',
        metavar = 'COUNT',
        help="maximum number of worker threads",
        type=int,
        default=ProgramContext.max_threads
    )

    scontext, argv = cli_main(parser)

    field_names = set(f.name for f in fields(ProgramContext))

    context = ProgramContext(
        **{
            **{k:v for k,v in argv.items() if k in field_names},
            **{
                'ssl': SSLContext(PROTOCOL_SSLv23)
            }
        }
    )

    main(context, scontext)