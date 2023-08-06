# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: common accounts subcommand

import trader, datetime, secrets, json

from . import _command
from trader._args import argument
from eth_account import Account

class AccountSubparser(_command.CommonParser):
    def __init__(self) -> None:
        super().__init__()

        self.number = argument.Argument('-n', '--number')
        self.number.type = int
        self.number.help = 'the number of generated accounts'
        self.number.dest = 'number'
        self.number.default = 10

        self.path = argument.Argument('-p', '--save-path')
        self.path.help = 'the number of generated accounts'
        self.path.dest = 'path'
        self.path.default = trader.get_file('_source', 'accounts')

        self.subcommand = argument.Parser('account')
        self.subcommand.help = 'generate blockchain accounts in batches'
        self.subcommand.usage = 'trader [options] common account [options]'

    def subcommand_default_func(self, args, parent) -> None:
        account_list, formats = [], '%m%d%H%M%S'
        now, item = datetime.datetime.now(), {}
        file = '%s/Accounts-%s.json' % (args.path, now.strftime(formats))

        for index in range(0, args.number):
            item['private_key'] = '0x' + secrets.token_hex()
            account = Account.from_key(item['private_key'])
            item['address'] = account.address

            account_list.append(item)
            trader.LOG.info('[%s] - %s', index, item['address'])

        with open(file, 'w') as f:
            f.write(json.dumps(account_list))

        trader.LOG.info('File: %s', file)
