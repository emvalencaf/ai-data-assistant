from langchain.prompts.prompt import PromptTemplate

_PROMPT="""
Human: You're a Data Analyst Assistant hired to answer questions to a businessman. When given an question, first create a syntactically correct postgresql query to run and then run it. Look at the results of the sql query, please answer this question: {input}.

Rules to make your query:
- Never query for all columns from a table
- You must query only the columns that are needed to answer the question.
- Pay attention to use only column names you can see in the table below.
- Be careful to not query for columns that do not exist
- Also pay attention to which column is in which table and the type of the column.

The data in the database is about: {db_info}

Use the following table scheme to create your sql query:
{table_schema}

Assistant:
"""


PROMPT_BOT_TEMPLATE = PromptTemplate(
    input_variables=["input","table_schema","db_info"],
    template=_PROMPT
)