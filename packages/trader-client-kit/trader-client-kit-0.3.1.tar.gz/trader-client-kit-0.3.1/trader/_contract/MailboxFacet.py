# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: MuteSwitchRouterDynamic setting

from web3 import Web3
from trader._utils import ContractBasic

class MailboxFacet(ContractBasic):
    def __init__(self, client: Web3) -> None:
        addr = '0x32400084C286CF3E17e7B677ea9583e60a000324'
        
        super().__init__(client, addr, [
            {
                "inputs":[
                    {
                        "internalType":"uint256",
                        "name":"_gasPrice",
                        "type":"uint256"
                    },
                    {
                        "internalType":"uint256",
                        "name":"_l2GasLimit",
                        "type":"uint256"
                    },
                    {
                        "internalType":"uint256",
                        "name":"_l2GasPerPubdataByteLimit",
                        "type":"uint256"
                    }
                ],
                "name":"l2TransactionBaseCost",
                "outputs":[
                    {
                        "internalType":"uint256",
                        "name":"",
                        "type":"uint256"
                    }
                ],
                "stateMutability":"pure",
                "type":"function"
            },
            {
                "inputs":[
                    {
                        "internalType":"address",
                        "name":"_contractL2",
                        "type":"address"
                    },
                    {
                        "internalType":"uint256",
                        "name":"_l2Value",
                        "type":"uint256"
                    },
                    {
                        "internalType":"bytes",
                        "name":"_calldata",
                        "type":"bytes"
                    },
                    {
                        "internalType":"uint256",
                        "name":"_l2GasLimit",
                        "type":"uint256"
                    },
                    {
                        "internalType":"uint256",
                        "name":"_l2GasPerPubdataByteLimit",
                        "type":"uint256"
                    },
                    {
                        "internalType":"bytes[]",
                        "name":"_factoryDeps",
                        "type":"bytes[]"
                    },
                    {
                        "internalType":"address",
                        "name":"_refundRecipient",
                        "type":"address"
                    }
                ],
                "name":"requestL2Transaction",
                "outputs":[
                    {
                        "internalType":"bytes32",
                        "name":"canonicalTxHash",
                        "type":"bytes32"
                    }
                ],
                "stateMutability":"payable",
                "type":"function"
            }
        ])