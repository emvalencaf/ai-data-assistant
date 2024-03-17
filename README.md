# AI Data Assistant

## Summary

- [Documentation (Brazilian Portuguese)](/README.md#documentação)
    - [Sumário da Documentação](/README.md#sumário-da-documentação)
    - [Sobre o Projeto](/README.md#sobre-o-projeto)
        - [Adaptações do Projeto](/README.md#adaptações-do-projeto)
    - [A Arquitetura do Projeto](/README.md#a-arquitetura-do-projeto)
    - [Fontes](/README.md#fontes)
- [Documentation (USA English)](/README.md#documentation)
    - [Documentation Summary](/README.md#documentation-summary)
    - [About the Project](/README.md#about-the-project)
        - [Project Adaptations](/README.md#project-adaptations)
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
    - [About the Source Code](/src/load-local-data-into-s3/README.md#about-the-source-code)
        - [Required Policies for Load Local Data Into S3 Operation](/src/load-local-data-into-s3/README.md#required-policies-for-load-local-data-into-s3-operation)
        - [Usage of the Source Code](/src/load-local-data-into-s3/README.md#usage-of-the-source-code)
    - [Considerations on Load Local Data Into S3 Operation](/src/load-local-data-into-s3/README.md#)
        - [Structure of Load Local Data Into S3](/src/load-local-data-into-s3/README.md#structure-of-load-local-data-into-s3)

### About the Project

The `AI Data Assistant` project is a chatbot where users can inquire about data in a database and receive responses in natural language (human language). The project was developed for learning purposes in the area of Data Engineering, D&A in General, and AWS.

![Diagram to show how the AI Data Assistant works](/docs/diagrams/AWSDiagram!AI%20DataAssistant%20Generic%20Logic.jpg)

The project was divided into three stages:

1. Data ingestion into AWS (via a Docker container)
2. Creation of a database from the data stored in AWS
3. Creation of an intelligent Data Assistant from a connection to the created database.

The `AI Data Assistant` was developed using the [LangChain](https://python.langchain.com/docs/get_started/introduction) framework and the `Claude` LLM (Large Language Model) from [Anthropic](https://www.anthropic.com/news/introducing-claude) available on [AWS Bedrock](https://aws.amazon.com/pt/bedrock/?gclid=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE&trk=82b1c10f-8aa4-4e6c-ab52-c75550a4a31e&sc_channel=ps&ef_id=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE:G:s&s_kwcid=AL!4422!3!692006001529!e!!g!!aws%20bedrock!21054971723!164977098371) platform.


#### Project Adaptations
The data engineering process applied in the project was considerably simplified since the main focus was on working with the AI Data Assistant. However, it would be possible to add more stages to the Data Pipeline to meet the project's needs in cases where: (i) data from various sources (local, API, and other databases in AWS) are to be worked on, (ii) the AI Data Assistant database needs to adhere to a specific business rule, or (iii) unstructured or semi-structured data is involved.

For the aforementioned cases, for example, an AWS Lambda function could be created for data ingestion from an API, and AWS Glue jobs could be created to transform unstructured and semi-structured data into structured data, and then modeled according to the logical model that meets the business rules of the database.

### Project Architecture

The AWS architecture used preferred AWS Lambda, AWS Glue, AWS Athena, Amazon S3, and Amazon Bedrock serverless services to compose the architecture, as follows:

![AI Data Assistant AWS Architecture Diagram](/docs/diagrams/AWSDiagram!AIDataAssistant.jpg)

1. Data is ingested via a Docker container to execute the following [script](/src/load-local-data-into-s3/README.md#documentation) in an Amazon S3 bucket.
2. Once the data is ingested, it is integrated using the AWS Glue Crawler service, which extracts, transforms, and loads the data into a database (created in AWS Lake Formation and AWS Glue Data Catalog).
3. Finally, the end user can interact with a Chatbot, developed by this [script](/src/ai-data-assistant/README.md#documentation), which will create SQL queries based on questions and execute them using Amazon Athena. Upon receiving the query result, the Chatbot will process the result to communicate it in natural language to the end user.

### Sources

- The ingested file is a `csv` from Kaggle containing video game sales data from 1980 to 2016, follow the [File Source](https://www.kaggle.com/code/upadorprofzs/eda-video-game-sales/input?select=vgsales.csv)
- The following references were used for code development:
    - Natalie's (nataindata) repository `AI Data Engineering Project` was the main inspiration for coding and the starting point for study direction: [click here](https://github.com/nataindata/ai-data-engineering-project/blob/main/Nataindata_BigQuery_with_LangChain.ipynb)
    - Ryan Gomes' repository `Conversational AI LLM's with Amazon Lex and Sagemaker`: [click here](https://github.com/aws-samples/conversational-ai-llms-with-amazon-lex-and-sagemaker)
    - Gary A. Stafford's repository `LLM Langchain SQL Demo`: [click here](https://github.com/garystafford/llm-langchain-sql-demo/tree/main)
    - Greg Vinton's article `Generative AI with Amazon Bedrock and Amazon Athena`: [click here](https://repost.aws/articles/ARDEyn8B0aQLud6ZGK7yyX3Q/generative-ai-with-amazon-bedrock-and-amazon-athena)
    - Kushal Dulani's article `Mastering Language Models with AWS Bedrock and LangChain Framework for Generative AI Applications Part-1`: [click here](https://medium.com/into-the-ai-frontier-navigating-genai-computer/mastering-language-models-with-aws-bedrock-and-langchain-%EF%B8%8Fframework-for-generative-ai-e7f786c5e10c)


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
- [Código da Ingestão de Dados](/src/load-local-data-into-s3/README.md#documentação)
    - [Sobre o Código Fonte](/src/load-local-data-into-s3/README.md#sobre-o-código-fonte)
        - [Políticas Necessárias para o Funcionamento do Load Local Data Into S3](/src/load-local-data-into-s3/README.md#políticas-necessárias-para-o-funcionamento-do-load-local-data-into-s3)
        - [Uso do Código Fonte](/src/load-local-data-into-s3/README.md#uso-do-código-fonte)
    - [Considerações sobre o funcionamento do Load Local Data Into S3](/src/load-local-data-into-s3/README.md#)
        - [A Estrutura do Load Local Data Into S3](/src/load-local-data-into-s3/README.md#a-estrutura-do-load-local-data-into-s3)

### Sobre o Projeto

O projeto `AI Data Assistant` é um *chatbot* em que o usuário pode perguntar sobre os dados em um banco de dados e receber resposta em linguagem natural (linguagem humana). O projeto foi desenvolvido para fins de aprendizado na área de Engenharia de Dados, D&A em Geral e AWS.

![Diagram to show how the AI Data Assistant works](/docs/diagrams/AWSDiagram!AI%20DataAssistant%20Generic%20Logic.jpg)

O projeto foi dividido em três etapas:

1. Ingestão dos dados na AWS (por meio de um *container* ***Docker***)
2. Criação de banco de dados a partir dos dados armazenados na AWS
3. Criação de um Assistente de Dados inteligente de uma conexão ao banco de dados criado.

O `AI Data Assistant` foi desenvolvido usando o framework da [LangChain](https://python.langchain.com/docs/get_started/introduction) e o LLM (*Large Language Model* ou Grande Modelo de Linguagem) `Claude` da [Anthropic](https://www.anthropic.com/news/introducing-claude) disponível no [AWS Bedrock](https://aws.amazon.com/pt/bedrock/?gclid=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE&trk=82b1c10f-8aa4-4e6c-ab52-c75550a4a31e&sc_channel=ps&ef_id=CjwKCAjw48-vBhBbEiwAzqrZVOqyWfTR8CxM6lHYtXWp8vFrG4lsCSRcKPuz8X0WcZjqPpXhyaGotBoCYcwQAvD_BwE:G:s&s_kwcid=AL!4422!3!692006001529!e!!g!!aws%20bedrock!21054971723!164977098371)

#### Adaptações do Projeto

A processo de engenharia de dados aplicado no projeto foi bastante simplificado uma vez que a ideia foi trabalhar majoritariamente o `AI Data Assistant`. Entretanto, seria possível adicionar mais fases ao *Data Pipeline* para atender as necessidades do projeto nos casos em que serão trabalhados: (i) dados de várias origens (locais, de API e outros bancos de dados na AWS), (ii) o banco de dados do `AI Data Assistant` precisa atender a uma regra de negócio específica , ou, (iv) dados não-estruturados ou semi-estruturados.

Para os casos acima citados, por exemplo, poderia ser criado uma função AWS Lambda para ingestão dos dados de uma API e criado *jobs* no AWS Glue para transformar os dados não-estruturados e semi-estruturados em dados estruturados e em seguida modelados de acordo com o modelo lógico que atenda as regras de negócio do banco dde dados.

### A Arquitetura do Projeto

A arquitetura da AWS usada prezou por serviços *serverless* AWS Lambda, AWS Glue, AWS Athena, Amazon S3 e Amazon Bedrock, para compor a arquitetura, conforme abaixo:  

![Diagrama da Arquitetura da AWS do Projeto AI Data Assistant](/docs/diagrams/AWSDiagram!AIDataAssistant.jpg)


1. Os dados são ingeridos por meio de um *container* ***Docker*** para executar o seguinte [script](/src/load-local-data-into-s3/README.md#documentação) em um *bucket* do Amazon S3
2. Uma vez que os dados são ingeridos eles são integrados usando o serviço AWS Glue Crawler que vai extrair, transformar e carregar os dados em um banco de dados (criado no AWS Lake Formation e AWS Glue Data Catalog).
3. Por fim, o usuário final pode interagir com um *Chatbot*, desenvolvido por esse [script](/src/ai-data-assistant/README.md#documentação), que criará *queries* SQL com base nas perguntas e as executará usando o Amazon Athena, quando recebido o resultado da *query* o *Chatbot* fará um processamento do resultado para comunicá-lo em linguagem natural ao usuário final.

### Fontes

- O arquivo ingerido é um `csv` do *Kaggle* em que estão registrados os dados de vendas de vídeo-game no período de 1980 a 2016, segue a [Fonte do Arquivo](https://www.kaggle.com/code/upadorprofzs/eda-video-game-sales/input?select=vgsales.csv)
- Para o desenvolvimento do código foram usadas as seguintes referências:
    - O repositório de Natalie (nataindata) `AI Data Engineering Project` foi a principal inspiração para a codificação e o ponto de começo para o direcionamento do estudo: [clique aqui](https://github.com/nataindata/ai-data-engineering-project/blob/main/Nataindata_BigQuery_with_LangChain.ipynb)
    - O repositório de Ryan Gomes `Conversational AI LLM's with Amazon Lex and Sagemaker`: [clique aqui](https://github.com/aws-samples/conversational-ai-llms-with-amazon-lex-and-sagemaker)
    - O repositório de Gary A. Stafford `LLM Langchain SQL Demo`: [clique aqui](https://github.com/garystafford/llm-langchain-sql-demo/tree/main)
    - O artigo `Generative AI with Amazon Bedrock and Amazon Athena` do Greg Vinton: [clique aqui](https://repost.aws/articles/ARDEyn8B0aQLud6ZGK7yyX3Q/generative-ai-with-amazon-bedrock-and-amazon-athena)
    - O artigo `Mastering Language Models with AWS Bedrock and LangChain Framework for Generative AI Applications Part-1` do Kushal Dulani: [clique aqui](https://medium.com/into-the-ai-frontier-navigating-genai-computer/mastering-language-models-with-aws-bedrock-and-langchain-%EF%B8%8Fframework-for-generative-ai-e7f786c5e10c)