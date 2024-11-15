from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from llm.logger import log_kwargs, log_exception
from llm.base_llm import BaseGPT

import instructor

class OllamaOpenAI(BaseGPT):
    def __init__(self, model_name: str, base_url: str = None):
        self.model_name = model_name
        self.base_url = base_url
        self.client = instructor.from_openai(
            OpenAI(
                base_url=base_url,
                api_key="ollama",  # required, but unused
            ),
            mode=instructor.Mode.JSON,
        )
        self.client.on("completion:kwargs", log_kwargs)
        self.client.on("completion:error", log_exception)

    def generate(
        self,
        prompt: str,
        response_model,
        max_retries: int = 6,
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
        # print(self.model_name)
        # print(messages)
        # print(max_retries)
        # print(response_model)
        # print(validation_context)
        gpt_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_retries=max_retries,
            response_model=response_model,
            validation_context=validation_context,
        )

        return gpt_response
