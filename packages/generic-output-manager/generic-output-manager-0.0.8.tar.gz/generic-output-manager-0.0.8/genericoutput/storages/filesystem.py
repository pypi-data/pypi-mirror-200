from .storage import Storage
import os
import glob
import shutil
import json


class Filesystem(Storage):
    storage_type = os.path.basename(__file__).split('.py')[0]
    
    def __init__(self, storage_type=None):
        super().__init__(storage_type)

        # If not specified use /resources. Helps running locally without passing too many parameters
        if self.base_path is None:
            self.base_path = "/resources/generic_outputs"

    def list_files(self):
        return glob.glob(os.path.join(self.base_path, '*.json'))
    
    def save(self, path, metadata):
        
        # Check if is a file or a log
        isFile = True
        if path is None:
            path = metadata['name']
            isFile = False

        dst = os.path.join(self.base_path, os.path.basename(os.path.normpath(path)))
        if isFile:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(path, dst)
        metadataDst = dst + ".json"
        with open(metadataDst, "w") as write_file:
            json.dump(metadata, write_file, indent=4)
    
        return dst
    
    # def remove(self, path):
    #     dst = os.path.join(self.base_path, os.path.basename(os.path.normpath(path)))
    #     os.remove(dst)
    #     metadataDst = dst + ".json"
    #     os.remove(metadataDst)