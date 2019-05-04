"""
功能描述：
1. 输入：大学排名URL链接
(URL: http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html)
2. 爬取内容：排名、学校名称、省市、总分
3. 输出：大学排名信息的屏幕输出以及相关信息保存在"result.xlsx"文档
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup

TARGET_URL = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html"
SELECTOR_PATH = "body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table"


class RequestWebPageUtil:
    def __init__(self, target_url):
        self.url = target_url
        self.web_content = None

    def current_url(self):
        print("[*] Current target url:", self.url)

    def requests_url(self):
        result = requests.get(self.url)
        result.encoding = 'utf-8'
        self.web_content = str(result.text)

    def print_web_content(self):
        print(self.web_content)

    def extract_table(self, selector_path):
        _selector_path = selector_path
        if _selector_path is None or len(_selector_path) <= 1:
            """
            SELECTOR: body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table
            XPATH： /html/body/div[3]/div/div[2]/div/div[3]/div/table
            """
            _selector_path = "body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table"
        soup_content = BeautifulSoup(self.web_content, 'html.parser')
        tables = soup_content.select(_selector_path)
        return tables


def best_university_ranking_specialized_processor(tables, result_file):
    table_df = pd.read_html(str(tables[0]), index_col=[0, 1, 2, 3])
    del table_df[0]['指标得分 生源质量（新生高考成绩得分） 培养结果（毕业生就业率） 社会声誉（社会捐赠收入·千元） 科研规模（论文数量·篇） 科研质量（论文质量·FWCI） 顶尖成果（高被引论文·篇） 顶尖人才（高被引学者·人） 科技服务（企业科研经费·千元） 成果转化（技术转让收入·千元） 学生国际化（留学生比例）']
    table_df[0].to_excel(result_file)


def extract_url(target_url):
    web_content = RequestWebPageUtil(target_url)
    web_content.requests_url()
    return web_content


def best_university_ranking(web_content, selector_path, result_file):
    best_university_ranking_2019_table = web_content.extract_table(selector_path)
    best_university_ranking_specialized_processor(best_university_ranking_2019_table, result_file)


def main():
    best_university_ranking(
        extract_url(TARGET_URL), SELECTOR_PATH, 'result.xlsx'
    )


if __name__ == "__main__":
    main()
