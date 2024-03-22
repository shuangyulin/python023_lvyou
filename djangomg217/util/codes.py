# coding:utf-8
# author:ila
normal_code = 0  # 正常
redirect_code = 301  # 跳转
temporary_redirect_code = 302  # 暂时跳转

empty_param_code = 10001  # 请求参数为空或错误
validate_param_code = 10002  # 请求参数不规范
is_not_json_code = 10003  # 数据格式不是json

other_code = 10020  # 其它错误
crud_error_code = 10021  # 数据库操作失败
header_error_code = 10023  # 头部错误
captcha_error_code = 10024  # 验证码错误
id_exist_code = 10025  # id或用户名已存在
id_notexist_code = 10026  # id或用户名不存在
username_error_code = 10027  # 用户名错误
password_error_code = 10028  # 密码错误
file_notexist_code = 10029  # 上传文件不存在

token_error_code = 20001  # token错误
token_expired_code = 20002  # token错误
non_authorized_code = 20003  # 无权限

system_error_code = 40001  # 系统级错误
request_expired_code = 40002  # 请求已过期
repeated_request_code = 40003  # 重复请求
