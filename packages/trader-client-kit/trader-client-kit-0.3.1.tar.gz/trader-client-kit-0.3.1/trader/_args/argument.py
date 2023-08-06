# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: argparse argument

import enum, trader

from trader._utils import parse_to_argument, CustomFormatter

class ArgBasic(object):
    @property
    def __argument__(self) -> dict:
        return parse_to_argument(self.__dict__, ['name'])
    
    @property
    def __parser__(self) -> dict:
        return parse_to_argument(self.__dict__, ['name', 'func'])
    
    @property
    def __subparser__(self) -> dict:
        return parse_to_argument(self.__dict__, ['name'])

class Argument(ArgBasic):
    def __init__(self, *args) -> None:
        self.name = args
        self.action = None
        self.nargs = None
        self.default = None
        self.type = None
        self.choices = None
        self.required = None
        self.help = None
        self.metavar = None
        self.dest = None
        self.version = None

    class Action(enum.Enum):
        STORE = 'store'
        STORE_CONST = 'store_const'
        STORE_TRUE = 'store_true'
        STORE_FALSE = 'store_false'
        APPEND = 'append'
        APPEND_CONST = 'append_const'
        COUNT = 'count'
        HELP = 'help'
        VERSION = 'version'
        EXTEND = 'extend'

class Parser(ArgBasic):
    def __init__(self, name: str) -> None:
        self.name = name
        self.func = None
        self.help = None
        self.formatter_class = CustomFormatter
        self.epilog = trader.CONF.get('trader', 'APPLICATION_EPILOG')
        self.metavar = None
        self.usage = None
        # self.description = trader.parser.description
        self.description = None

class Subparser(ArgBasic):
    def __init__(self) -> None:
        self.nargs = None
        self.default = None
        self.choices = None
        self.required = None
        self.help = None
        self.metavar = ''
        self.dest = None
        self.title = 'required commands'