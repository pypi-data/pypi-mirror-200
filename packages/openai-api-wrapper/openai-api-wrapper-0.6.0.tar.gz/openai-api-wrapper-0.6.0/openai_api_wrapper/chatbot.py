import os, json
import time, uuid
from typing import Optional, List, Dict
import openai

class ChatBot:
    """
    A wrapper for the OpenAI API to interact with the ChatGPT model.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        engine: str = "gpt-3.5-turbo",
        # max_tokens: int = 3000,
        temperature: float = 0.5,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        proxy: str = None,
        max_turns: int = -1,
        max_retries: int = 3,
        keep_round: int = 2,
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        """
        Initialize the Chatbot class.

        :param api_key: OpenAI API key, defaults to None.
        :param engine: GPT engine to use, defaults to "gpt-3.5-turbo".
        # :param max_tokens: Maximum number of tokens to generate, defaults to 3000.
        :param temperature: Sampling temperature, lower values make the output more focused and deterministic, defaults to 0.5.
        :param top_p: The nucleus sampling parameter, set to 1.0 to disable, defaults to 1.0.
        :param presence_penalty: Controls the model's tendency to repeat itself, defaults to 0.0.
        :param frequency_penalty: Controls the model's use of less frequent words, defaults to 0.0.
        :param proxy: Optional proxy setting like "socks://<proxy_server>:<proxy_port>" or "http://<proxy_server:proxy_port>", defaults to None. 
        :param max_turns: Maximum number of turns per conversation, defaults to -1 for unlimited turns.
        :param max_retries: Number of retries to ask the model if the response is empty, defaults to 3.
        :param keep_round: Number of rounds to keep in the conversation history, defaults to 2.
        :param system_prompt: The prompt for the system messages, defaults to "You are a helpful assistant."
        """
        self.engine = engine
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.api_key
        # self.max_tokens = max_tokens or 3000
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_retries = max_retries

        openai.proxy = proxy or os.environ.get("OPENAI_PROXY")

        self.conversations = {}
        self.system_contents = {}
        self.max_turns = max_turns

        self.keep_round = keep_round
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def start_conversation(self, conversation_id: str = "default", system_content : str = "You are a helpful assistant.") -> None:
        """
        Start a new conversation with the given conversation_id.

        :param conversation_id: The unique identifier for the conversation.
        :param system_content: The content of the system message, defaults to "You are a helpful assistant."
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
            self.system_contents[conversation_id] = system_content 
    
    def remove_conversation(self, conversation_id: str = "default") -> None:
        """
        Remove a conversation from the conversation history.

        :param conversation_id: The unique identifier for the conversation.
        """
        if conversation_id in self.conversations:
            self.conversations.pop(conversation_id)
            self.system_contents.pop(conversation_id)

    def add_message(self, message: str, role: str, conversation_id: str = "default") -> None:
        """
        Add a message to the conversation.

        :param message: The content of the message.
        :param role: The role of the message sender, either "user" or "assistant".
        :param conversation_id: The unique identifier for the conversation, defaults to "default".
        """
        if self.max_turns > 0 and len(self.conversations[conversation_id]) >= self.max_turns:
            raise ValueError(f"Cannot add more messages. Maximum turns of {self.max_turns} reached.")
        
        self.conversations[conversation_id].append({"role": role, "content": message})

    def get_last_reply_content(self, conversation_id: str = "default") -> str:
        """
        Get the last response from the conversation.

        :param conversation_id: The unique identifier for the conversation, defaults to "default".
        :return: The last response from the conversation.
        """
        if len(self.conversations[conversation_id]) == 0:
            return ""

        return self.conversations[conversation_id][-1]["content"] 
        

    def get_conversation_turns(self, conversation_id: str = "default") -> int:
        """
        Get the number of turns in the conversation.

        :param conversation_id: The unique identifier for the conversation, defaults to "default".
        :return: The number of turns in the conversation.
        """
        return len(self.conversations[conversation_id]) // 2

    def get_token_count(self, text: str) -> int:
        """
        Get the token count of the given text.

        :param text: The text to count tokens for.
        :return: The number of tokens in the text.
        """
        return len(openai.api_utils.tokens_of_string(text))

    def _chat_completion(self, prompt: str = None, messages: List[Dict[str, str]] = None, role: str = "user", conversation_id: str = "default", stream: bool = False) -> openai.ChatCompletion:
        """
        Generate a response for the given prompt.
        :param prompt: The user's input to generate a response for.
        :param role: The role of the message sender, either "user" or "assistant".
        :param conversation_id: The unique identifier for the conversation, defaults to "default".
        :return: The response from the model.
        """
        assert prompt is not None or messages is not None, "Either prompt or messages must be provided."

        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=messages or 
            [
                {
                    "role": "system",
                    # "content": self.system_contents[conversation_id]
                    "content": self.system_prompt
                },
                {
                    "role": role,
                    "content": prompt
                },
            ],
            temperature=self.temperature,
            # max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            n=1,
            stream=stream,
        )

        return response

    def ask_stream_iterator(self, prompt: str, role: str = "user", conversation_id: str = "default"):
        """
        Generate a response to the given prompt using streaming API.
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb

        :param prompt: The user's input to generate a response for.
        :param role: The role of the message sender, either "user" or "assistant".
        :param conversation_id: The unique identifier for the conversation, defaults to "default".
        :return: A generator yielding chunks of the generated response.
        """
        self.start_conversation(conversation_id)
        self.add_message(prompt, role=role, conversation_id=conversation_id)

        retries = 0
        while retries < self.max_retries:
            retries += 1

            try:
                response = self._chat_completion(prompt = prompt, role=role, conversation_id=conversation_id, stream=True)
                collected_messages = []
                for chunk in response:
                    chunk_message = chunk['choices'][0]['delta']
                    collected_messages.append(chunk_message)
                    yield chunk_message.get("content", '')
        
                reply_content = ''.join([m.get('content', '') for m in collected_messages])
                self.add_message(reply_content, role="assistant", conversation_id=conversation_id)
            except openai.error.APIConnectionError as e:
                print(f"Error: {e}")
                print(f"Retrying... ({retries}/{self.max_retries})")
                time.sleep(1)
                continue



    def ask(self, prompt: str, role: str = "user", conversation_id: str = "default", stream=False) -> str:
        """
        Generate a response to the given prompt.

        :param prompt: The user's input to generate a response for.
        :param role: The role of the message sender, either "user" or "assistant".
        :param conversation_id: The unique identifier for the conversation, defaults to "default".
        :param stream: Whether to use the streaming API.
        :return: The generated response.
        """
        self.start_conversation(conversation_id)
        self.add_message(prompt, role=role, conversation_id=conversation_id)

        retries = 0
        while retries < self.max_retries:
            retries += 1

            try:
                response = self._chat_completion(prompt=prompt, role=role, conversation_id=conversation_id, stream=stream)
                if stream:
                    unfinished_reply_content= ""
                    for chunked_reply_content in self.ask_stream_iterator(prompt, conversation_id=conversation_id):
                        unfinished_reply_content+= chunked_reply_content
                        print(unfinished_reply_content)
                    reply_content= self.get_last_reply_content(conversation_id)
                else:
                    reply_content = response.choices[0].message.content.strip()
                    self.add_message(reply_content, role="assistant", conversation_id=conversation_id)
            except openai.error.APIConnectionError as e:
                print(f"Error: {e}")
                print(f"Retrying... ({retries}/{self.max_retries})")
                time.sleep(1)
                continue


        return reply_content

    def send_msg(self, messages: List[Dict[str,str]], role: str = "user", conversation_id: str = "default", stream: bool = False):
        """
        Send a message to the assistant.

        :param msg: The message to send to the assistant.
        :return: The assistant's response.
        """
        # if self.conversation_id is None:
        #     self.conversation_id = str(uuid.uuid4())

        # if self.conversation_turns == 0:
        #     self.conversation_start_time = time.time()
            
        # self.conversation_turns += 1

        # prompt = self._get_prompt(msg)
        # reply = self._get_reply(prompt)

        self.start_conversation(conversation_id)
        # self.add_message(prompt, role=role, conversation_id=conversation_id)

        retries = 0
        while retries < self.max_retries:
            retries += 1

            try:
                response = self._chat_completion(messages=messages, conversation_id=conversation_id, stream=stream)
                reply_content = response.choices[0].message.content.strip()
            except openai.error.APIConnectionError as e:
                print(f"Error: {e}")
                print(f"Retrying... ({retries}/{self.max_retries})")
                time.sleep(1)
                continue

        return reply_content

    def chat(self, message):
        # This method is used to send a message and get a response from the OpenAI API
        print(f"Total messages: {len(self.messages)}\nfirst_message: {self.messages[0]}\n")

        # Adding the user message to the conversation messages
        self.messages.append({"role": "user", "content": message})
        # Sending the messages to the API and getting the response
        response = self.send_msg(self.messages)
        # Adding the system response to the conversation messages
        self.messages.append({"role": "assistant", "content": response})
        # Dropping previous conversation messages to keep the conversation history short
        self.messages = self._drop_conversation(self.messages)
        # Returning the system response
        return response
        
    def _drop_conversation(self, msg):
        # This method is used to drop previous messages from the conversation and keep only recent ones
        if len(msg) >= (self.keep_round + 1) * 2 + 1:
            # new_msg = [msg[0]]
            new_msg = [{"role": "assistant", "content": self.system_prompt}]
            for i in range(3, len(msg)):
                new_msg.append(msg[i])
            return new_msg
        else:
            return msg