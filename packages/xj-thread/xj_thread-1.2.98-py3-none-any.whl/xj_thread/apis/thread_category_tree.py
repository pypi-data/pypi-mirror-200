"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块逻辑分发
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.thread_category_tree_service import ThreadCategoryTreeServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data
from ..utils.user_wrapper import user_authentication_force_wrapper


class ThreadCategoryTreeAPIView(APIView):
    """
    get: 信息表列表
    post: 信息表新增
    """

    def get(self, request, category_value=None, *args, **kwargs):
        params = parse_data(request)
        print("> ThreadCategoryTreeAPIView params category_value:", params, category_value)
        category_value = category_value if category_value else params.get('category_value', None)
        category_id = params.get('category_id', None)
        print("> ThreadCategoryTreeAPIView category_value, category_id:", category_value, category_id)
        if category_value or category_id:
            category_serv, error_text = ThreadCategoryTreeServices.get_category_tree(category_id=category_id, category_value=category_value)
        else:
            category_serv, error_text = ThreadCategoryTreeServices.get_category_tree()

        if error_text:
            return Response({'err': 1000, 'msg': error_text})

        return Response({'err': 0, 'msg': 'OK', 'data': category_serv})

    # V2版本列别树
    @user_authentication_force_wrapper
    def get_category_tree_by_user(self, *args, user_info=None, **kwargs):
        if user_info is None:
            user_info = {}
        user_id = user_info.get("user_id")
        category_serv, error_text = ThreadCategoryTreeServices.get_category_tree_by_user(user_id=user_id)
        if error_text:
            return util_response(err=1000, msg=error_text)
        return util_response(data=category_serv)
