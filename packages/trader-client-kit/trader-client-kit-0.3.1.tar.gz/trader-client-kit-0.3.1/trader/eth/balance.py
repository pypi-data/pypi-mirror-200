# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: zkSync withdrawal subcommand

import trader

from . import _command
from trader._args import argument
from trader._utils import get_web3_provider

class EthBalanceSubparser(_command.EthParser, _command.EthBasic):
    def __init__(self) -> None:
        super().__init__()
        
        self.account = argument.Argument('-a', '--account')
        self.account.help = 'the address of account'
        self.account.dest = 'account'
        self.account.required = True

        self.subcommand = argument.Parser('balance')
        self.subcommand.help = 'get eth balance'
        self.subcommand.func = self.subcommand_func
        self.subcommand.usage = 'trader [options] eth balance [options]'

    def subcommand_default_func(self, args, parent) -> None:
        client = get_web3_provider(args.network, 'HONG_KONG')
        balance = client.eth.get_balance(args.account)

        trader.LOG.info(args.account)
        trader.LOG.info('%s (eth)', client.fromWei(balance, 'ether'))
