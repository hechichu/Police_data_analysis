# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 21:14:14 2024

@author: DWiz

"""

import requests
from bs4 import BeautifulSoup
import csv

# url root
base_url = ('https://gaj.sh.gov.cn/shga/wzXxfbZfgkml/pagaList?pa'
            '=0150ec9ce81d4bde0b042ffef9fbb51b11b120eafe4fda679ecdbdf5fc86559f3f1f1f48cf7ba8d139266173c9d1d8a82334d0264a3110dce9c3b4f3251bb779bf3a00ca574997521e509e726093dbaf4e761432ef56538145b1f2eebf98bdaf5225949ee058061bb49bc6dc6185f58f&page={page}&type=1')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                  'Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/105',
    'Host': 'gaj.sh.gov.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

#define start and end page
s_p = 1
e_p = 256

with open('penalty_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["序号", "处罚决定书文号", "案件名称", "被处罚人姓名", "处罚事由", "处罚依据", "处罚结果",
                  "行政执法单位名称", "处罚日期"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for page in range(s_p, e_p + 1):
        url = base_url.format(page=page)
        print(f'Fetching URL: {url}')  # Print URL for debugging
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f'Failed to fetch page {page}, status code: {response.status_code}')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'Page {page} content length: {len(response.text)}')  # Print response content length for debugging

        rows = soup.find_all('tr')

        for row in rows[1:11:]:
            cols = row.find_all('td')
            if len(cols) < 9:
                print(f'Row does not have enough columns: {row}')
                continue
            data = {
                "序号": cols[0].text.strip(),
                "处罚决定书文号": cols[1].text.strip(),
                "案件名称": cols[2].text.strip(),
                "被处罚人姓名": cols[3].text.strip(),
                "处罚事由": cols[4].text.strip(),
                "处罚依据": cols[5].text.strip(),
                "处罚结果": cols[6].text.strip(),
                "行政执法单位名称": cols[7].text.strip(),
                "处罚日期": cols[8].text.strip()
            }
            writer.writerow(data)

        print(f'第{page}页采集完成')

print('全部页面采集完成')
