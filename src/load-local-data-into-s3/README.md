# Load Local Data Into S3

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

### About the Source Code

The `Load Local Data Into S3` is a layered program with `controller`, `services`, and `repositories`, and its main functionality is to perform ETL (Extract, Transform, and Load) of `csv` files from a folder in Amazon S3.

For this purpose, a Docker container is used, which will use the image in the [Dockerfile](/src/load-local-data-into-s3/Dockerfile). The source code and the file will be loaded into the container, and then the source code will be executed.

![Diagram of the Load Local Data Into S3](/docs/diagrams/AWSDiagram!LoadLocalDataIntoS3.jpg)

#### Required Policies for Load Local Data Into S3 Operation

It is necessary to have the permission assigned to an IAM User to upload, list buckets, and create buckets on Amazon S3.

#### Usage of the Source Code

1. The first step is to create a `.env` file in the root of the project `/src/load-local-data-into-s3` with the following environment variables filled in:

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SESSION_TOKEN=
AWS_REGION=
AWS_S3_BUCKET_NAME=
S3_ZONE=
INPUT_DIRFILES=
```

2. The variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` are variables of the IAM User credential, however, `AWS_SESSION_TOKEN` is not mandatory for the program. Finally, it is also necessary to inform the AWS region.

3. The variables `AWS_S3_BUCKET_ZONE`, `S3_ZONE`, and `INPUT_DIRFILES` are necessary for the function to work, however, they can be passed as parameters through flags:
    - For the name of the S3 Bucket: `-b <bucket name>` or `--bucketName <bucket name>`;
    - For the directory where the files to be ingested are located: `-idir <path>` or `--inputDir <path>`;
    - To name the zone where the files will be ingested: `-z <zone>` or `--zone <zone>`

4. Once the environment variables are configured, there are two paths:
    1. Manually create the Docker image and container, or;
    2. Execute the `run_app.sh` file that will perform the routine automatically.

### Considerations on Load Local Data Into S3 Operation

#### Structure of Load Local Data Into S3

The `Load Local Data Into S3` was developed in layers following the Object-Oriented Programming paradigm, where there are the following classes: `LoaderService`, `S3Repository`, `ExtractorService`, and `ETLController`.

As per the following Class Diagram:

![Class Diagram of Load Local Data Into S3](/docs/diagrams/ClassDiagram!LoadLocalDataIntoS3.jpg)

The idea is that each of the classes is responsible for a function of the ETL process, with the `controllers` handling the calls and services, the `services` handling the logic, and the `repositories` handling the connection to external APIs.

Since there is no need to transform the data, there is no need for a `services` to perform data transformation.

The Source Code is executed as per the following Sequence Diagram:

![Sequence Diagram of Load Local Data Into S3](/docs/diagrams/SequenceDiagram!LoadLocalDataIntoS3.jpg)

1. The user executes the code from [run_app.sh](/src/load-local-data-into-s3/run_app.sh)

2. A Docker image pointing to a volume is created.

3. A container is created based on the image and will receive the source code, the `.env` file, and the files to be ingested.

4. The container will execute the source code `LoadLocalDataIntoS3`.

5. An instance of the `S3Repository` class will be instantiated, which will be responsible for making calls to the [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) API.

6. Next, an instance of `ExtractorService` will be instantiated, and finally `LoaderService` - the constructor of the `LoaderService` class will receive `S3Repository` as its parameter.

7. Instances of `ExtractorService` and `LoaderService` will be passed as parameters to the constructor of the `ETLController` class, which will be instantiated.

8. Once the `ETLController` class is instantiated, the `uploadFilesFromLocalDir()` method of the `ETLController` class instance will be triggered.

9. The `uploadFilesFromLocalDir()` method will call the `extractFilesPathFromDir()` method of the `ExtractorService` object, which will return a list with the `path` of each file in the directory.

10. Still in the routine of the `uploadFilesFromLocalDir()` method, the `loadFiles()` method of the `LoaderService` object will be called.

11. Within the routine of the `loadFiles()` method of the `LoaderService` object, it will be checked if a bucket has been created; if not, it will be created. Finally, the files will be loaded into the zone within the bucket.

12. The routine of the `uploadFilesFromLocalDir()` method will be completed, and the result of the data ingestion operation will be printed to the console.

13. The routine of the [run_app.sh](/src/load-local-data-into-s3/run_app.sh) file will continue, saving the log of the operation.

14. Next, the Docker container, image, and volume will be deleted.

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

### Sobre o Código Fonte

O `Load Local Data Into S3` é um programa desenvolvido em camadas com `controller`, `services` e `repositories`, e sua principal funcionalidade é fazer o ETL (Extract, Transform and Load ou Extrair, Transformar e Carregar) dos arquivos `csv` de uma pasta no Amazon S3.

Para isso é usado um *container* *Docker* que usará a imagem no [Dockerfile](/src/load-local-data-into-s3/Dockerfile), no *container* será carregado o código fonte e o arquivo e em seguida executado o código fonte.

![Diagram of the Load Local Data Into S3](/docs/diagrams/AWSDiagram!LoadLocalDataIntoS3.jpg)

#### Políticas Necessárias para o Funcionamento do Load Local Data Into S3

É necessário ter a permissão atribuída a um *IAM USER* para fazer o *upload*, listar *buckets* e criar *buckets*, no Amazon S3.

#### Uso do Código Fonte

1. O primeiro passo é criar um arquivo `.env` na raiz do projeto `/src/load-local-data-into-s3` com as seguintes variáveis de ambiente preenchidas:

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SESSION_TOKEN=
AWS_REGION=
AWS_S3_BUCKET_NAME=
S3_ZONE=
INPUT_DIRFILES=
```

2. As variáveis `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `AWS_SESSION_TOKEN`, são variáveis da credencial do *IAM User*, entretanto, a `AWS_SESSION_TOKEN` não é obrigatória para o programa. Por fim, é também necessário informar a região da AWS.

3. As variáveis `AWS_S3_BUCKET_ZONE`, `S3_ZONE` e `INPUT_DIRFILES`, são necessárias para o funcionamento da função, entretanto, podem ser passadas como parâmetros por meio de *flags*:
    - Para o nome do Bucket do S3: `-b <coloque o nome>` ou `--bucketName <coloque o nome>`;
    - Para o diretório em que se encontram os arquivos a ser ingeridos: `-idir <path>` ou `--inputDir <path>`;
    - Para nomear a zona em que os arquivos serão ingeridos: `-z <zona>` ou `--zone <zona>`

4. Configurada as variáveis de ambiente, é possível dois caminhos:
    1. Criar a imagem e container Docker de forma manual, ou;
    2. Executar o arquivo `run_app.sh` que fará a rotina de forma automatizada.

### Considerações sobre o funcionamento do Load Local Data Into S3

#### A Estrutura do Load Local Data Into S3

o `Load Local Data Into S3` foi desenvolvido em camadas seguindo o paradigma da Programação Orientada ao Objeto em que há as seguintes classes: `LoaderService`, `S3Repository`, `ExtractorService` e `ETLController`.

Conforme o Diagrama de Classe a seguir:

![Diagrama de Classe do Load Local Data Into S3](/docs/diagrams/ClassDiagram!LoadLocalDataIntoS3.jpg)

A ideia é que cada uma das classes fique responsável por uma função do processo de ETL, os `controllers` ficando com a função de gerenciar as chamadas e serviços e os `services` encarregados com a lógica e o `repositories` com a conexão com API externas.

Como não há necessidade de transformar os dados não há a necessidade de um `services` para fazer a transformação de dados.

O Código Fonte é executado conforme o seguinte Diagrama de Sequência:

![Diagrama de Sequência do Load Local Data Into S3](/docs/diagrams/SequenceDiagram!LoadLocalDataIntoS3.jpg)

1. O usuário executa o código do [run_app.sh](/src/load-local-data-into-s3/run_app.sh)

2. É criada uma imagem do Docker que apontará para um volume.

3. Um *container* será criado com base na imagem e receberá o código fonte, o arquivo `.env` e os arquivos a serem ingeridos.

4. O *container* executará o código fonte `LoadLocalDataIntoS3`.

5. Será instanciado uma instância da classe `S3Repository`, essa classe ficará responsável por fazer as chamadas a API do [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

6. Em seguida será instanciado uma instância de `ExtractorService` e, por fim, `LoaderService` - o construtor da classe `LoaderService` receberá em seu parâmetro S3Repository.

7. As instâncias de `ExtractorService` e `LoaderService` serão passadas por parâmetro ao construtor da classe `ETLController` que será instanciada.

8. Instanciada a classe `ETLController`, será acionado o método `uploadFilesFromLocalDir()` da instância da classe `ETLController`.

9. O método `uploadFilesFromLocalDir()` fará a chamada ao método `extractFilesPathFromDir()` do objeto `ExtractorService` que vai retornar uma lista com os `path` de cada arquivo no diretório.

10. Ainda na rotina do método `uploadFilesFromLocalDir()` será chamado o método `loadFiles()` do objeto `LoaderService`.

11. Dentro da rotina do método `loadFiles()` do objeto `LoaderService` será checado se há uma *bucket* criado, caso não será criado. Por fim, os arquivos serão carregados na *zone* dentro do *bucket*.

12. A rotina do método `uploadFilesFromLocalDir()` será encerrada e imprimido no console o resultado da operação de ingestão de dados.

13. Será dado continuidade a rotina do arquivo [run_app.sh](/src/load-local-data-into-s3/run_app.sh) que salvará o log da operação.

14. Em seguida, serão deletados os *container*, imagem e volume, do Docker.

