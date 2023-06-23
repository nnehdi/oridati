
from commands.Talk import DataModelDesignerTalk

def talk_command(args):

    talk = DataModelDesignerTalk(filepath='requirements.md')
    exit_conditions = (":q", "quit", "exit")
    output_conditions = ("datamodel:prisma", "sample:json")
    talk.complete()
    while True:
        user_prompt = input("> ")
        if user_prompt in exit_conditions:
            break
        elif user_prompt in output_conditions:
            if user_prompt == "datamodel:prisma":
                talk.save_data_model()
            elif user_prompt == "sample:json":
                talk.save_samples()
        else:
            response = talk.talk(user_prompt)
            print(f"🪴 {response}")
