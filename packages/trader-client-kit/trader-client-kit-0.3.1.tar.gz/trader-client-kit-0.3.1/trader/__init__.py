# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: application __init__

import os, sys, logging, configparser, argparse

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

from logging import config
from dotenv import find_dotenv, load_dotenv

class ExtraInfoAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['user'], msg), kwargs
    
def get_file(base, path): return os.path.join(ROOT_PATH, base, path)

config.fileConfig(get_file('_source', 'conf/logging.conf'))
LOG: logging.Logger = logging.getLogger('trader')
# LOG = ExtraInfoAdapter(LOG, {'user': 'main'})
# logging.getLogger('rustyrlp').setLevel(logging.WARNING)

CONF: configparser.ConfigParser = configparser.ConfigParser()
CONF.read(get_file('_source', 'conf/trader.conf'))

ARGPARSE_EIPLOG = CONF.get('trader', 'APPLICATION_EPILOG')
APPLICATION_VERSION = CONF.get('trader', 'APPLICATION_VERSION')

PARSER: argparse.ArgumentParser = argparse.ArgumentParser()

from trader import general, _utils
from ._args.basic import ParserBasic, init_argparser

from trader.common import *
from trader.eth import *
from trader.zksync import *

def main(argv=None):
    try:
        load_dotenv(find_dotenv(get_file('_source', 'conf/.env')))

        PARSER.prog = 'Trader Application'
        PARSER.usage = 'trader <command> [options]'
        info = 'Trader %s - a common tool for blockchain'
        PARSER.description = info % APPLICATION_VERSION
        PARSER.epilog = ARGPARSE_EIPLOG
        PARSER.formatter_class = _utils.CustomFormatter

        subparser = PARSER.add_subparsers()
        subparser.dest = 'subparser'
        subparser.title = 'required commands'
        subparser.metavar = ''

        general.GeneralCommand().__add_arguments__(PARSER)
        init_argparser(ParserBasic, subparser)

        args = PARSER.parse_args()
        if args.subparser: args.func(args, subparser)
        else: PARSER.print_help()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user \n')
    except Exception as e:
        LOG.error('__main__: %s' % str(e))

__all__ = ['main', 'LOG', 'CONF']