from googleapiclient.discovery import build


class YoutubeAPI:
    """Retrieve video links searched on YouTube through the YouTube Data v3 API.
    """

    def __init__(self, DEVELOPER_KEY: str):
        """Please input the developer API key from the YouTube API console.

        :param DEVELOPER_KEY: YouTube Data API Key
        :type DEVELOPER_KEY: str
        """
        self._DEV_KEY = DEVELOPER_KEY
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

    def get_links(self, search_keyword: str, max_link_len: int) -> list:
        """Retrieve video links by searching for a keyword on YouTube and limiting the number of links to max_link_len.

        :param search_keyword: The YouTube search keyword
        :type search_keyword: str
        :param max_link_len: Maximum returned link count
        :type max_link_len: int
        :return: List of searched video links
        :rtype: list
        """
        youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self._DEV_KEY,
        )
        search_response = (
            youtube.search()
            .list(
                q=search_keyword,
                type="video",
                part="id,snippet",
                maxResults=max_link_len,
            )
            .execute()
        )

        links = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                links.append(
                    "https://www.youtube.com/watch?v={}".format(
                        search_result["id"]["videoId"]
                    )
                )

        return links
