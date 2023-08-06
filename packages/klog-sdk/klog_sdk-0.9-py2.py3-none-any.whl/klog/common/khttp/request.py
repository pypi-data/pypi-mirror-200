#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import certifi

import klog.common.k_logger

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from klog.common.exception.klog_exception import KlogException

logger = klog.common.k_logger.logger


def _get_proxy_from_env(host, varname="HTTPS_PROXY"):
    no_proxy = os.environ.get("NO_PROXY") or os.environ.get("no_proxy")
    if no_proxy and host in no_proxy:
        return None
    return os.environ.get(varname.lower()) or os.environ.get(varname.upper())


class RequestInternal(object):
    def __init__(self, host="", method="", uri="", header=None, data=""):
        self.host = host
        self.method = method
        self.uri = uri
        self.header = header if header is not None else {}
        self.data = data

    def __str__(self):
        headers = "\n".join("%s: %s" % (k, v) for k, v in self.header.items())
        return ("Host: %s\nMethod: %s\nUri: %s\nHeader: %s\nData: %s\n"
                % (self.host, self.method, self.uri, headers, self.data))

    def add_param(self, key, value):
        if not self.uri.__contains__("?"):
            self.uri = "{}?{}={}".format(self.uri, key, value)
        else:
            self.uri = "{}&{}={}".format(self.uri, key, value)

    def convert_to_request(self):
        return requests.Request(method=self.method.upper(), url=self.get_url(),
                                headers=self.header, data=self.data)

    def get_url(self):
        return self.host + self.uri

    def is_klog_direct_endpoint(self):
        return not self.host.__contains__("api")

    def set_action(self, action):
        self.uri += action


class ResponseInternal(object):
    def __init__(self, status=0, header=None, data=""):
        if header is None:
            header = {}
        self.status = status
        self.header = header
        self.data = data

    def __str__(self):
        headers = "\n".join("%s: %s" % (k, v) for k, v in self.header.items())
        return ("Status: %s\nHeader: %s\nData: %s\n"
                % (self.status, headers, self.data))


class ProxyConnection(object):
    def __init__(self, host, timeout=60, proxy=None, certification=None, is_http=False):
        self.request_host = host
        self.certification = certification
        if not certification:
            self.certification = certifi.where()
        self.timeout = timeout
        self.proxy = None
        if is_http:
            proxy = proxy or _get_proxy_from_env(host, varname="HTTP_PROXY")
        else:
            proxy = proxy or _get_proxy_from_env(host, varname="HTTPS_PROXY")
        if proxy:
            if is_http:
                self.proxy = {"khttp": proxy}
            else:
                self.proxy = {"https": proxy}
        self.request_length = 0

    def request(self, method, url, body=None, headers={}):
        self.request_length = 0
        p = urlparse(url)
        headers.setdefault("Host", p.hostname)
        return requests.request(method=method,
                                url=url,
                                data=body,
                                headers=headers,
                                proxies=self.proxy,
                                verify=self.certification,
                                timeout=self.timeout)


class ApiRequest(object):
    def __init__(self, host, req_timeout=60, debug=False, proxy=None,
                 is_http=False, certification=None, keep_alive=False):
        self.conn = ProxyConnection(host, timeout=req_timeout, proxy=proxy, certification=certification,
                                    is_http=is_http)
        url = urlparse(host)
        if not url.hostname:
            if is_http:
                host = "khttp://" + host
            else:
                host = "https://" + host
        self.host = host
        self.req_timeout = req_timeout
        self.keep_alive = keep_alive
        self.debug = debug
        self.request_size = 0
        self.response_size = 0

    def set_req_timeout(self, req_timeout):
        self.req_timeout = req_timeout

    def is_keep_alive(self):
        return self.keep_alive

    def set_keep_alive(self, flag=True):
        self.keep_alive = flag

    def set_debug(self, debug):
        self.debug = debug

    def _request(self, req_inter):
        if self.keep_alive:
            req_inter.header["Connection"] = "Keep-Alive"
        if self.debug:
            logger.debug("SendRequest %s" % req_inter)
        if req_inter.method == 'GET':
            req_inter_url = req_inter.get_url()
            return self.conn.request(req_inter.method, req_inter_url, None, req_inter.header)
        elif req_inter.method == 'POST' or req_inter.method == 'PUT' or req_inter.method == 'DELETE':
            return self.conn.request(req_inter.method, req_inter.get_url(), req_inter.data, req_inter.header)
        else:
            raise KlogException("ClientParamsError", 'Method only support (GET, POST, PUT, DELETE)')

    def send_request(self, req_inter):
        try:
            http_resp = self._request(req_inter)
            headers = dict(http_resp.headers)
            resp_inter = ResponseInternal(status=http_resp.status_code, header=headers, data=http_resp.text)
            self.request_size = self.conn.request_length
            self.response_size = len(resp_inter.data)
            logger.debug("uri: %s response: %s", req_inter.uri, resp_inter)
            return resp_inter
        except Exception as e:
            raise KlogException("ClientNetworkError", str(e))
