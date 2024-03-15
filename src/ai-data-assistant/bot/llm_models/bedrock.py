import os
from typing import List, Optional
import boto3
from langchain.llms.bedrock import Bedrock
from bot.models.bot_model import _BotModel

from dotenv import load_dotenv # comment on when import code to AWS Lambda

load_dotenv() # comment on when  import code to AWS Lambda

class BedrockLLM(_BotModel):
    def __init__(self, **values):
        super().__init__(**values)
        
        self._runtime = boto3.client('bedrock-runtime',
                                       aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                       aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                                       region_name=os.getenv("AWS_REGION"))
        # When import the code to a lambda function just omit aws_access_key_id, aws_secret_access_key and region_name as arg to boto3.client
        
        params = {**self._default_params, **values}
        self.client = Bedrock(client=self._runtime,
                              model_id=self.llm_model_id,
                              model_kwargs= {
                                  "temperature": params["temperature"],
                                  "max_tokens_to_sample": params["max_tokens_to_sample"]
                              })
        
        print(self.client.client)
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return self._predict(prompt, stop)