# _*_coding:utf-8_*_

import os, logging, time, json, copy
from rest_framework.response import Response
from rest_framework import generics

from xj_user.services.user_service import UserService
from ..services.finance_transacts_service import FinanceTransactsService
from ..utils.model_handle import parse_data, util_response
from ..services.finance_service import FinanceService

logger = logging.getLogger(__name__)


# 获取余额
class FinanceBalance(generics.UpdateAPIView):  # 或继承(APIView)

    def get(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return util_response(err=4001, msg='缺少Token')

        data, err_txt = UserService.check_token(token)
        if err_txt:
            return util_response(err=47766, msg=err_txt)
        # params = parse_data(self)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': FinanceService.check_balance(account_id=data['user_id'], platform=None,
                                                 platform_id=data['platform_id'], currency='CNY',
                                                 sand_box=None)
        })

    def cash_withdrawal(self):
        token = self.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return util_response(err=4001, msg='缺少Token')

        data, err_txt = UserService.check_token(token)
        if err_txt:
            return util_response(err=47766, msg=err_txt)
        params = parse_data(self)
        params['user_id'] = data['user_id']
        params['platform_id'] = data['platform_id']
        cash_withdrawal_set, err = FinanceTransactsService.cash_withdrawal(params)
        if err is None:
            return util_response(data=cash_withdrawal_set)

        return util_response(err=47767, msg=err)
