from dataclasses import dataclass
from Library.Common.Utils.Contexts import env_context
import yaml
import os


file_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/config.yaml'
with open(file_name, 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


# 读取yaml配置
@dataclass
class YamlUtil(object):

    @staticmethod
    def __load_service_config():
        """
        load service all config
        :return: all config
        """
        return data.get("service")

    @staticmethod
    def load_common_config(sys_name, project_name='bw'):
        """
        :param project_name: 项目名称
        :param sys_name: 系统名称
        :return: 对应中间件配置内容
        """
        middleware_config = YamlUtil.__load_service_config().get(project_name).get(sys_name)
        if middleware_config is None:
            raise Exception(f"获取项目：{project_name}，中间件：{sys_name} 失败,请查看其是否存在!!!")
        config_data = middleware_config.get(env_context.get())
        if config_data is None:
            raise Exception(
                f"获取项目：{project_name}，中间件：{sys_name} ,环境：{env_context.get()} 失败,请查看其是否存在!!!")
        return config_data

    @staticmethod
    def get_backend_host(sys_name='backend', project_name='bw') -> str:
        return YamlUtil().load_common_config(sys_name, project_name)['host']

    @staticmethod
    def get_site_host(site_number='1', project_name='bw') -> str:
        return YamlUtil().load_common_config(f'site_backend{site_number}', project_name)['host']

    @staticmethod
    def get_agent_host(site_number='1', project_name='bw') -> str:
        return YamlUtil().load_common_config(f'site_agent{site_number}', project_name)['host']

    @staticmethod
    def get_client_host(site_index='1', project_name='bw') -> str:
        return YamlUtil().load_common_config(f'site_client{site_index}', project_name)['host']

    @staticmethod
    def get_api_host(site_index='1', project_name='bw') -> str:
        return YamlUtil().load_common_config(f'site_api{site_index}', project_name)['host']

    @staticmethod
    def get_client_capcha_api_key(project_name='bw') -> str:
        return YamlUtil().load_common_config(f'capcha_api_key', project_name)['api_key']

    @staticmethod
    def get_site_code(site_index='1', project_name='bw') -> str:
        return YamlUtil().load_common_config('site_code', project_name)[f'host{site_index}']


if __name__ == '__main__':
    env_context.set('sit')
    print(YamlUtil.load_common_config('mongo', 'live'))
