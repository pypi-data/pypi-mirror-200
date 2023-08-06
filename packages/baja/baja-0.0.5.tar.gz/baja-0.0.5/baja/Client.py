from baja.Collection import Collection
from baja.Project import Project


class Client:
    def __init__(self, url, token, project_id):
        self.project = Project(url, token, project_id)
        self.collection = Collection(url, token, project_id)

    def get_project(self):
        return self.project

    def get_collection(self):
        return self.collection
