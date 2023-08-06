# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: zkSync withdrawal subcommand

import trader, threading

from . import _command
from trader._args import argument
from trader._utils import create_threading

class BalanceSubparser(_command.ZksyncParser, _command.ZksyncBasic):
    def __init__(self) -> None:
        super().__init__()
        
        self.accounts = argument.Argument('-j', '--json')
        self.accounts.type = str
        self.accounts.help = 'the json file path of the accounts'
        self.accounts.dest = 'account_json'
        self.accounts.required = True

        self.subcommand = argument.Parser('balance')
        self.subcommand.help = 'get eth balance on Era Mainnet'
        self.subcommand.func = self.subcommand_func
        self.subcommand.usage = 'trader [options] zksync balance [options]'

    def __run_get_balance(self) -> None:
        global accounts, account_balance

        while True:
            mutex = threading.Lock()
            mutex.acquire()
            if len(accounts) <= 0: break

            account, data = accounts[0], {}
            accounts.pop(0)

            addr = account['address']
            data['address'] = addr
            data['zks'] = self.get_balance(self.zksync, addr)
            data['eth'] = self.get_balance(self.ethereum, addr)
            account_balance.append(data)

            mutex.release()

    def subcommand_default_func(self, args, parent) -> None:
        global accounts, account_balance
        accounts, account_balance = self.import_accounts(args), []

        self.init_web3_provider()
        create_threading(args.thread, **{'target': self.__run_get_balance})

        for item in account_balance:
            trader.LOG.info(
                '[%s]: %s(zks) %s(eth)',
                item['address'], item['zks'], item['eth']
            )