import browser_cookie3
def GetCookies(domain_name):
    # 获取 Edge 浏览器中 example.com 的 Cookies
    return browser_cookie3.edge(domain_name="www.zhihu.com")


__all__ = ["GetCookies"]