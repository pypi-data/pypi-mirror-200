from .gasset import GAsset
import os

class File(GAsset):
    def __init__(self, name, localPath, title=None, description=None, var=None, messageType="file"):
        super().__init__(name=name, title=title, description=description, var=var, messageType=messageType)
        self.localPath = localPath
        self.path = None

    def set_path(self, path):
        self.localPath = path

    def get_path(self):
        return self.localPath
    
    def update_infos(self):
        self.set_extension_based_on_path()
        self.set_filename_based_on_path()
        
    def set_extension_based_on_path(self):
        self.extension = self.localPath.split(".")[-1]

    def set_filename_based_on_path(self):
        self.filename = os.path.basename(os.path.normpath(self.localPath))

    def to_json(self):
        
        self.update_infos()

        result = super().to_json()
        result['localPath'] = self.localPath 
        result['path'] = self.path
        result['extension'] = self.extension
        result['filename'] = self.filename

        return result

