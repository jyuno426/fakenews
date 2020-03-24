# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def crawl_raw_html(url):
    """
    raw html text 가져오기
    timeout 15초
    무조건 크롤링 성공시켜야하나???
    """
    while True:
        try:
            return requests.get(url, timeout=15).text
        except TimeoutError:
            pass
        except Exception as e:
            raise e


def beautifulize(raw_html):
    """
    raw html text를 BeautifulSoup 객체로 변환 (파싱)
    """
    return BeautifulSoup(raw_html, "lxml")


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
                reference_url = content.find("a", {"class": "reference"})["href"]
                # reference_content = beautifulize(
                #     crawl_raw_html(reference_url)).text
            except TypeError:
                pass

            detail_url = base_url + content.find("a")["href"]
            detail_content = beautifulize(crawl_raw_html(detail_url))
            title = (
                detail_content.find("div", {"class": "fcItem_detail_li_p"})
                .find("a")
                .text.replace("\n", " ")
                .strip()
            )

            ind = "@@@@"
            with open("res.txt", "a+") as f:
                f.write(
                    id + ind + title + ind + str(score) + ind + reference_url + "\n"
                )


def get_article():
    try:
        driver = webdriver.Chrome("./chromedriver")
    except:
        driver = webdriver.Chrome("./chromedriver.exe")
    driver.implicitly_wait(5)

    with open("res.txt", "r") as f:
        for line in f.readlines():
            id, _, _, reference_url = line.strip().split("@@@@")
            with open("articles/" + id + ".txt", "w") as g:
                # try:
                driver.get(reference_url)
                text = driver.find_element_by_tag_name("body").text.replace("\n", " ")
                g.write(text + "\n")
                # except:
                driver.quit()
                break


if __name__ == "__main__":
    # crawl_snu_factcheck()
    get_article()
