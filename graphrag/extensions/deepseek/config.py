"""OpenAI Configuration class definition."""

from typing import Annotated, Literal

from pydantic import Field

from graphrag.extensions.deepseek.params import DeepSeekChatParameters
from fnllm.openai import PublicOpenAIConfig
from fnllm.openai.config import (
    CommonOpenAIConfig, 
)

class DeepSeekAIConfig(PublicOpenAIConfig, frozen=True, extra="allow", protected_namespaces=()):
    """DeepSeek AI 配置，继承 PublicOpenAIConfig，并确保 response_format 存在。"""

    base_url: str = Field(
        default="http://127.0.0.1:11434/v1", description="The DeepSeek API base URL."
    )

    # chat_parameters: DeepSeekChatParameters = Field(
    #     default_factory=lambda: {"response_format": {"type": "json_object"}},
    #     description="Global chat parameters to be used across calls, ensuring response_format is set.",
    # )