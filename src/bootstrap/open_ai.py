from openai import OpenAI
import os
class OpenAIDriver:
    def __init__(self):
        self.client = OpenAI()
        self.client.api_key = os.getenv("OPENAI_API_KEY")

    def get_response(self, prompt: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            instructions="Eres Maria Bracho, Vendedora de la empresa, Genera un mensaje único para el usuario basado en el texto ingresado",
            input=prompt
        )
        return response.output_text

