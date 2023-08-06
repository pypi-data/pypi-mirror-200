import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

try:
    from klog.common.protobuf.klog_pb2 import LogGroup, LogGroupList
    from klog.common.compress import Lz4Compressor
    from klog.common.const import *
except ImportError:
    from klog.common.protobuf.klog_pb2 import LogGroup, LogGroupList
    from klog.common.compress import Lz4Compressor
    from klog.common.const import *


class KLogHandler(BaseHTTPRequestHandler):
    STAT = dict()
    MODE = dict()

    def do_GET(self):
        self._code("", "", 404)

    def do_POST(self):
        p = urlparse(self.path)
        qa = parse_qs(p.query)
        params = {k: v[0] for k, v in qa.items()}

        data = None
        content_length = int(self.headers.get('content-length', '0'))
        if content_length > 0:
            data = self.rfile.read(content_length)

        if p.path == '/PutLogs':
            p = params.get("ProjectName", "")
            l = params.get("LogPoolName", "")
            self.put_logs(p, l, data)
        elif p.path == '/PutLogsM':
            drop = params.get("DropIfPoolNotExists", "").lower() == "true"
            self.put_logs_m(drop, data)
        elif p.path == '/_bulk':
            self.bulk(data)
        elif p.path == '/_set_mode':
            self.MODE["mode"] = params.get('mode')
        elif p.path == '/_stat':
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.STAT).encode())
        elif p.path == '/_clear_stat':
            self.send_response(200)
            self.end_headers()
            self.STAT.clear()
            self.MODE.clear()
        else:
            self._code("", "", 404)

    def put_logs(self, p, l, data):
        self._add_stat(p, l, "requests", 1)

        mode = self.MODE.get('mode')
        if mode == 'InternalServerError':
            self._code(p, l, 500)
            return

        if 'not_exists' in l:
            self._code(p, l, 400)
            self._err_code('ProjectOrLogPoolNotExist')
            return

        if self.headers.get('Authorization') == '':
            self._code(p, l, 400)
            self._err_code('MissingAuthorization')
            return
        elif self.headers.get('x-klog-compress-type') == 'lz4':
            compressor = Lz4Compressor()
            try:
                data = compressor.decompress(data)
            except Exception as e:
                print(str(e))
                self._code(p, l, 400)
                self._err_code('PostBodyUncompressError')
                return

        lg = LogGroup()

        try:
            lg.ParseFromString(data)
        except Exception as e:
            print(str(e))
            self._code(p, l, 400)
            self._err_code('InvalidProtobufData')
            return

        if lg.ByteSize() > 3 << 20:
            self._code(p, l, 400)
            self._err_code('PostBodyTooLarge')
            return

        if len(lg.logs) > MAX_BULK_SIZE:
            self._code(p, l, 400)
            self._err_code('MaxBulkSizeExceeded')
            return

        for pb_log in lg.logs:
            if len(pb_log.contents) > MAX_KEY_COUNT:
                self._code(p, l, 400)
                self._err_code('MaxKeyCountExceeded')
                return

            for content in pb_log.contents:
                if len(content.key) > MAX_KEY_SIZE:
                    self._code(p, l, 400)
                    self._err_code('MaxKeySizeExceeded')
                    return

                if len(content.value) > MAX_VALUE_SIZE:
                    self._code(p, l, 400)
                    self._err_code('MaxValueSizeExceeded')
                    return

            self._add_stat(p, l, "contents", len(pb_log.contents))

        self._add_stat(p, l, "logs", len(lg.logs))
        self._code(p, l, 200)

    def put_logs_m(self, drop, data):
        time.sleep(0.05)
        self._add_stat('', '', "requests", 1)

        mode = self.MODE.get('mode')
        if mode == 'InternalServerError':
            self._code('', '', 500)
            return

        if self.headers.get('Authorization') == '':
            self._code('', '', 400)
            self._err_code('MissingAuthorization')
            return
        elif self.headers.get('x-klog-compress-type') == 'lz4':
            compressor = Lz4Compressor()
            try:
                data = compressor.decompress(data)
            except Exception as e:
                print(str(e))
                self._code('', '', 400)
                self._err_code('PostBodyUncompressError')
                return

        lgl = LogGroupList()

        try:
            lgl.ParseFromString(data)
        except Exception as e:
            print(str(e))
            self._code('', '', 400)
            self._err_code('InvalidProtobufData')
            return

        if lgl.ByteSize() > 3 << 20:
            self._code('', '', 400)
            self._err_code('PostBodyTooLarge')
            return

        count = 0
        for lg in lgl.logGroupList:
            count += len(lg.logs)
        if count > MAX_BULK_SIZE:
            self._code('', '', 400)
            self._err_code('MaxBulkSizeExceeded')
            return

        dropped = 0
        for lg in lgl.logGroupList:
            p = lg.project
            l = lg.pool

            if 'not_exists' in l:
                if not drop:
                    self._code('', '', 400)
                    self._err_code('ProjectOrLogPoolNotExist')
                    return
                else:
                    dropped += len(lg.logs)

            for pb_log in lg.logs:
                if len(pb_log.contents) > MAX_KEY_COUNT:
                    self._code('', '', 400)
                    self._err_code('MaxKeyCountExceeded')
                    return

                for content in pb_log.contents:
                    if len(content.key) > MAX_KEY_SIZE:
                        self._code('', '', 400)
                        self._err_code('MaxKeySizeExceeded')
                        return

                    if len(content.value) > MAX_VALUE_SIZE:
                        self._code('', '', 400)
                        self._err_code('MaxValueSizeExceeded')
                        return

                self._add_stat(p, l, 'contents', len(pb_log.contents))
            self._add_stat(p, l, 'batches', 1)
            self._add_stat(p, l, 'logs', len(lg.logs))
        self._code('', '', 200)
        if dropped > 0:
            dic = {
                'DroppedLogs': dropped,
            }
            self.wfile.write(json.dumps(dic).encode())

    def bulk(self, data):
        self._add_stat('', '', "requests", 1)

        mode = self.MODE.get('mode')
        if mode == 'InternalServerError':
            self._code('', '', 500)
            return
        elif mode == 'BadJsonReturn':
            bad_json = '{"a: 1,"b": 2}'
            self._code('', '', 200)
            self.wfile.write(bad_json.encode())
            return
        elif mode == 'BadRequest':
            ret = {
                "error": {
                    "root_cause": [
                        {
                            "type": "index_not_found_exception",
                            "reason": "no such index [mock-index]",
                            "resource.type": "index_or_alias",
                            "resource.id": "mock-index",
                            "index_uuid": "_na_",
                            "index": "mock-index"
                        }
                    ],
                    "type": "index_not_found_exception",
                    "reason": "no such index [mock-index]",
                    "resource.type": "index_or_alias",
                    "resource.id": "mock-index",
                    "index_uuid": "_na_",
                    "index": "mock-index"
                },
                "status": 400
            }
            self._code('', '', 400)
            self.wfile.write(json.dumps(ret).encode())
            return

        ret = {
            'took': 50,
            'errors': False,
            'items': []
        }

        count = 0
        err_count = 0
        pre_index = ''
        for line in data.decode().split("\n"):
            if not line:
                continue
            dic = json.loads(line.encode())
            index = dic.get('index', {}).get('_index')
            if not index:
                self._add_stat('', '', 'contents', len(dic))
                self._add_stat('', pre_index, 'contents', len(dic))
            else:
                count += 1
                if mode in ['PartiallyError', 'PartiallyErrorWithout400'] and count % 2 == 0:
                    ret['errors'] = True
                    err_count += 1
                    rotate = err_count % 4
                    status = 0
                    if rotate == 0:
                        status = 0
                    elif rotate == 1:
                        if mode == 'PartiallyErrorWithout400':
                            status = 429
                        else:
                            status = 400
                    elif rotate == 2:
                        status = 429
                    elif rotate == 3:
                        status = 500

                    item = {
                        "_index": index,
                        "_type": "_doc",
                        "_id": "5",
                        "status": status,
                        "error": {
                            "type": "doc_status_{}".format(status),
                            "reason": "mock_doc_error_reason",
                            "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA",
                            "shard": "0",
                            "index": "index1"
                        }
                    }
                else:
                    item = {
                        "_index": index,
                        "_type": "_doc",
                        "_id": "1",
                        "_version": 1,
                        "result": "created",
                        "_shards": {
                            "total": 2,
                            "successful": 1,
                            "failed": 0
                        },
                        "status": 201,
                        "_seq_no": 0,
                        "_primary_term": 1
                    }
                    self._add_stat('', index, 'logs', 1)
                    self._add_stat('', '', 'logs', 1)
                ret['items'].append({"index": item})
                pre_index = index

        self._code('', '', 200)
        self.wfile.write(json.dumps(ret).encode())

    def _err_code(self, err_code, err_msg=''):
        dic = {
            "ErrorCode": err_code,
            "ErrorMessage": err_msg,
        }
        self.wfile.write(json.dumps(dic).encode())

    def _code(self, project_name, log_pool_name, code):
        self.send_response(code)
        self.end_headers()
        self._add_stat(project_name, log_pool_name, str(code), 1)
        if project_name or log_pool_name:
            self._add_stat('', '', str(code), 1)

    def _add_stat(self, project_name, log_pool_name, name, delta):
        key = '{}__{}'.format(project_name, log_pool_name)
        if key not in self.STAT:
            self.STAT[key] = dict()

        pool_stat = self.STAT[key]
        if name not in pool_stat:
            pool_stat[name] = delta
        else:
            pool_stat[name] += delta


def main():
    port = 8765
    srv = HTTPServer(('', port), KLogHandler)
    print('Server started on port %s' % port)
    srv.serve_forever()


if __name__ == '__main__':
    main()
