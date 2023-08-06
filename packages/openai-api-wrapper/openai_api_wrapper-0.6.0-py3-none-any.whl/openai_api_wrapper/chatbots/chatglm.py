# -*- coding: utf-8 -*-
"""
This program is a wrapper around ChatGLM large language models. It provides a class called ChatGLM 
that contains methods for generating chat responses using the model. The program also includes 
functions for retrying completion calls and for generating chat responses asynchronously.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple
import torch
from transformers import AutoModel, AutoTokenizer

from pydantic import BaseModel, Extra, Field, root_validator
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from langchain.chat_models.base import BaseChatModel
from langchain.schema import (
    BaseMessage,
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
    ChatGeneration,
    ChatResult,
)

import logging
logger = logging.getLogger(__file__)

def _create_retry_decorator(llm: ChatGLM) -> Callable[[Any], Any]:
    min_seconds = 4
    max_seconds = 10
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(llm.max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )

def completion_with_retry(llm: ChatGLM, **kwargs: Any) -> Any:
    """Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(llm)

    @retry_decorator
    def _completion_with_retry(**kwargs: Any) -> Any:
        streaming = kwargs.pop('streaming')
        if streaming:
            return llm.model.stream_chat(**kwargs)
        else:
            return llm.model.chat(**kwargs)

    return _completion_with_retry(**kwargs)

async def acompletion_with_retry(llm: ChatGLM, **kwargs: Any) -> Any:
    """Use tenacity to retry the async completion call."""
    retry_decorator = _create_retry_decorator(llm)

    @retry_decorator
    async def _completion_with_retry(**kwargs: Any) -> Any:
        streaming = kwargs.pop('streaming')
        if streaming:
            return await llm.model.stream_chat(**kwargs)
        else:
            return await llm.model.chat(**kwargs)

    return await _completion_with_retry(**kwargs)

# -------------------- class ChatGLM --------------------

class ChatGLM(BaseChatModel, BaseModel):
    """Wrapper around ChatGLM large language models.
    """

    model_name: str = "THUDM/chatglm-6b"
    max_retries: int = 3
    tokenizer: Optional[Any] = None
    model: Optional[Any] = None
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    device: str = "cuda"
    verbose: bool = False
    streaming: bool = False

    temperature: float = 0.95
    top_p: float = 0.7
    max_length: int = 2048
    history: List[Tuple[str, str]] = Field(default_factory=list)

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.ignore
    
    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        model_name = values.get("model_name", "")

        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        device_name = values.get("device", "")
        device = torch.device(device_name)
        model = AutoModel.from_pretrained(model_name, trust_remote_code=True).half().to(device)
        model = model.eval()

        values['tokenizer'] = tokenizer
        values["model"] = model

        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling OpenAI API."""
        return {

            'tokenizer': self.tokenizer, 
            'temperature': self.temperature,
            'top_p': self.top_p,
            'max_length': self.max_length,
            'history': self.history,
            'streaming': self.streaming,
            **self.model_kwargs,
        }


    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None) -> ChatResult:
        params: Dict[str, Any] = self._default_params

        query = ""
        for  message in messages:
            role = None
            if isinstance(message, ChatMessage):
                role = message.role
            elif isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, SystemMessage):
                role = "system"
            else:
                raise ValueError(f"Got unknown type {message}")
            query += f"{role}: {message.content}\n"

        if self.streaming:
            inner_completion = ""
            for stream_resp, _ in completion_with_retry(self, query=query, **params):
                inner_completion += stream_resp
                self.callback_manager.on_llm_new_token(stream_resp, verbose=self.verbose)
            stream_message = AIMessage(content=inner_completion)
            return ChatResult(generations=[ChatGeneration(message=stream_message)])

        params.pop('streaming')
        response, _ = self.model.chat(query=query, **params)
        message = AIMessage(content=response)
        return ChatResult(generations=[ChatGeneration(message=message)])

    async def _agenerate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None) -> ChatResult:
        params: Dict[str, Any] = self._default_params

        query = ""
        for  message in messages:
            role = None
            if isinstance(message, ChatMessage):
                role = message.role
            elif isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, SystemMessage):
                role = "system"
            else:
                raise ValueError(f"Got unknown type {message}")
            query += f"{role}: {message.content}\n"

        if self.streaming:
            inner_completion = ""
            async for stream_resp, _ in await acompletion_with_retry(self, query=query, **params):
                inner_completion += stream_resp
                if self.callback_manager.is_async:
                    await self.callback_manager.on_llm_new_token(stream_resp, verbose=self.verbose)
                else:
                    self.callback_manager.on_llm_new_token(stream_resp, verbose=self.verbose)
            stream_message = AIMessage(content=inner_completion)
            return ChatResult(generations=[ChatGeneration(message=stream_message)])
        params.pop('streaming')
        response, _ = self.model.chat(query=query, **params)
        message = AIMessage(content=response)
        return ChatResult(generations=[ChatGeneration(message=message)])

