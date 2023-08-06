#!/usr/bin/env python3
import argparse
import base64
import datetime
import itertools
import json
import logging
import os
import sys
from io import BytesIO
from typing import Optional

import fitz
import markdown
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration

from ugctools.server import serve_images_files

logger = logging.getLogger(__name__)

CHROME_GUESSES_MACOS = (
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)

# https://stackoverflow.com/a/40674915/409879
CHROME_GUESSES_WINDOWS = (
    # Windows 10
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    # Windows 7
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    # Vista
    r"C:\Users\UserName\AppDataLocal\Google\Chrome",
    # XP
    r"C:\Documents and Settings\UserName\Local Settings\Application Data\Google\Chrome",
)

# https://unix.stackexchange.com/a/439956/20079
CHROME_GUESSES_LINUX = [
    "/".join((path, executable))
    for path, executable in itertools.product(
        (
            "/usr/local/sbin",
            "/usr/local/bin",
            "/usr/sbin",
            "/usr/bin",
            "/sbin",
            "/bin",
            "/opt/google/chrome",
        ),
        ("google-chrome", "chrome", "chromium", "chromium-browser"),
    )
]

def load_config(file: str)->dict:
    """加载配置

    配置文件内容：
    ```json
        title: 专栏的名字
        author: 作者的名字

    ```

    Returns:
        a dictionary indicates the config
    """
    _dir = os.path.dirname(file)

    with open(file, "r") as f:
        cfg = json.load(f)

        if not "css" in cfg:
            with open(os.path.join(_dir, "style.css"), "r") as f:
                css = "".join(f.readlines())
                cfg["css"] = css

        return cfg

def guess_chrome_path() -> str:
    if sys.platform == "darwin":
        guesses = CHROME_GUESSES_MACOS
    elif sys.platform == "win32":
        guesses = CHROME_GUESSES_WINDOWS
    else:
        guesses = CHROME_GUESSES_LINUX
    for guess in guesses:
        if os.path.exists(guess):
            logging.info("Found Chrome or Chromium at " + guess)
            return guess
    raise ValueError("Could not find Chrome. Please set CHROME_PATH.")


def make_html(template: str, md:str, variables: Optional[dict]=None)->str:
    """生成html

    将md渲染成html,合并到template中，并完成值替换
    """
    variables = variables or {}
    variables["content"] = markdown.markdown(md, extensions=["smarty", "abbr"])
    return template.format(**variables)

def make_pdf(html: str, css: Optional[str] = None) -> BytesIO:
    """将html转换成pdf"""
    page = HTML(string=html)

    buffer = BytesIO()

    if css is not None:
        font_config = FontConfiguration()
        styles = CSS(string=css, font_config=font_config)

        page.write_pdf(buffer, font_config = font_config)
    else:
        page.write_pdf(buffer)
        
    return buffer

def rend_as_png(html: str, save_to: str, css:Optional[str]=None) -> None:
    pdf = make_pdf(html, css)
    doc = fitz.Document(stream = pdf)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300)

    pix.save(save_to)

def write_pdf(html: str, save_to:str)->None:
    """将html生成为pdf，并写盘"""
    stream = make_pdf(html)

    with open(save_to, 'wb') as f:
        f.write(stream.read())
