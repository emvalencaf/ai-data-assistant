# repositories
from repositories.s3 import S3Repository

# services
from services.extractor import ExtractorService
from services.loader import LoaderService

# controller
from controllers.etl import ETLController

# instanced s3 repository
s3Repository = S3Repository()

# instanced loader service
loaderService = LoaderService(s3Repository=s3Repository)

# instanced extractor service
extractorService = ExtractorService()

# instanced etl controller
ingestLocalDataApp = ETLController(extractorService=extractorService,
                                   loaderService=loaderService)