#!/usr/bin/env python3
"""
Run the following to get additional information on using the command-line 
interface:

    $ aws-spitzel --help

If you neither specifiy ``--from``, nor ``--to``, the entire available date 
range will be used.
"""
from argparse import (
    ArgumentParser,
    ArgumentDefaultsHelpFormatter,
    RawDescriptionHelpFormatter,
)
from pathlib import Path
import json
import datetime
import sys
from subprocess import check_output
from typing import Dict, Optional, List

sys.path.insert(0, str(Path(__file__).parent.parent))
import aws_spitzel


class ArgparseFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
    """A formatter class for showing default values and not inserting new line
       when showing the help text header
    """


def get_parser():
    """
    """
    parser = ArgumentParser(
        prog=Path(__file__).parent.name.replace('_', '-'),
        description='\n'.join([aws_spitzel.__doc__, __doc__]),
        epilog = 'Make sure to specify the correct AWS CLI profile through the '
                 'AWS_PROFILE environment variable',
        formatter_class = ArgparseFormatter,
    )

    parser.add_argument('action',
        metavar = 'IAM_ACTION',
        type = lambda s: aws_spitzel.Action(*s.split(':', 1)),
        help = "service id and action name in AWS IAM policy statement format "
               "($service_id:$action_name)",
        nargs = "+"
    )

    parser.add_argument('--match',
        metavar = "EXPRESSION",
        help = "JSONPath filter",
        required = False,
        action = "append",
        type=lambda s: aws_spitzel.Filter(expression = aws_spitzel.get_expression_object(s)),
        default=[]
    )

    parser.add_argument('--from',
        metavar = 'DATETIME',
        help = "start of date range to find events in",
        type = lambda s: datetime.datetime.strptime(s, aws_spitzel.DateRange._format),
        default= datetime.datetime.now() - datetime.timedelta(days=90)
    )

    parser.add_argument('--to',
        metavar = 'DATETIME',
        help="end of date range to find events in",
        type=lambda s: datetime.datetime.strptime(s, aws_spitzel.DateRange._format),
        default= datetime.datetime.now()
    )

    parser.add_argument('--last-minute',
        metavar = 'MINUTES',
        help="from now back to x minutes ago",
        type=int,
        default= 300
    )

    return parser