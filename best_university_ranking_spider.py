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
        """
        :return: self.web_content - 由requests get到的页面html内容
        """
        result = requests.get(self.url)
        result.encoding = 'utf-8'
        self.web_content = str(result.text)

    def print_web_content(self):
        print(self.web_content)

    def extract_table(self, selector_path):
        """
        从页面中提取表格部分的html
        :param selector_path: 默认的path是全局变量中提取
        :return: tables, 页面中的表格标签html
        """
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
    """
    针对最好大学页面的特定处理，删除无用列，然后存档到excel文件
    :param tables: web_content.extract_table中从页面中提取的表格部分
    :param result_file: 目标存储文件
    :return: Nothing
    """
    table_df = pd.read_html(str(tables[0]), index_col=[0, 1, 2, 3])
    del table_df[0]['指标得分 生源质量（新生高考成绩得分） 培养结果（毕业生就业率） 社会声誉（社会捐赠收入·千元） 科研规模（论文数量·篇） 科研质量（论文质量·FWCI） 顶尖成果（高被引论文·篇） 顶尖人才（高被引学者·人） 科技服务（企业科研经费·千元） 成果转化（技术转让收入·千元） 学生国际化（留学生比例）']
    table_df[0].to_excel(result_file)


def web_content(target_url):
    """
    将传入的target_url用RequestWebPageUtil类中封装的request方法请求并返回页面内容
    :param target_url: 一个有效的URL地址，默认是全局变量中的TARGET_URL
    :return: 返回target_url的页面内容html
    """
    web_content = RequestWebPageUtil(target_url)
    web_content.requests_url()
    return web_content


def best_university_ranking(web_content, selector_path, result_file):
    """
    解析最好大学页面中的表格，提取目标字段列，存储到result_file中
    :param web_content: 页面内容html,由extract_url方法返回
    :param selector_path: 默认selector是提取页面中的表格SELECTOR_PATH
    :param result_file: 结构存储的文件地址
    :return: Nothing
    """
    best_university_ranking_2019_table = web_content.extract_table(selector_path)
    best_university_ranking_specialized_processor(best_university_ranking_2019_table, result_file)


def main():
    best_university_ranking(
        web_content(TARGET_URL), SELECTOR_PATH, 'result.xlsx'
    )


if __name__ == "__main__":
    main()
