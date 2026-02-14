#groq_llm.py
import os
from pydantic import root_validator
from langchain_core.language_models.llms import LLM
from groq import Groq


class GroqLLM(LLM):
    groq_client: Groq # tell Pydantic about this field
    temperature: float = 1

    @root_validator(pre=True)
    def init_client(cls, values):
        #Build the Groq client once, reading .env key
        api_key = os.getenv("GROQ_CHATBOT_API_KEY")
        values["groq_client"] = Groq(api_key=api_key)
        return values
    
    @property
    def _llm_type(self) -> str:
        return "groq"
    
    def _call(self, prompt:str, **kwargs) -> str:
        response = self.groq_client.chat.completions.create(
            messages=[{"role":"user","content":prompt}],
            #Parameterize model name if you want:
            model= kwargs.pop("model","openai/gpt-oss-120b"),
            temperature= self.temperature, **kwargs
        )
        return response.choices[0].message.content
    
    def __call__(self, prompt: str, **kwargs) -> str:
        return self._call(prompt, **kwargs)