
# llms
from bot.llm_models.bedrock import BedrockLLM

# template bot
from bot.prompt_templates.prompt_bot import PROMPT_BOT_TEMPLATE

# tools
from tools.athena_db import AthenaDB

from langchain_experimental.sql import SQLDatabaseChain

# sql alchemy
from sqlalchemy import inspect

from dotenv import load_dotenv # comment on when  import code to AWS Lambda
import os

load_dotenv() # comment on when  import code to AWS Lambda

class DataAssistantBot:
    def __init__(self):
        self._athena_db = AthenaDB()

        self._llm = BedrockLLM(verbose=True)
        
        self._db_chain = SQLDatabaseChain.from_llm(llm=self._llm.client,
                                                   db=self._athena_db.db,
                                                   verbose=True,)
        self._table_schema = '\n'.join(self._athena_db.tables)
        
        self._db_info = os.getenv("DB_INFO")
        
        self._bot_prompt = PROMPT_BOT_TEMPLATE
    
    def query_to(self, question: str):
        
        final_prompt = self._bot_prompt.format(input=question,
                                               top_k=int(os.getenv("LLM_TOP_K")),
                                               table_name=os.getenv("ATHENA_TABLE_NAME"),
                                               table_schema=self._table_schema,
                                               db_info=self._db_info)
        
        print("final prompt: ", final_prompt)
            
        output = self._db_chain(final_prompt)
        
        print(f'Raw Output - ', output)
        
        print(f"Output - {output['result']}")
        return output['result']
    