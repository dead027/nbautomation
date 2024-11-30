*** Settings ***
Resource  ../../基础关键字/Resources.robot
Library    String

*** Keywords ***
登录客户端并进入视讯场馆龙虎房间
    [Arguments]  ${会员账号}=${会员账号_vip0[0]}  ${站点编号}=${站点信息_1["站点编号"]}
    ...  ${游戏编码}=${默认场馆及游戏["龙虎游戏编码"]}  ${游戏房间}=${默认场馆及游戏["龙虎房间"]}
	ws close
#	${会员场馆账号信息}  get_user_venue_info_dao  ${站点编号}  ${会员账号}
	# 登录客户端
	login_client  ${会员账号}  ${通用密码}
	# 登录金喜真人
	${token}  enter_game_sh  ${游戏编码}
	client_connect_to_ws  ${token}
	${场馆会员账号}  ${场馆会员ID}  get_user_venue_info_dao  ${站点编号}  ${会员账号}  视界真人
	${视讯系统会员ID}  get_user_id_sh  ${场馆会员账号}
	# 进入龙虎房间
	join_room  ${视讯系统会员ID}  ${游戏房间}
	Set Global Variable  ${场馆会员账号}
	Set Global Variable  ${视讯系统会员ID}