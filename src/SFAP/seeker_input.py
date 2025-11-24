from .publish_channel import PublishChannel

class SeekerInput:
    def __init__(self, keywords: list[str], filters: list[str], publish_channels: list[PublishChannel]):
        self.keywords = keywords
        self.filters = filters
        self.publish_channels = publish_channels
