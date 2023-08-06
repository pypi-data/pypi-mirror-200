# -*- coding: utf-8 -*-
"""
This program defines a BaseChatBot class that initializes a language model and a prompt template. 
The chatbot is able to generate human-like text based on the input it receives, allowing it to engage 
in natural-sounding conversations and provide responses that are coherent and relevant to the topic 
at hand. The chatbot is designed to be able to assist with a wide range of tasks, from answering 
simple questions to providing in-depth explanations and discussions on a wide range of topics. The 
chatbot is constantly learning and improving, and its capabilities are constantly evolving. It is 
able to process and understand large amounts of text, and can use this knowledge to provide accurate 
and informative responses to a wide range of questions. The chatbot must answer questions in Chinese.

"""
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

class BaseChatBot:
    def __init__(self,  human: str = "Human", assistant: str = "Assistant", company: str = "Company Name", template: str = None, proxy: str = None, **kwargs):
        self.human = human or "Human"
        self.assistant = assistant or "Assistant"
        self.company = company
        self.proxy = proxy

        self.model_params = self._default_model_params
        if kwargs:
            for k, v in kwargs.items():
                if v:
                    self.model_params[k] = v

        self.template = template or """{assistant} is a large language model trained by {company}.
        {assistant} is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, {assistant} is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
        {assistant} is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, {assistant} is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
        {assistant} must answer questions in a way that is consistent with the information it has been trained on. For example, if {assistant} is asked a question about a topic that it has not been trained on, it will not be able to provide an answer. However, if {assistant} is asked a question about a topic that it has been trained on, it will be able to provide an answer that is consistent with the information it has been trained on.
        Asistant's answer must be all in Chinese.
        Overall, {assistant} is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, {assistant} is here to assist.

        {history}
        {human}: {human_input}
        {assistant}:"""

        self.template = self.template.replace("{human}", self.human).replace("{assistant}", self.assistant).replace("{company}", self.company)

        self.prompt = PromptTemplate(
            input_variables=["history", "human_input"], 
            template=self.template
        )

        self.chatgpt_chain = LLMChain(
            llm=self._llm,
            prompt=self.prompt, 
            verbose=False, 
            memory=ConversationBufferWindowMemory(k=2, human_prefix=self.human, ai_prefix=self.assistant),
        )

    @property
    def _llm(self):
        raise NotImplementedError("The abstract method 'llm' is not implemented.")

    @property
    def _default_model_params(self):
        raise NotImplementedError("The abstract method 'model_params' is not implemented.")


    def ask(self, human_input: str) -> str:
        return self.chatgpt_chain.predict(human_input=human_input)
