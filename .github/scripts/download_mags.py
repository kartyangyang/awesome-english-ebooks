import os
import requests
import re
from bs4 import BeautifulSoup

# 源仓库的README地址
source_url = "https://github.com/hehonghui/awesome-english-ebooks"

def get_latest_issue_links():
    """从源仓库README中提取最新一期的下载链接（逻辑简化版，可能需要根据实际情况调整）"""
    print("正在获取最新期刊信息...")
    response = requests.get(source_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    readme = soup.find('article', class_='markdown-body').get_text()
    
    # 简单的匹配逻辑：寻找以 http 开头，以 .pdf/.epub/.mobi 结尾的链接
    # 注意：这个逻辑可能需要根据源仓库的实际格式进行调整
    links = re.findall(r'(https?://[^\s]+?\.(?:pdf|epub|mobi))', readme)
    print(f"找到 {len(links)} 个文件链接")
    return links

def download_files(links):
    """下载文件到 mags 目录"""
    download_dir = 'mags'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    for link in links[-5:]:  # 只下载最新的几个文件，避免仓库过大
        filename = os.path.join(download_dir, link.split('/')[-1].split('?')[0])
        print(f"正在下载: {filename}")
        try:
            response = requests.get(link, stream=True, timeout=30)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"下载完成: {filename}")
        except Exception as e:
            print(f"下载失败 {link}: {e}")

if __name__ == "__main__":
    mag_links = get_latest_issue_links()
    if mag_links:
        download_files(mag_links)
    else:
        print("未找到新的期刊链接")
