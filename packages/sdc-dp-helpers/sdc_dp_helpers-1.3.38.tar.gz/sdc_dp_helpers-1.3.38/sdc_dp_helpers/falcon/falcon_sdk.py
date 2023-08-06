# pylint: disable=too-few-public-methods,arguments-differ,import-error,too-many-arguments
""" Falcon Reader SDK"""
from abc import abstractmethod
from typing import List, Dict
import os
from datetime import datetime
import requests

from sdc_dp_helpers.api_utilities.retry_managers import request_handler, retry_handler


class RequestHandler:
    """Interface for  API Call method"""

    def __init__(self, session, creds):
        self.session: requests.Session = session
        self.base_url: str = "https://api.falcon.io/"
        self._creds = creds

    @abstractmethod
    def make_api_call(self, **kwargs):
        """Make API Call"""
        raise NotImplementedError


class FalconAPICall:
    """Class for Making API Call"""

    def __init__(self, session, creds, config):
        self.session = session
        self._creds = creds
        self.config = config
        self.channel_ids = self.get_channel_ids()
        self.start = 0
        self.curr_channels = []

    def get_channel_ids(self):
        """This gets channel ids"""
        channel_id_methods = {"v1": ChannelIdsV1, "v2": ChannelIdsV2}
        version = self.config["version"]
        if version not in channel_id_methods:
            raise KeyError(
                f"unkown value for 'version' in configs, expecting 'v1' or 'v2'. Got {version}"
            )
        channel_ids_caller = channel_id_methods[version](
            session=self.session, creds=self._creds
        )
        channel_ids = channel_ids_caller.make_api_call()

        return channel_ids

    def get_data(
        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> dict:
        """Gets the API Call Handler to Use"""
        endpoint_handlers = {
            "channel_insights": ChannelInsights,
            "content_insights": ContentInsights,
            "published_posts": PublishedPosts,
        }
        endpoint_name = self.config["endpoint_name"]
        if endpoint_name not in endpoint_handlers:
            raise KeyError(
                f"""
                unkown endpoint name in configs, expecting 'channel_insights',
                'content_insights' or 'published_posts'. Got {endpoint_name}
                """
            )
        endpoint_caller = endpoint_handlers[endpoint_name](
            session=self.session, creds=self._creds, config=self.config
        )
        data = endpoint_caller.get_dataset(start_date, end_date, network, channel_ids)

        return data


class ChannelIdsV1(RequestHandler):
    """Class for v1 channel ids"""

    @retry_handler(exceptions=ConnectionError, total_tries=5)
    def make_api_call(self, **kwargs):
        """
        Gather all available channel ids v1.
        """
        print("GET v1: channel ids.")
        endpoint_url = f"channels?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        response = self.session.get(url=url, params={"limit": "9999"})

        response_data = response.json()
        if response.status_code == 200:
            channel_ids = set()
            for item in response_data.get("items", []):
                channel_ids.add(item["id"])

            return list(channel_ids)

        raise ConnectionError(
            f"Falcon API failed to return channel ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )


class ChannelIdsV2(RequestHandler):
    """Class for v2 channel ids"""

    @retry_handler(exceptions=ConnectionError, total_tries=5)
    def make_api_call(self, **kwargs):
        """
        Gather all available channel ids v2.
        """

        print("GET v2: channel ids.")
        endpoint_url = f"channels?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        response = self.session.get(url=url, params={"limit": "9999"})

        response_data = response.json()
        if response.status_code == 200:
            channel_ids = {}
            for item in response_data.get("items", []):
                channel_ids[item["uuid"]] = item["name"]
            return channel_ids

        raise ConnectionError(
            f"Falcon API failed to return channel ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )


class ContentIdByChannelId(RequestHandler):
    """Class to get Content Ids by Channel id"""

    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(
        self, start_date: str, end_date: str, network: str, channel_ids: Dict[str, str]
    ) -> dict:
        print("GET: content ids by channel id.")
        date_filters = f"since={start_date}&until={end_date}"
        endpoint_url = (
            f"publish/items?apikey={self._creds['api_key']}"
            f"&statuses=published"
            f"&networks={network}"
            f"&{date_filters}"
        )
        content_ids_by_channel_id = {}
        while endpoint_url is not None:
            url = f"{self.base_url}{endpoint_url}"
            response = self.session.get(url=url)
            response_data = response.json()
            if response.status_code != 200:
                raise ConnectionError(
                    f"Falcon API failed to return content ids. "
                    f"Status code: {response.status_code}, Reason: {response.reason}."
                )
            for item in response_data.get("items"):
                content_id = item.get("id")
                channel_id = item.get("channels")
                if channel_id is not None:
                    channel_id = channel_id[0]
                    if network == "linkedIn":
                        channel_id = channel_id.replace("-", "")

                    if channel_id in channel_ids:
                        content_ids_by_channel_id.setdefault(channel_id, []).append(
                            content_id
                        )
            endpoint_url = response_data.get("next", {"href": None}).get("href")
        return content_ids_by_channel_id


class PublishedPostsByChannelId(RequestHandler):
    """Gets the published posts by channel id"""

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    @retry_handler(exceptions=TimeoutError, total_tries=5, initial_wait=900)
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=900)
    def make_api_call(
        self,
        start_date: str,
        end_date: str,
        network: str,
        channel_ids: list,
        statuses: str,
        limit: int,
        index: int,
    ) -> list:
        """Gets the published posts by channel id
        SEE: https://falconio.docs.apiary.io/
        #reference/content-api/get-content-metrics-by-channel-ids
        :param: channel_id - integer
        :param: date - string '2022-07-20' but converted to isoformat '2022-07-20T00:00:00'
        :returns: list of dictionaries
        """

        dataset: list = []
        endpoint_url: str = f"publish/items?apikey={self._creds['api_key']}"
        while endpoint_url:
            print(
                f"INFO: channel id index: {index}, "
                f"channel id: {channel_ids},  date: {start_date}, offset: {len(dataset)}."
            )
            response = self.session.get(
                url=f"{self.base_url}{endpoint_url}",
                headers={"Content-Type": "application/json"},
                params={
                    "channels": channel_ids,
                    "since": start_date,
                    "until": end_date,
                    "networks": network,
                    "statuses": statuses,
                    "limit": limit,
                },
            )
            status_code: int = response.status_code
            reason: str = response.reason
            if response.status_code == 200:
                results: dict = response.json()
                items_data: list = results.get("items", [])
                dataset.extend(items_data)

                endpoint_url = results.get("next", {"href": None}).get("href")

                if len(items_data) == 0 or endpoint_url is None:
                    break

            elif reason == "Not Found" and status_code == 404:
                print(f"No data for channel id: {channel_ids}, skipping.\n")
                break
            elif status_code == 429:
                raise TimeoutError("Rolling Window Quota [429] reached.")
            else:
                raise ConnectionError(f"Reason: {reason}, Status: {status_code}.")

        return dataset


class ContentInsightsRequestId(RequestHandler):
    """This class gets Content Insights Request Id"""

    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(
        self,
        start_date: str,
        end_date: str,
        metric_ids: List[str],
        content_ids_by_channel_id: Dict[str, List],
    ) -> Dict[str, str]:
        print("GET: insights request id.")
        endpoint_url = f"measure/v2/insights/content?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        body = {
            "since": start_date,
            "until": end_date,
            "metricIds": metric_ids,
            "channels": [],
        }
        for key, value in content_ids_by_channel_id.items():
            body["channels"].append({"id": key, "contentIds": value})
        response = self.session.post(
            url=url, headers={"Content-Type": "application/json"}, json=body
        )
        if response.status_code == 200:
            response_data = response.json()
            insights_request_id = response_data["insightsRequestId"]
            return insights_request_id

        raise ConnectionError(
            f"Falcon API failed to return content ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )


class ChannelInsightsRequestId(RequestHandler):
    """This class gets Channel Insights Request Id"""

    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(
        self,
        start_date: str,
        end_date: str,
        metric_ids: List[str],
        channel_ids: List[str],
    ) -> Dict[str, str]:
        print("GET: insights request id.")
        start_date = datetime.strftime(
            datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ"), "%Y-%m-%d"
        )
        end_date = start_date
        endpoint_url = f"measure/v2/insights/channel?apikey={self._creds['api_key']}"
        url = f"{self.base_url}{endpoint_url}"
        body = {
            "since": start_date,
            "until": end_date,
            "metricIds": metric_ids,
            "channelIds": channel_ids,
        }
        response = self.session.post(
            url=url, headers={"Content-Type": "application/json"}, json=body
        )
        if response.status_code == 200:
            response_data = response.json()
            insights_request_id = response_data["insightsRequestId"]
            return insights_request_id

        raise ConnectionError(
            f"Falcon API failed to return content ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )


class Insights(RequestHandler):
    """This class gets insights data"""

    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=5)
    def make_api_call(self, insights_request_id: Dict[str, str] = None):
        print("GET: insights.")
        endpoint_url = (
            f"measure/v2/insights/{insights_request_id}?apikey={self._creds['api_key']}"
        )
        url = f"{self.base_url}{endpoint_url}"
        response = self.session.get(url=url)

        response_data = response.json()
        if response.status_code == 200:
            if response_data["status"] == "READY":
                return response_data
            if response_data["status"] == "EXPIRED":
                return None
        raise ConnectionError(
            f"Falcon API failed to return content ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )


class ContentInsights(FalconAPICall):
    """This class  gets content insights and normalises the data"""

    @staticmethod
    def _normalize_data(dataset: dict, network: str, channel_ids: dict) -> List[Dict]:
        temp = {}

        for metric, data_items in dataset.items():
            if not data_items:
                # if we have nothing in value
                continue
            for data in data_items:
                data[metric] = data.pop("value")
                data["network"] = network
                data["brand"] = channel_ids.get(data["channelId"], None)
                check_point = tuple(map(data.get, ["channelId", "date", "contentId"]))
                if not temp.get(check_point):
                    temp[check_point] = data
                else:
                    missing_keys = set(data).difference(set(temp[check_point]))
                    # flatten
                    for key in missing_keys:
                        temp[check_point].update({key: data[key]})
        normalized_data = list(temp.values())
        return normalized_data

    def get_dataset(
        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> dict:
        """Fucntion handles content insights query"""
        channel_steps = self.config.get("channel_steps", 10)
        metric_ids = self.config["metrics"]
        content_ids_by_channel_id = ContentIdByChannelId(
            creds=self._creds, session=self.session
        ).make_api_call(
            start_date=start_date,
            end_date=end_date,
            network=network,
            channel_ids=channel_ids,
        )
        channels = list(content_ids_by_channel_id.keys())
        channel_id_length = len(channels)
        dataset = []
        data = []
        for _ in range(0, channel_id_length, channel_steps):
            self.curr_channels = channels[self.start : self.start + channel_steps]
            request_content_ids_by_channel_id = {
                key: value
                for key, value in content_ids_by_channel_id.items()
                if key in self.curr_channels
            }

            if len(request_content_ids_by_channel_id) > 0:
                insights_request_id = ContentInsightsRequestId(
                    creds=self._creds, session=self.session
                ).make_api_call(
                    start_date=start_date,
                    end_date=end_date,
                    metric_ids=metric_ids,
                    content_ids_by_channel_id=request_content_ids_by_channel_id,
                )
                results = Insights(
                    creds=self._creds, session=self.session
                ).make_api_call(insights_request_id)
                if results is None:
                    insights_request_id = ContentInsightsRequestId(
                        creds=self._creds, session=self.session
                    ).make_api_call(
                        start_date=start_date,
                        end_date=end_date,
                        metric_ids=metric_ids,
                        content_ids_by_channel_id=request_content_ids_by_channel_id,
                    )
                    results = Insights(
                        creds=self._creds, session=self.session
                    ).make_api_call(insights_request_id)
                data = results["data"]["insights"]
                dataset.extend(self._normalize_data(data, network, channel_ids))
            self.start = self.start + channel_steps
        return dataset


class ChannelInsights(FalconAPICall):
    """This class  gets channel insights and normalises the data"""

    @staticmethod
    def _normalize_data(dataset: dict, network: str, channel_ids: dict) -> List[Dict]:
        templist = []

        for metric, data_items in dataset.items():
            if not data_items:
                # if we have nothing in value
                continue
            for data in data_items:
                data[metric] = data.pop("value")
                data["network"] = network
                data["brand"] = channel_ids.get(data["channelId"], None)
                templist.append(data)
        normalized_data = templist

        return normalized_data

    def get_dataset(
        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> dict:
        """Fucntion handles channel insights query"""
        channels = list(channel_ids.keys())
        channel_id_length = len(channels)
        channel_steps = self.config.get("channel_steps", 10)
        metric_ids = self.config["metrics"]
        dataset = []
        data = []
        for _ in range(0, channel_id_length, channel_steps):
            self.curr_channels = channels[self.start : self.start + channel_steps]
            insights_request_id = ChannelInsightsRequestId(
                creds=self._creds, session=self.session
            ).make_api_call(
                start_date=start_date,
                end_date=end_date,
                metric_ids=metric_ids,
                channel_ids=self.curr_channels,
            )
            results = Insights(creds=self._creds, session=self.session).make_api_call(
                insights_request_id
            )
            if results is None:
                insights_request_id = ChannelInsightsRequestId(
                    creds=self._creds, session=self.session
                ).make_api_call(
                    start_date=start_date,
                    end_date=end_date,
                    metric_ids=metric_ids,
                    channel_ids=self.curr_channels,
                )
                results = Insights(
                    creds=self._creds, session=self.session
                ).make_api_call(insights_request_id)
            data = results["data"]["insights"]
            dataset.extend(self._normalize_data(data, network, channel_ids))
            self.start = self.start + channel_steps
        return dataset


class PublishedPosts(FalconAPICall):
    """This class gets published posts data"""

    def get_dataset(
        self, start_date: str, end_date: str, network: str, channel_ids: list
    ) -> dict:
        """Fucntion handles published posts query"""
        print(f"Attempting to gather metrics from {len(channel_ids)} channel ids.")
        statuses = self.config.get("statuses", "published")
        limit = self.config.get("limit", 2000)
        dataset = []
        for channel_id in channel_ids:
            self.curr_channels = [channel_id]
            results = PublishedPostsByChannelId(
                creds=self._creds, session=self.session
            ).make_api_call(
                start_date=start_date,
                end_date=end_date,
                network=network,
                channel_ids=[channel_id],
                statuses=statuses,
                limit=limit,
                index=self.start,
            )
            print(len(results))
            dataset.extend(results)
            self.start += 1
        return dataset
