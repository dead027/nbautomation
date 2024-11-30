*** Settings ***
Library  ${CURDIR}/../../Library/Dao/  sit
Library  ${CURDIR}/../../Library/VO/  sit
Library  ${CURDIR}/../../Library/BO/  sit
Library  ${CURDIR}/../../Library/ApiRequests/  sit
Library  ${CURDIR}/../../Library/Common/Utils/LoginUtil.py
Library  ${CURDIR}/../../Library/Common/Utils/ValidateUtil.py
Library  ${CURDIR}/../../Library/Common/Utils/GenerateStrUtil.py
Library  ${CURDIR}/../../Library/LiveLibrary/FrontendLibrary
Library  ${CURDIR}/../../Library/ApiRequests/XJobApi/BaseOperation.py
Library  ${CURDIR}/../../Library/LiveLibrary/FrontendLibrary
Resource  全局变量.robot
Resource  通用方法.robot