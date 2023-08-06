from __future__ import annotations

import dataclasses
from dataclasses import dataclass
import os
from typing import Optional

import openai

from chateval.kernels.kernel import Kernel, KernelConfig

openai.api_key = os.environ["OPENAI_API_KEY"]


@dataclass
class OpenAICompletionConfig(KernelConfig):
    model_name: str = "text-curie-001"
    max_tokens: int = 64
    temperature: float = 0.7
    top_p: float = 1
    suffix: str = ""
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    logprobs: float = 1
    n: int = 1
    echo: bool = False
    stop: object = None

    def to_kernel(self) -> Kernel:
        return OpenAICompletion(self)

    @classmethod
    def from_dict(cls, data_dict: dict) -> OpenAICompletionConfig:
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in data_dict.items() if k in field_names})


class OpenAICompletion(Kernel):
    def __init__(self, config: Optional[OpenAICompletionConfig] = None):

        self.config = (
            config
            if config is not None
            else OpenAICompletionConfig(
                model_name="text-curie-001",
                suffix="",
                temperature=0,
                max_tokens=10,
                logprobs=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                echo=False,
                stop=None,
            )
        )

    def execute(self, code) -> dict[str, str]:
        # Set the API key from the environment variable

        response = openai.Completion.create(
            model=self.config.model_name,
            prompt=code,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            frequency_penalty=self.config.frequency_penalty,
            presence_penalty=self.config.presence_penalty,
            logprobs=self.config.logprobs,
            n=self.config.n,
            echo=self.config.echo,
            stop=self.config.stop,
        )

        out = {
            "text": response["choices"][0]["text"],
            "token_logprobs": response["choices"][0]["logprobs"]["token_logprobs"],
            "tokens": response["choices"][0]["logprobs"]["tokens"],
        }

        return out
