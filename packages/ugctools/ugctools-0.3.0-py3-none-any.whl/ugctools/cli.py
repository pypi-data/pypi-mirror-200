import logging
import os
import shutil

import fire

from ugctools.redbook import news

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    logging.basicConfig(level=logging.WARNING)
    fire.Fire({
        "news": news.render
    })

fire.Fire({
    "news": news.render
})
