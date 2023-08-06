import requests

from hypobox_api.Interfaces import ICollection
from hypobox_api.Downloader import Downloader
from hypobox_api.Filter import Filter
from hypobox_api.Utils import Utils
import copy


class Collection(ICollection):
    def __init__(self, url, token, project_id):
        self.url = url
        self.token = token
        self.project_id = project_id
        self.current_s3_paths = []
        self.assets = []
        self.filtered_assets = []

    def get_data_from_hypobox(self, collection_name):
        project_response = requests.get(f"{self.url}/api/project/{self.project_id}/asset/",
                                        headers={'Token': self.token}).json()
        collection_response = requests.get(f"{self.url}/api/project/{self.project_id}/collection/",
                                           headers={'Token': self.token}).json()

        collections = collection_response.get('results')

        # Use a list comprehension to find the current collection
        current_collection = next((c for c in collections if c['name'] == collection_name), None)

        if current_collection is None:
            self.current_s3_paths = []
            return self

        # Use a list comprehension and generator expression to find the s3 paths
        self.assets = [asset
                       for asset_id in current_collection.get('assets', [])
                       for asset in project_response.get('results', [])
                       if asset_id == asset['id'] and asset['images']]

        self.filtered_assets = copy.deepcopy(self.assets)

        return self

    def filter_by_file_size(self, greater_than=None, less_than=None):
        self.filtered_assets = Filter.filter_by_number(self.filtered_assets, 'file_size', greater_than, less_than)
        return self

    def filter_by_file_num_faces(self, greater_than=None, less_than=None):
        self.filtered_assets = Filter.filter_by_number(self.filtered_assets, 'num_faces', greater_than, less_than)
        return self

    def filter_by_file_num_vertices(self, greater_than=None, less_than=None):
        self.filtered_assets = Filter.filter_by_number(self.filtered_assets, 'num_vertices', greater_than, less_than)
        return self

    def filter_by_orientation(self, equal_to):
        self.filtered_assets = Filter.filter_by_string(self.filtered_assets, 'orientation', equal_to)
        return self

    def clear_applied_filters(self):
        self.filtered_assets.clear()
        self.filtered_assets = copy.deepcopy(self.assets)
        return self

    def download(self, folder_name):
        Downloader.download_glb(folder_name, Utils.get_s3_paths_from_assets(self.filtered_assets))
        return self

    def download_all(self, folder_name):
        Downloader.download_glb(folder_name, Utils.get_s3_paths_from_assets(self.assets))
        return self
