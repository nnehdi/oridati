
from commands.Talk import Conversation, Talk
import os
import json

def save_data_model(data_model_str):
    with open('./schema.prisma', 'w+', encoding='utf-8') as fn:
        fn.write(data_model_str)

def save_samples(json_str):
    with open('./samples.json', 'w+', encoding='utf-8') as fn:
        fn.write(json.dumps(json.loads(json_str)))

def gather_command(args):
    role_prompt = """
    You are OrigamiAnalyzer, a AI powered command line tool designed to gather DATA MODEL SPECIFICATION from the client.  \
    You and client will work together by having a conversation cosidering followin points:

    METHOD
    Your goal is to clarify the DATA MODEL SPECIFICATION step by step.
    You will iterate over different user stories one by one,For each user story you follow these steps:
    - FOCUS: You focus on one user story or usecase.
    - ASSUME: Analyze the chosen user story and provide client with users,entities and relationshiop that you infered from the story.
    - INTERACT: interact with client to verify and extend your assume.
    - REPEAT: reapeat the process, with each step you make the DATA MODEL SPECIFICATION more clear.

    In each interaction during the conversation, first provide your tips or assumption, then ask your question.
    Ask one question at the time.Try to cut the bullshit and go strait to the point. 

    DATA MODEL SPECIFICATION
    A specification contains the following sections.
    - Different type of  users or persona
    - Entitietis
    - Entitietis attributes
    - The relationship between those Entities
    - The relationship and interaction of users with Entities.

    """
    OUTPUT_JSON_COMMAND = """
    Output few sample data for each entity in the generated .prisma model. 
    Use the exact naming for Entities and their attributes.
    Fill in id's and foreign keys to represent the relationship between the entities.
    It output should be a series of prisma create query. 

    """
    conversation = Conversation(filepath='requirements.md')
    conversation.config(role_prompt)
    conversation.load()
    if not len(conversation):
        conversation.assistant(
            'Hi I am OrigamiAnalyzer! We will be working to together to analyes users stories of your desire project to design the data model. please provide me the first user story.')
    talk = Talk(conversation)
    exit_conditions = (":q", "quit", "exit")
    output_conditions = ("datamodel:prisma", "sample:json")
    talk.complete()
    while True:
        user_prompt = input("> ")
        if user_prompt in exit_conditions:
            break
        elif user_prompt in output_conditions:
            if user_prompt == "datamodel:prisma":
                response = talk.talk(
                    ['Output the designed data model in .prisma format'])
                print("")
                print(f"{response}")
                try:
                    prisma_str = response.split("```")[1]
                    save_data_model(prisma_str)
                except IndexError:
                    pass
            elif user_prompt == "sample:json":
                commands = [
                    'Output the designed data model in .prisma format', OUTPUT_JSON_COMMAND
                ]
                response = talk.talk(commands)
                print("")
                print(f"{response}")
                try:
                    json_str = response.split("```")[1]
                    save_samples(json_str)
                except IndexError:
                    pass

        else:
            response = talk.talk(user_prompt)
            print(f"🪴 {response}")
