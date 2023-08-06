# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: zkSync subcommand

import trader, os, json
from web3 import Web3

from trader._args import basic, argument
from trader._utils import get_web3_provider

class ZksyncSubCommand(basic.ParserBasic):
    def __init__(self) -> None:
        super().__init__()

        self.subcommand = argument.Parser('zksync')
        self.subcommand.help = 'makes transaction records for zkSync'
        self.subcommand.usage = 'trader zksync <command> [options]'

class ZksyncParser(ZksyncSubCommand):
    def __init__(self) -> None:
        super().__init__()

        self.subcommand = argument.Subparser()
        self.subcommand.dest = 'zks_parser'

class ZksyncBasic(object):
    def __init__(self) -> None:
        self.accounts = argument.Argument('-j', '--json')
        self.accounts.type = str
        self.accounts.help = 'the json file path of the accounts'
        self.accounts.dest = 'account_json'
        self.accounts.required = True

        self.thread = argument.Argument('-t', '--thread')
        self.thread.type = int
        self.thread.help = 'number of threads to start'
        self.thread.dest = 'thread'
        self.thread.default = trader.CONF.get('trader', 'THREAD_NUMBER')

        self.zksync: Web3 = None
        self.ethereum: Web3 = None

    def import_accounts(self, args) -> dict:
        if not os.path.exists(args.account_json):
            raise Exception('File not exists')

        with open(args.account_json, 'r') as f:
            accounts = json.loads(f.read())
            trader.LOG.info('Total Account: [%s]', len(accounts))
            return accounts
        
    def get_balance(self, w3: Web3, addr) -> float:
        balance = w3.eth.get_balance(addr)
        balance = w3.fromWei(balance, 'ether')
        trader.LOG.info('[%s]: - [%s]', addr[38:], balance)

        return balance
    
    def init_web3_provider(self) -> None:
        self.zksync: Web3 = get_web3_provider('zksync', 'HONG_KONG')
        self.ethereum: Web3 = get_web3_provider('ethereum', 'HONG_KONG')