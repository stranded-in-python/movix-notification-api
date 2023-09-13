class Error(BaseException):
    ...


class DataInconsistentError(Error):
    ...


class ConnectionFailedError(Error):
    ...


class EventNameError(Error):
    ...


class NOTIFICATION_NOT_FOUND(Error):
    ...
