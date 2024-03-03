# services
from services.extractor import ExtractorService
from services.loader import LoaderService

class ETLController:
    def __init__(self, loaderService: LoaderService, extractorService: ExtractorService):
        self._services = {
            "extractor": extractorService,
            "loader": loaderService
        }
    
    def uploadFilesFromLocalDir(self, dirFiles:str, bucketName: str, s3_zone: str):
        try:
            # get files paths in files directory
            filesPath = self._services["extractor"].extractFilesPathFromDir(dirFiles=dirFiles)

            # load files from files path
            self._services["loader"].loadFiles(filesPath=filesPath,
                                               bucketName=bucketName,
                                               s3_zone=s3_zone)
        except Exception as e:
            print(e)



    