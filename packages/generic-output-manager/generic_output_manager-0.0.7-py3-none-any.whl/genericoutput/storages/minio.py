from .storage import Storage
import os
import glob
import json
from alidaargparser import get_asset_property
import boto3

class Minio(Storage):
    storage_type = os.path.basename(__file__).split('.py')[0]
    
    def __init__(self, storage_type=None):
        super().__init__(storage_type)

        if self.base_path is None:
            raise Exception("Base path must be set!")

        endpoint_url = get_asset_property(asset_name="go_manager", property='minIO_URL')
        aws_access_key_id = get_asset_property(asset_name="go_manager", property='minIO_ACCESS_KEY')
        aws_secret_access_key = get_asset_property(asset_name="go_manager", property='minIO_SECRET_KEY')
        
        s3 = boto3.resource('s3', 
            endpoint_url = "http://" + endpoint_url,
            aws_access_key_id = aws_access_key_id, 
            aws_secret_access_key = aws_secret_access_key)
        self.bucket = s3.Bucket(get_asset_property(asset_name="go_manager", property='minio_bucket') )


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
            self.bucket.upload_file(path, dst) #, ExtraArgs={'Metadata': {'a': '2'}})
            metadata['path'] = dst
        
        metadataDst = path + ".json"
        with open(metadataDst, "w") as write_file:
            json.dump(metadata, write_file, indent=4)
        self.bucket.upload_file(metadataDst, dst + ".json")

        return dst
    # def remove(self, path):
    #     dst = os.path.join(self.base_path, os.path.basename(os.path.normpath(path)))
    #     os.remove(dst)
    #     metadataDst = dst + ".json"
    #     os.remove(metadataDst)
