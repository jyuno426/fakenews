# -*- coding:utf-8 -*-

import re
import kss
import requests
from bs4 import BeautifulSoup


def crawl_raw_html(url):
    """
    raw html text 가져오기
    timeout 15초
    무조건 크롤링 성공시켜야하나???
    """
    # return requests.get(url, timeout=15).text
    while True:
        try:
            return requests.get(url, timeout=5).text
        except TimeoutError:
            pass
        except Exception as e:
            raise e


def beautifulize(raw_html):
    """
    raw html text를 BeautifulSoup 객체로 변환 (파싱)
    """
    return BeautifulSoup(raw_html, "lxml")


def normalize(text):
    return " ".join(text.strip().replace('"', "").replace("'", "").split())


def crawl_snu_factcheck():
    base_url = "http://factcheck.snu.ac.kr"
    id_set = set()
    for page in range(1, 268):
        print("page:", page)
        url = base_url + "/v2/facts?page=" + str(page)
        html = beautifulize(crawl_raw_html(url))

        contents = html.find("div", {"class": "fcItem_wrap"})

        content_list = contents.find_all("li", {"class": "fcItem_wrap_li"})

        for content in content_list:
            # title = content.find("a").text.replace("\n", " ").strip()
            metric = content.find("script").text
            metric = metric.replace(" ", "").replace("\n", "")[15:-3]
            metrics = metric.split(",")

            id = metrics[0][6:-1]
            if id in id_set:
                raise Exception("same id")
            else:
                id_set.add(id)
            scores = ",".join(metrics[1:-1])[9:-1]

            score = {}
            if "," not in scores:
                assert scores == ""
            else:
                for score_by in scores[:-1].split(","):
                    judge, score_str = score_by.split(":")
                    score[judge[1:-1]] = int(score_str)

            reference_url = ""
            # reference_content = ""
            try:
                reference_url = content.find("a",
                                             {"class": "reference"})["href"]
                # reference_content = beautifulize(
                #     crawl_raw_html(reference_url)).text
            except TypeError:
                pass

            detail_url = base_url + content.find("a")["href"]
            detail_content = beautifulize(crawl_raw_html(detail_url))
            title = normalize(
                detail_content.find("div", {
                    "class": "fcItem_detail_li_p"
                }).find("a"))

            ind = "@@@@"
            with open("res.txt", "a+") as f:
                f.write(id + ind + title + ind + str(score) + ind +
                        reference_url + "\n")


def get_article():
    with open("res.txt", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            print(i + 1, "/", len(lines))
            id, _, _, reference_url = line.strip().split("@@@@")

            import os

            if os.path.exists("articles/" + id + ".txt"):
                continue

            try:
                soup = beautifulize(crawl_raw_html(reference_url))
            except:
                continue

            with open("articles/" + id + ".txt", "w") as g:
                for elem in soup.find_all(["script", "style"]):
                    elem.extract()
                text = normalize(soup.get_text())
                for sentence in kss.split_sentences(text):
                    g.write(sentence + "\n")


if __name__ == "__main__":
    # crawl_snu_factcheck()
    get_article()
