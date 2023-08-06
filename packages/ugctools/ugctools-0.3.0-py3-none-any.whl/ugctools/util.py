#!/usr/bin/env python3
import base64
import io
import itertools
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from io import BytesIO
from typing import List, Optional

import fitz
import markdown

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

def get_temp_filename(suffix:str="pdf")->str:
    _dir = tempfile.gettempdir()

    return os.path.join(_dir, f"{uuid.uuid1()}.{suffix}")

def translate_logging_level(level:str):
    return {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "fatal": logging.FATAL,
    }.get(level.lower(), logging.WARNING)

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
    variables["content"] = markdown.markdown(md, extensions=[
        "extra", 
        "attr_list",
        "admonition",
        "codehilite"
    ])
    return template.format(**variables)

def make_pdf_weasy_print(html: str, css: Optional[str] = None) -> BytesIO:
    """将html转换成pdf"""
    from weasyprint import CSS, HTML
    from weasyprint.text.fonts import FontConfiguration

    page = HTML(string=html)

    buffer = BytesIO()

    if css is not None:
        font_config = FontConfiguration()
        styles = CSS(string=css, font_config=font_config)

        page.write_pdf(buffer, font_config = font_config)
    else:
        page.write_pdf(buffer)
        
    return buffer

def rend_as_png(html: str, save_to: str, css:Optional[str]=None) -> List[str]:
    """将html渲染成png图片，并返回生成的图片文件名列表（全路径）"""
    pdf = make_pdf(html, css)
    doc = fitz.Document(stream = pdf)

    files = []
    if doc.page_count > 1:
        stem, ext = os.path.splitext(save_to)
        for i, page in enumerate(doc.pages()):
            pix = page.get_pixmap(dpi=300)

            file = f"{stem}-{i}-{ext}"
            pix.save(file)
            files.append(file)
    else:
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi = 300)
        pix.save(save_to)
        files.append(save_to)

    return files

def write_pdf(html: str, save_to:str)->None:
    """将html生成为pdf，并写盘"""
    stream = make_pdf(html)

    with open(save_to, 'wb') as f:
        f.write(stream.read())

def make_pdf(html: str, css: Optional[str] = None, chrome:str="") -> BytesIO:
    """
    render html as pdf stream
    """
    prefix = "ugctools"

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

    output_file = get_temp_filename()
    try:
        subprocess.run(
            [
                chrome,
                *options,
                f"--print-to-pdf={output_file}",
                "data:text/html;base64," + html64.decode("utf-8"),
            ],
            check=True,
        )
        logging.info(f"Wrote {output_file}")

        with open(output_file, "rb") as f:
            buffer = io.BytesIO()
            buffer.write(f.read())

            return buffer

    except subprocess.CalledProcessError as exc:
        if exc.returncode == -6:
            logging.warning(
                "Chrome died with <Signals.SIGABRT: 6> "
                f"but you may find {output_file} was created successfully."
            )
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        if os.path.isdir(tmpdir):
            logging.debug(f"Could not delete {tmpdir}")

    # when something went wrong, try weasyprint
    logger.warning("chrome failed, try weasyprint")
    return make_pdf_weasy_print(html, css)

