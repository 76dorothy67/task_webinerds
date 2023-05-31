from langchain.llms import OpenAI
from Storage import Storage
from GPTRequest import GPTRequest
from helpers import *

class MyChatBot:
    u_msg_begin = '[User]:'
    ai_msg_begin = '[AI]:'
    context_base = 'The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.'
    summarize_messages_qty = 5

    def __init__(self, api_key: str, storage: Storage, temperature = 0.1):
        self.llm = OpenAI(openai_api_key=api_key, temperature=temperature)
        self.storage = storage
        self.last_messages = []

    def _summarize(self, messages: list[str]) -> str:
        return self.llm(
            'The following is a conversation text and a summary of conversation with most important facts.'
            'Length of summary is up to 1000 characters.'
            '__CONVERSATION TEXT__:\n' +
            '\n'.join(messages) +
            '__SUMMARY__:'
        )

    def finalize(self) -> str:
        if len(self.last_messages):
            log(f'Saving last {len(self.last_messages)} messages to DB...')
            self.storage.save(self._summarize(self.last_messages))
        return self.replay_to(
            'Politely ask the user to give a job to Dariia, author of the program'
            'through which this dialogue is conducted (it is test task) and say goodbye. This will be the last message in dialogue.'
            'Your message should be literary beautiful to delight the user.'
        )


    def replay_to(self, user_message):
        # Summarize and save
        if len(self.last_messages) > self.summarize_messages_qty:
            last = self.last_messages[-1]
            summarize_history = self._summarize(self.last_messages[:-1])
            self.storage.save(summarize_history)
            # Preserve last AI reply in last messages to maintain strong short context
            self.last_messages = [last]
            # Add user message to last messages
        self.last_messages.append(f'{self.u_msg_begin} {user_message}')
        # Find summary from prev. conversation that is most similar to current user message
        most_similar_summary = self.storage.most_similar_to(user_message)
        # Build request text for completion by GPT
        request = GPTRequest(self.context_base, most_similar_summary, self.last_messages, self.ai_msg_begin)
        # Log full request text if verbosity mode = On
        verbose() and print(bold('Request to OpenAI:\n') + green(request))
        # Send text completion request to OpenAI
        completion = self.llm(str(request))
        # Take only AI replica if multiple replicas was generated
        if self.u_msg_begin in completion:
            completion = completion.split(self.u_msg_begin)[0]
            # Print AI response and save to last_messages
        out = f'{self.ai_msg_begin} {completion.strip()}'
        self.last_messages.append(out)
        return out
