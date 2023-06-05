class SearchResult:
    def __init__(self, yt_vid_id, title, description="", thumbnail_link="", channel_name=""):
        self.yt_vid_id = yt_vid_id
        self.title = title
        self.description = description
        self.thumbnail_link = thumbnail_link
        self.channel_name = channel_name

    def getLink(self):
        return f"https://www.youtube.com/watch?v={self.yt_vid_id}"
