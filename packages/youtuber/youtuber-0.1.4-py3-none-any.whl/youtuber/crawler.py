import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YoutubeCrawler:
    """A class for crawling comments using Python Selenium 
    """

    def __init__(self, chromedriver_path: str):
        """Please input the path to the Chrome driver as an argument.

        :param chromedriver_path: Path of 'chorome.exe'
        :type chromedriver_path: str
        """
        self._chrome = chromedriver_path

    @staticmethod
    def get_comment(chromedriver_path: str, link: str, max_comment_pg_len: int) -> list:
        """Use this staticmethod if you want to crawl comments for a single video link.

        :param chromedriver_path: Path of 'chorome.exe'
        :type chromedriver_path: str
        :param link: Link of YouTube video
        :type link: str
        :param max_comment_pg_len: Maximum number of comment pages to search
        :type max_comment_pg_len: int
        :return: List of comments in the video link
        :rtype: list
        """
        data = []
        with Chrome(executable_path=chromedriver_path) as driver:
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

    def get_comment(self, link: str, max_comment_pg_len: int) -> list:
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

    def get_comment_df(self, links: list, max_comment_pg_len: int) -> pd.DataFrame:
        """This method crawls comments existing in multiple video links and creates a dataframe consisting of the 'comments' column containing the comments and the 'link' column containing the video link source of those comments.

        :param links: Links of YouTube video
        :type links: list
        :param max_comment_pg_len: Maximum number of comment pages to search
        :type max_comment_pg_len: int
        :return: a dataframe consisting of the 'comments' column containing the comments and the 'link' column containing the video link source of those comments.
        :rtype: pd.DataFrame
        """
        for i in range(len(links)):
            data = self.get_comment(links[i], max_comment_pg_len)
            if i == 0:
                df = pd.DataFrame(data, columns=["comments"])
                df["link"] = links[0]
            else:
                temp_df = pd.DataFrame(data, columns=["comments"])
                temp_df["link"] = links[i]
                df = pd.concat([df, temp_df])
        df.dropna(how="any", inplace=True)

        return df
