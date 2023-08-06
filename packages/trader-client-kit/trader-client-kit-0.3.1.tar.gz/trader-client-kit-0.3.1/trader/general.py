# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: general argument

from trader import CONF
from trader._args import basic, argument

class GeneralCommand(basic.ParserBasic):
    def __init__(self) -> None:
        super().__init__()

        self.version = argument.Argument('-v', '--version')
        self.version.action = argument.Argument.Action.VERSION.value
        self.version.help = 'show program\'s version number and exit'
        self.version.version = CONF.get('trader', 'APPLICATION_VERSION')