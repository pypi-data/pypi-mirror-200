from abc import abstractmethod


class BasicBotoS3:
    @abstractmethod
    def __init__(self, boto_service):
        pass

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def upload_file(self, bucket_path: str, file_path: str, file_path_new: str):
        pass

    @abstractmethod
    def download_file(self, bucket_path: str, file_path: str, file_path_new: str):
        pass

    @abstractmethod
    def has_file(self, bucket_path: str, file_path: str) -> bool:
        pass


class BotoS3:
    def __init__(self, interactor_service):
        self.interactor_service = interactor_service

    def upload_file(self,
                    bucket_path: str,
                    file_path: str,
                    file_path_new: str):
        self.interactor_service.upload_file(
            bucket_path=bucket_path,
            file_path=file_path,
            file_path_new=file_path_new,)

    def download_file(self,
                      bucket_path: str,
                      file_path: str,
                      file_path_new: str):
        self.interactor_service.download_file(
            bucket_path=bucket_path,
            file_path=file_path,
            file_path_new=file_path_new,)

    def has_file(self, bucket_path: str, file_path: str) -> bool:
        return self.interactor_service.has_file(
            bucket_path=bucket_path,
            file_path=file_path
        )
