#!/usr/bin/env python3
"""
"""
import sys
import json


def main():
    """
    """
    while True:

        line = sys.stdin.readline()

        print(json.dumps({'event': json.loads(line)}))

        if line == '':
            break


if __name__ == '__main__':

    main()