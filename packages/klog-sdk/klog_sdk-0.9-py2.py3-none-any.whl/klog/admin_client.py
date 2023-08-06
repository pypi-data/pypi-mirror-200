# coding=utf-8

from klog.cli import models
from klog.common import const
from klog.common.abstract_client import AbstractClient


class KlogClient(AbstractClient):
    _apiVersion = const.API_VERSION
    _endpoint = const.DEFAULT_API_ENDPOINT
    _service = const.SERVICE_NAME

    def CreateProject(self, request):
        params = request.serialize()
        response = self._call("CreateProject", params)
        return response

    def DescribeProject(self, request):
        params = request.serialize()
        r = models.DescribeProjectResponse()
        response = self._call("DescribeProject", params, obj=r)
        return response

    def UpdateProject(self, request):
        params = request.serialize()
        response = self._call("UpdateProject", params)
        return response

    def DeleteProject(self, request):
        params = request.serialize()
        response = self._call("DeleteProject", params)
        return response

    def ListProjects(self, request):
        params = request.serialize()
        r = models.ListProjectsResponse()
        response = self._call("ListProjects", params, obj=r)
        return response

    def CreateLogPool(self, request):
        params = request.serialize()
        response = self._call("CreateLogPool", params)
        return response

    def DescribeLogPool(self, request):
        params = request.serialize()
        r = models.DescribeLogPoolResponse()
        response = self._call("DescribeLogPool", params, obj=r)
        return response

    def UpdateLogPool(self, request):
        params = request.serialize()
        response = self._call("UpdateLogPool", params)
        return response

    def DeleteLogPool(self, request):
        params = request.serialize()
        response = self._call("DeleteLogPool", params)
        return response

    def ListLogPools(self, request):
        params = request.serialize()
        r = models.ListLogPoolsResponse()
        response = self._call("ListLogPools", params, obj=r)
        return response

    def GetLogs(self, request):
        params = request.serialize()
        r = models.GetLogsResponse()
        response = self._call("GetLogs", params, obj=r)
        return response

    def CreateQuickSearch(self, request):
        params = request.serialize()
        response = self._call("CreateQuickSearch", params)
        return response

    def ListQuickSearchs(self, request):
        params = request.serialize()
        r = models.ListQuickSearchResponse()
        response = self._call("ListQuickSearchs", params, obj=r)
        return response

    def GetQuickSearch(self, request):
        params = request.serialize()
        response = self._call("GetQuickSearch", params)
        return response

    def DeleteQuickSearchs(self, request):
        params = request.serialize()
        response = self._call("DeleteQuickSearchs", params)
        return response

    def CreateDashboard(self, request):
        params = request.serialize()
        response = self._call("CreateDashboard", params)
        return response

    def DeleteDashboard(self, request):
        params = request.serialize()
        response = self._call("DeleteDashboard", params)
        return response

    def DescribeDashboard(self, request):
        params = request.serialize()
        response = self._call("DescribeDashboard", params)
        return response

    def ListDashboards(self, request):
        params = request.serialize()
        response = self._call("ListDashboards", params)
        return response

    def CreateChart(self, request):
        params = request.serialize()
        response = self._call("CreateChart", params)
        return response

    def DeleteChart(self, request):
        params = request.serialize()
        response = self._call("DeleteChart", params)
        return response

    def GetDashboardNamesByIds(self, request):
        params = request.serialize()
        response = self._call("GetDashboardNamesByIds", params)
        return response

    def GetChartNamesByIds(self, request):
        params = request.serialize()
        response = self._call("GetChartNamesByIds", params)
        return response

    def UpdateDashboard(self, request):
        params = request.serialize()
        response = self._call("UpdateDashboard", params)
        return response

    def GetUsage(self, request=None):
        params = {} if request is None else request.serialize()
        r = models.GetUsageResponse()
        response = self._call("GetUsage", params, obj=r)
        return response

    def GetUserStatus(self, request=None):
        params = {} if request is None else request.serialize()
        r = models.GetUserStatusResponse()
        response = self._call("GetUserStatus", params, obj=r)
        return response

    def SetIndexTemplate(self, request):
        params = request.serialize()
        response = self._call("SetIndexTemplate", params)
        return response

    def GetIndexTemplate(self, request):
        params = request.serialize()
        r = models.GetIndexTemplateResponse()
        response = self._call("GetIndexTemplate", params, obj=r)
        return response

    def GetDynamicIndex(self, request):
        params = request.serialize()
        r = models.GetIndexTemplateResponse()
        response = self._call("GetDynamicIndex", params, obj=r)
        return response

    def CreateDownloadTask(self, request):
        params = request.serialize()
        response = self._call("CreateDownloadTask", params)
        return response

    def ListDownloadTasks(self, request):
        params = request.serialize()
        r = models.ListDownloadTaskResponse()
        response = self._call("ListDownloadTasks", params, obj=r)
        return response

    def GetDownloadUrls(self, request):
        params = request.serialize()
        r = models.GetDownloadUrlResponse()
        response = self._call("GetDownloadUrls", params, obj=r)
        return response

    def GetMonitorData(self, request):
        params = request.serialize()
        r = models.GetMonitorDataResponse()
        response = self._call("GetMonitorData", params, obj=r)
        return response

    def DescribeLogErrorReason(self, request=None):
        params = {} if request is None else request.serialize()
        response = self._call("DescribeLogErrorReason", params)
        return response

    def GetToken(self, request=None):
        params = {} if request is None else request.serialize()
        r = models.GetTokenResponse()
        response = self._call("GetToken", params, obj=r)
        return response
