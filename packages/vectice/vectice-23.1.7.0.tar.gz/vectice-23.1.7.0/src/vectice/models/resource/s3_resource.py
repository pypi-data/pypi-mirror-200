from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.resource.base import Resource
from vectice.models.resource.metadata.base import DatasetSourceOrigin
from vectice.models.resource.metadata.files_metadata import File, FilesMetadata

if TYPE_CHECKING:
    from mypy_boto3_s3 import Client
    from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef, ObjectTypeDef


class S3Resource(Resource):
    """Wrap columnar data and its metadata in AWS S3.

    Vectice stores metadata -- data about your dataset -- communicated
    with a resource. Your actual dataset is not stored by Vectice.

    This resource wraps data that you have stored in AWS S3.
    You assign it to a step.

    ```python
    from vectice import S3Resource
    from boto3.session import Session

    s3_session = Session(  # (1)
        aws_access_key_id="...",
        aws_secret_access_key="...",
        region_name="us-east-1",
    )
    s3_client = s3_session.client(service_name="s3")  # (2)

    s3_resource = S3Resource(
        s3_client,
        bucket_name="my_bucket",
        resource_path="my_resource_path",
    )
    ```

    1. See [boto3 sessions][boto3.session.Session].
    1. See [boto3 session client][boto3.session.Session.client].

    Note that these three concepts are distinct, even if easily conflated:

    * Where the data is stored
    * The format at rest (in storage)
    * The format when loaded in a running Python program

    Notably, the statistics collectors provided by Vectice operate
    only on this last and only in the event that the data is loaded as
    a pandas dataframe.
    """

    _origin = DatasetSourceOrigin.S3.value

    def __init__(
        self,
        s3_client: Client,
        bucket_name: str,
        resource_path: str,
    ):
        """Initialize an S3 resource.

        Parameters:
            s3_client: The client used to interact with Amazon s3.
            bucket_name: The name of the bucket to get data from.
            resource_path: The paths of the resources to get.
        """
        super().__init__()
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.resource_path = resource_path

    def _fetch_data(self) -> dict[str, bytes]:
        s3_objects_list = self._get_s3_objects_list()
        datas = {}
        for s3_object in s3_objects_list["Contents"]:
            object_path = s3_object["Key"]
            data = self._get_aws_data(object_path)
            datas[f"{self.bucket_name}/{object_path}"] = data
        return datas

    def _get_aws_data(self, object_path: str):
        data_response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_path)
        return data_response["Body"].read()

    def _build_metadata(self) -> FilesMetadata:
        s3_objects_list = self._get_s3_objects_list()
        metadata = self._build_metadata_from_objects(s3_objects_list)
        return metadata

    def _get_s3_objects_list(self) -> ListObjectsV2OutputTypeDef:
        return self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.resource_path)

    def _build_metadata_from_objects(self, s3_objects_list: ListObjectsV2OutputTypeDef) -> FilesMetadata:
        if s3_objects_list["KeyCount"] == 0:
            raise NoSuchS3ResourceError(self.bucket_name, self.resource_path)
        s3_objects = s3_objects_list["Contents"]
        files, total_size = self._build_files_list_with_size(s3_objects)
        metadata = FilesMetadata(files=files, origin=self._origin, size=total_size)
        return metadata

    def _build_files_list_with_size(self, s3_objects: list[ObjectTypeDef]) -> tuple[list[File], int]:
        files: list[File] = []
        total_size = 0
        for object in s3_objects:
            if not self._is_s3_object_a_folder(object):
                name = object["Key"]
                size = object["Size"]
                file = File(
                    name=name,
                    size=size,
                    fingerprint=self._get_formatted_etag_from_object(object),
                    updated_date=object["LastModified"].isoformat(),
                    created_date=None,
                    uri=f"s3://{self.bucket_name}/{name}",
                )
                total_size += size
                files.append(file)
        return files, total_size

    @staticmethod
    def _get_formatted_etag_from_object(object: ObjectTypeDef) -> str:
        return str(object["ETag"].replace("'", "").replace('"', ""))

    @staticmethod
    def _is_s3_object_a_folder(object: ObjectTypeDef) -> bool:
        return bool(object["Key"].endswith("/"))


class NoSuchS3ResourceError(Exception):
    def __init__(self, bucket: str, resource: str):
        self.message = f"{resource} does not exist in the AWS s3 bucket {bucket}."
        super().__init__(self.message)
