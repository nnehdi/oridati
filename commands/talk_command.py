from commands.Talk import DataModelDesignerTalk


class TalkCommand:
    def __init__(self, root_parser):
        talk_parser = root_parser.add_parser(
            "talk",
            help="A chatbot to design and generate the datamodel by interviewing the client!",
        )
        talk_parser.add_argument("--complete", action="store_true")
        talk_parser.add_argument("--generate-datamodel", action="store_true")
        talk_parser.add_argument("--generate-samples", action="store_true")
        talk_parser.set_defaults(func=do)


def do(args):
    talk = DataModelDesignerTalk(filepath="requirements.md")
    if args.complete:
        talk.complete()
        return
    elif args.generate_datamodel:
        talk.save_data_model()
        return
    elif args.generate_samples:
        talk.generate_samples()
        return

    exit_conditions = (":q", "quit", "exit")
    output_conditions = ("datamodel:prisma", "sample:json")
    while True:
        user_prompt = input("> ")
        if user_prompt in exit_conditions:
            break
        elif user_prompt in output_conditions:
            if user_prompt == "datamodel:prisma":
                talk.save_data_model()
            elif user_prompt == "sample:json":
                talk.generate_samples()
        else:
            user_prompt += "\n"
            response = talk.talk(user_prompt)
            print(f"🪴 {response}")
