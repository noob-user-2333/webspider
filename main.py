from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import WebPage

url = 'https://www.zhihu.com'

# 清空已有数据
WebPage.WebPage.truncate_table()

# 配置Edge浏览器
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Edge(options=options)

try:
    driver.get(url)
    print("已访问知乎首页，开始滚动加载...")

    # 等待初始内容加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ContentItem"))
    )

    # 获取初始页面高度
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 设置滚动次数和间隔时间
    scroll_count = 5  # 滚动次数
    scroll_pause_time = 2  # 每次滚动后等待时间(秒)

    for i in range(scroll_count):
        # 滚动到页面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"已完成第 {i + 1}/{scroll_count} 次滚动，等待新内容加载...")

        # 等待新内容加载
        time.sleep(scroll_pause_time)

        # 计算新高度并与上次比较，判断是否已加载到底部
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("似乎已到达页面底部，停止滚动")
            break
        last_height = new_height

        

    # 获取最终页面源码
    sources = driver.page_source
    print(f"页面加载完成，HTML长度: {len(sources)}")

    # 存储到数据库
    WebPage.WebPage.create(url=url, html=sources)
    print("数据已保存到数据库")

    # 从数据库读取并处理
    pages = WebPage.WebPage.select()
    for page in pages:
        print(f"URL: {page.url}")
        print(f"HTML长度: {len(page.html)}")
        print(f"更新时间: {page.timestamp}")
        print("-" * 50)

        soup = BeautifulSoup(page.html, 'html.parser')
        # 提取问题标题
        questions = soup.find_all('div', class_='ContentItem-title')
        for q in questions:
            title = q.get_text(strip=True)
            if title:  # 过滤空标题
                print(title)

finally:
    driver.quit()
    print("浏览器已关闭")