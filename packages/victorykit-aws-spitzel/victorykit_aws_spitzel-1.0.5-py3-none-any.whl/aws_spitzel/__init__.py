#!/usr/bin/env python3
"""Heuristic CloudTrail Event History Lookup for AWS IAM Forensics

Lightweight and flexible AWS DevOps command-line tool and Python 3.9 module for 
security operation duties (SOC) of AWS platform services.

This program extends the 
`native AWS CloudTrail API LookupEvents action <https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_LookupEvents.html>`_ by being 
able to query against CloudTrail event objects with JSONPath expressions and a 
barebone implementation of comparison operations for Python built-in types, and
regular expressions. In addition, the UNIX filename pattern of AWS IAM policy 
statement actions is used for filtering events by service and action 
(e.g. ``s3:List*``), instead of the CloudTrail API schema attributes.
(``eventName``, ``eventSource``, etc.).

This program is licensed under the 
"Data licence Germany – attribution – Version 2.0".
`URL <http://www.govdata.de/dl-de/by-2-0>`_
"""
from dataclasses import dataclass, field, asdict
import json
from datetime import datetime
from typing import Dict, Optional, List, Callable, Generator, Any, Tuple
from queue import PriorityQueue
from threading import Thread
from ast import parse as astparse
from re import match as regexmatch
from fnmatch import fnmatch
from time import sleep
import sys

import boto3
from jsonpath import jsonpath


class DefaultAWSAPIClients:

    cloudtrail = boto3.client('cloudtrail')


@dataclass(order=True)
class PrioritizedQueueItem:
    """
    """
    priority: int
    item: Any = field(compare=False)


@dataclass
class Expression:
    """
    """
    left_operand: str
    right_operand: str
    operator: str


def get_expression_object(
    raw: str,
    operators: Optional[List[str]] = ['==', '!=', 'regex']
) -> Expression:
    """
    """

    expression_size = len(raw)

    bfr = ''

    operator_index = -1

    operator_size = -1

    for index in range(expression_size):

        # this is groovy 🕺
        opts = [op[len(bfr)] for op in operators if len(op) -1 >= len(bfr)]

        if raw[index] in opts:

            if bfr == '':

                operator_index = index

            bfr += raw[index]

        else:

            operator_index = -1

            bfr = ''

            continue

        if bfr in operators:

            operator_size = len(bfr)

            break

    if operator_index == -1 or operator_size == -1:

        raise Exception('unable to parse operator')

    right_operand = astparse(raw[operator_index + operator_size:].lstrip(),
                             mode='eval').body.n

    return Expression(
        left_operand = raw[0:operator_index].rstrip(),
        right_operand = right_operand,
        operator = raw[operator_index:operator_index + operator_size],
    )


@dataclass
class Action:
    """AWS IAM action
    """
    #: id of service (e.g. `s3`)
    service_id: str
    #: name of action (e.g. `ListBuckets`)
    action_name: str


@dataclass
class DateRange:
    """
    """
    #: start of range
    start: datetime
    #: end of range
    end: datetime
    #: string format of datetime
    format: str = '%Y-%m-%d %H:%M:%S'


@dataclass
class Filter:
    """
    """
    expression: Expression


@dataclass
class ProgramContext:
    """
    """
    actions: List[Action]
    date_range: DateRange
    filters: Optional[List[Filter]] = field(default_factory=[])


def boto3_next_token(
    callable_: Callable,
    kwargs={},
    next_token='',
    max_results=50,
    args = []
) -> Generator[Tuple[dict, str], None, None]:
    """
    """

    failures_in_a_row = 0

    while next_token != None:

        kwargs_proto = {
            'MaxResults': max_results
        }

        if next_token != '':

            kwargs_proto['NextToken'] = next_token

        try:

            response = callable_(
                *args,
                **{
                    **kwargs_proto,
                    **kwargs
                }
            )
        except Exception as err:

            if failures_in_a_row >= 3:

                raise err from err

            failures_in_a_row += 1

            print('API Throttle',file=sys.stderr)

            sleep(1)

            continue

        next_token = response.get('NextToken', None)

        yield response, next_token

        if next_token is None:

            break



def lookup_event_response(
    response: dict,
    context: ProgramContext,
    action: Action,
    callback: Callable[[Any], None],
    operations: Optional[Dict[str, Callable]] = {
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b,
        'regex': lambda a, b: False if regexmatch(b, a) is None else True
    }
) -> None:
    """retrieve matches of a boto3 CloudTrail API lookup through a callback

    :param response: a cloudtrail boto3 LookupEvents API response object
    :param action: the action (eventSource) the API request was made for
    :param context: the global request object of the program
    :param callback: callable for reporting a succesful operation
    :param operations: comparison operation callables
    """
    for _event in response.get('Events', []):

        event = json.loads(_event['CloudTrailEvent'])

        if not fnmatch(event['eventName'], action.action_name):

            continue

        match = True
        for filter_ in context.filters:

            json_path_matches = jsonpath(
                event,
                filter_.expression.left_operand,
                'VALUE'
            )

            if isinstance(json_path_matches, list) and \
               len(json_path_matches) == 0:

                match = False

                break

            elif isinstance(json_path_matches, list) \
                 and len(json_path_matches) > 1:

                print(f'JSONPath {filter_.expression.left_operand} returns '
                       'more than one match', file=sys.stderr)

                break

            json_path_match = json_path_matches[0] if isinstance(json_path_matches, list) else json_path_matches

            match = operations[filter_.expression.operator](
                json_path_match,
                filter_.expression.right_operand
            )

            if match is not True:

                break

        if match is True:

            callback(event)


def handle_action_lookup(
    context: ProgramContext,
    action: Action,
    queue: PriorityQueue,
    worker_threads: Optional[list] = [],
    cloudtrail_api_client = DefaultAWSAPIClients.cloudtrail,
):
    """
    :param context: the global request object of the program
    :param action: the action (eventSource) the API request will be made for
    :param queue: lookup match item queue for synchronising threads
    :param worker_threads: list instance of worker threads assigned to this handler thread
    :param cloudtrail_api_client: 
    """
    for response_page, next_token in boto3_next_token(
        cloudtrail_api_client.lookup_events,
        {
            'LookupAttributes': [
                {
                    'AttributeKey': 'EventSource',
                    'AttributeValue': f'{action.service_id}.amazonaws.com'
                },
            ],
            'StartTime': context.date_range.start,
            'EndTime': context.date_range.end,
        }
    ):

        thread = Thread(
            name=next_token,
            target=lookup_event_response,
            args=[
                response_page,
                context,
                action,
                lambda item: queue.put(
                    PrioritizedQueueItem(priority=0, item=item)
                ),
            ]
        )

        worker_threads.append(thread)

        thread.start()

    for thread in worker_threads:

        thread.join()

    queue.put(PrioritizedQueueItem(priority=2, item='WORKERS_JOINED'))


def main(context: ProgramContext) -> dict:
    """
    :param range: date range to search in 
    """

    queue = PriorityQueue()

    handler_threads = []

    for action in context.actions:

        thread = Thread(
            target = handle_action_lookup,
            args = [
                context,
                action,
                queue,
                [],
                boto3.client('cloudtrail')
            ]
        )

        handler_threads.append(thread)

        thread.start()

    done = 0

    while True:

        item = queue.get(True)

        if item.item == 'WORKERS_JOINED':

            done += 1
        else:

            yield item.item

        if done == len(handler_threads):

            break

    for thread in handler_threads:

        thread.join()
