#!/usr/bin/env python3
import argparse
import base64
import datetime
import itertools
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Optional

import arrow
import fire
import fitz
import markdown

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

def load_config(column_name: str)->dict:
    """根据专栏名字加载配置

    配置文件{package_name}/assets/{column_name}/cfg.json
    配置文件内容：
    ```json
        title: 专栏的名字
        author: 作者的名字

    ```

    Returns:
        a dictionary indicates the config
    """
    cfg_dir = os.path.expanduser(f"~/.ugc/config/{column_name}")
    if not os.path.exists(cfg_dir):
        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(pkg_dir, f"assets/{column_name}")
        
        shutil.copytree(src, cfg_dir, dirs_exist_ok=True)

    cfg_file = os.path.join(cfg_dir, "cfg.json")

    with open(cfg_file, "r") as f:
        cfg = json.load(f)
        if not "preamble" in cfg:
            with open(os.path.join(cfg_dir, "preamble"), "r") as f:
                cfg["preamble"] = f.read()

        if not "postamble" in cfg:
            with open(os.path.join(cfg_dir, "postamble"), "r") as f:
                cfg["postamble"] = f.read()
        
        if not "css" in cfg:
            with open(os.path.join(cfg_dir, "main.css"), "r") as f:
                cfg["css"] = f.read()

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


def make_html(md: str, cfg: dict) -> str:
    """
    Compile md to HTML and prepend/append preamble/postamble.

    Insert <prefix>.css if it exists.
    """
    return "".join(
        (
            cfg["preamble"].format(title=cfg["title"], css=cfg["css"]),
            markdown.markdown(md, extensions=["smarty", "abbr"]),
            cfg["postamble"],
        )
    )


def write_pdf(html: str, prefix: str, chrome:str="") -> None:
    """
    Write html to prefix.pdf
    """
    chrome = chrome or guess_chrome_path()
    html64 = base64.b64encode(html.encode("utf-8"))
    options = [
        "--no-sandbox",
        "--headless",
        "--print-to-pdf-no-header",
        "--enable-logging=stderr",
        "--log-level=2",
        "--in-process-gpu",
        "--disable-gpu",
    ]

    # Ideally we'd use tempfile.TemporaryDirectory here. We can't because
    # attempts to delete the tmpdir fail on Windows because Chrome creates a
    # file the python process does not have permission to delete. See
    # https://github.com/puppeteer/puppeteer/issues/2778,
    # https://github.com/puppeteer/puppeteer/issues/298, and
    # https://bugs.python.org/issue26660. If we ever drop Python 3.9 support we
    # can use TemporaryDirectory with ignore_cleanup_errors=True as a context
    # manager.
    tmpdir = tempfile.mkdtemp(prefix=prefix)
    options.append(f"--crash-dumps-dir={tmpdir}")
    options.append(f"--user-data-dir={tmpdir}")

    try:
        subprocess.run(
            [
                chrome,
                *options,
                f"--print-to-pdf=/tmp/{prefix}.pdf",
                "data:text/html;base64," + html64.decode("utf-8"),
            ],
            check=True,
        )
        logging.info(f"Wrote /tmp/{prefix}")
    except subprocess.CalledProcessError as exc:
        if exc.returncode == -6:
            logging.warning(
                "Chrome died with <Signals.SIGABRT: 6> "
                f"but you may find /tmp/{prefix} was created successfully."
            )
        else:
            raise exc
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        if os.path.isdir(tmpdir):
            logging.debug(f"Could not delete {tmpdir}")

def build_redbook_meta(cfg: dict, date: arrow.Arrow, extra: str)->str:
    fields = []

    for field in cfg["meta"]:
        if "{title}" in field:
            txt = field.format(title=cfg["title"])
            fields.append(f"<div id='title'>{txt}</div>")
        elif "{date}" in field:
            txt = field.format(date=date.format('YYYY年MM月DD日'))
            fields.append(f"<div id='date'>{txt}</div>")
        elif "{author}" in field:
            txt = field.format(author=cfg["author"])
            fields.append(f"<div id='author'>{txt}</div>")
        elif "{extra}" in field:
            txt = field.format(extra=extra)
            fields.append(f"<div id='extra'>{txt}</div>")
        else:
            logger.warning("%s not support", field)

    return "<div id='meta'>" + "\n".join(fields) + "</div>\n"

def redbook(name:str, date:Optional[str]=None, extra:str="", serve:bool=False):
    """生成一觉醒来系列小红书图片

    将输入 markdown 文件转换成{dst}/下的同名文件（但格式为图片）。如果输入文件包含多个节，则将自动转换为name-1.png, name-2.png, ...等。

    生成的文件中将包含以下元素:
    ```
    <dir id="rb"> 根元素
    <div id="title"> 系列标题元素
    <div id="author"> 作者元素

    ```
    Args:
        name: 输入文件名
    """
    cfg = load_config("hello")

    src_dir = os.path.expanduser(cfg.get("src") or "~/articles/hello/src")
    dst_dir = os.path.expanduser(cfg.get("dst") or "~/articles/hello/dst")

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    src = os.path.join(src_dir, f"{name}.md")
    with open(src, "r") as f:
        buffer = "".join(f.readlines())
        sections = buffer.split("<!--page-->\n")
    
    date = arrow.get(date or arrow.now())
    image_files = []
    for i, section in enumerate(sections):
        if i == 0:
            meta = build_redbook_meta(cfg, date, extra)
            html = make_html(meta + section, cfg)
        else:
            html = make_html(section, cfg)

        with open(f"/tmp/{name}-{i}.html", "w", encoding="utf-8") as htmlfp:
            htmlfp.write(html)
            logging.info(f"Wrote {htmlfp.name}")

        prefix = f"{name}-{i}"
        write_pdf(html, prefix)

        with fitz.open(f"/tmp/{name}-{i}.pdf") as doc:
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=300)

            output_path = os.path.join(dst_dir, f"{name}-{i}.png")
            pix.save(output_path)
            image_files.append(output_path)

    if serve:
        serve_images_files(image_files, cfg.get("port", 1086))
        

def main():
    logging.basicConfig(level=logging.INFO)
    fire.Fire({
        "rb": redbook,
    })


if __name__ == "__main__":
    main()
