#!/usr/bin/env python3
import argparse
import logging
import os
import sys

from nmrbox_iptables import nblogger
from nmrbox_iptables.iptables import Manager


def main():
    if os.getuid() != 0:
        print("Run as root",file=sys.stderr)
        sys.exit(1)
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', default='WARN', help="Python logging level")

    args = parser.parse_args()
    cfg = Manager("test driver2")
    nblogger.setLevel(getattr(logging, args.loglevel))
    cfg.standard_configuration()
    cfg.add_tcp_rule(8081,'127.9.9.1')
    cfg.add_tcp_rule(8081,'127.9.9.2')
    for i in range(1,256):
        cfg.add_tcp_rule(8081,f'127.9.9.{i}')


if __name__ == "__main__":
    main()
