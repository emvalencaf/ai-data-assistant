import os
from glob import glob

class ExtractorService:
    def __init__(self):
        pass

    def extractFilesPathFromDir(self, dirFiles: str) -> list[str]:
        # verifies if the directory does exist
        if not os.path.exists(dirFiles):
            raise Exception(f"The path directory {dirFiles} does not exists")
        
        # List all files in directory
        print(f"[System] - in the {dirFiles} are theses files:")
        print(os.listdir(dirFiles))

        # find csv in directory
        files = glob(os.path.join(dirFiles,"*.csv"))

        return files