#!/usr/bin/env python3
from pathlib import Path
import datetime
import sys
import json
from typing import Dict, Optional, List

sys.path.insert(0, str(Path(__file__).parent.parent))

import aws_spitzel

from aws_spitzel import cli


def main() -> None:

    parser = cli.get_parser()

    argv = vars(parser.parse_args())

    if argv.get('last_minute', None):

        from_ = datetime.datetime.now() - datetime.timedelta(minutes=argv['last_minute'])

    else:

        from_ = argv['from']

    for match in aws_spitzel.main(aws_spitzel.ProgramContext(
        actions=argv['action'],
        filters=argv['match'],
        date_range=aws_spitzel.DateRange(
            start=from_,
            end=argv['to']
        )
    )):

        print(json.dumps(match))

    sys.exit()


if __name__ == '__main__':

    main()