# _*_coding:utf-8_*_

from rest_framework.views import APIView

from xj_role.services.role_service import RoleService
from xj_role.services.user_group_service import UserGroupService
from ..services.user_service import UserService
from ..utils.custom_tool import request_params_wrapper
from ..utils.model_handle import util_response
from ..utils.user_wrapper import user_authentication_force_wrapper


# 管理员添加用户
class UserAdd(APIView):

    @user_authentication_force_wrapper
    @request_params_wrapper
    def post(self, request, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}

        # 获取角色和部门的id列表
        user_role_list = request_params.pop('user_role_list', None)
        user_group_list = request_params.pop('user_group_list', None)

        # 进行用户添加
        data, err = UserService.user_add(request_params)
        if err:
            return util_response(err=1001, msg=err)

        # 绑定用户的角色和组织
        if user_group_list:
            UserGroupService.bind_user_group(data.get("user_id"), user_group_list)
        if user_role_list:
            RoleService.bind_user_role(data.get("user_id"), user_role_list)

        return util_response(data=data)
