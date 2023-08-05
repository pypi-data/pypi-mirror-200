from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_enroll.models import Enroll
from xj_enroll.service.valuation_service import ValuationService
from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.utils.user_wrapper import user_authentication_force_wrapper
from ..service.enroll_record_serivce import EnrollRecordServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data, flow_service_wrapper
from ..utils.join_list import JoinList


class RecordAPI(APIView):
    # 添加记录,用户报名
    @require_http_methods(['POST'])
    @user_authentication_force_wrapper
    @flow_service_wrapper
    def add(self, *args, user_info=None, **kwargs, ):
        # 表单数据验证
        # is_valid, error = RecordValidator(params).validate()
        # if not is_valid:
        #     return util_response(err=1000, msg=error)

        # 提取参数
        params = parse_data(self) or {}
        params['user_id'] = user_info.get("user_id")

        # 通过 again_price计算出 initiator_again_price
        enroll_id = params.get("enroll_id")
        if not enroll_id:
            return None, "enroll_id不能为空"
        enroll_info = Enroll.objects.filter(id=enroll_id).first()
        if not enroll_info:
            return None, "报名ID不正确"
        # 计算 比例后的追加价格 initiator_again_price
        try:
            valuation_res, err = ValuationService.valuate(
                enroll_rule_group_id=enroll_info.enroll_rule_group_id,
                variables_dict={"again_price": params.get("again_price", 0)}
            )
            params["initiator_again_price"] = valuation_res.get("initiator_again_price", 0)
        except Exception as e:
            pass
        # 添加数据
        data, err = EnrollRecordServices.record_add(params)
        if err:
            return util_response(err=1002, msg=err)

        # 报名触发倒计时,取消自动成单
        # clocker = ClockService()
        # data, err = clocker.add_clock(enroll_id, user_id)
        return util_response(data={"id": data.get("id")})

    @require_http_methods(['GET'])
    def list(self, *args, **kwargs, ):
        params = parse_data(self)
        need_pagination = params.get("need_pagination", 1)
        need_pagination = int(need_pagination)
        data, err = EnrollRecordServices.record_list(params=params, need_pagination=need_pagination)
        if err:
            return util_response(err=1000, msg=err)
        user_ids = []
        if need_pagination:
            user_infos = DetailInfoService.get_list_detail({}, user_ids)
            data["list"] = JoinList(data["list"], user_infos, "user_id", "user_id").join()
        else:
            user_infos = DetailInfoService.get_list_detail({}, user_ids)
            data = JoinList(data, user_infos, "user_id", "user_id").join()

        return util_response(data=data)

    @require_http_methods(['GET'])
    def list_v2(self, *args, **kwargs, ):
        params = parse_data(self)
        data, err = EnrollRecordServices.complex_record_list(params=params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['DELETE'])
    def record_del(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk") or params.pop("id")
        data, err = EnrollRecordServices.record_del(pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def record_edit(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk") or params.pop("id")
        data, err = EnrollRecordServices.record_edit(params, pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    def record_detail(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk", None) or params.pop("id", None) or params.pop("record_id", None) or None
        if not pk:
            return util_response(err=1000, msg="参数错误")
        data, err = EnrollRecordServices.record_detail(pk, search_params=params)

        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    @user_authentication_force_wrapper
    def appoint(self, *args, user_info=None, **kwargs, ):
        """
        需求描述：报名可多人报名，不在自动成单，可以手动指派报名
        1.由用户或者客服进行指派工作人员完成任务。
        2.没有被选中的用户，报名状态修改成草稿状态。
        3.主报名项目，则进入代补差价状态。
        :return: response
        """
        params = parse_data(self)
        enroll_id = params.get("enroll_id", None)
        record_id = params.get("record_id", None)
        subitem_id = params.get("subitem_id", None)
        if enroll_id is None or record_id is None or subitem_id is None:
            return util_response(err=1000, msg="参数错误")
        data, err = EnrollRecordServices.appoint(enroll_id, record_id, subitem_id)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data, msg="指派成功")
