nmrbox_iptables
=================

Utility for setting ip table rules

Usage
-----
Package is undergoing development. There is a command line utility, addrule, which accepts a YAML file.
See ./lib/python3.8/site-packages/example/multitest.yaml for an example.

from nmrbox_iptables import Manager

It is best used as a context manager.

addrule add <yaml file>

addrule remove <yaml file>


