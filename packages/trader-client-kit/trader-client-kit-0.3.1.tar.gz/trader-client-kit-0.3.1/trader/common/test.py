# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: common test subcommand

import trader, datetime, secrets, json

from . import _command
from trader._args import argument
from eth_account import Account

class TestSubparser(_command.CommonParser):
    def __init__(self) -> None:
        super().__init__()

        self.value = argument.Argument('-v', '--value')
        self.value.type = int
        self.value.help = 'the argument for testing'
        self.value.dest = 'value'
        self.value.default = 10

        self.subcommand = argument.Parser('test')
        self.subcommand.help = 'for some common tests'
        # self.subcommand.func = self.subcommand_func
        self.subcommand.usage = 'trader [options] common test [options]'

    def subcommand_default_func(self, args, parent) -> None:
        trader.LOG.warning('Test Warning')
        trader.LOG.info('Test Info')
        trader.LOG.debug('Test Debug')
        trader.LOG.error('Test Error')
