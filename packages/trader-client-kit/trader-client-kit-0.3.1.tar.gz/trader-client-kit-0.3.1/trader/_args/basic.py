# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: argparse basic

import sys, trader

from .argument import Argument, Parser, Subparser

class ParserBasic(object):
    def __add_arguments__(self, parser) -> None:
        arguments = self.__dict__

        def check_to_add(key: str) -> None:
            arg = arguments[key]
            parser.add_argument(*arg.name, **arg.__argument__)

        for key in arguments.keys():
            if not isinstance(arguments[key], Argument):
                continue

            check_to_add(key)

    def subcommand_default_func(self, args, parent) -> None:
        if args.parent.dest != 'subparser':
            choices = getattr(args, args.parent.dest)
            command = args.parent.choices[choices]
            command.print_help()
        else:
            self.parent = parent
            command = args.parent.choices[args.subparser]
            command.print_help()

    def subcommand_func(self, args, parent) -> None:
        trader.LOG.warning(' '.join(sys.argv[1:]))
        self.subcommand_default_func(args, parent)
        trader.LOG.warning('Everything is done')

def init_argparser(basic: ParserBasic, parent) -> None:
    def init_add_parser(sub: object) -> object:
        command = sub.subcommand
        parser = parent.add_parser(command.name, **command.__parser__)
        func = sub.subcommand_func
        parser.set_defaults(func=func, parent=parent)
        sub.__add_arguments__(parser)

        return parser
    
    def check_to_init(sub: object) -> object:
        subcommand = sub.subcommand
        if isinstance(subcommand, Parser):
            return init_add_parser(sub)

        if isinstance(subcommand, Subparser):
            return parent.add_subparsers(**subcommand.__subparser__)

    for subclass in basic.__subclasses__():
        if subclass.__name__ == 'GeneralCommand': continue
        
        subparser = subclass()
        parser = check_to_init(subparser)

        if subclass.__subclasses__():
            init_argparser(subclass, parser)