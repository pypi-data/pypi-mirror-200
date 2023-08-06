from .Response import Response


def response_optimized(func):
    """response对象优化"""

    def inner(*args, **kwargs):
        response = func(*args, **kwargs)

        # 自适应编码
        response.encoding = response.apparent_encoding

        reqs = Response(response)  # Response对象
        reqs.__dict__.update(response.__dict__)  # 从原始数据更新到新对象

        return reqs

    return inner
