#!/usr/bin/env python3
"""
"""
import sys
import json
from datetime import datetime



def main():
    """
    """
    while True:

        line = sys.stdin.readline()

        event = json.loads(line)

        print(json.dumps({
            'event': event,
            'time': int(datetime.strptime(event['eventTime'], "%Y-%m-%dT%H:%M:%SZ").timestamp()),
            'source': event['eventSource']
        }))

        if line == '':
            break


if __name__ == '__main__':

    main()