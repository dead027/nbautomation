*** Keywords ***
生成会员账号
    ${账号}  generate_string  6
    ${账号}  Set Variable  sit${账号}0
    RETURN  ${账号}
    
生成随机手机号码
    [Arguments]  ${区号}=${手机区号1}  ${长度}=8
    ${手机号码}  generate_string  ${长度}  数字
    RETURN  158${手机号码}
    
生成随机邮箱
    ${账号}  generate_string  8
    ${邮箱}  Set Variable  sit${账号}@gmail.com
    RETURN  ${邮箱}