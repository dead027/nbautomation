from enum import Enum


# 请求头枚举类
class RequestHeaderEnum(Enum):
    ADMIN = [('admin-foreign', 'admin-manager'), {'Admin-Client': 'Admin'}]  # 中控后台
    SITE_ADMIN = [('site_admin', '/site/'), {'Admin-Client': 'Admin'}]  # 站点后台
    AGENT = [('agenth52', 'admin-agent'), {'Agent-Client': 'Agent'}]  # 代理H5
    CLIENT = [('app-foreign',), {'Sign': ''}]
    SbClient = [('app-foreign',), {'Sign': ''}]
