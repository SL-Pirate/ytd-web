class VideoProcessingFailureException(Exception):
    msg = "Video Processing failed"
    def __init__(self, msg=None) -> None:
        msg = VideoProcessingFailureException.msg + ": " + msg if msg is not None else VideoProcessingFailureException.msg
        super().__init__(msg)

class AudioProcessingFailureException(Exception):
    msg = "Audio Processing failed"
    def __init__(self, msg=None) -> None:
        msg = AudioProcessingFailureException.msg + ": " + msg if msg is not None else AudioProcessingFailureException.msg
        super().__init__(msg)

class InvalidVideoResolutionException(Exception):
    msg = "Invalid Resolution"
    def __init__(self, msg=None) -> None:
        msg = InvalidVideoResolutionException.msg + ": " + msg if msg is not None else InvalidVideoResolutionException.msg
        super().__init__(msg)
