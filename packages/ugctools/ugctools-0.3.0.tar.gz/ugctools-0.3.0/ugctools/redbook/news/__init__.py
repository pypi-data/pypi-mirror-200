
import json
import logging
import os
import re
import shutil
from posixpath import isabs
from typing import List, Optional

import arrow

from ugctools import util
from ugctools.server import serve_images_files

logger = logging.getLogger(__name__)


def load_config():
    dst_dir = os.path.expanduser(f"~/.ugc/redbook/news")
    dst = os.path.join(dst_dir, "cfg.json")
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(pkg_dir, "cfg.json")
        shutil.copy(src, dst)

    with open(dst, "r", encoding='utf-8') as f:
        cfg = json.load(f)
        if "logging" in cfg:
            logging.basicConfig(level=util.translate_logging_level(cfg["logging"]))
        return cfg

def render_subtitle(subtitles: List[str], cfg:dict, page:str)->str:
    fields = []

    for field in subtitles:
        if "{title}" in field:
            title = cfg.get("title") or cfg.get(page, {}).get("title")
            if title:
                txt = field.format(title=title)
                fields.append(f"<div id='title'>{txt}</div>")
        elif "{date}" in field:
            date = cfg.get("date") or arrow.now()
            txt = field.format(date=date.format('YYYY年MM月DD日'))
            fields.append(f"<div id='date'>{txt}</div>")
        elif "{author}" in field:
            txt = field.format(author=cfg["author"])
            fields.append(f"<div id='author'>{txt}</div>")
        elif "{extra}" in field and "extra" in cfg:
            txt = field.format(extra=cfg["extra"])
            fields.append(f"<div id='extra'>{txt}</div>")
        else:
            logger.warning("%s not support", field)

    return "<div id='meta'>" + "\n".join(fields) + "</div>\n"


def load_template(theme: str, i: int)->str:
    """load template from ~/.ugc/redbook/news/{theme}"""
    _dir = os.path.join(os.path.expanduser(f"~/.ugc/redbook/news/{theme}"))

    path = os.path.join(_dir, f"page-{i}.tpl")

    if not os.path.exists(path):
        path = os.path.join(_dir, "default.tpl")

    with open(path,"r", encoding='utf-8') as f:
        return "".join(f.readlines())
    
def load_css(theme: str)->str:
    _dir = os.path.join(os.path.expanduser(f"~/.ugc/redbook/news/{theme}"))
    path = os.path.join(_dir, "style.css")

    with open(path, "r", encoding='utf-8') as f:
        return f.read()

def render(name:str="", extra:str="", date:Optional[str]=None, serve:bool=False,
           theme:Optional[str]=None, set_theme:Optional[str]=None):
    """生成一觉醒来系列小红书图片

    将输入 markdown 文件转换成{dst}/下的同名文件（但格式为图片）。如果输入文件包含多个节，则将自动转换为name-1.png, name-2.png, ...等。

    生成的文件中将包含以下元素:
    ```
    <dir id="rb"> 根元素
    <div id="title"> 系列标题元素
    <div id="author"> 作者元素

    ```
    Args:
        name: 要转换的文件。合法格式为绝对路径，或者仅包含文件名。当仅包含文件名时，将从cfg.json->src指定的目录中搜索，此时可以不提供文件扩展名。
        date: 新闻所属日期，如果不提供，使用当天日期
        extra: 放在副标题当中的特别信息
        serve: 是否以http服务的方式呈现生成的图片
        theme: 当前使用的theme，此theme为一次使用
        set_theme: 设置当前及此后使用的theme。请勿与theme同时使用
    """
    if set_theme is not None:
        use_theme(set_theme)
        theme = set_theme

    cfg = load_config()
    if theme is not None:
        ensure_theme_exists(theme)
    else:
        theme = "default"

    cfg["css"] = load_css(theme)
    src_dir = os.path.expanduser(cfg.get("src") or "~/articles/news/src")
    dst_dir = os.path.expanduser(cfg.get("dst") or "~/articles/news/dst")

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    if not name.endswith(".md"):
        name = name + ".md"

    name = os.path.expanduser(name)
    if not os.path.isabs(name):
        src = os.path.join(src_dir, name)
    else:
        src = name
    with open(src, "r", encoding="utf-8") as f:
        buffer = "".join(f.readlines())
        sections = re.split(r"<\!--\s*page\s*-->\n", buffer) # type: ignore

    image_files = []
    variables = {
        "date": arrow.get(date) if date is not None else arrow.now(),
        "extra": extra,
        "css": cfg["css"],
        "author": cfg["author"]
    }

    stem = os.path.splitext(os.path.basename(name))[0]

    for i, md in enumerate(sections):
        template = load_template(theme, i)

        html = util.make_html(template, md, variables)

        html_file = os.path.join(dst_dir, f"{stem}-{i}.html")
        with open(html_file, "w", encoding="utf-8") as htmlfp:
            htmlfp.write(html)
            logging.info(f"Wrote {htmlfp.name}")

        output_path = os.path.join(dst_dir, f"{stem}-{i}.png")
        files = util.rend_as_png(html, output_path, cfg["css"])
        image_files.extend([os.path.basename(f) for f in files])

    if serve:
        logger.info("serving files at %s", dst_dir)
        serve_images_files(dst_dir, image_files, cfg.get("port", 1086))

def use_theme(theme:str):
    """set the theme, copy if needed
    
    if the theme is already in ~/.ugc/redbook/news, then skip coping

    Args:
        theme: the name of the theme, i.e., 'default'
    """
    cfg = load_config()

    ensure_theme_exists(theme)

    if cfg.get("theme") == theme:
        print("Theme not changed, skipping")
    else:
        cfg["theme"] = theme
        print(f"Theme changed to {theme}.")
        

def ensure_theme_exists(theme:str):
    theme_dir = os.path.join(os.path.expanduser("~/.ugc/redbook/news"), theme)

    if not os.path.exists(theme_dir):
        os.makedirs(theme_dir, exist_ok=True)
        pkd_dir = os.path.dirname(__file__)
        src_theme_dir = os.path.join(pkd_dir, theme)

        if not os.path.exists(src_theme_dir):
            raise ValueError(f"theme {theme} does not exist")
        else:
            shutil.copytree(src_theme_dir, theme_dir, dirs_exist_ok=True)
