class VideoProcessingFailureException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AgeRestrictedVideoException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnavailableVideoQualityException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidLinkError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
