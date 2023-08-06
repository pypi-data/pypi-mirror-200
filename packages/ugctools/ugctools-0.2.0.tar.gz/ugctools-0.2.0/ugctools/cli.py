import logging

import fire

from ugctools.redbook import news

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    logging.basicConfig(level=logging.INFO)
    fire.Fire({
        "news": news.render
    })

fire.Fire({
    "news": news.render
})
