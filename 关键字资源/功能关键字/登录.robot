*** Settings ***
Resource  ../基础关键字/Resources.robot

*** Keywords ***
登录总台
    [Documentation]  需要报错信息: 是｜否
    [Arguments]  ${用户名}  ${密码}=${通用密码}  ${需要报错信息}=否
    ${自动校验状态}  set variable if  "${需要报错信息}"=="是"  ${False}  ${TRUE}
    ${错误信息}  login_client  ${用户名}  ${密码}  ${自动校验状态}
    RETURN  ${错误信息}

登录站点后台
    [Documentation]  需要报错信息: 是｜否
    [Arguments]  ${用户名}=${站点信息_1["用户名1"]}  ${密码}=${通用密码}  ${需要报错信息}=否  ${站点编号}=${站点信息_1["站点编号"]}
    ${自动校验状态}  set variable if  "${需要报错信息}"=="是"  ${False}  ${TRUE}
    ${错误信息}  login_site_backend  ${站点编号}  ${用户名}  ${密码}  check_code=${自动校验状态}
    ${站点编号}  set variable  ${站点信息_1["站点编号"]}
    Set Suite Variable  ${站点编号}
    RETURN  ${错误信息}

登录客户端
    [Documentation]  需要报错信息: 是｜否
    [Arguments]  ${用户名}  ${密码}=${通用密码}  ${需要报错信息}=否
    ${自动校验状态}  set variable if  "${需要报错信息}"=="是"  ${False}  ${TRUE}
    ${错误信息}  login_client  ${用户名}  ${密码}  ${自动校验状态}
    RETURN  ${错误信息}
