# Load Local Data Into S3

## Summary
- [Documentation (Brazilian Portuguese)](/src/load-local-data-into-s3/README.md#documentação)
- [Documentation (USA English)](/src/load-local-data-into-s3/README.md#documentation)

## Documentation

## Documentação

### Breve Resumo

Esse módulo do projeto trata em ingerir os dados locais em um *bucket* do S3 da AWS por meio do SDK (*Software Development Kit*) [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) via [Docker](https://docs.docker.com/).

### Arquitetura do Código

O código foi desenvolvimento em camadas ficando cada camada responsável por uma funcionalidade, conforme o diagrama de classe abaixo:
![Diagrama de Classe do Módulo de Ingestão de Dados Locais ao S3](/docs/diagrams/ClassDiagram!LoadLocalDataIntoS3.jpg)
- A classe `S3Repository` é a responsável por chamar os comandos da API do do Boto3 e, portanto, é essa a classe que faz a "conexão" entre a AWS e o código.
- A classe `ExtractorService` é a responsável por pegar e retornar os *paths* dos arquivos em um diretório
- A classe `LoaderService` é a responsável por a partir da extração dos *paths* dos arquivos carregar (usando o `S3Repository`) no *bucket* da S3 os arquivos `csv` locais.
- A classe `ETLController` é responsável por chamar os métodos do `LoaderService` e `ExtractorService`

###