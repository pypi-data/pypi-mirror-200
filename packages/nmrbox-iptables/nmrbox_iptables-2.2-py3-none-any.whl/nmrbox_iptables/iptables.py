#!/usr/bin/env python3
import collections
from typing import Optional, Iterable, Mapping, List, Dict

import iptc
from iptc import Rule, Chain

from nmrbox_iptables import SUBCHAIN, INPUT, nblogger


class Manager:

    def __init__(self, application: str, makesubchain: bool = True):
        """
        :param application: used for iptable comments
        """
        self.application = application
        self.setup = False
        self.makesubchain = makesubchain
        self.revert = False

    def __enter__(self):
        self.standard_configuration()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def find_chain(self, name: str) -> Optional[Chain]:
        """Search for a chain"""
        for chain in self.table.chains:
            if chain.name == name:
                return chain
        return None

    @property
    def rulecomments(self) -> Mapping[str,List[Rule]]:
        rval : Dict[str,List[Rule]]= collections.defaultdict(list)
        for chain in self.table.chains:
            r: iptc.Rule
            for r in chain.rules:
                for m in r.matches:
                    if m.name == 'comment':
                        if (comment := m.parameters.get('comment',None)) is not None:
                            rval[comment].append(r)
        return rval

    def _is_established(self, rule: Rule) -> bool:
        """See if rule is state established"""
        for m in rule.matches:
            if m.name == 'state':
                return m.parameters.get('state') == 'RELATED,ESTABLISHED'
        return False

    def standard_configuration(self):
        """Make established rule first, add SUBCHAIN"""
        if self.setup:
            return
        self.table = iptc.Table(iptc.Table.FILTER, autocommit=False)
        self.table.refresh()
        self.input = self.find_chain(INPUT)
        irules = self.input.rules
        state_rule_first = len(irules) > 0 and self._is_established(irules[0])
        altered = False
        for r in irules[1:]:
            if self._is_established(r):
                nblogger.info("deleting superfluous state rule")
                self.input.delete_rule(r)
                altered = True
        if not state_rule_first:
            altered = True
            self._add_state_rule()
        if altered:
            self.table.commit()
        if self.makesubchain:
            self._setup_chain(SUBCHAIN, position=1)
        self.setup = True

    def setup_chain(self, chain_name: str, *, position: int = None, last_accept: bool = True):
        """Setup chain
        position: specific position
        last_accept: add chain to last accept if True
        """
        if (p := position) is None:
            if last_accept:
                p = self._last_any_accept(self.find_chain(INPUT), 'tcp')
            else:
                p = 1
        self._setup_chain(chain_name, position=p)

    def _setup_chain(self, chain_name: str, position: int):
        """Setup dedicated chain and add INPUT rule, if not already present"""
        if chain_name == INPUT:
            return
        self.table.refresh()  # this avoids some IPTCError / resource temporarily unavailable exceptions
        if self.find_chain(chain_name) is None:
            nblogger.info("Creating chain {}".format(chain_name))
            self.vnc_chain = self.table.create_chain(chain_name)
            self.table.commit()
            self.table.refresh()  # this avoids some IPTCError / resource temporarily unavailable exceptions
        number_vnc_rule = len([r for r in self.input.rules if r.target.name == chain_name])
        if (number_vnc_rule == 1):
            nblogger.debug("{} chain rule already present".format(chain_name))
            return
        if (number_vnc_rule == 0):
            nblogger.info("Creating {} chain rule".format(chain_name))
            rule = iptc.Rule()
            rule.protocol = "tcp"
            rule.target = iptc.Target(rule, chain_name)
            self.input.insert_rule(rule, position=position)
            self.table.commit()
            return
        raise ValueError("Found {:d} {} rules".format(number_vnc_rule, chain_name))

    def _add_comment(self, rule: Rule, description: str = None):
        """annotate source of comment"""
        comment = iptc.Match(rule, "comment")
        if description is None:
            comment.comment = f"added by Python nmrbox-iptables by application: {self.application}"
        else:
            comment.comment = description
        rule.add_match(comment)

    def _add_state_rule(self):
        """Add state rule to front of INPUT chain. Does not commit"""
        nblogger.info("Adding state rule to front of INPUT")
        rule = iptc.Rule()
        rule.target = iptc.Target(rule, "ACCEPT")
        match = iptc.Match(rule, "state")
        match.state = "RELATED,ESTABLISHED"
        rule.add_match(match)
        self._add_comment(rule)
        self.input.insert_rule(rule)

    def add_tcp_rule(self, port: int, source: Optional[str] = None, *, chain=SUBCHAIN) -> None:
        """add tcp rule to chain
        port: port open
        source: source expression, may be single IP or range
        chain: insert to this chain
        """
        self.standard_configuration()
        self.table.refresh()
        sc: Chain = self.find_chain(chain)
        rule = iptc.Rule()
        rule.protocol = 'tcp'
        if source is not None:
            rule.src = source
        rule.target = iptc.Target(rule, "ACCEPT")
        match = rule.create_match("tcp")
        match.dport = str(port)
        self._add_comment(rule)
        for existing in sc.rules:
            if rule == existing:
                nblogger.debug(f"Rule {port} {source} already present")
                return
        nblogger.info(f"Adding Rule {port} {source}")
        sc.insert_rule(rule)
        self.table.commit()

    def _last_any_accept(self, chain: Chain, protocol: Optional[str]):
        """Line number of last accept"""
        last_accept = -1
        n = len(chain.rules)
        for i in range(n):
            r: iptc.Rule = chain.rules[i]
            if r.in_interface is not None:
                continue
            if r.target.name == 'ACCEPT':
                if protocol is None or r.protocol == protocol:
                    last_accept = i
        return last_accept + 1  # iptables start with 1

    def remove(self,comment:str):
        """Remove rules with comment"""
        self.table.refresh()
        altered = False
        for rule in self.rulecomments.get(comment,[]):
            altered = True
            nblogger.info(f"delete {comment} rule")
            rule.chain.delete_rule(rule)
        if altered:
            self.table.commit()



    def add_accept_tcp_multi(self, ports: str, chain_name: str, beginning: bool,
                             comment: str):
        """ports: comma separated or range with :
        beginning: insert at beginning
        comment: comment to add"""
        self.table.refresh()
        if comment in self.rulecomments:
            nblogger.info(f"{comment} already present")
            return
        sc: Chain = self.find_chain(chain_name)
        rule = iptc.Rule()
        rule.protocol = 'tcp'
        rule.target = iptc.Target(rule, "ACCEPT")
        match = rule.create_match('multiport')
        match.dports = ports
        self._add_comment(rule, comment)
        # skip 0 because that should be the established state rule
        position = 1 if beginning else self._last_any_accept(sc, 'tcp')
        sc.insert_rule(rule, position)
        self.table.commit()

    def list_rules(self):
        r: iptc.Rule
        for r in self.input.rules:
            d = iptc.easy.decode_iptc_rule(r)
            print(d)

            print(f"{r.protocol} {r.in_interface} {r.src} {r.target.name}")
