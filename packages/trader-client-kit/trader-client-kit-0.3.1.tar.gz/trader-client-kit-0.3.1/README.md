# 区块链相关操作工具大全

介绍: 该工具是为区块链工具大全，相关操作包含：智能合约、各类交易所API、自定义抢空投等

## 通用功能
批量创建链上钱包

    // -n/--number 需要创建的钱包数量，默认为10
    // 运行结束后会生成一个Account-XXXXXXXXXXXX.json文件保存在本地
    trader-cli common account --number 100

## zkSync Era Mainnet 空投
随机生成交易 (基于okx交易所提币)

    // -j/--json 需要交易的账号json文件路径
    // 批量账号可以通过 批量创建链上钱包 创建
    // 该操作需要输入OKX的APIKEY、SECREAT_KEY、PASSPHRASE
    // 申请地址: https://www.okx.com/docs-v5/zh/#overview
    // -t/--thread 线程数量 默认为1
    trader-cli zksync transfer --json path -t 10

查询钱包链上余额（包含主网、zkSync Era主网）

    // -j/--json 需要查询的账户列表（.json文件）必填
    // -t/--thread 线程数量 默认为1
    trader-cli zksync balance -j path -t 10

OKX交易所提币并跨链到zkSync Era主网

    // -a/--amount 需要提币的金额（每个账户都一样）
    // -j/--json 需要查询的账户列表（.json文件）必填
    // -t/--thread 线程数量 默认为1
    trader-cli zksync withdraw -a 0.1 -j path -t 10