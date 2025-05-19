from openai import OpenAI
import os
class OpenAIDriver:
    def __init__(self, open_data: dict):
        self.client = OpenAI()
        self.client.api_key = os.getenv("OPENAI_API_KEY")
        self.open_data = open_data

    def get_response(self, prompt: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            instructions=f"Eres {self.open_data['name']}, {self.open_data['context']}",
            input=prompt
        )
        return response.output_text

