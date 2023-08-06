from core.metrics import latency, counter


def report_request_success(metrics_prefix: str, url: str, begin: float):
    url_tag = _build_url_tags(url)
    tag_kvs = _append_base_tag(url_tag)
    latency(_build_latency_key(metrics_prefix), begin, tag_kvs)
    counter(_build_counter_key(metrics_prefix), 1, tag_kvs)


def report_request_error(metrics_prefix: str, url: str, begin: float, code: int, message: str):
    url_tag = _build_url_tags(url)
    tag_kvs = _append_base_tag(url_tag)
    tag_kvs.extend(["code:" + str(code), "message:" + message])
    latency(_build_latency_key(metrics_prefix), begin, tag_kvs)
    counter(_build_counter_key(metrics_prefix), 1, tag_kvs)


def report_request_exception(metrics_prefix: str, url: str, begin: float, e: BaseException):
    url_tag = _build_url_tags(url)
    tag_kvs = _with_exception_tags(url_tag, e)
    tag_kvs = _append_base_tag(tag_kvs)
    latency(_build_latency_key(metrics_prefix), begin, tag_kvs)
    counter(_build_counter_key(metrics_prefix), 1, tag_kvs)


def _with_exception_tags(tag_kvs: list, e: BaseException):
    msg = str(e).lower()
    if "time" in msg and "out" in msg:
        if "connect" in msg:
            tag_kvs.append("message:connect-timeout")
            return tag_kvs
        if "read" in msg:
            tag_kvs.append("message:read-timeout")
            return tag_kvs
        tag_kvs.append("message:timeout")
        return tag_kvs
    tag_kvs.append("message:other")
    return tag_kvs


def _build_url_tags(url: str):
    if url.__contains__("ping"):
        return ["url:" + _adjust_url_tag(url), "req_type:ping"]
    if url.__contains__("data/api"):
        return ["url:" + _adjust_url_tag(url), "req_type:data-api", "tenant:" + _parse_tenant(url),
                "scene:" + _parse_scene(url)]
    if url.__contains__("predict/api"):
        return ["url:" + _adjust_url_tag(url), "req_type:predict-api", "tenant:" + _parse_tenant(url),
                "scene:" + _parse_scene(url)]
    return ["url:" + _adjust_url_tag(url), "req_type:unknown"]


def _parse_tenant(url: str):
    sp = url.split("?")[0].split("/")
    if len(sp) < 2:
        return ""
    return sp[len(sp) - 2]


def _parse_scene(url: str):
    sp = url.split("?")[0].split("/")
    if len(sp) < 2:
        return ""
    return sp[len(sp) - 1]


def _adjust_url_tag(url: str):
    return url.replace("=", "_is_")


def _build_counter_key(metrics_prefix: str):
    return metrics_prefix + "." + "count"


def _build_latency_key(metrics_prefix: str):
    return metrics_prefix + "." + "latency"


def _append_base_tag(tag_kvs: list):
    version = "1.3.0"
    tag_kvs.extend(["language:python", "version:" + version])
    return tag_kvs
