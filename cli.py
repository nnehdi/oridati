
from argparse import ArgumentParser
from commands.gather_command import gather_command

class OrigamiCLI:
    def __init__(self):
        self._parser = ArgumentParser(description="Data Origami cli tool!")
        sub_parsers = self._parser.add_subparsers(required=True)
        gather_parser = sub_parsers.add_parser('gather', help="A chatbot to design and generate the datamodel by interviewing the client!")
        gather_parser.set_defaults(func=gather_command)

    def run(self):
        args = self._parser.parse_args()
        args.func(args)