import copy

import requests
from baja.Downloader import Downloader
from baja.Filter import Filter
from baja.Interfaces import IProject
from baja.Utils import Utils


class Project(IProject):
    def __init__(self, url, token, project_id):
        self.url = url
        self.token = token
        self.project_id = project_id
        self.current_s3_paths = []
        self.assets = []
        self.filtered_assets = []

    def get_data_from_hypobox(self):
        project = requests.get(f"{self.url}/api/project/{self.project_id}/asset/", headers={'Token': self.token}).json()

        self.assets = [asset for asset in project.get('results', []) if asset['models']]

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
        print(self.filtered_assets)
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
