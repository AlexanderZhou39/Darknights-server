import mitmproxy
# from mitmproxy.models import HTTPResponse
# from netlib.http import Headers
def request(flow):
    host_name = flow.request.pretty_host
    if host_name.endswith("gs.arknights.global") or host_name.endswith("passport.arknights.global"):
        if (
            'app/' not in flow.request.path and 
            'user/login' not in flow.request.path 
            # 'account/login' not in flow.request.path and
            # 'account/syncData' not in flow.request.path
        ):
            mitmproxy.ctx.log( flow.request.path )
            # method = flow.request.path.split('/')[3].split('?')[0]
            flow.request.host = "127.0.0.1"
            flow.request.port = 9444
            flow.request.scheme = 'http'
            # if method == 'getjson':
            #     flow.request.path=flow.request.path.replace(method,"getxml")
            flow.request.headers["Host"] = "127.0.0.1"
