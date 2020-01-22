class OverpassTooManyRequests(Exception):
    """Error 429: Too many requests."""
    pass

class OverpassGatewayTimeout(Exception):
    """Error 504: Too much load."""
    pass
