# -*- coding: utf-8 -*-
#
# Copyright 2022 Ksyun Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import json
import logging.handlers
import uuid
import warnings

from klog.cli.models import KlogResponse
from klog.common import const
from klog.common.signer import AWSRequestsSigner

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from klog.common.exception.klog_exception import KlogException
from klog.common.khttp.request import ApiRequest, RequestInternal
from klog.common.profile.client_profile import ClientProfile

warnings.filterwarnings("ignore")

_json_content = 'application/json'


class EmptyHandler(logging.Handler):
    def emit(self, message):
        pass


class AbstractClient(object):
    _requestPath = '/'
    _params = {}
    _apiVersion = ''
    _endpoint = ''
    _service = ''
    _sdkVersion = const.X_KLOG_API_VERSION
    _default_content_type = _json_content
    _FMT = '%(asctime)s %(process)d %(filename)s L%(lineno)s %(levelname)s %(message)s'
    _logger = None

    def __init__(self, credential, region, profile=None, logger=None):
        if credential is None:
            raise KlogException(
                "InvalidCredential", "Credential is None or invalid")
        self._credential = credential
        self._region = region
        self._profile = ClientProfile() if profile is None else profile
        is_http = True if self._profile.httpProfile.scheme == "http" else False
        self._request = ApiRequest(
            self._get_endpoint(),
            req_timeout=self._profile.httpProfile.reqTimeout,
            proxy=self._profile.httpProfile.proxy,
            is_http=is_http,
            certification=self._profile.httpProfile.certification
        )
        if self._profile.httpProfile.keepAlive:
            self._request.set_keep_alive()
        self._set_logger(logger)

    def _set_logger(self, logger):
        self._logger = logger
        pass

    def _fix_params(self, params):
        if not isinstance(params, (dict,)):
            return params
        return self._format_params(None, params)

    def _format_params(self, prefix, params):
        d = {}
        if params is None:
            return d

        if not isinstance(params, (tuple, list, dict)):
            d[prefix] = params
            return d

        if isinstance(params, (list, tuple)):
            for idx, item in enumerate(params):
                if prefix:
                    key = "{0}.{1}".format(prefix, idx)
                else:
                    key = "{0}".format(idx)
                d.update(self._format_params(key, item))
            return d

        if isinstance(params, dict):
            for k, v in params.items():
                if prefix:
                    key = '{0}.{1}'.format(prefix, k)
                else:
                    key = '{0}'.format(k)
                d.update(self._format_params(key, v))
            return d

        raise KlogException("ClientParamsError", "some params type error")

    def _build_req(self, action, params, req, options=None):
        if self._profile.signMethod in "HMAC-SHA256":
            self._build_req_with_signature(action, params, req, options)
        else:
            raise KlogException("ClientError", "Invalid signature method.")

    def _build_req_with_signature(self, action, params, req, options=None):
        params = copy.deepcopy(self._fix_params(params))

        if not req.is_klog_direct_endpoint():
            req.add_param("Action", action)
            req.add_param("Version", self._apiVersion)
            # 服务端依据这个请求头判断是否对请求体进行hash
            req.header['content-md5'] = '1'
        else:
            req.set_action(action)

        # 请求头
        req.header["Accept"] = _json_content
        content_type = self._default_content_type
        req.header["Content-Type"] = content_type
        request_id = str(uuid.uuid4())
        req.header['x-klog-requestid'] = request_id
        req.header['x-klog-api-version'] = const.X_KLOG_API_VERSION
        self._logger.debug("request id: %s", request_id)
        if content_type == _json_content and req.method != 'GET':
            req.data = json.dumps(params)
        elif req.method == 'GET':
            for k in params:
                req.add_param(k, params[k])
            req.data = json.dumps({})
        signer = AWSRequestsSigner(secret_key_id=self._credential.secret_id, secret_key=self._credential.secret_key,
                                   region=self._region, service=self._service, r=req.convert_to_request())
        headers = signer.get_aws_request_headers()
        req.header.update(headers)

    def _get_service_domain(self):
        rootDomain = self._profile.httpProfile.rootDomain
        return self._service + "." + rootDomain

    def _get_endpoint(self):
        endpoint = self._profile.httpProfile.endpoint
        if endpoint is None:
            endpoint = self._get_service_domain()
        return endpoint

    def __get_method_from_action(self, action):
        return "GET" if action in "GetToken" else "POST"

    def _do_call(self, action, params, options=None):
        method = self.__get_method_from_action(action)
        req = RequestInternal(self._get_endpoint(), method, self._requestPath)
        self._build_req(action, params, req, options)
        resp_inter = self._request.send_request(req)
        return resp_inter

    def _check_error(self, response_object):
        if response_object.status == 200 and response_object.data == '':
            request_id = response_object.header.get("x-klog-requestid")
            res = KlogResponse(request_id=request_id)
            return res

        response = json.loads(response_object.data)

        if "Error" not in response:
            request_id = response_object.header.get("x-klog-requestid")
            if "ErrorCode" not in response and 200 <= response_object.status < 300:
                res = KlogResponse(data=response, request_id=request_id)
                return res
            else:
                c = response.get("ErrorCode")
                m = response.get("ErrorMessage")
                c = 'UnknownError' if c is None else c
                m = "status: {} response body: {}".format(response_object.status, response) if m is None else m
                raise KlogException(c, m, request_id)
        else:
            code = response["Error"]["Code"]
            message = response["Error"]["Message"]
            request_id = response["RequestId"]
            raise KlogException(code, message, request_id)

    def _call(self, action, params, obj=None, options=None):
        try:
            body = self._do_call(action, params, options)
            response = self._check_error(body)
            if obj is None:
                return response
            else:
                obj.set_request_id(response.request_id)
                obj.set_status(response.status)
                obj.set_data(response.get_data())
                return response.deserialize_obj(obj)
        except Exception as e:
            if isinstance(e, KlogException):
                raise
            else:
                raise KlogException(e, e)
