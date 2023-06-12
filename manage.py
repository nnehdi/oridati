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

description = "A platform similar to Resident Advisor that provides information about upcoming music events, festivals, and concerts. The platform would allow users to search for events by location, genre, and date, and would provide detailed information about each event, including the lineup, venue, and ticket prices. Users could also create profiles to track their favorite artists and receive personalized recommendations for events based on their music preferences. The platform could generate revenue through ticket sales and partnerships with event organizers and sponsors. "
role_prompt = """
 You are OrigamiAnalyzer, a AI powered command line tool designed to gather data model specification from the client.  \
 You and client will work together by having a conversation cosidering followin points:

METHOD
Then You will take an iterative incremental approach to clarify and specify the data model with following phases:
  - FOCUS: choose one or two entities or user
  - IDENTIFY: find the possible relationship between them.
  - SPECIFY: clarify the type of relationships and attributes. 
  - REPEAT: reapeat the follwoing process until you specifiy the whole daatamodel.

Always provide helpful tips and examples, don't let client answer the whole questions.
You are not a chatbot, try to cut the bulltshit and go strait to the point. 

GOAL 
At the end of conversation you will have clearly specified the following info which are used to generate the FINAL OUTPUT.
 - Different type of  users or persona
 - Entitietis
 - Entitietis attributes
 - The relationship between those Entities
 - The relationship and interaction of users with Entities.

FINAL OUTPUT
When you get done specifying model, you will ask user if she doesn't have anything to add and agrees with the results \n
if not you output final data model desing in .prisma format delimited in <OUTPUT><OUTPUT>based on what you disscuss with client.
"""
context = [ {'role':'system', 'content': role_prompt}]  # accumulate messages

response = get_completion_from_messages(context)

print(context)
print(response)

exit_conditions = (":q", "quit", "exit")
while True:
    user_prompt = input("> ")
    if user_prompt in exit_conditions:
        break
    else:
        context.append({'role':'user','content':user_prompt})
        response = get_completion_from_messages(context)
        context.append({'role':'assistant','content':response})
        print(f"🪴 {response}")