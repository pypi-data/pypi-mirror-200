# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: common subcommand

from trader._args import basic, argument

class CommonSubCommand(basic.ParserBasic):
    def __init__(self) -> None:
        super().__init__()

        self.subcommand = argument.Parser('common')
        self.subcommand.help = 'some general operations of the blockchain'
        self.subcommand.usage = 'trader common <command> [options]'

class CommonParser(CommonSubCommand):
    def __init__(self) -> None:
        super().__init__()

        self.subcommand = argument.Subparser()
        self.subcommand.dest = 'common_parser'
