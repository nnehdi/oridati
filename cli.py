from argparse import ArgumentParser
from commands.talk_command import TalkCommand
from commands.model_command import model_command


class OrigamiCLI:
    def __init__(self):
        self._parser = ArgumentParser(description="Web Origami cli tool!")
        sub_parsers = self._parser.add_subparsers(required=True)

        TalkCommand(sub_parsers)

        model_parser = sub_parsers.add_parser(
            "model", help="generate and managing the models"
        )
        model_parser.set_defaults(func=model_command)

    def run(self):
        args = self._parser.parse_args()
        args.func(args)
