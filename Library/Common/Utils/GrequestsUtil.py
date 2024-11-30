import json
import grequests
import logging

from requests import Response
from urllib.parse import urlparse, parse_qs
from Library.Common.enum.HeadersEnum import RequestHeaderEnum

logging.basicConfig(level=logging.INFO)


class GRequestsUtil:

    @staticmethod
    def build_headers(url: str, extra_headers: dict = None):
        """
        构建请求头内容
        :param url: url
        :param extra_headers: 自定义请求头字典 如:{ "Sign" : "Sign" }
        :return: headers
        """
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0.0.0 Safari/537.36'
        }
        # 添加不同服务端需要的请求头
        for header_enum in RequestHeaderEnum:
            keywords, custom_headers = header_enum.value
            if any(keyword in url for keyword in keywords):
                headers.update(custom_headers)
                break
        else:
            _, custom_headers = RequestHeaderEnum.OTHER.value
            headers.update(custom_headers)
        # 支持入参添加请求头
        if extra_headers:
            headers.update(extra_headers)
        return headers

    @staticmethod
    def common_get(url, params=None, extra_headers: dict = None, callback=None):
        """
        GET请求
        :param url:
        :param params:
        :param extra_headers:  自定义请求头字典 如:{ "Sign" : "Sign" }
        :param callback:
        :return: partial
        """
        headers = GRequestsUtil.build_headers(url, extra_headers)
        return grequests.get(url, headers=headers, params=params, callback=callback)

    @staticmethod
    def common_post(url, json_data=None, extra_headers: dict = None, callback=None):
        """
        POST请求
        :param url:
        :param json_data:
        :param extra_headers: 自定义请求头字典 如:{ "Sign" : "Sign" }
        :param callback:
        :return: partial
        """
        headers = GRequestsUtil.build_headers(url, extra_headers)
        return GRequestsUtil.map_requests(grequests.post(url, headers=headers, json=json_data, callback=callback))[0]

    @staticmethod
    def send_request(request):
        """
        执行单个请求
        :param request: partial
        :return: request.response
        """
        return GRequestsUtil.map_requests([request])[0]

    @staticmethod
    def map_requests(requests_data, size=None):
        """
        执行批量请求
        :param requests_data:
        :param size: 步长
        :return: [request.response]
        """
        if type(requests_data) != list:
            requests_data = [requests_data]
        response_list = grequests.map(requests_data, size=size)
        # return [GRequestsUtil.response_callback(response) for response in response_list]
        return [response.json() for response in response_list]

    @staticmethod
    def response_callback(response: Response):
        """
        请求响应自定义回调函数
        :param response: request.response
        :return: 自定义字典
        """
        result = {'url': response.url if response else 'Unknown URL', 'success': False}
        if response:
            logging.info(f"URL: {response.url}, 请求方法: {response.request.method}")
            if response.request.method == 'GET':
                query_params = parse_qs(urlparse(response.url).query)
                logging.info(f"查询参数: {query_params}")
            elif response.request.method == 'POST' and response.request.body:
                try:
                    request_data = json.loads(response.request.body)
                    logging.info(f"请求数据: {request_data}")
                except json.JSONDecodeError:
                    logging.error(f"请求数据: {response.request.body}")

            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'image' in content_type:  # 验证码接口
                    result.update({'success': True, 'data': ""})
                elif 'application/json' in content_type:
                    try:
                        data = json.loads(response.text)
                        result.update({'success': True, 'data': data})
                    except json.JSONDecodeError:
                        logging.error(f"解析 JSON 响应失败，来自 {response.url}")
                else:
                    logging.error(f"未知内容类型: {content_type}，来自 {response.url}")
            else:
                logging.error(f"请求 {response.url} 失败，状态码 {response.status_code}")
        else:
            logging.error(f"未收到响应<response>:{response.json()}")
        logging.info(f"<response_callback> 响应数据: {result}")
        return result


if __name__ == '__main__':
    urls = [
        "https://jsonplaceholder.typicode.com/posts?userId=1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]
    requests = [GRequestsUtil.common_get(url) for url in urls]
    responses = GRequestsUtil.map_requests(requests)
    print(responses)
