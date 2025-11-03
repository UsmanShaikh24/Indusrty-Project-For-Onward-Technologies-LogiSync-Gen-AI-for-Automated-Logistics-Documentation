"""
Ollama integration for document generation
"""
import httpx
from typing import Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        
    async def generate_text(self, prompt: str, model: str = "llama2:latest") -> str:
        """
        Generate text using Ollama with Llama2 model
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                }
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Ollama API error: {response.text}")
    
    async def generate_document(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Generate a document using a template and variables
        """
        prompt = f"""[INST] As a logistics documentation expert, please generate a professional document based on the following template and variables. Maintain formal language and ensure accuracy.

Template to follow:
{template}

Variables to use:
{variables}

Generate a clear, concise, and professional document incorporating all the provided information. [/INST]"""