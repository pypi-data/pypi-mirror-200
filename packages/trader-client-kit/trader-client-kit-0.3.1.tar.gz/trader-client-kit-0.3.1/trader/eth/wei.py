# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: zkSync withdrawal subcommand

import trader, web3

from . import _command
from trader._args import argument
from trader._utils import get_web3_provider

class WeiSubparser(_command.EthParser, _command.EthBasic):
    def __init__(self) -> None:
        super().__init__()
        
        self.amount = argument.Argument('-a', '--amount')
        self.amount.type = int
        self.amount.help = 'the amount of toWei/fromWei'
        self.amount.dest = 'amount'
        self.amount.required = True
        
        self.uint = argument.Argument('--uint')
        self.uint.help = 'the uint of toWei/fromWei'
        self.uint.dest = 'uint'
        self.uint.default = 'ether'
        self.uint.choices = [
            'kwei', 'mwei', 'gwei', 'szabo', 'finney', 'ether'
        ]
        
        self.wei = argument.Argument('--wei')
        self.wei.dest = 'wei'
        self.wei.action = argument.Argument.Action.STORE_TRUE.value
        self.wei.help = 'process the amount as fromWei(false) / toWei(true)'

        self.subcommand = argument.Parser('wei')
        self.subcommand.help = 'get eth balance'
        self.subcommand.func = self.subcommand_func
        self.subcommand.usage = 'trader [options] eth wei [options]'

    def subcommand_default_func(self, args, parent) -> None:
        client, amount, r = web3.Web3(), 0, {}
        if args.wei: amount = client.toWei(args.amount, args.uint)
        else: amount = client.fromWei(args.amount, args.uint)

        r['a'] = args.amount
        r['u'] = args.uint
        r['w'] = 'toWei' if args.wei else 'fromWei'
        r['ra'] = amount

        trader.LOG.info('%(a)s.%(w)s(%(u)s): %(ra)s' % r)
