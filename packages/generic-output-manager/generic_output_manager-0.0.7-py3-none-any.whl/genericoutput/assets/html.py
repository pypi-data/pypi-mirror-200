from .file import File

class Html(File):

    def __init__(self, name, localPath, title=None, description=None, var=None):
        super().__init__(name=name, messageType="html", localPath=localPath, title=title, description=description, var=var)
