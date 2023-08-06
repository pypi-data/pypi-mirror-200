#!/usr/bin/env python3
from pathlib import Path
import datetime
import sys
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

import aws_spitzel

from aws_spitzel import cli


def main() -> None:
    """main program execution when called as a Python module from command-line
    """

    context, _ = cli.main()

    for match in aws_spitzel.main(context):

        print(json.dumps(match))

    sys.exit()


if __name__ == '__main__':

    main()
