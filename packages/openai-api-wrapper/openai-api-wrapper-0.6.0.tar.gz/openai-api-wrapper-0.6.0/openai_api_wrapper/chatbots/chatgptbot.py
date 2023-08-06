# -*- coding: utf-8 -*-
"""
This program defines a ChatGPTBot class that inherits from BaseChatBot. It uses the OpenAI API to
generate responses to user input. The class has properties for model parameters and a method for
initializing the ChatOpenAI model.

"""
import os
import openai
from langchain.chat_models import ChatOpenAI
from basechatbot import BaseChatBot

class ChatGPTBot(BaseChatBot):
    def __init__(self, template: str = None, human: str = "Human", assistant: str = "Assistant", company: str = "OpenAI", proxy: str = None, **kwargs):
        openai.proxy = proxy or os.getenv('OPENAI_PROXY')
        super(ChatGPTBot, self).__init__(human, assistant, company or "OpenAI", template, proxy, **kwargs)

    @property
    def _llm(self):
        return ChatOpenAI(**self.model_params)

    @property
    def _default_model_params(self):
        model_params = {
            'model_name': "gpt-3.5-turbo",
            'temperature': 0.95,
            'max_retries': 3,
            'streaming': False,
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'max_tokens': 2048,
            'top_p': 0.7,
            'presence_penalty': 0,
            'n': 1,
            'logit_bias': dict(),
        }
        return model_params

