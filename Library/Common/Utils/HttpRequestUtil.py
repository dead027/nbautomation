#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/12 17:30
import requests
import ssl
from Library.Common.Utils.SingletonTypeUtil import SingletonType
from Library.Common.Utils.Contexts import *
from Library.Common.Enum.HeadersEnum import RequestHeaderEnum
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HttpRequestUtil(metaclass=SingletonType):
    session = requests.session()
    session.verify = False

    @staticmethod
    def build_headers(url: str, extra_headers: dict = None, content_type: str = 'json'):
        """
        构建请求头内容
        :param url: url
        :param extra_headers: 自定义请求头字典 如:{ "Sign" : "Sign" }
        :param content_type: json | params
        :return: headers
        """
        content_type_dic = {"json": 'application/json;charset=UTF-8',
                            'params': 'application/x-www-form-urlencoded; charset=UTF-8'}
        headers = {
            'Content-Type': content_type_dic[content_type],
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0.0.0 Safari/537.36',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Sign": ""
        }
        # 添加不同服务端需要的请求头
        # for header_enum in RequestHeaderEnum:
        #     keywords, custom_headers = header_enum.value
        #     if any(keyword in url for keyword in keywords):
        #         headers.update(custom_headers)
        #         break
        # else:
        #     _, custom_headers = RequestHeaderEnum.CLIENT.value
        #     headers.update(custom_headers)
        for header_enum in RequestHeaderEnum:
            keywords, custom_headers = header_enum.value
            if any(keyword in url for keyword in keywords):
                headers.update(custom_headers)
                break
        # 支持入参添加请求头
        if extra_headers:
            headers.update(extra_headers)
        return headers

    @staticmethod
    def get(url, json=None, params=None, headers=None, check_code=True, site_index='1'):
        print(f'【Get 请求地址】\n{url}')
        if json:
            print(f'【请求内容 json】\n{json}')
        if params:
            print(f'【请求内容 params】\n{params}')
        if not headers:
            for header_enum in RequestHeaderEnum:
                if any(keyword in url for keyword in header_enum.value[0]):
                    if header_enum.name == 'ADMIN':
                        headers = header_backend_context.get()
                    elif header_enum.name == 'SITE_ADMIN':
                        headers = header_site_context_1.get() if int(site_index) == 1 else header_site_context_2.get()
                    elif header_enum.name == 'AGENT':
                        headers = header_agent_context_1.get() if int(site_index) == 1 else header_agent_context_2.get()
                    elif header_enum.name == 'CLIENT':
                        headers = header_client_context_1.get() if int(site_index) == 1 else \
                            header_client_context_2.get()
                    elif header_enum.name == 'SbClient':
                        headers = sb_client_context.get()
                    else:
                        pass
                    break
            else:
                raise AssertionError("无法判断是什么后台，请检查url")
        # print(f'【请求内容 headers】\n{headers}')
        resp = HttpRequestUtil.session.get(url, params=params, json=json, headers=headers).json()
        if resp['code'] != 10000 and check_code:
            raise AssertionError(f"Http响应状态码异常: \n{resp['code']}, message: {resp['message']}")
        print(f'【响应】\n {resp.json()}')
        return resp

    @staticmethod
    def post(url, json=None, params=None, headers=None, all_page=False, check_code=True, return_origin=False,
             files=None, data=None, return_total=False, site_index='1'):
        """
        post
        :param url:
        :param json:
        :param params:
        :param headers:
        :param files:
        :param data:
        :param all_page: 是否获取所有页
        :param check_code: 是否检查状态码
        :param return_origin: 是否返回原值
        :param return_total: 是否返回总计
        :param site_index:
        :return:
        """
        print(f'【Post 请求地址】\n{url}')
        if json:
            print(f'【请求内容 json】\n{json}')
        if params:
            print(f'【请求内容 params】\n{params}')
        if not headers:
            for header_enum in RequestHeaderEnum:
                if any(keyword in url for keyword in header_enum.value[0]):
                    if header_enum.name == 'ADMIN':
                        headers = header_backend_context.get()
                    elif header_enum.name == 'SITE_ADMIN':
                        headers = header_site_context_1.get() if int(site_index) == 1 else header_site_context_2.get()
                    elif header_enum.name == 'AGENT':
                        headers = header_agent_context_1.get() if int(site_index) == 1 else header_agent_context_2.get()
                    elif header_enum.name == 'CLIENT':
                        headers = header_client_context_1.get() if int(site_index) == 1 else \
                            header_client_context_2.get()
                    elif header_enum.name == 'SbClient':
                        headers = sb_client_context.get()
                    else:
                        pass
                    break
            else:
                raise AssertionError("无法判断是什么后台，请检查url")
        # print(f'【请求内容 headers】\n{headers}')
        if files:
            headers.pop('Content-Type')
            files = {"file": open(files, 'rb')}
        total_data = None
        if all_page:
            total_page_num = 1
            current_page = 1
            resp_list = []

            while current_page <= total_page_num:
                json["pageNumber"] = current_page
                resp = HttpRequestUtil.session.post(url, params=params, json=json, headers=headers, files=files).json()
                if resp['code'] != 10000 and check_code:
                    raise AssertionError(f"Http响应状态码异常: \n{resp['code']}, message: {resp['message']}")
                elif resp['code'] != 10000:
                    return resp
                if 'pageList' in resp["data"]:
                    total_page_num = resp["data"]['pageList']["pages"]
                    resp_list += resp["data"]['pageList']["records"]
                elif 'userLoginPage' in resp['data']:
                    total_page_num = resp["data"]['userLoginPage']["total"]
                    resp_list += resp["data"]['userLoginPage']["records"]
                else:
                    total_page_num = resp["data"]["pages"]
                    resp_list += resp["data"]["records"]
                if return_total and not total_data:
                    for name in ['totalPage', 'totalInfo']:
                        if name in resp["data"]:
                            total_data = resp["data"][name]
                            break
                current_page += 1
                print(f'【响应】\n{resp}')
            if return_total:
                return resp_list, total_data
            else:
                return resp_list
        else:
            resp = HttpRequestUtil.session.post(url, params=params, json=json, headers=headers, verify=False,
                                                files=files, data=data)
            # print(resp.content)
            if return_origin:
                return resp
            resp = resp.json()
            if check_code:
                try:
                    if resp['code'] != 10000:
                        raise AssertionError(f"Http响应状态码异常: {resp['code']}, message: {resp['message']}")
                except:
                    raise AssertionError(f"消息发送失败: {resp}")
            print(f'【响应】\n{resp}')
            return resp
