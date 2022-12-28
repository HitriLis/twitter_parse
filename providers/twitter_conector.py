from json.decoder import JSONDecodeError
import httpx
from settings import settings


test = 'http://uJEM1BHn:HBPjf7Tc@212.193.143.51:48707'


class TwitterClient:
    """
    Модуль интеграции с twitter
    """

    def __init__(self):
        self.base_url = 'https://api.twitter.com/1.1/'
        self.base_headers = {
            'Authorization': f'Bearer {settings.vendor_twitter_api_bearer_token}',
        }

    @staticmethod
    def _force_json(response: httpx.Response) -> dict:
        try:
            return response.json()
        except (JSONDecodeError, TypeError, AttributeError):
            return {}

    def __urljoin(self, path):
        return '/'.join([self.base_url.strip('/'), path.strip('/')])

    async def call(self, method: str, url: str, json_data: dict = None, **kwargs):
        """
        Отправляет запрос к апи
        :param method: метод запроса
        :param url: path запроса,
        :param json_data: тело запроса
        :return:
        """

        async with httpx.AsyncClient(proxies=test, headers=self.base_headers) as client:
            url = self.__urljoin(url)
            try:
                response = await client.request(method=method, url=url, json=json_data, **kwargs)
                response_data = self._force_json(response)
                return response_data, response.status_code
            except Exception as e:
                print(e)

    async def get_user_screen_name(self, screen_name: str):
        search_params = {
            "screen_name": screen_name
        }

        data, status_code = await self.call(method='GET', url='users/show.json', params=search_params)
        return {
            'twitter_id': data.get('id'),
            'name': data.get('name'),
            'username': data.get('screen_name'),
            'followers_count': data.get('followers_count'),
            'description': data.get('description'),
        } if status_code == 200 else None

    async def get_tweets(self, twitter_id: int):
        search_params = {
            "user_id": twitter_id,
            'count': 7
        }

        data, status_code = await self.call(method='GET', url='statuses/user_timeline.json', params=search_params)
        return data if status_code == 200 else None


twitter_api = TwitterClient()
