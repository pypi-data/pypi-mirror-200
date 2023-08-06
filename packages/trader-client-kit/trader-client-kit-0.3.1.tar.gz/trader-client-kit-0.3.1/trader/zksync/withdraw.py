# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: zkSync withdrawal subcommand

import trader, getpass, threading, time, random

from . import _command
from trader._args import argument
from trader._utils import create_threading
from trader._contract import MailboxFacet

from web3 import Web3, exceptions
from okx import Funding

class WidthdrawSubparser(_command.ZksyncParser, _command.ZksyncBasic):
    def __init__(self) -> None:
        super().__init__()

        self.amount = argument.Argument('-a', '--amount')
        self.amount.type = float
        self.amount.help = 'the amount of to transfer per account'
        self.amount.dest = 'amount'
        self.amount.default = 0.03

        self.subcommand = argument.Parser('withdraw')
        self.subcommand.help = 'withdraw token from the Okx to Era Mainnet'
        self.subcommand.func = self.subcommand_func
        self.subcommand.usage = 'trader [options] zksync withdraw [options]'

        self.zksync: Web3 = None
        self.ethereum: Web3 = None
        self.MAILBOX: MailboxFacet.MailboxFacet = None

        self.funding, self.args = None, None
        self.config, self.withdraw_data = {}, {}

        self.withdraw_data['ccy'] = 'ETH'
        self.withdraw_data['dest'] = '4'
        self.withdraw_data['fee'] = '0'
        self.withdraw_data['chain'] = 'ETH-ERC20'
        self.withdraw_data['amt'] = 0

    def __init_okxsdk(self, total, funding=None) -> Funding.FundingAPI:
        def real_init_okxsdk(config: dict) -> tuple:
            funding = Funding.FundingAPI(**config)

            # 获取账户余额后输出用以判断OKX的API链接是否成功
            result = funding.get_balances('ETH')
            if result['code'] != '0': return (False, result['msg'], None)

            availBal = result['data'][0]['availBal']
            trader.LOG.info('Okx login successful ...')
            trader.LOG.info('ETH Balance: [%s]', availBal)

            # 如果可用余额小于要提币的金额*总的账户数量则提示余额不足
            if float(availBal) < float(total) * float(self.args.amount):
                trader.PARSER.error('Insufficient ETH balance')

            return (True, result['msg'], funding)

        while True:
            # 如果OKX的API链接失败则重复以下操作
            info, config = 'Please enter apikey: ', {}
            config['api_key'] = getpass.getpass(info)

            info = 'Please enter secret key: '
            config['api_secret_key'] = getpass.getpass(info)

            info = 'Please enter subaccount passphrase: '
            config['passphrase'] = getpass.getpass(info)
            
            config['flag'], config['debug'] = '0', False

            status, msg, funding = real_init_okxsdk(config)
            if status == True: break

            trader.LOG.info(msg)
            print('\nContinue? (y/n): ')
            if input() == 'n': trader.PARSER.exit()

        return funding
    
    def __get_withdrawal_history(self, filteres: dict) -> str:
        # 这里是查询提币记录用于判断提币是否成功
        result = self.funding.get_withdrawal_history(**filteres)
        if result['code'] != '0': '-1'

        time.sleep(random.randint(10, 20))
        return result['data'][0]['state']
    
    def __get_currencies(self) -> str:
        # 获取OKX提币的手续费
        result = self.funding.get_currencies('ETH')
        if result['code'] != '0': return '0'
        ERC20 = next(filter(lambda x: x['chain'] == 'ETH-ERC20', result['data']))
        return ERC20['minFee']
    
    def __funding_withdrawal(self, account: dict) -> bool:
        # 从OKX进行提币操作
        self.withdraw_data['toAddr'] = account['address']
        addr = self.withdraw_data['toAddr'][38:]

        # 获取OKX提币的手续费
        self.withdraw_data['fee'] = self.__get_currencies()
        trader.LOG.info('Start to withdrawal ...')
        trader.LOG.debug(self.withdraw_data)

        # 执行OKX的提币函数
        result = self.funding.withdrawal(**self.withdraw_data)
        trader.LOG.info('[%s] - [%s] - %s', addr, result['code'], result['msg'])
        if result['code'] != '0': return False

        filteres, info = {}, '[%s] - [%s] - [%s]'
        filteres['limit'] = 1
        filteres['wdId'] = result['data']['wdId']
        filteres['ccy'] = self.withdraw_data['ccy']

        while True:
            # 根据wdId查询OKX提币是否成功，如果状态是-3、-2、-1则提币失败
            state = self.__get_withdrawal_history(filteres)
            trader.LOG.info(info, addr, filteres['wdId'], state)

            if state != '2': continue
            if state in ['-3', '-2', '-1']: return False

            return True
        
    def __get_basecost(self) -> int:
        # 获取跨链的手续费（需要加到value里面）
        price = self.ethereum.eth.gas_price + 10000000000
        func = self.MAILBOX.contract.functions.l2TransactionBaseCost
        return self.MAILBOX.call(func, price, 694246, 800)
        
    def __deposit_to_zksync(self, account: dict) -> None:
        # 从以太主网跨链（https://bridge.zksync.io/）
        addr, pk = account['address'], account['private_key']
        amount = self.ethereum.toWei(self.args.amount, 'ether')
        trader.LOG.info('[%s] - Start to deposit ...', addr[38:])

        # 获取跨链的手续费（需要加到value里面）
        cost = self.__get_basecost() + amount
        cost = self.ethereum.fromWei(cost, 'ether')
        trader.LOG.debug('Base Cost: %s', cost)

        # 执行合约的跨链函数（有时候因为gas的原因可能会导致交易查不到）
        request = self.MAILBOX.contract.functions.requestL2Transaction
        tx_hash = self.MAILBOX.send(request, pk, cost, addr, amount, b'', 694246, 800, [], addr)
        time.sleep(random.randint(30, 60))

        while True:
            try:
                # 根据txId查询链上交易状态
                receipt = self.ethereum.eth.get_transaction_receipt(tx_hash.hex())
                if receipt['status'] == 1: break

                trader.LOG.debug(receipt)
                info = '(Deposit Status)[%s] - [%s]'
                trader.LOG.info(info, addr[38:], receipt['status'])

                time.sleep(random.randint(10, 20))
            except exceptions.TransactionNotFound as notfound:
                trader.LOG.info(str(notfound))

        trader.LOG.info('[%s] - SUCCESS', addr)
    
    def __run_withdrawal(self) -> None:
        global accounts

        while True:
            mutex = threading.Lock()
            mutex.acquire()
            if len(accounts) <= 0: break

            account = accounts[0]
            accounts.pop(0)

            try:
                # 执行OKX的提币
                is_withdraw = self.__funding_withdrawal(account)
                if not is_withdraw: continue

                # 执行合约的跨链函数
                self.__deposit_to_zksync(account)

                # 跨链成功后去查询一下ETH余额
                self.get_balance(self.zksync, account['address'])
            except Exception as e:
                trader.LOG.error(e)
                trader.LOG.debug(account['address'])

            mutex.acquire()

    def subcommand_default_func(self, args, parent) -> None:
        # 根据json文件导入本次要操作的所有账户
        # 账户可以用trader-cli common account -n 100 命令创建
        global accounts, account_balance
        accounts, account_balance = self.import_accounts(args), []

        # 根据输入的配置实例OKX的SDK
        self.args = args
        self.funding = self.__init_okxsdk(len(accounts))

        # 实例web3和跨链的合约
        self.withdraw_data['amt'] = str(args.amount)
        self.init_web3_provider()
        self.MAILBOX = MailboxFacet.MailboxFacet(self.ethereum)

        # 根据配置创建对应数量的线程
        create_threading(args.thread, **{'target': self.__run_withdrawal})