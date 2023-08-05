from .file import File

class Picture(File):

    def __init__(self, name, localPath, title=None, description=None, var=None) -> None:
        super().__init__(name=name, localPath=localPath, title=title, description=description, var=var, messageType="picture")
