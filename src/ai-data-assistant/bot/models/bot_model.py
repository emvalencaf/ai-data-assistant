import os

from typing import Any, Mapping, Optional, List

from pydantic import BaseModel

from langchain.llms.utils import enforce_stop_tokens

from dotenv import load_dotenv

load_dotenv()

class _BotModel(BaseModel):
    client: Any = None
    llm_model_id: str = os.getenv("LLM_MODEL_ID")
    _runtime: Any = None
    _temperature: float = float(os.getenv("LLM_TEMPERATURE"))
    _top_p: float = float(os.getenv("LLM_TOP_P"))
    _top_k: int = int(os.getenv("LLM_TOP_K"))
    _max_tokens_to_sample: int = int(os.getenv("LLM_MAX_TOKENS_TO_SAMPLE"))

    @property
    def _default_params(self) -> Mapping[str, Any]:
        return {
            "temperature": self._temperature,
            "top_p": self._top_p,
            "top_k": self._top_k,
            "max_tokens_to_sample": self._max_tokens_to_sample
        }
    
    def _predict(self, prompt: str, stop: Optional[List[str]]) -> str:
        res = self.client.predict(prompt, **self._default_params)
        return self._enforce_stop_words(res.text, stop)
    
    def _enforce_stop_words(self, text: str, stop: Optional[List[str]]) -> str:
        if stop:
            return enforce_stop_tokens(text, stop)
        return text
    
    @property
    def _llm_type(self) -> str:
        return "custom bedrock llm"