# Copyright 2024 The Chain-of-Table authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import instructor
from openai import OpenAI
from dataclasses import dataclass
from llm.logger import log_kwargs, log_exception
from pydantic import BaseModel
from textwrap import dedent
from prompt_engineering.structured_reasoning import generate_structured_response


@dataclass
class LLMOptions:
    temperature: float = 0.0
    n: int = 1
    top_p: float = 1.0
    max_tokens: int = 150


class ChatGPT:
    def __init__(self, model_name, key):
        self.model_name = model_name
        self.key = key
        self.client = instructor.from_openai(OpenAI(api_key=key))
        self.client.on("completion:kwargs", log_kwargs)
        self.client.on("completion:error", log_exception)

    def generate(
        self,
        query: str,
        prompt: str,
        response_model,
        max_retries: int = 10,
        validation_context: dict = None,
        system_message: str = "You are a helpful assistant.",
    ):

        messages = [
            {
                "role": "system",
                "content": system_message,
            },
            {"role": "user", "content": prompt},
        ]
        gpt_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_retries=max_retries,
            response_model=response_model,
            validation_context=validation_context,
        )

        return gpt_response

    def generate_structured_reasoning_response(
        self,
        query: str,
        context: str,
        response_model: BaseModel,
        validation_context: dict = None,
        max_retries: int = 10,
    ):
        response = self.client.chat.completions.create(
            model=self.model_name,
            response_model=generate_structured_response(response_model),
            max_retries=max_retries,
            validation_context=validation_context,
            messages=[
                {"role": "system", "content": "you are a helpful assistant"},
                {
                    "role": "user",
                    "content": dedent(
                        f"""
                    <system>
                        <role>expert in applying table operations</role>
                        <instruction>Make sure to output your reasoning in structured reasoning steps before generating a response to the user's query.</instruction>
                    </system>

                    <context>
                        {context}
                    </context>

                    <query>
                        {query}
                    </query>
                    """
                    ),
                },
            ],
        )
        return response
