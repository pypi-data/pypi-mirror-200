class BrawlAPIException(Exception):
    pass

class ClientError(BrawlAPIException):
    # 403
    pass

class ServerError(BrawlAPIException):
    # 5xx
    pass

def generate_exception(code: int, message: str = ''):
    if code == 403:
        return ClientError(message)
    elif code >= 500:
        return ServerError(message)
    else:
        return BrawlAPIException(f'error code {code}: {message}')