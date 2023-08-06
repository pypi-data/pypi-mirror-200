# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: utils __init__

import trader, argparse, threading, time

from web3 import Web3, contract
from web3.contract import ContractFunction
from eth_account import Account
from hexbytes import HexBytes

class CustomFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            # if metavar: metavar = 'trader ' + metavar
            return metavar
        else:
            option_strings = list(action.option_strings)
            return ', '.join(option_strings)

class ContractBasic(object):
    def __init__(
        self, client: Web3, addr: str=None, abi: list=[]
    ) -> None:
        self.address = addr
        self.client: Web3 = client

        self.__config = {}
        self.__config['address'] = addr
        self.__config['abi'] = abi

        self.contract: contract = self.__init_contract()

    def __init_contract(self) -> contract:
        if not self.__config['abi']: return None
        return self.client.eth.contract(**self.__config)
    
    def __get_transaction(self, addr: str, value: int) -> dict:
        transaction = {}

        transaction['from'] = addr
        transaction['gasPrice'] = self.client.eth.gas_price
        transaction['nonce'] = self.client.eth.get_transaction_count(addr)

        if value: transaction['value'] = self.client.toWei(value, 'ether')
        trader.LOG.debug(transaction)

        return transaction
    
    def call(self, function: ContractFunction, *args) -> any:
        return function(*args).call()
    
    def send(
        self, function: ContractFunction, private_key: str, value: int, *args
    ) -> HexBytes:
        account = Account.from_key(private_key)
        addr = account.address

        trader.LOG.info('[%s]: %s()', addr[38:], function.__class__.__name__)
        trader.LOG.debug(args)

        transaction = self.__get_transaction(addr, value)
        transaction_txn = function(*args).build_transaction(transaction)

        sign_transaction = self.client.eth.account.sign_transaction(
            transaction_txn, private_key
        )

        tx_hash = self.client.eth.send_raw_transaction(
            sign_transaction.rawTransaction
        )

        trader.LOG.info('TX HASH: ' + tx_hash.hex())

        return tx_hash

def parse_to_argument(arguments: dict, fil: list) -> dict:
    result_argument = {}

    for k in arguments.keys():
        if k in fil or arguments[k] is None: continue
        result_argument[k] = arguments[k]

    return result_argument

def create_threading(thread, **kwargs) -> None:
    thread_list = []

    for index in range(0, thread):
        th = threading.Thread(**kwargs)
        thread_list.append(th)
        th.start()

        trader.LOG.info('%s [%s] - start', th.name, index)
        time.sleep(0.5)

    for index, th in enumerate(thread_list):
        th.join()
        trader.LOG.info('%s [%s] - done', th.name, index)

def get_oxylabs_proxy(node: str) -> dict:
    proxy_url = trader.CONF.get('proxy', node)
    trader.LOG.debug('[proxy] - [%s]', node)

    return {'HTTP': proxy_url, 'HTTPS': proxy_url}

def get_web3_provider(network: str, proxy: str=None) -> Web3:
    host = trader.CONF.get(network, 'RPC')
    trader.LOG.debug('[network] - [%s]', host)

    if proxy is None: return Web3(Web3.HTTPProvider(host))

    return Web3(Web3.HTTPProvider(host, request_kwargs={
        'proxies': get_oxylabs_proxy(proxy)
    }))
