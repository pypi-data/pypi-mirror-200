from googleapiclient.discovery import build
from youtuber.api import YoutubeAPI
from youtuber.crawler import YoutubeCrawler
import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutoCrawler:
    """If you enter YouTube keywords, the comment crawled data is saved as a csv file and provided._summary_
    """

    def __init__(self, DEVELOPER_KEY: str, CRHOM_PATH: str) -> None:
        """Enter the developer key of youtube data api v3 and the path of chorme.exe.

        :param DEVELOPER_KEY: Developer key of youtube data api v3
        :type DEVELOPER_KEY: str
        :param CRHOM_PATH: Path of chorme.exe.
        :type CRHOM_PATH: str
        """
        self._DEV_KEY = DEVELOPER_KEY
        self._CHROME = CRHOM_PATH
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

    def _get_links(self, search_keyword: str, max_link_len: int) -> list:
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

    def __get_comment(self, link: str, max_comment_pg_len: int) -> list:
        """This classmethod is used in the get_comment_df method.

        :param link: Link of YouTube video
        :type link: str
        :param max_comment_pg_len: Maximum number of comment pages to search
        :type max_comment_pg_len: int
        :return: List of comments in the video link
        :rtype: list
        """
        data = []
        with Chrome(executable_path=self._chrome) as driver:
            wait = WebDriverWait(driver, 3)
            driver.get(link)
            for item in range(max_comment_pg_len):
                wait.until(
                    EC.visibility_of_element_located((By.TAG_NAME, "body"))
                ).send_keys(Keys.END)
                time.sleep(7)
            for comment in wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))
            ):
                data.append(comment.text)

        return data

    def _get_comment_df(self, links: list, max_comment_pg_len: int) -> pd.DataFrame:
        """This method crawls comments existing in multiple video links and creates a dataframe consisting of the 'comments' column containing the comments and the 'link' column containing the video link source of those comments.

        :param links: Links of YouTube video
        :type links: list
        :param max_comment_pg_len: Maximum number of comment pages to search
        :type max_comment_pg_len: int
        :return: a dataframe consisting of the 'comments' column containing the comments and the 'link' column containing the video link source of those comments.
        :rtype: pd.DataFrame
        """
        for i in range(len(links)):
            data = self.__get_comment(links[i], max_comment_pg_len)
            if i == 0:
                df = pd.DataFrame(data, columns=["comments"])
                df["link"] = links[0]
            else:
                temp_df = pd.DataFrame(data, columns=["comments"])
                temp_df["link"] = links[i]
                df = pd.concat([df, temp_df])
        df.dropna(how="any", inplace=True)

        return df

    def run(
        self,
        search_keyword: str,
        max_link_len: int,
        max_comment_pg_len: int,
        save_path: str,
    ) -> pd.DataFrame:
        """If you enter YouTube keywords, the comment crawled data is saved as a csv file and provided.

        :param search_keyword: The YouTube search keyword
        :type search_keyword: str
        :param max_link_len: Maximum returned link count
        :type max_link_len: int
        :param max_comment_pg_len: Maximum number of comment pages to search
        :type max_comment_pg_len: int
        :param save_path: Enter the full path to the csv file.
        :type save_path: str
        :return: Returns a pd.DataFrame object saved as a csv file.
        :rtype: pd.DataFrame
        """
        links = self._get_links(search_keyword, max_link_len)
        df = self._get_comment_df(links, max_comment_pg_len)
        if save_path is not None:
            df.to_csv(save_path, encoding="utf-8-sig", index=False)

        return df
