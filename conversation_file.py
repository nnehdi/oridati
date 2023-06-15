class ConversationFile:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.conversation = []

    def load(self, filepath):
        self.filepath = filepath
        self.conversation = []

        with open(filepath, 'r') as file:
            lines = file.readlines()

        current_role = None
        current_content = ""

        for line in lines:
            line = line.strip()

            if line.startswith("User:"):
                if current_role:
                    self.conversation.append((current_role, current_content.strip()))
                    current_content = ""

                current_role = "User"
                current_content += line[len("User:"):].strip()

            elif line.startswith("Assistant:"):
                if current_role:
                    self.conversation.append((current_role, current_content.strip()))
                    current_content = ""

                current_role = "Assistant"
                current_content += line[len("Assistant:"):].strip()

            else:
                current_content += line.strip()

        if current_role:
            self.conversation.append((current_role, current_content.strip()))

    def save(self, filepath=None):
        if not filepath:
            filepath = self.filepath

        with open(filepath, 'w') as file:
            for turn in self.conversation:
                role, content = turn
                file.write(f"{role}: {content}\n")

    def add_turn(self, role, content):
        self.conversation.append((role, content))

    def get_conversation(self):
        return self.conversation
