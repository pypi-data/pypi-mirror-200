import asyncio
from functools import wraps
from typing import Any, Callable

from aiohttp import client
from yarl import URL


def deferred_init(func) -> Callable:
    """
    A decorator to indicate that a property should trigger deferred init.
    :param func: the function to wrap.
    :return: a Callable
    """

    @wraps(func)
    def _decorator(self, *args, **kwargs):
        if not self._done_init:
            self._deferred_init()

        return func(self, *args, **kwargs)

    return _decorator


class AWSConnector:
    """
    A class to connect to AWS.
    """

    def _deferred_init(self) -> None:
        """
        This is a deferred init function that will be called when the first
        property is accessed. We defer the init because boto3 has slow startup
        times and this accelerates the test suite.
        :return: None
        """
        import boto3
        from botocore import UNSIGNED
        from botocore.config import Config

        self.config = Config(
            signature_version=UNSIGNED,
            region_name="us-east-1",
        )

        self.signed_config = Config(region_name="us-east-1")

        self._s3_client = (
            boto3.client("s3", config=self.config)
            if not self._endpoint_url
            else boto3.client(
                "s3", endpoint_url=self._endpoint_url, config=self.config
            )
        )

        self._cloudwatch_client = (
            boto3.client(
                "cloudwatch",
                config=self.signed_config,
            )
            if not self._endpoint_url
            else boto3.client(
                "cloudwatch",
                endpoint_url=self._endpoint_url,
                config=self.signed_config,
            )
        )

        self._session = boto3.Session()
        self._resource = (
            self._session.resource("s3", config=self.config)
            if not self._endpoint_url
            else self._session.resource(
                "s3", endpoint_url=self._endpoint_url, config=self.config
            )
        )

        self._bucket = self._resource.Bucket(self._bucket_name)

        self._done_init = True

    def __init__(self, endpoint_url: str = None, bucket: str = ""):
        self._done_init = False
        self._endpoint_url = endpoint_url
        self.config = None
        self._s3_client = None
        self._cloudwatch_client = None
        self._session = None
        self._resource = None
        self._bucket = None
        self._bucket_name = bucket
        self._instrumentation = None

    @property
    def instrumentation(self):
        """
        Return the instrumentation/logging class
        :return: an Instrumentation class
        """
        return self._instrumentation

    @instrumentation.setter
    def instrumentation(self, value):
        """
        Set the instrumentation/logging class
        :param value: an Instrumentation class
        :return: None
        """
        self._instrumentation = value

    @property
    @deferred_init
    def s3_client(self):
        """
        Get the s3 client
        :return: S3 client
        """
        return self._s3_client

    @s3_client.setter
    @deferred_init
    def s3_client(self, value):
        """
        Set the s3 client
        :param value: the s3 client
        :return: None
        """
        self._s3_client = value

    @property
    @deferred_init
    def cloudwatch_client(self):
        """
        Get the CloudWatch client
        :return: the CloudWatch client
        """
        return self._cloudwatch_client

    @cloudwatch_client.setter
    @deferred_init
    def cloudwatch_client(self, value):
        """
        Set the CloudWatch client
        :param value: the CloudWatch client
        :return: None
        """
        self._cloudwatch_client = value

    @property
    @deferred_init
    def s3_resource(self):
        """
        Get the s3 resource
        :return: the s3 resource object
        """
        return self._resource

    @s3_resource.setter
    @deferred_init
    def s3_resource(self, value):
        """
        Set the s3 resource
        :param value: the s3 resource object
        :return: None
        """
        self._resource = value

    @property
    @deferred_init
    def s3_session(self):
        """
        Get the s3 session
        :return: the s3 session object
        """
        return self._session

    @s3_session.setter
    @deferred_init
    def s3_session(self, value):
        """
        Set the s3 session
        :param value: the s3 session object
        :return: None
        """
        self._session = value

    @property
    @deferred_init
    def bucket(self):
        """
        Get the s3 bucket
        :return: the s3 bucket object
        """

        return self._bucket

    async def download_s3_obj(
        self,
        bucket: str,
        key: str,
        aiohttp_session: client.ClientSession,
    ) -> dict:
        """
        Download the s3 object asynchronously
        :param bucket: the bucket to get the object from
        :param key: the key to get
        :param aiohttp_session: an aiohttp session to reuse
        :return: a dictionary of the key and the downloaded object
        """
        if self.instrumentation:
            self.instrumentation.logger.info(f"Async getting s3 object: {key}")

        request_url = self.s3_client.generate_presigned_url(
            "get_object", {"Bucket": bucket, "Key": key}
        )

        async with aiohttp_session.get(
            URL(request_url, encoded=True)
        ) as response:
            result = await response.read()

            result = result.decode("utf-8")

            if not result.startswith("{"):
                # if we hit here, it's an "annotation not found" error
                result = "{}"

            return {key: result}

    async def _get_tasks(
        self, bucket: str, s3_objs: list
    ) -> tuple[list, client.ClientSession]:
        """
        Get the tasks for the async download
        :param bucket: the bucket to get the objects from
        :param s3_objs: the list of s3 objects to get
        :return: a set of tasks and the aiohttp session
        """
        session = client.ClientSession()

        return [
            self.download_s3_obj(
                bucket=bucket,
                key=f,
                aiohttp_session=session,
            )
            for f in s3_objs
        ], session

    def get_multiple_s3_objs(
        self, bucket, s3_objs
    ) -> tuple[
        BaseException | Any,
        BaseException | Any,
        BaseException | Any,
        BaseException | Any,
        BaseException | Any,
    ]:
        """
        Get multiple s3 objects in parallel
        :param bucket: the bucket to get the objects from
        :param s3_objs: the list of s3 objects to get
        :return: a tuple of the results
        """
        loop = asyncio.get_event_loop()
        tasks, session = loop.run_until_complete(
            self._get_tasks(bucket=bucket, s3_objs=s3_objs)
        )
        tasks = loop.run_until_complete(asyncio.gather(*tasks))
        loop.run_until_complete(session.close())

        return tasks

    def s3_obj_to_str(
        self,
        bucket: str,
        s3_path: str,
        raise_on_fail=False,
    ) -> str:
        """
        Get the s3 object as a string
        :param bucket: the bucket to get the object from
        :param s3_path: the path to the object
        :param raise_on_fail: whether to raise an exception if the object is
        not found
        :return: a string result
        """
        if self.instrumentation:
            self.instrumentation.logger.info(f"Getting s3 object: {s3_path}")

        try:
            return (
                self.s3_client.get_object(
                    Bucket=bucket,
                    Key=s3_path,
                )["Body"]
                .read()
                .decode("utf-8")
            )
        except Exception as e:
            if self.instrumentation:
                self.instrumentation.logger.error(
                    f"Error getting s3 object: {s3_path} {e}"
                )
            if raise_on_fail:
                raise S3ObjException(e) from e
            else:
                return "{}"

    @staticmethod
    def s3_to_json_key(key) -> str:
        """
        Get a json key from the s3 key
        :param key: the key
        :return: a string
        """
        return key.split("/")[-1].split(".")[0]


class S3ObjException(Exception):
    """
    Exception for S3 object errors
    """

    pass
