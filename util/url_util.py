from selenium import webdriver

key_urls = {
    'mp.zhizhuma.com/qr.html': '1',
    'www.hdsdjf.com/smp': '2',
    'mp.zhizhuma.com/book.htm': '3',
    'mp.zhizhuma.com/share/audio.htm': '1',

}

header = {
    "ua_base": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 "
               "Safari/537.36 micromessenger/5.0.1.352 "
}


def get_url_type(mp3_code_url: str):
    mp3_code_keys = mp3_code_url.split('//')
    if len(mp3_code_keys) >= 2:
        for key_url in key_urls:
            if mp3_code_keys[1].startswith(key_url):
                return key_urls.get(key_url)
        return 0
    else:
        return -1


def open_chrome_get_html(html_url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(html_url)
    return driver.page_source
