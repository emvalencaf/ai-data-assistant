# AI Data Assistant: AI Data Assistant Source Code

## Summary

- [Documentation (Brazilian Portuguese)](/README.md#documentação)
    - [Sumário da Documentação](/README.md#sumário-da-documentação)
    - [Sobre o Projeto](/README.md#sobre-o-projeto)
    - [A Arquitetura do Projeto](/README.md#a-arquitetura-do-projeto)
    - [Fontes](/README.md#fontes)
- [Documentation (USA English)](/README.md#documentation)
    - [Documentation Summary](/README.md#documentation-summary)
    - [About the Project](/README.md#about-the-project)
    - [Project Architecture](/README.md#project-architecture)
    - [Sources](/README.md#sources)


## Documentation

### Documentation Summary

- [AI Data Assistant Source Code](/src/ai-data-assistant/README.md#documentation)
    - [About the Source Code](/src/ai-data-assistant/README.md#about-the-ai-data-assistant-source-code)
        - [Necessary Policies for AI Data Assistant Operation](/src/ai-data-assistant/README.md#necessary-policies-for-ai-data-assistant-operation)
        - [Using the Source Code in AWS Lambda](/src/ai-data-assistant/README.md#using-the-source-code-in-aws-lambda)
    - [Considerations on AI Data Assistant Operation](/src/ai-data-assistant/README.md#considerations-on-ai-data-assistant-operation)
        - [AI Data Assistant Structure](/src/ai-data-assistant/README.md#ai-data-assistant-structure)
        - [Accessing the Database via Amazon Athena](/src/ai-data-assistant/README.md#accessing-the-database-via-amazon-athena)
        - [Chatbot with a Data Analyst Assistant Role](/src/ai-data-assistant/README.md#chatbot-with-a-data-analyst-assistant-role)
- [Load Local Data Into S3 Source Code](/src/load-local-data-into-s3/README.md#documentation)


### About the Source Code: AI Data Assistant

The `AI Data Assistant` was developed using the [LangChain](https://python.langchain.com/docs/get_started/introduction) framework and the `Claude` LLM (Large Language Model) from [Anthropic](https://www.anthropic.com/news/introducing-claude) available on [AWS Bedrock](https://aws.amazon.com/pt/bedrock/?gclid=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE&trk=82b1c10f-8aa4-4e6c-ab52-c75550a4a31e&sc_channel=ps&ef_id=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE:G:s&s_kwcid=AL!4422!3!692006001529!e!!g!!aws%20bedrock!21054971723!164977098371) platform. The role of this chatbot is:

1. Receive questions from an end user.
2. Transform it into an SQL query.
3. Execute this SQL query through Amazon Athena.
4. Transform the results of the SQL query into natural language.
5. Send the response to the end user.

The required environment variables are located in the following file: [.env.example](/src/ai-data-assistant/.env.example)

#### Necessary Policies for AI Data Assistant Operation

It is necessary to configure permissions for `Amazon S3`, `AWS Glue`, `Amazon Athena`, and grant privileges in the database in `Data Lake Formation`.

#### Using the Source Code in AWS Lambda

The step-by-step process to import the Source Code to AWS Lambda:

1. The first step is to create the AWS Lambda layer so that AWS Lambda can access the necessary libraries for executing the Source Code.

2. To create the layer, it is necessary to run the [Docker image](/src/ai-data-assistant/Dockerfile) and execute the image and extract a zip file with the libraries from the container.

3. This routine can be simplified by executing the [run_app.sh](/src/ai-data-assistant/run_app.sh) file.

4. Next, with the `.zip` file in hand, it is necessary to upload it to an Amazon S3 bucket and use this bucket object as a layer of the `AWS Lambda`.

5. It is necessary to comment out (or delete) the codes where "load_dotenv()" and "from dotenv import load_dotenv" are present in the files `/src/ai-data-assistant/tools/athena_db.py`, `/src/ai-data-assistant/bot/llm_models/bedrock.py`, and `/src/ai-data-assistant/bot/data_assistant_bot.py`.

6. In the files `/src/ai-data-assistant/tools/athena_db.py` and `/src/ai-data-assistant/bot/llm_models/bedrock.py`, it is necessary to remove the AWS credentials.

- For example, in the file `/src/ai-data-assistant/bot/llm_models/bedrock.py`:

```
(...)
class BedrockLLM(_BotModel):
    def __init__(self, **values):
        super().__init__(**values)
        
        self._runtime = boto3.client('bedrock-runtime',
                                       aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                       aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                                       region_name=os.getenv("AWS_REGION"))
        # When import the code to a lambda function just omit aws_access_key_id, aws_secret_access_key and region_name as arg to boto3.client

        (...)
```

It should be adjusted to the following form:

```
(...)
class BedrockLLM(_BotModel):
    def __init__(self, **values):
        super().__init__(**values)
        
        self._runtime = boto3.client('bedrock-runtime')
        
        (...)
```


### Considerations on AI Data Assistant Operation

#### AI Data Assistant Structure

The `AI Data Assistant` was developed in layers under the Object-Oriented Programming paradigm, in the project the following classes: `AthenaDB`, `DataAssistantBot`, `_BotModel`, and `BedrockLLM` are represented in the following Class Diagram:

![AI Data Assistant Class Diagram](/docs/diagrams/ClassDiagram!DataAssistantBot.jpg)

The main class (a controller or the outermost class) is the `DataAssistantBot` which is responsible for controlling the end user's interaction with the database and the `Claude` LLM. Thus, the `AthenaDB` class is a part of the `DataAssistantBot`, as well as the `BedrockLLM`.

The classes interact as expressed in the Sequence Diagram:

![AI Data Assistant Sequence Diagram](/docs/diagrams/SequenceDiagrama!AIDataAssistant.jpg)

1. The user asks a question to the database.

- Stage: Instance of the `DataAssistantBot` class.

2. The `DataAssistantBot` class will be instantiated.
3. During the instantiation of the `DataAssistantBot` class, an `AthenaDB` class will be instantiated and the instance of the `AthenaDB` class will be returned to the attributes of the `DataAssistantBot` object.
4. During the instantiation of the `DataAssistantBot` class, the `BedrockLLM` class will be instantiated which will be modeled on the `_BotModel` template.
5. During the instantiation of the `DataAssistantBot` class, the `SQLDatabaseChain` class (originating from the framework [LangChain](https://python.langchain.com/docs/get_started/introduction)) with the attributes of the LLM `Claude` and the connection to `Amazon Athena` will be configured.
6. During the instantiation of the `DataAssistantBot` class, the prompt will be set, assigning the role that the LLM will assume.

- Code Execution Stage

7. The `query_to` method of the `DataAssistantBot` object will be called with the end user's question as its parameter, which will be inserted into the prompt instructing the role that the `DataAssistantBot` will assume.

- Sub-Stage: Dialoguing with the Database

8. The `DataAssistantBot` object will call the `SQLDatabaseChain` which will execute the `_call()` method of the `BedrockLLM` object which will call the `_predict()` method - and within it executing the `_enforce_stop_words()` method - inherited from the `_BotModel` class, creating the SQL query.
9. The `SQLDatabaseChain` will receive the SQL query and using the connection of `AthenaDB` will execute it.
10. The `SQLDatabaseChain` will fetch the result of the SQL query and trigger the `_call()` method of the `BedrockLLM` object which will call the `_predict()` method - within it executing the `_enforce_stop_words()` method - inherited from the `_BotModel` class, creating the response according to the instructed role and results of the SQL query.

- Return Stage: Returning the response to the end user

11. The `SQLDatabaseChain` will return the result to the `DataAssistantBot` which will return it to the end user.

#### Accessing the Database via Amazon Athena

The `AI Data Assistant` has access to the database via [Amazon Athena](https://aws.amazon.com/pt/athena/) using the Python library of [SQL Alchemy](https://www.sqlalchemy.org/), this tool is given through the following environment variables (which for local execution must be stored in `.env` and for AWS Lambda in environment variables)

```
ATHENA_PORT=
ATHENA_SCHEMA=
ATHENA_STAGING=
ATHENA_WORK_GROUP=
```

Through these variables, Python will establish a connection to Athena, it is important to note that:

1. If the source code is being executed locally, the file `/src/ai-data-assistant/tools/athena_db.py` should be as follows:

```
        (...)
    def __init__(self):
        port = int(os.getenv("ATHENA_PORT"))
        schema = os.getenv("ATHENA_SCHEMA")
        S3_staging = os.getenv("ATHENA_STAGING")
        wkgroup = os.getenv("ATHENA_WORK_GROUP")
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")

        conn_credentials = f"awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}"

        (...)
```

2. On the other hand, if it is being executed on AWS Lambda, it should be as follows:

```
        (...)
    def __init__(self):
        port = int(os.getenv("ATHENA_PORT"))
        schema = os.getenv("ATHENA_SCHEMA")
        S3_staging = os.getenv("ATHENA_STAGING")
        wkgroup = os.getenv("ATHENA_WORK_GROUP")

        conn_credentials = f"awsathena+rest://"

        (...)
```


The reason for the need for difference is that AWS Lambda accesses AWS resources through *IAM Role* instead of the credentials of a *IAM USER*.

#### Chatbot with a Data Analyst Assistant Role

The main foundation that makes the LLM `Claude` behave according to a "Virtual Data Analyst" is the briefing given in the [source code](/src/ai-data-assistant/bot/prompt_templates/prompt_bot.py). Or better saying, `Claude` was instructed to assume a role through the following prompt:

```
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
``` 


During the development of the chatbot, it was learned that `Claude` performs better with more direct, objective, and clear instructions. The LLM not only needs a role such as: `You're a Data Analyst Assistant hired to answer questions to a businessman`; and a clear instruction of what to do: `When given an question, first create a syntactically correct postgresql query to run and then run it. Look at the results of the sql query, please answer this question: `; but also information on how to do it, what the database is about, and what is the table schema (or schemas).

It is important to briefly discuss what the database is about, especially when the data in the table is not intuitive enough for `Claude` to understand based on the question asked to him. It is also necessary to provide the table schema so that `Claude` knows which are the columns, the data types, and what those data are about.

The higher the level of abstraction and unintuitiveness of the data, the more effort and attention will be needed in drafting the prompt.

In the `AI Data Assistant` project, `db_info` and `table_schema` are extracted from environment variables (which should be in `.env` locally or in the `AWS Lambda` environment variable):

```
ATHENA_TABLE_NAME=

# RESUME THE DATABASE
DB_INFO=
```

The `ATHENA_TABLE_NAME` variable admits receiving a string with several table names, each name must be separated by a comma, for example: `tb_sales, tb_customers, tb_supplier`. This string will be processed (in the code) and converted into a schema.

On the other hand, `DB_INFO` should receive a brief summary of what the database is about and provide a description that helps `Claude` understand the data he is processing.


## Documentação

### Sumário da Documentação

- [Código Fonte do AI Data Assistant](/src/ai-data-assistant/README.md#documentação)
    - [Sobre o Código Fonte](/src/ai-data-assistant/README.md#sobre-o-código-fonte-ai-data-assistant)
        - [Políticas Necessárias para o Funcionamento do AI Data Assistant](/src/ai-data-assistant/README.md#políticas-necessárias-para-o-funcionamento-do-ai-data-assistant)
        - [Uso do Código Fonte no AWS Lambda](/src/ai-data-assistant/README.md#uso-do-código-fonte-no-aws-lambda)
    - [Considerações sobre o funcionamento do AI Data Assistant](/src/ai-data-assistant/README.md#considerações-sobre-o-funcionamento-do-ai-data-assistant)
        - [Estrutura do AI Data Assistant](/src/ai-data-assistant/README.md#a-estrutura-do-ai-data-assistant)
        - [Acesso ao banco de dados por meio do Amazon Athena](/src/ai-data-assistant/README.md#acesso-ao-banco-de-dados-por-meio-do-amazon-athena)
        - [Chatbot com um papel de Data Analyst Assistant](/src/ai-data-assistant/README.md#um-chatbot-com-um-papel-de-data-analyst-assistant)
- [Código Fonte do Load Local Data Into S3](/src/load-local-data-into-s3/README.md#documentação)
    - [Sobre o Código Fonte](/src/load-local-data-into-s3/README.md#sobre-o-código-fonte)
        - [Políticas Necessárias para o Funcionamento do Load Local Data Into S3](/src/load-local-data-into-s3/README.md#políticas-necessárias-para-o-funcionamento-do-load-local-data-into-s3)
        - [Uso do Código Fonte](/src/load-local-data-into-s3/README.md#uso-do-código-fonte)
    - [Considerações sobre o funcionamento do Load Local Data Into S3](/src/load-local-data-into-s3/README.md#)
        - [A Estrutura do Load Local Data Into S3](/src/load-local-data-into-s3/README.md#a-estrutura-do-load-local-data-into-s3)

### Sobre o Código Fonte: AI Data Assistant

O `AI Data Assistant` foi desenvolvido usando o *framework* da [LangChain](https://python.langchain.com/docs/get_started/introduction) e o LLM (*Large Language Model* ou Grande Modelo de Linguagem) `Claude` da [Anthropic](https://www.anthropic.com/news/introducing-claude) disponível no [AWS Bedrock](https://aws.amazon.com/pt/bedrock/?gclid=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE&trk=82b1c10f-8aa4-4e6c-ab52-c75550a4a31e&sc_channel=ps&ef_id=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE:G:s&s_kwcid=AL!4422!3!692006001529!e!!g!!aws%20bedrock!21054971723!164977098371), a sua função desse *chatbot* é:

1. Receber perguntas de um usuário-final;
2. Transformá-la em uma SQL *query*;
3. Executar essa SQL *query* por meio do Amazon Athena;
4. Transformar os resultados da SQL *query* em linguagem natural;
5. Enviar a resposta ao usuário final.

As variáveis de ambiente necessárias se encontram no seguinte arquivo: [.env.example](/src/ai-data-assistant/.env.example)

#### Políticas necessárias para o funcionamento do AI Data Assistant

É preciso configurar permissões do `Amazon S3`, `AWS Glue`, `Amazon Athena` e conceder privilégios no banco de dados no `Data Lake Formation`.

#### Uso do Código Fonte no AWS Lambda

O passo a passo para importar o Código Fonte para o AWS Lambda:

1. O primeiro passo é criar a camada do AWS Lambda para que o AWS Lambda possa acessar as bibliotecas necessárias para a execução do Código Fonte.

2. Para criar a camada é preciso executar a [imagem do Docker](/src/ai-data-assistant/Dockerfile) e executada a imagem e extraída do *container* um *zip* com as bibliotecas.

3. Essa rotina pode ser feita mais fácil executando o arquivo [run_app.sh](/src/ai-data-assistant/run_app.sh)

4. Em seguida, com o `.zip` em mãos é preciso fazer o *upload* em um *bucket* da Amazon S3 e usar esse objeto do *bucket* como camada da `AWS Lambda`.

5. É preciso comentar (ou apagar) os códigos em que há "load_dotenv()" e "from dotenv import load_dotenv" nos arquivos `/src/ai-data-assistant/tools/athena_db.py`, `/src/ai-data-assistant/bot/llm_models/bedrock.py` e `/src/ai-data-assistant/bot/data_assistant_bot.py`.

6. Nos arquivos `/src/ai-data-assistant/tools/athena_db.py` e `/src/ai-data-assistant/bot/llm_models/bedrock.py`, é preciso retirar as credenciais da AWS

- Por exemplo, no arquivo `/src/ai-data-assistant/bot/llm_models/bedrock.py`:

```
(...)
class BedrockLLM(_BotModel):
    def __init__(self, **values):
        super().__init__(**values)
        
        self._runtime = boto3.client('bedrock-runtime',
                                       aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                       aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                                       region_name=os.getenv("AWS_REGION"))
        # When import the code to a lambda function just omit aws_access_key_id, aws_secret_access_key and region_name as arg to boto3.client

        (...)
```

É só tratar para ficar da seguinte forma:

```
(...)
class BedrockLLM(_BotModel):
    def __init__(self, **values):
        super().__init__(**values)
        
        self._runtime = boto3.client('bedrock-runtime')
        
        (...)
```


### Considerações sobre o funcionamento do AI Data Assistant

#### Estrutura do AI Data Assistant

O `AI Data Assistant` foi desenvolvido em camadas sob o paradigma da Programação Orientada ao Objeto, no projeto as seguintes classes: `AthenaDB`, `DataAssistantBot`, `_BotModel` e `BedrockLLM`, que estão representadas no seguinte Diagrama de Classe:

![Diagrama de Classe do AI Data Assistant](/docs/diagrams/ClassDiagram!DataAssistantBot.jpg)

A classe principal (um *controller* ou a classe mais externa) é a `DataAssistantBot` que é responsável por controlar a interação do usuário-final ao banco de dados e ao LLM `Claude`. Desta forma, a classe `AthenaDB` é uma parte da `DataAssistantBot`, assim como a `BedrockLLM`.

As classes interagem da seguinte forma, conforme expressado no Diagrama de Sequência:

![Diagrama de Sequência da AI Data Assistant](/docs/diagrams/SequenceDiagrama!AIDataAssistant.jpg)

1. O usuário faz uma pergunta ao banco de dados

- Etapa: Instância da classe `DataAssistantBot`

2. A classe `DataAssistantBot` será instanciado
3. Durante a instância da classe `DataAssistantBot`, será instanciada uma classe `AthenaDB` e retornada a instância da classe `AthenaDB` aos atributos do objeto `DataAssistantBot`
4. Durante a instância da classe `DataAssistantBot`, será instanciada a classe `BedrockLLM` que será modelada nos moldes `_BotModel`
5. Durante a instância da classe `DataAssistantBot`, será instanciado a classe `SQLDatabaseChain` (classe originária do *framework* [LangChain](https://python.langchain.com/docs/get_started/introduction)) com os atributos da LLM `Claude` e a conexão ao `Amazon Athena`
6. Durante a instância da classe `DataAssistantBot`, será configurado a *prompt* que atribuíra a *role* que o LLM assumirá.

- Etapa: Execução do Código 

7. O método `query_to` do objeto da classe `DataAssistantBot` e receberá em seu parâmetro a pergunta do usuário-final que será inserida na *prompt* que instruí a *role* que o `DataAssistantBot` assumirá.

- Sub-Etapa: Dialogando com o Banco de Dados

8. O objeto `DataAssistantBot` vai chamar o `SQLDatabaseChain` que vai executar o método `_call()` do objeto da classe `BedrockLLM` que chamará o método `_predict()` - e dentro dela executando o método `_enforce_stop_words()` - herdado da classe `_BotModel`, sendo criada a *query* do SQL.
9. O `SQLDatabaseChain` vai receber a *query* do SQL e usando a conexão do `AthenaDB` vai executá-la.
10. O `SQLDatabaseChain` vai pegar o resultado da *query* do SQL e acionar o método `_call()` do objeto da classe `BedrockLLM` que chamará o método `_predict()` - dentro dela executando o método `_enforce_stop_words()` - herdado da classe `_BotModel`, sendo criada a resposta de acordo com a *role* instruída e resultados da *query* do SQL

- Etapa: Retornando a resposta ao usuário-final

11. O `SQLDatabaseChain` vai retornar o resultado ao `DataAssistantBot` que vai retornar ao usuário-final.

#### Acesso ao banco de dados por meio do Amazon Athena

O `AI Data Assistant` tem acesso ao banco de dados por meio do [Amazon Athena](https://aws.amazon.com/pt/athena/) usando a biblioteca Python do [SQL Alchemy](https://www.sqlalchemy.org/), essa ferramenta se dá por meio das seguintes variáveis de ambiente (que para execução local devem ser guardadas no `.env` e para o AWS Lambda nas variáveis de ambiente)

```
ATHENA_PORT=
ATHENA_SCHEMA=
ATHENA_STAGING=
ATHENA_WORK_GROUP=
```

Por meio dessas variáveis o Python estabelecerá uma conexão ao Athena, é importante destacar quê:
1. Caso o código fonte esteja sendo executado localmente o arquivo `/src/ai-data-assistant/tools/athena_db.py` deverá estar da seguinte forma:

```
        (...)
    def __init__(self):
        port = int(os.getenv("ATHENA_PORT"))
        schema = os.getenv("ATHENA_SCHEMA")
        S3_staging = os.getenv("ATHENA_STAGING")
        wkgroup = os.getenv("ATHENA_WORK_GROUP")
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")

        conn_credentials = f"awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}"

        (...)
```

2. Por sua vez, se estiver sendo executado no AWS Lambda, deverá estar dessa forma:

```
        (...)
    def __init__(self):
        port = int(os.getenv("ATHENA_PORT"))
        schema = os.getenv("ATHENA_SCHEMA")
        S3_staging = os.getenv("ATHENA_STAGING")
        wkgroup = os.getenv("ATHENA_WORK_GROUP")

        conn_credentials = f"awsathena+rest://"

        (...)
```

A razão pela necessidade da diferença é que o AWS Lambda faz acesso aos recursos da AWS por meio de *IAM Role* ao invés das chaves de credenciais de um usuário *IAM USER*. 

#### Chatbot com um papel de Data Analyst Assistant

O principal alicerce que faz o LLM `Claude` se comportar de acordo como um "Analista de Dados Virtual" é o *briefing* dado no [source code](/src/ai-data-assistant/bot/prompt_templates/prompt_bot.py). Ou melhor dizendo, o `Claude` foi instruído a assumir uma *role* (papel) por meio da seguinte *prompt*:

```
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
``` 

Durante o desenvolvimento do *chatbot* foi aprendido que o `Claude` se dá melhor com instruções mais diretas, objetivas e claras. O LLM não só precisa de uma *role* como: `You're a Data Analyst Assistant hired to answer questions to a businessman`; e uma instrução clara do que fazer: `When given an question, first create a syntactically correct postgresql query to run and thenn run it. Look at the results of the sql query, please answer this question: `; como também informações de como fazer, sobre o quê é o banco de dados e qual é o esquema (*schema*) da tabela (ou tabelas).

É importante discorrer brevemente sobre o que é o banco de dados, principalmente, quando os dados na tabela não são intuitivos suficiente para o `Claude` entender com base na pergunta feita a ele. Também é necessário o esquema da tabela para que o `Claude` saiba quais são as colunas, os tipos de dados e sobre o que são aqueles dados.

Quanto maior o nível de abstração e contraintuitivo dos dados, mais esforço e atenção será necessário na elaboração do *prompt*.

No projeto `AI Data Assistant`, o `db_info` e `table_scheme` são extraídos das variáveis de ambiente (que devem ficar no `.env` em local ou na variável de ambientes do `AWS Lambda`):

```
ATHENA_TABLE_NAME=

# RESUME THE DATABASE
DB_INFO=
```

A variável `ATHENA_TABLE_NAME` admite receber uma string com vários nomes de tabelas, cada nome deve ser separado por vírgula, por exemplo: `tb_vendas, tb_clientes, tb_fornecedor`. Essa string será processada (no código) e convertida em um *schema*.

Por sua vez, `DB_INFO` deve receber um breve resumo do que se trata o banco de dados e oferecer uma descrição que auxilie o `Claude` a entender os dados que ele está processando.

