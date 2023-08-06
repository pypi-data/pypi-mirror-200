import requests
import os
from pathlib import Path


class Downloader:
    @staticmethod
    def download_glb(folder_name, current_s3_paths):
        if not os.path.exists(os.path.join(os.path.join(os.getcwd(), folder_name))):
            os.makedirs(os.path.join(os.path.join(os.getcwd(), folder_name)))

        for s3_path in current_s3_paths:
            uuid = Path(s3_path).parts[4]
            file_path = os.path.join(folder_name, f"{uuid}.glb")
            image_response = requests.get(s3_path)

            with open(file_path, 'wb') as f:
                f.write(image_response.content)
