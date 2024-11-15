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
from llm.logger import log_kwargs, log_exception


class BaseGPT:
    def __init__(self, model_name, key, base_url):
        pass

    def generate(
        self,
        prompt: str,
        response_model,
        max_retries: int = 3,
        validation_context: dict=None,
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
