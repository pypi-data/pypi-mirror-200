# encoding: utf-8
"""
@project: djangoModel->user_info_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户信息服务
@created_time: 2022/6/27 19:51
"""
from django.core.paginator import Paginator
from django.db.models import F

from ..models import ExtendField, DetailInfo, BaseInfo
from ..utils.custom_tool import *


class DetailInfoService:

    @staticmethod
    def get_list_detail(params: dict = None, user_id_list: list = None, filter_fields: list = None):
        """
        详细信息列表
        :param filter_fields: 需要过滤的字段
        :param params: 搜索参数
        :param user_id_list: 用户ID列表
        :return: list,err
        """
        filed_map_list = list(ExtendField.objects.all().values("field", 'field_index'))
        filed_map = {item['field_index']: item['field'] for item in filed_map_list}
        reversal_filed_map = {item['field']: item['field_index'] for item in filed_map_list}

        # 过滤字段优化
        filter_fields = format_list_handle(
            param_list=filter_fields or [],
            filter_filed_list=list(reversal_filed_map.keys()) + [
                'user_id', 'real_name', 'sex', 'birth', 'tags', 'signature', 'avatar', 'cover', 'language', 'region_code', 'more',
                'full_name', 'user_name', 'nickname', 'register_time'
            ],
            alias_dict=reversal_filed_map
        )

        if not user_id_list is None and isinstance(user_id_list, list):
            res_obj = DetailInfo.objects.filter(user_id__in=user_id_list) \
                .annotate(full_name=F("user__full_name")) \
                .annotate(user_name=F("user__user_name")) \
                .annotate(nickname=F("user__nickname")) \
                .annotate(register_time=F("user__register_time"))

            res_list = res_obj.values(*filter_fields)
            res_data = filter_result_field(
                result_list=res_list,
                alias_dict=filed_map
            )
            res_data = filter_result_field(
                result_list=res_data,
                remove_filed_list=[
                    "field_1", "field_2", "field_3", "field_4", "field_5", "field_6", "field_7",
                    "field_8", "field_9", "field_10", "field_11", "field_12", "field_13", "field_14",
                    "field_15", "id"
                ],
                alias_dict={"cover": "user_cover"}
            )
            return res_data
        else:
            # 查询用户详细信息列表
            transformed_dict = format_params_handle(
                param_dict=params,
                alias_dict=reversal_filed_map
            )
            page = transformed_dict.pop('page', 1)
            limit = transformed_dict.pop('limit', 20)
            # 查询排序
            sort = transformed_dict.pop('sort', "-register_time")
            sort = sort if sort in [
                "register_time", "-register_time", "user_id", "-user_id"
            ] else "-id"

            try:
                list_set = DetailInfo.objects.filter(**transformed_dict) \
                    .annotate(full_name=F("user__full_name")) \
                    .annotate(user_name=F("user__user_name")) \
                    .annotate(nickname=F("user__nickname")) \
                    .annotate(register_time=F("user__register_time"))
                list_set = list_set.order_by(sort)

                count = DetailInfo.objects.filter(**transformed_dict).count()
            except Exception as e:
                return None, e.__str__()
            # 分页数据
            page_set = list(Paginator(list_set.values(*filter_fields), limit).page(page))
            res_data = filter_result_field(
                result_list=page_set,
                alias_dict=filed_map,
                remove_filed_list=["id"]
            )
            res_data = filter_result_field(
                result_list=res_data,
                remove_filed_list=[
                    "field_1", "field_2", "field_3", "field_4", "field_5", "field_6", "field_7",
                    "field_8", "field_9", "field_10", "field_11", "field_12", "field_13", "field_14",
                    "field_15", "id"
                ],
                alias_dict={"cover": "user_cover"}
            )
            # 数据拼装
            result = {'list': res_data, 'limit': int(limit), 'page': int(page), 'count': count}
            return result, None

    @staticmethod
    def get_detail(user_id: int = None, search_params: dict = None):
        """
        获取当前用户的基础信息和详细信息集合
        :param search_params: 根据参数搜索，取第一条
        :param user_id: 通过用户ID搜索
        :return: detail_info,err_msg
        """
        # 参数验证
        if search_params is None:
            search_params = {}
        search_params = format_params_handle(
            param_dict=search_params,
            filter_filed_list=["user_name", "nickname", "phone", "email"]
        )
        if not user_id and not search_params:
            return None, "参数错误，无法检索用户"

        # 允许使用用户ID或者使用条件参数搜素
        if user_id:
            user_base = BaseInfo.objects.filter(id=user_id).first()
        else:
            user_base = BaseInfo.objects.filter(**search_params).first()
        if not user_base:
            return None, '用户不存在'

        # 获取用户信息字典，补充用户ID
        user_base_info = user_base.to_json()
        user_id = user_id if user_id else user_base_info.get("id")

        # 获取扩展字段
        field_dict = {item['field_index']: item['field'] for item in ExtendField.objects.all().values("field", 'field_index')}
        model_fields = [i.name for i in DetailInfo._meta.fields] + list(field_dict.values()) + ["user_id"]
        model_fields = [i for i in model_fields if not i[0:6] == "field_"]

        # 获取详细信息
        user_detail = DetailInfo.objects.filter(user_id=user_id) \
            .annotate(user_name=F("user__user_name")) \
            .annotate(full_name=F("user__full_name")) \
            .annotate(nickname=F("user__nickname")) \
            .annotate(phone=F("user__phone")) \
            .annotate(email=F("user__email")) \
            .annotate(register_time=F("user__register_time")) \
            .annotate(user_info=F("user__user_info")) \
            .annotate(wechat_openid=F("user__wechat_openid")) \
            .values().first()

        try:
            # 获取用户的部门信息
            if not getattr(sys.modules.get("xj_role.services.role_service"), "RoleService", None):
                from xj_role.services.role_service import RoleService
            else:
                RoleService = getattr(sys.modules.get("xj_role.services.role_service"), "RoleService")
            user_role_list, err = RoleService.get_user_role_info(user_id=user_id, field_list=["role_id"])
            user_role_list = [i["role_id"] for i in user_role_list]
        except Exception:
            user_role_list = []

        try:
            # 获取角色的信息信息
            if not getattr(sys.modules.get("xj_role.services.user_group_service"), "UserGroupService", None):
                from xj_role.services.user_group_service import UserGroupService
            else:
                UserGroupService = getattr(sys.modules.get("xj_role.services.user_group_service"), "UserGroupService")
            user_group_list, err = UserGroupService.get_user_group_info(user_id=user_id, field_list=["user_group_id"])
            user_group_list = [i["user_group_id"] for i in user_group_list]
        except Exception:
            user_group_list = []

        # 返回用户信息
        if not user_detail:  # 当前用户没有填写详细信息的时候
            # 默认空字段返回
            user_base_info_fields = user_base_info.keys()
            for i in model_fields:
                if i in user_base_info_fields:
                    continue
                user_base_info[i] = ""
            user_base_info["user_id"] = user_base_info["id"]  # 把user_id重新赋值
            user_base_info["user_role_list"] = user_role_list
            user_base_info["user_group_id_list"] = user_group_list
            return format_params_handle(
                param_dict=user_base_info,
                alias_dict={"user": "user_id"},
                is_remove_null=False,
                date_format_dict={"register_time": ("%Y-%m-%dT%H:%m:%s", "%Y-%m-%d %H:%m:%s")}
            ), None
        else:  # 当前用户填写过详细信息
            # 扩展字段转换
            user_detail["user_role_id_list"] = user_role_list
            user_detail["user_group_id_list"] = user_group_list
            alias_dict = format_params_handle(
                param_dict=user_detail,
                alias_dict=field_dict,
                is_remove_null=False
            )
            filter_dict = format_params_handle(
                param_dict=alias_dict,
                filter_filed_list=model_fields + ["user_name", "nickname", "phone", "email", "register_time", "user_info",
                                                  "wechat_openid", "full_name", "user_group_id_list", "user_role_id_list"],
                is_remove_null=False,
                date_format_dict={"register_time": ("%Y-%m-%dT%H:%m:%s", "%Y-%m-%d %H:%M:%S")}
            )
            filter_dict.pop("id", None)
            return filter_dict, None

    @staticmethod
    def create_or_update_detail(params):
        """
        添加或者更新用户的详细信息
        :param params: 添加/修改参数
        :return: None,err_msg
        """
        # 参数判断
        if not params:
            return None, None
        user_id = params.pop('user_id', None)
        if not user_id:
            return None, "参数错误"

        # 判断用户是否存在
        user_base = BaseInfo.objects.filter(id=user_id)
        user_base_info = user_base.first()
        if not user_base_info:
            return None, '用户不存在'

        # 扩展字段处理，还原
        alias_dict = {item['field']: item['field_index'] for item in ExtendField.objects.all().values("field", 'field_index')}
        filter_filed_list = [i.name for i in DetailInfo._meta.fields] + list(alias_dict.values())
        alias_params = format_params_handle(
            param_dict=params,
            alias_dict=alias_dict
        )
        transformed_params = format_params_handle(
            param_dict=alias_params,
            filter_filed_list=filter_filed_list
        )
        transformed_params.setdefault("user_id", user_id)
        # 进行数据库操作
        try:
            # 判断是否添加过
            detail_user_obj = DetailInfo.objects.filter(user_id=user_id)
            if not detail_user_obj.first():  # 没有添加，进行添加操作
                DetailInfo.objects.create(**transformed_params)
            else:  # 添加过进行跟新
                detail_user_obj.update(**transformed_params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def get_extend_fields():
        fields = ExtendField.objects.order_by("-sort").all().to_json()
        return fields, None
