#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/2 21:28

import os
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil


class CommonFunc(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def upload_file_api(file_name='poker.png'):
        """
        上传图片
        @return:
        """
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images", file_name)
        url = YamlUtil.get_site_host() + '/site/file/api/upload/baowang'
        resp = HttpRequestUtil.post(url, files=file_path)
        return resp["data"]["url"]


