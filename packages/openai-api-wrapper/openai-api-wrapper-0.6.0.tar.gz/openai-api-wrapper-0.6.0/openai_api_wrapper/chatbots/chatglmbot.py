# -*- coding: utf-8 -*-
"""
This program defines a ChatGLMBot class that inherits from BaseChatBot and uses the ChatGLM model to
generate responses to user input. The ChatGLMBot class initializes with default model parameters and can
be customized with additional parameters.

"""

from basechatbot import BaseChatBot
from chatglm import ChatGLM

class ChatGLMBot(BaseChatBot):
    def __init__(self, template: str = None, human: str = "Human", assistant: str = "Assistant", company: str = "THUDM", proxy: str = None, **kwargs):
        super(ChatGLMBot, self).__init__(human, assistant, company or "THUDM", template, proxy, **kwargs)

    @property
    def _llm(self):
        return ChatGLM(**self.model_params)

    @property
    def _default_model_params(self):
        model_params = {
            'model_name': "THUDM/chatglm-6b",
            'device': "cuda",
            'temperature': 0.95,
            'top_p': 0.7,
            'max_length': 2048,
            'max_retries': 3,
            'streaming': False,
        }
        return model_params
