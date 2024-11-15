from openai import OpenAI
from pydantic import BaseModel
from textwrap import dedent
from llm.logger import log_kwargs, log_exception
from prompt_engineering.structured_reasoning import generate_structured_response

import instructor


class OllamaOpenAI:
    def __init__(self, model_name, base_url: str = None):
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
