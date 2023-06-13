import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]


def save_data_model(data_model_str):
    with open('./data/datamodel.prisma', 'w+',encoding='utf-8') as fn:
        fn.write(data_model_str)
    
def gather_command(args):
    description = "A platform similar to Resident Advisor that provides information about upcoming music events, festivals, and concerts. The platform would allow users to search for events by location, genre, and date, and would provide detailed information about each event, including the lineup, venue, and ticket prices. Users could also create profiles to track their favorite artists and receive personalized recommendations for events based on their music preferences. The platform could generate revenue through ticket sales and partnerships with event organizers and sponsors. "
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
    context = [ {'role':'system', 'content': role_prompt},
    {'role':'assistant','content':'Hi I am OrigamiAnalyzer! We will be working to together to analyes users stories of your desire project to design the data model. please provide me the first user story.'},
    ]  # accumulate messages

    print(context)
    exit_conditions = (":q", "quit", "exit")
    output_conditions = (":output",)

    while True:
        user_prompt = input("> ")
        if user_prompt in exit_conditions:
            break
        elif user_prompt in output_conditions:
            output_context = context.copy()
            output_context.append({'role':'system','content':'Output the designed data model in .prisma format'})
            response = get_completion_from_messages(output_context)
            print("")
            print(f"{response}")
            try:
                prisma_str = response.split("```")[1]
                save_data_model(prisma_str)
            except IndexError:
                pass
                
        else:
            context.append({'role':'user','content':user_prompt})
            response = get_completion_from_messages(context)
            context.append({'role':'assistant','content':response})
            print(f"🪴 {response}")