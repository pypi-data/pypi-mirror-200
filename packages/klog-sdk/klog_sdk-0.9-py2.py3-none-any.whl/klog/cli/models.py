# coding=utf-8
import time
from datetime import datetime

from klog.common import const
from klog.common.abstract_model import AbstractModel, Serializer
from klog.common.exception import KlogException


class TagInfo(Serializer):
    def __init__(self, key, value, id=None):
        self.Key = key
        self.Value = value
        self.Id = id


class TimeRange(Serializer):
    def __init__(self):
        self.From = 0
        self.To = 0


class ProjectInfo(Serializer):
    def __init__(self):
        self.ProjectName = ""
        self.Description = ""
        self.LogPoolNum = 0
        self.IamProjectId = 0
        self.IamProjectName = ""
        self.Region = ""
        self.Tags = []
        self.UpdateTime = ""


class LogPoolInfo(Serializer):
    def __init__(self):
        self.ProjectName = ""
        self.LogPoolName = ""
        self.LogPoolId = ""
        self.Tags = []
        self.Partitions = 0
        self.RetentionDays = 0
        self.Description = ""
        self.UpdateTime = ""
        self.CreateTime = ""


class PageSize(Serializer):
    def __init__(self):
        self.Page = 0
        self.Size = 0


class UserStatus(Serializer):
    def __init__(self):
        self.UserId = ""
        self.Status = 0


class DownloadTask(TimeRange, LogPoolInfo):
    def __init__(self):
        super(DownloadTask, self).__init__()
        self.DownloadID = ""
        self.StartTime = 0
        self.EndTime = 0


class DownloadUrlInfo(TimeRange):
    def __init__(self):
        super(DownloadUrlInfo, self).__init__()
        self.Url = ""
        self.FileName = ""
        self.Status = ""
        self.Size = 0.0
        self.SizeUnit = ""


class GetUsageInfo(Serializer):
    def __init__(self):
        self.Projects = []
        self.TimeSeries = []
        self.Data = {}


class ChartSearchInfo(Serializer):
    def __init__(self):
        self.LogPoolName = ""
        self.TimeRange = ""
        self.Query = ""


class ChartInfo(Serializer):
    def __init__(self):
        self.DashboardId = 0
        self.ChartName = ""
        self.ChartType = ""
        self.Search = {}
        self.CreateTime = ""
        self.UpdateTime = ""
        self.Display = ""


class DashboardInfo(Serializer):
    def __init__(self):
        self.DashboardId = 0
        self.DashboardName = ""
        self.ProjectName = ""
        self.Charts = []
        self.CreateTime = ""
        self.UpdateTime = ""


class QuickSearch(Serializer):
    def __init__(self):
        self.ProjectName = ""
        self.LogPoolName = ""
        self.Query = ""
        self.QuickSearchName = ""
        self.TimeRange = ""
        # 查询时填写，查询的快速查询名称，可以模糊搜索
        self.Filter = ""


class LogErrorReasonInfo(LogPoolInfo):
    def __init__(self):
        super(LogErrorReasonInfo, self).__init__()
        self.TypicalErrorReason = ""
        self.FailedLogCount = 0
        self.ErrorOccurredTimeMs = 0
        self.Start = 0
        self.End = 0


class KlogResponse(Serializer):
    def __init__(self, data=None, request_id="", status="success"):
        self.request_id = request_id
        self._data = data
        self.status = status

    def __str__(self):
        d = {} if self.get_data() is None else self.get_data()
        return "request_id: {} data: {} status: {}".format(self.request_id, d, self.status)

    def get_data(self):
        return self._data

    def get_request_id(self):
        return self.request_id

    def get_status(self):
        return self.status

    def set_data(self, data):
        self._data = data

    def set_request_id(self, request_id):
        self.request_id = request_id

    def set_status(self, status):
        self.status = status

    def deserialize_obj(self, obj):
        self.deserialize(self._data, obj=obj)
        return obj


class CreateProjectRequest(AbstractModel, ProjectInfo):

    def __init__(self, project_name, region=const.DEFAULT_KLOG_REGION_BEIJING):
        super(CreateProjectRequest, self).__init__()
        self.ProjectName = project_name
        self.Region = region

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("Description"):
            self.Description = params.get("Description")
        if params.get("Region"):
            self.Region = params.get("Region")
        if params.get("IamProjectId"):
            self.IamProjectId = params.get("IamProjectId")
        if params.get("IamProjectName"):
            self.IamProjectName = params.get("IamProjectName")


class DescribeProjectRequest(AbstractModel, ProjectInfo):
    """DescribeProject请求参数结构体
    """

    def __init__(self, project_name):
        r"""项目详情
        :param ProjectName: 工程名称
        :type str
        """
        super(DescribeProjectRequest, self).__init__()
        self.ProjectName = project_name

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")


class UpdateProjectRequest(AbstractModel, ProjectInfo):
    """UpdateProject请求参数结构体
    """

    def __init__(self, project_name):
        r"""更新项目
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param Description: 工程描述
        :type PathPrefix: String
        :param IamProjectId: 项目id，不填写则不会改变绑定项目
        :type PathPrefix: Int
        """
        super(UpdateProjectRequest, self).__init__()
        self.ProjectName = project_name

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("Description"):
            self.Description = params.get("Description")
        if params.get("IamProjectId"):
            self.IamProjectId = params.get("IamProjectId")


class DeleteProjectRequest(AbstractModel, ProjectInfo):
    """DeleteProject请求参数结构体
    """

    def __init__(self, projectName):
        r"""删除项目
        :param ProjectName: 工程名称
        :type PathPrefix: String
        """
        super(DeleteProjectRequest, self).__init__()
        self.ProjectName = projectName

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")


class ListProjectsRequest(AbstractModel, PageSize, ProjectInfo):
    """ListProjects请求参数结构体
    """

    def __init__(self, page, size):
        r"""查看项目列表
        :param Page: 返回记录的页码，从0开始
        :type PathPrefix: Int
        :param Size: 每页返回最大条目，默认 500（最大值）
        :type PathPrefix: Int
        """
        super(ListProjectsRequest, self).__init__()
        self.Page = page
        self.Size = size

    def _deserialize(self, params):
        if params.get("Page"):
            self.Page = params.get("Page")
        if params.get("Size"):
            self.Size = params.get("Size")


class CreateLogPoolRequest(AbstractModel, LogPoolInfo):
    """CreateLogPool请求参数结构体
    """

    def __init__(self, project_name, log_pool_name, partitions=1, retention_days=2):
        r"""创建日志池
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        :param RetentionDays: 数据保存时间，单位为天，范围1~3600
        :type PathPrefix: Int
        :param Partitions: 分区个数，2-64
        :type PathPrefix: Int
        :param Description: 日志池描述
        :type PathPrefix: String
        """
        super(CreateLogPoolRequest, self).__init__()
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name
        self.Partitions = partitions
        self.RetentionDays = retention_days

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("RetentionDays"):
            self.RetentionDays = params.get("RetentionDays")
        if params.get("Partitions"):
            self.Partitions = params.get("Partitions")
        if params.get("Description"):
            self.Description = params.get("Description")


class DescribeLogPoolRequest(AbstractModel):
    """DescribeLogPool请求参数结构体
    """

    def __init__(self):
        r"""日志池详情
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        """
        self.ProjectName = None
        self.LogPoolName = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")


class UpdateLogPoolRequest(AbstractModel, LogPoolInfo):
    """UpdateLogPool请求参数结构体
    """

    def __init__(self, project_name, log_pool_name):
        r"""修个日志池
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        :param RetentionDays: 数据保存时间，单位为天，范围1~3600
        :type PathPrefix: Int
        :param Partitions: 分区数量
        :type PathPrefix: Int
        :param Description: 日志池描述
        :type PathPrefix: String
        """
        super(UpdateLogPoolRequest, self).__init__()
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("RetentionDays"):
            self.RetentionDays = params.get("RetentionDays")
        if params.get("Partitions"):
            self.Partitions = params.get("Partitions")
        if params.get("Description"):
            self.Description = params.get("Description")


class DeleteLogPoolRequest(AbstractModel):
    """DeleteLogPool请求参数结构体
    """

    def __init__(self, project_name, log_pool_name):
        r"""删除日志池
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        """
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")


class ListLogPoolsRequest(AbstractModel, PageSize, LogPoolInfo):
    """ListLogPools请求参数结构体
    """

    def __init__(self, project_name, page, size):
        r"""获取日志池列表
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param Page: 页码，从0开始
        :type PathPrefix: Int
        :param Size: 每页返回最大条目，默认 500（最大值）
        :type PathPrefix: Int
        :param LogPoolName: 如果想要根据名称搜索某个日志池，该字段必须填写
        :type PathPrefix: String
        """
        super(ListLogPoolsRequest, self).__init__()
        self.ProjectName = project_name
        self.Page = page
        self.Size = size

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("Page"):
            self.Page = params.get("Page")
        if params.get("Size"):
            self.Size = params.get("Size")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")


class GetLogsRequest(AbstractModel, LogPoolInfo, TimeRange):
    """GetLogs请求参数结构体
    """

    def __init__(self, project_name, log_pool_name, start_time,
                 end_time=time.time() * 1000, hits_open=False):
        super(GetLogsRequest, self).__init__()
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name
        self.From = start_time
        self.To = end_time
        self.Query = ""
        self.HitsOpen = hits_open
        self.Interval = None
        self.SortBy = None
        self.Offset = None
        self.Size = None
        if self.HitsOpen:
            self.__set_interval()

    def __check_timestamp(self):
        if self.From > self.To:
            raise KlogException(code="ClientError", message="GetLogs from or must less than to")

    def __set_interval(self):
        self.__check_timestamp()
        start_time = datetime.fromtimestamp(self.From / 1000)
        end_time = datetime.fromtimestamp(self.To / 1000)
        timedelta = (end_time - start_time) / 50

        if timedelta.days > 7:
            t = timedelta.days / 7
            unit_idx = 4
        elif timedelta.days > 0:
            t = timedelta.days
            unit_idx = 3
        elif timedelta.seconds > 3600:
            t = timedelta.seconds / 3600
            unit_idx = 2
        elif timedelta.seconds > 60:
            t = timedelta.seconds / 60
            unit_idx = 1
        else:
            t = timedelta.seconds
            unit_idx = 0

        u = const.TIME_UNIT[unit_idx]
        self.Interval = str(int(t)) + u

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("From"):
            self.From = params.get("From")
        if params.get("To"):
            self.To = params.get("To")
        if params.get("Query"):
            self.Query = params.get("Query")
        if params.get("LogPoolId"):
            self.LogPoolId = params.get("LogPoolId")
        if params.get("HitsOpen"):
            self.HitsOpen = params.get("HitsOpen")
        if params.get("Interval"):
            self.Interval = params.get("Interval")
        if params.get("SortBy"):
            self.SortBy = params.get("SortBy")
        if params.get("Offset"):
            self.Offset = params.get("Offset")
        if params.get("Size"):
            self.Size = params.get("Size")


class CreateQuickSearchRequest(AbstractModel):
    """CreateQuickSearch请求参数结构体
    """

    def __init__(self):
        self.ProjectName = None
        self.LogPoolName = None
        self.QuickSearchName = None
        self.Description = None
        self.TimeRange = None
        self.Query = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("QuickSearchName"):
            self.QuickSearchName = params.get("QuickSearchName")
        if params.get("Description"):
            self.Description = params.get("Description")
        if params.get("TimeRange"):
            self.TimeRange = params.get("TimeRange")
        if params.get("Query"):
            self.Query = params.get("Query")


class ListQuickSearchsRequest(AbstractModel):
    """ListQuickSearchs请求参数结构体
    """

    def __init__(self):
        r"""获取快速查询列表
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        :param Filter: 根据快速查询名称过滤列表，支持模糊搜索
        :type PathPrefix: String
        :param Page: 页码，从0开始
        :type PathPrefix: Int
        :param Size: 每页返回最大条目，默认 500（最大值）
        :type PathPrefix: Int
        """
        self.ProjectName = None
        self.LogPoolName = None
        self.Filter = None
        self.Page = None
        self.Size = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("Filter"):
            self.Filter = params.get("Filter")
        if params.get("Page"):
            self.Page = params.get("Page")
        if params.get("Size"):
            self.Size = params.get("Size")


class GetQuickSearchRequest(AbstractModel):
    """GetQuickSearch请求参数结构体
    """

    def __init__(self):
        r"""获取快速查询列表
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        :param QuickSearchName: 快速查询名称
        :type PathPrefix: String
        """
        self.ProjectName = None
        self.LogPoolName = None
        self.QuickSearchName = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("QuickSearchName"):
            self.QuickSearchName = params.get("QuickSearchName")


class DeleteQuickSearchsRequest(AbstractModel):
    """DeleteQuickSearchs请求参数结构体
    """

    def __init__(self):
        r"""删除快速查询
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        :param QuickSearchName: 快速查询名称
        :type PathPrefix: String
        """
        self.ProjectName = None
        self.LogPoolName = None
        self.QuickSearchNames = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("QuickSearchName"):
            self.QuickSearchName = params.get("QuickSearchName")


class CreateDashboardRequest(AbstractModel, DashboardInfo):
    def __init__(self, project_name, dashboard_name):
        super(CreateDashboardRequest, self).__init__()
        self.ProjectName = project_name
        self.DashboardName = dashboard_name

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("DashboardName"):
            self.DashboardName = params.get("DashboardName")


class DeleteDashboardRequest(AbstractModel, DashboardInfo):
    """DeleteDashboard请求参数结构体
    """

    def __init__(self, dashboard_id):
        super(DeleteDashboardRequest, self).__init__()
        self.DashboardId = dashboard_id

    def _deserialize(self, params):
        if params.get("DashboardId"):
            self.DashboardId = params.get("DashboardId")


class DescribeDashboardRequest(AbstractModel, DashboardInfo):
    """DescribeDashboard请求参数结构体
    """

    def __init__(self, dashboard_id):
        r"""仪表盘信息
        :param DashboardId: 仪表盘ID
        :type PathPrefix: String
        """
        super(DescribeDashboardRequest, self).__init__()
        self.DashboardId = dashboard_id

    def _deserialize(self, params):
        if params.get("DashboardId"):
            self.DashboardId = params.get("DashboardId")


class ListDashboardsRequest(AbstractModel):
    """ListDashboards请求参数结构体
    """

    def __init__(self):
        r"""获取仪表盘列表
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param Page: 返回的分页数，从0开始
        :type PathPrefix: Int
        :param Size: 每页返回最大条目，默认 500（最大值）
        :type PathPrefix: Int
        """
        self.ProjectName = None
        self.Page = None
        self.Size = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("Page"):
            self.Page = params.get("Page")
        if params.get("Size"):
            self.Size = params.get("Size")


class CreateChartRequest(AbstractModel):
    """CreateChart请求参数结构体
    """

    def __init__(self):
        r"""创建图表
        :param DashboardId: 仪表盘ID
        :type PathPrefix: String
        :param ChartName: 图表名称
        :type PathPrefix: String
        :param ChartType: 图表类型，line，table
        :type PathPrefix: String
        :param Search: 查询主体
        :type PathPrefix: String
        :param Display: 展示参数
        :type PathPrefix: String
        :param 参数名称: 描述
        :type PathPrefix: String
        :param -: -
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        :param TimeRange: 查询数据的时间范围
        :type PathPrefix: String
        :param Query: 查询语句
        :type PathPrefix: String
        """
        self.DashboardId = None
        self.ChartName = None
        self.ChartType = None
        self.Search = None
        self.Display = None
        self.LogPoolName = None
        self.TimeRange = None
        self.Query = None

    def _deserialize(self, params):
        if params.get("DashboardId"):
            self.DashboardId = params.get("DashboardId")
        if params.get("ChartName"):
            self.ChartName = params.get("ChartName")
        if params.get("ChartType"):
            self.ChartType = params.get("ChartType")
        if params.get("Search"):
            self.Search = params.get("Search")
        if params.get("Display"):
            self.Display = params.get("Display")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("TimeRange"):
            self.TimeRange = params.get("TimeRange")
        if params.get("Query"):
            self.Query = params.get("Query")


class DeleteChartRequest(AbstractModel):
    """DeleteChart请求参数结构体
    """

    def __init__(self):
        r"""删除图表
        :param ChartId: 图表ID
        :type PathPrefix: String
        """
        self.ChartId = None

    def _deserialize(self, params):
        if params.get("ChartId"):
            self.ChartId = params.get("ChartId")


class GetDashboardNamesByIdsRequest(AbstractModel):
    """GetDashboardNamesByIds请求参数结构体
    """

    def __init__(self):
        r"""获取仪表盘名称
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param DashboardIds: 仪表盘id列表
        :type PathPrefix: String
        """
        self.ProjectName = None
        self.DashboardIds = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("DashboardIds"):
            self.DashboardIds = params.get("DashboardIds")


class GetChartNamesByIdsRequest(AbstractModel):
    """GetChartNamesByIds请求参数结构体
    """

    def __init__(self):
        r"""获取图表名称
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param ChartIds: 图表id列表
        :type PathPrefix: String
        """
        self.ProjectName = None
        self.ChartIds = None

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("ChartIds"):
            self.ChartIds = params.get("ChartIds")


class UpdateDashboardRequest(AbstractModel):
    """UpdateDashboard请求参数结构体
    """

    def __init__(self):
        r"""修改仪表盘
        :param DashboardId: 仪表盘ID
        :type PathPrefix: String
        :param DashboardName: 仪表盘名称
        :type PathPrefix: String
        """
        self.DashboardId = None
        self.DashboardName = None

    def _deserialize(self, params):
        if params.get("DashboardId"):
            self.DashboardId = params.get("DashboardId")
        if params.get("DashboardName"):
            self.DashboardName = params.get("DashboardName")


class GetUsageRequest(AbstractModel, GetUsageInfo):
    """GetUsage请求参数结构体
    """

    def __init__(self):
        super(GetUsageRequest, self).__init__()

    def _deserialize(self, params):
        if params.get("Projects"):
            self.Projects = params.get("Projects")
        if params.get("TimeSeries"):
            self.Metrics = params.get("TimeSeries")
        if params.get("Data"):
            self.Data = params.get("Data")


class FieldType(object):
    FT_TEXT = "text"
    FT_DATE = "date"
    FT_LONG = "long"
    FT_JSON = "json"
    FT_DOUBLE = "double"


class FullTextIndex(object):
    def __init__(self):
        self.Lowercase = False
        self.Separator = ""
        self.Chinese = False


class IndexField(FullTextIndex):
    def __int__(self):
        self.FieldName = ""
        self.FieldType = ""
        self.FieldAlias = ""
        self.SeparatorStatus = False
        self.SubFields = []
        self.Aggregate = False


class SetIndexTemplateRequest(AbstractModel):
    """SetIndexTemplate请求参数结构体
    """

    def __init__(self, project_name, log_pool_name, index_status=True):
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name
        self.IndexStatus = index_status
        self.FullTextIndex = None
        self.IndexFields = []
        self.FullTextStatus = False

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("IndexStatus"):
            self.IndexStatus = params.get("IndexStatus")
        if params.get("FullTextIndex"):
            self.FullTextIndex = params.get("FullTextIndex")
        if params.get("IndexFields"):
            self.IndexFields = params.get("IndexFields")
        if params.get("FullTextStatus"):
            self.FullTextStatus = params.get("SeparatorStatus")


class GetIndexTemplateRequest(AbstractModel):
    """GetIndexTemplate请求参数结构体
    """

    def __init__(self, project_name, log_pool_name):
        r"""获取当前用户已经设置的索引配置
        :param ProjectName: 工程名称
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        """
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name

    def _deserialize(self, params):
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")


class GetDynamicIndexRequest(GetIndexTemplateRequest):
    def __init__(self, project_name, log_pool_name):
        super(GetDynamicIndexRequest).__init__(project_name, log_pool_name)


class CreateDownloadTaskRequest(AbstractModel, DownloadTask):

    def __init__(self, project_name, log_pool_name, start, end):
        r"""创建下载任务
        :param From: 日志起始时间
        :type PathPrefix: String
        :param To: 日志截止时间，时间跨度不能超过24小时
        :type PathPrefix: String
        :param LogPoolName: 日志池名称
        :type PathPrefix: String
        :param ProjectName: 工程名称
        :type PathPrefix: String
        """
        super(CreateDownloadTaskRequest, self).__init__()
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name
        self.From = start
        self.To = end

    def _deserialize(self, params):
        if params.get("From"):
            self.From = params.get("From")
        if params.get("To"):
            self.To = params.get("To")
        if params.get("LogPoolName"):
            self.LogPoolName = params.get("LogPoolName")
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")


class ListDownloadTasksRequest(AbstractModel, PageSize, DownloadTask):
    """ListDownloadTasks请求参数结构体
    """

    def __init__(self, page, size, project_name):
        r"""列举下载任务
        :param Page: 页码
        :type PathPrefix: String
        :param Size: 每页大小
        :type PathPrefix: String
        :param ProjectName: 工程名称
        :type PathPrefix: String
        """
        super(ListDownloadTasksRequest, self).__init__()
        self.Page = page
        self.Size = size
        self.ProjectName = project_name

    def _deserialize(self, params):
        if params.get("Page"):
            self.Page = params.get("Page")
        if params.get("Size"):
            self.Size = params.get("Size")
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")


class GetDownloadUrlsRequest(AbstractModel, DownloadTask):
    """GetDownloadUrls请求参数结构体
    """

    def __init__(self, project_name, download_task_id):
        r"""获取下载Url
        :param DownloadID: 任务下载ID，通过获取下载任务列表获取
        :type PathPrefix: String
        :param ProjectName: 工程名称
        :type PathPrefix: String
        """
        super(GetDownloadUrlsRequest, self).__init__()
        self.DownloadID = download_task_id
        self.ProjectName = project_name

    def _deserialize(self, params):
        if params.get("DownloadID"):
            self.DownloadID = params.get("DownloadID")
        if params.get("ProjectName"):
            self.ProjectName = params.get("ProjectName")


class GetMonitorDataRequest(AbstractModel):
    """GetMonitorData请求参数结构体
    """

    def __init__(self):
        super(GetMonitorDataRequest, self).__init__()
        self.Service = ""
        self.ProjectName = ""
        self.MetricNames = []
        self.Period = 0
        self.LogPools = []
        self.StartTime = ""
        self.EndTime = ""
        self.PageSize = 0
        self.PageNumber = 0

    def _deserialize(self, params):
        return


class DescribeLogErrorReasonRequest(AbstractModel, LogErrorReasonInfo):
    """DescribeLogErrorReason请求参数结构体
    """

    def __init__(self, project_name=None, log_pool_name=None, start=None, end=None):
        r"""获取日志数据错误原因
        """
        super(DescribeLogErrorReasonRequest, self).__init__()
        self.ProjectName = project_name
        self.LogPoolName = log_pool_name
        self.Start = start
        self.End = end

    def _deserialize(self, params):
        return


class GetTokenRequest(AbstractModel):
    """获取Token
     :param ExireTime: 过期时间，单位秒
     :type int
    """

    def __init__(self, expire_time=30):
        self.ExpireTime = expire_time


class DescribeProjectResponse(KlogResponse, ProjectInfo):
    def __init__(self):
        super(DescribeProjectResponse, self).__init__()


class DescribeLogPoolResponse(KlogResponse, LogPoolInfo):
    def __init__(self):
        super(DescribeLogPoolResponse, self).__init__()


class GetUserStatusResponse(KlogResponse, UserStatus):
    def __init__(self):
        super(GetUserStatusResponse, self).__init__()


class ListCount(Serializer):
    def __init__(self):
        self.Total = 0
        self.Count = 0


class LogHistogram(Serializer):
    def __init__(self):
        self.Key = ""
        self.LogCount = 0


class GetLogsResponse(KlogResponse, ListCount):
    def __init__(self):
        super(GetLogsResponse, self).__init__()
        self.HasSql = False
        self.Logs = {}
        self.Keys = []
        self.Histogram = []
        self.KeyValues = None
        self.Aggregations = None


class GetTokenResponse(KlogResponse):
    def __init__(self):
        super(GetTokenResponse, self).__init__()
        self.Token = ""
        self.ExpireAt = 0


class ListProjectsResponse(KlogResponse, ListCount):
    def __init__(self):
        super(ListProjectsResponse, self).__init__()
        self.Projects = []


class ListLogPoolsResponse(KlogResponse, ListCount, ProjectInfo):
    def __init__(self):
        super(ListLogPoolsResponse, self).__init__()
        self.LogPools = []


class GetIndexTemplateResponse(KlogResponse):
    def __init__(self):
        super(GetIndexTemplateResponse, self).__init__()
        self.FullTextIndex = {}
        self.IndexStatus = False
        self.IndexFields = []


class GetDynamicIndexResponse(GetIndexTemplateResponse):
    def __init__(self):
        super(GetDynamicIndexResponse, self).__init__()


class ListDownloadTaskResponse(KlogResponse, ListCount):
    def __init__(self):
        super(ListDownloadTaskResponse, self).__init__()
        self.Downloads = []


class GetDownloadUrlResponse(KlogResponse):
    def __init__(self):
        super(GetDownloadUrlResponse, self).__init__()
        self.Urls = []


class GetMonitorDataResponse(KlogResponse):
    def __init__(self):
        super(GetMonitorDataResponse, self).__init__()
        self.TotalCount = 0
        self.PageSize = 0
        self.PageNumber = 0
        self.DataPoints = []


class GetUsageResponse(KlogResponse, GetUsageInfo):
    def __init__(self):
        super(GetUsageResponse, self).__init__()


class ListQuickSearchResponse(KlogResponse, ListCount, LogPoolInfo):
    def __init__(self):
        super(ListQuickSearchResponse, self).__init__()
        self.QuickSearchs = []


class DescribeLogErrorReasonResponse(KlogResponse):
    def __init__(self):
        super(DescribeLogErrorReasonResponse, self).__init__()
        self.Data = []
