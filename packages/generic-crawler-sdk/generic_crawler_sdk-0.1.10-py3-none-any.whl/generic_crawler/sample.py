from generic_crawler.core import GenericCrawler, ActionReader
from generic_crawler.config import Config

from dotenv import load_dotenv
load_dotenv()

endpoint = "endpoint"

config = Config(token="",
                endpoint_url=endpoint)

crawler = GenericCrawler(config=config)
reader = ActionReader(path_to_yaml="kanun_headline.yml")


data, _ = crawler.retrieve(reader.action)

crawled_products = []
crawled_products.extend(data['static review str in item boxes'])
pagin_url = data["last pagination item url"][0]

while 'no url found' != pagin_url:
    reader.action["url"] = pagin_url
    data, response = crawler.retrieve(reader.action)
    pagin_url = data["last pagination item url"][0]
    crawled_products.extend(data['static review str in item boxes'])





print("ok")
