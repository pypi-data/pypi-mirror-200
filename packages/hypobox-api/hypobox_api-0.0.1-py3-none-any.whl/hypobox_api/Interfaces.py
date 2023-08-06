from abc import ABC, abstractmethod


class AbstractProperty(ABC):
    def __init__(self, url, token, project_id):
        self.url = url
        self.token = token
        self.project_id = project_id
        self.current_s3_paths = []
        self.assets = []
        self.filtered_assets = []


class IFetcherCollection(ABC):
    @abstractmethod
    def get_data_from_hypobox(self, collection_name):
        pass


class IFetcherProject(ABC):
    @abstractmethod
    def get_data_from_hypobox(self):
        pass


class IFilter(ABC):
    @abstractmethod
    def filter_by_file_size(self, greater_than=None, less_than=None):
        pass

    @abstractmethod
    def filter_by_file_num_faces(self, greater_than=None, less_than=None):
        pass

    @abstractmethod
    def filter_by_file_num_vertices(self, greater_than=None, less_than=None):
        pass

    @abstractmethod
    def filter_by_orientation(self, equal_to):
        pass


class IClearner(ABC):
    @abstractmethod
    def clear_applied_filters(self):
        pass


class IDownloader(ABC):
    @abstractmethod
    def download(self, folder_name):
        pass

    @abstractmethod
    def download_all(self, folder_name):
        pass


class ICollection(AbstractProperty, IFetcherCollection, IFilter, IClearner, IDownloader, ABC):
    pass


class IProject(AbstractProperty, IFetcherProject, IFilter, IClearner, IDownloader, ABC):
    pass
