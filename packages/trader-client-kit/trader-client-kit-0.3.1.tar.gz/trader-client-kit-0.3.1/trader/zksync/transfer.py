# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: zkSync subcommand

import trader, threading, time, random

from . import _command
from trader._args import argument
from trader._utils import get_web3_provider, create_threading

from trader._contract import IERC20, MuteSwitchRouterDynamic

class TransferSubparser(_command.ZksyncParser, _command.ZksyncBasic):
    def __init__(self) -> None:
        super().__init__()

        self.subcommand = argument.Parser('transfer')
        self.subcommand.help = 'make transfer for zkSync on Era Mainnet'
        self.subcommand.func = self.subcommand_func
        self.subcommand.usage = 'trader [options] zksync transfer [options]'

        self.IERC20: IERC20.IERC20 = None
        self.SWAP: MuteSwitchRouterDynamic.MuteSwitchRouterDynamic = None

        self.ETH  = trader.CONF.get('zksync', 'ETH')
        self.USDC = trader.CONF.get('zksync', 'USDC')

    def __balance_of(self, account) -> int:
        balanceOf = self.IERC20.contract.functions.balanceOf
        return self.IERC20.call(balanceOf, account['address'])
    
    def __get_amount_out(self, amount, token_in: str, token_out: str) -> int:
        out = self.SWAP.contract.functions.getAmountOut
        result = self.SWAP.call(out, amount, token_in, token_out)
        return result[0]
        
        # return self.SWAP.fromWei(result[0], 'mwei')

    def __approve_to(self, account: dict, amount: int) -> None:
        pk, spender = account['private_key'], self.SWAP.address
        approve = self.IERC20.contract.functions.approve
        self.IERC20.send(approve, pk, 0, spender, amount)

    def __swap_usdc_to_eth(self, account: dict, usdc: int) -> None:
        allowance = self.IERC20.contract.function.allowance
        amount = self.IERC20.call(allowance, account['address'], self.SWAP.address)
        amount = self.IERC20.client.fromWei(amount, 'mwei')
        usdc_balance = self.IERC20.client.fromWei(usdc, 'mwei')
        approve_amt =  self.IERC20.client.toWei(1000, 'mwei')

        if amount < usdc_balance: self.__approve_to(account, approve_amt)

        amount_in, pk = usdc, account['private_key']
        out_min = self.__get_amount_out(usdc, self.USDC, self.ETH)
        to, deadline = account['address'], int(time.time()) + 120
        path, stable = [self.USDC, self.ETH], [False, False]

        swap = self.SWAP.contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens
        self.SWAP.send(swap, pk, 0, amount_in, out_min, path, to, deadline, stable)

    def __swap_eth_to_usdc(self, account: dict) -> None:
        percent, pk = random.randint(2, 5), account['private_key']
        eth = self.SWAP.client.eth.get_balance(account['address'])
        eth = self.SWAP.client.fromWei(eth, 'ether')

        # amount = self.SWAP.client.toWei('0.01', 'ether')
        amount = self.SWAP.client.toWei(eth * percent / 10, 'ether')

        out_min = self.__get_amount_out(amount, self.ETH, self.USDC)
        to, deadline = account['address'], int(time.time()) + 120
        path, stable = [self.ETH, self.USDC], [False, False]

        swap = self.SWAP.contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens
        self.SWAP.send(swap, pk, eth, out_min, path, to, deadline, stable)

    def __run_swap_transaction(self) -> None:
        global accounts

        def run_swap(account: dict, usdc: int) -> None:
            if usdc <= 0: self.__swap_eth_to_usdc(account)
            else: self.__swap_usdc_to_eth(account, usdc)

        while True:
            mutex = threading.Lock()
            mutex.acquire()
            if len(accounts) <= 0: break

            account = accounts[0]
            accounts.pop(0)

            usdc = self.__balance_of(account)
            run_swap(account, usdc)

            mutex.release()
            time.sleep(random.randint(30, 60))

    def subcommand_default_func(self, args, parent) -> None:
        global accounts

        accounts = self.import_accounts(args)
        client = get_web3_provider('zksync', 'HONG_KONG')
        self.IERC20 = IERC20.IERC20(client, self.USDC)
        self.SWAP = MuteSwitchRouterDynamic.MuteSwitchRouterDynamic(client)

        create_threading(args.thread, **{'target': self.__run_swap_transaction})