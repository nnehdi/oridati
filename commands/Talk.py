import os
import openai
import copy
import warnings

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY')


class Conversation:
    def __init__(self,filepath,messages=list()):
        self._messages = messages
        self._filepath = filepath

    def load(self):
        if not os.path.exists(self._filepath):
            return False
        self._messages = []
        warnings.warn(f"Loading file from {self._filepath}!")
        try:
            with open(self._filepath, 'r') as file:
                lines = file.readlines()
        except OSError:
            lines = list()
        current_role = None
        current_content = ""

        for line in lines:
            line = line

            if line.startswith("### user"):
                if current_role:
                    self._messages.append({'role':current_role, 'content':current_content})
                    current_content = ""

                current_role = "user"

            elif line.startswith("### assistant"):
                if current_role:
                    self._messages.append({'role':current_role, 'content':current_content.strip()})
                    current_content = ""

                current_role = "assistant"

            elif line.startswith("### system"):
                if current_role:
                    self._messages.append({'role':current_role, 'content':current_content.strip()})
                    current_content = ""

                current_role = "system"

            else:
                current_content += line

        if current_role:
            self._messages.append({'role':current_role, 'content':current_content})
        
        print(self._messages)
        return True

    def save(self):
        with open(self._filepath, 'w+') as file:
            for msg in self._messages:
                if msg != '\n':
                    file.write(f"### {msg['role']}\n{msg['content']}\n")

    def __len__(self):
        return len(self._messages)

    def __getitem__(self, position):
        return self._messages[position]

    def _add_msg(self, role, content):
        self._messages.append(
            {
                "role": role,
                "content": content
            }
        )
    def config(self, content):
        self._messages.insert(0,{
            'role': 'system',
            'content': content
        })

    def user(self, content):
        self._add_msg('user', content)

    def assistant(self, content):
        self._add_msg('assistant', content)

    def system(self, content):
        self._add_msg('system', content)

class ModelAdapter:
    def __init__(self, model="gpt-3.5-turbo"):
        self._model = model

    def get_completion(self, messages, temperature=0):
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=list(messages),
            temperature=temperature,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]

class Talk:
    def __init__(self, conversation, autosave = True):
        self._conversation = conversation
        self._model = ModelAdapter()
        self._autosave = autosave

    def talk(self, prompt=None):
        if prompt:
            self._conversation.user(prompt)
        response = self._model.get_completion(self._conversation)
        self._conversation.assistant(response)
        if self._autosave:
            self._conversation.save()
        return response
    
    def complete(self):
        if self._conversation[-1]['role'] != 'assistant':
            self.talk()