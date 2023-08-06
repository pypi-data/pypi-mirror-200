
import logging
import os
import re
import shutil
from typing import List, Optional

import arrow
import fitz
import markdown

from ugctools import util
from ugctools.server import serve_images_files

logger = logging.getLogger(__name__)


def load_config(column_name: str):
    cfg_dir = os.path.expanduser(f"~/.ugc/redbook/{column_name}")
    if not os.path.exists(cfg_dir):
        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(pkg_dir, "assets")
        
        shutil.copytree(src, cfg_dir, dirs_exist_ok=True)

    cfg_file = os.path.join(cfg_dir, "cfg.json")
    return util.load_config(cfg_file)

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


def load_template(name: str, i: int)->str:
    """load template from ~/.ugc/redbook/news/{name}"""
    _dir = os.path.join(os.path.expanduser(f"~/.ugc/redbook/{name}/"))

    path = os.path.join(_dir, f"page-{i}.tpl")

    if not os.path.exists(path):
        path = os.path.join(_dir, "default.tpl")

    with open(path) as f:
        return "".join(f.readlines())

def render(name:str, extra:str="", date:Optional[str]=None, serve:bool=False):
    """生成一觉醒来系列小红书图片

    将输入 markdown 文件转换成{dst}/下的同名文件（但格式为图片）。如果输入文件包含多个节，则将自动转换为name-1.png, name-2.png, ...等。

    生成的文件中将包含以下元素:
    ```
    <dir id="rb"> 根元素
    <div id="title"> 系列标题元素
    <div id="author"> 作者元素

    ```
    Args:
        name: 输入文件名，可省略".md"
        date: 新闻所属日期，如果不提供，使用当天日期
        extra: 放在副标题当中的特别信息
        serve: 是否以http服务的方式呈现生成的图片
    """
    cfg = load_config("news")

    src_dir = os.path.expanduser(cfg.get("src") or "~/articles/news/src")
    dst_dir = os.path.expanduser(cfg.get("dst") or "~/articles/news/dst")

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    if not name.endswith(".md"):
        name = name + ".md"

    src = os.path.join(src_dir, name)
    with open(src, "r") as f:
        buffer = "".join(f.readlines())
        sections = re.split(r"<\!--\s*page\s*-->\n", buffer) # type: ignore

    image_files = []
    variables = {
        "date": arrow.get(date) if date is not None else arrow.now(),
        "extra": extra,
        "css": cfg["css"],
        "author": cfg["author"]
    }

    for i, md in enumerate(sections):
        template = load_template("news", i)

        html = util.make_html(template, md, variables)

        html_file = os.path.join(dst_dir, f"{name[:-3]}-{i}.html")
        with open(html_file, "w", encoding="utf-8") as htmlfp:
            htmlfp.write(html)
            logging.info(f"Wrote {htmlfp.name}")

        output_path = os.path.join(dst_dir, f"{name}-{i}.png")
        util.rend_as_png(html, output_path, cfg["css"])
        image_files.append(f"/{name}-{i}.png")

    if serve:
        logger.info("serviing files at %s", dst_dir)
        serve_images_files(dst_dir, image_files, cfg.get("port", 1086))
        



