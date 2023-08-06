class DownloadCancel(Exception):
    pass


class GoPacException(Exception):
    pass


class CliNotFound(GoPacException):
    pass


class ErrorDecodeOutput(GoPacException):
    pass


class DownloadPacFileException(GoPacException):
    pass


class SavePacFileException(GoPacException):
    pass
