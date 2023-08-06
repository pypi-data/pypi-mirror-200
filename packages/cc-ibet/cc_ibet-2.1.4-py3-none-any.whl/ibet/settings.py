import os

IBET_AGENT_DOMAIN = os.getenv('IBET_AGENT_DOMAIN', 'https://www.wabi88.com/')
DEFAULT_HEADERS = {
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Encoding': '',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}
CAPTCHA_API_KEY = os.getenv('CAPTCHA_API_KEY', '6F216C5017F742BC84B0554511D7AA69')
CAPTCHA_API = os.getenv('CAPTCHA_API', 'http://captcha.lehongnam.com/')

WIN_LOSE_MONGODB_URL = os.getenv('WIN_LOSE_MONGODB_URL', os.getenv('MONGODB_URL', ''))
TICKET_MONGODB_URL = os.getenv('TICKET_MONGODB_URL', os.getenv('MONGODB_URL', 'mongodb://127.0.0.1/bookmaker'))
