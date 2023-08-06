# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: ethereum subcommand

from trader._args import basic, argument

class EthSubCommand(basic.ParserBasic):
    def __init__(self) -> None:
        super().__init__()

        self.subcommand = argument.Parser('eth')
        self.subcommand.help = 'web3 related tool functions'
        self.subcommand.usage = 'trader eth <command> [options]'

class EthParser(EthSubCommand):
    def __init__(self) -> None:
        super().__init__()

        self.subcommand = argument.Subparser()
        self.subcommand.dest = 'eth_parser'
class EthBasic(object):
    def __init__(self) -> None:
        
        self.network = argument.Argument('-n', '--network')
        self.network.help = 'choise blockchain network'
        self.network.dest = 'network'
        self.network.default = 'ethereum'
        self.network.choices = [
            'ethereum', 'binance', 'zksync', 'goerli', 'bsc_testnet'
        ]