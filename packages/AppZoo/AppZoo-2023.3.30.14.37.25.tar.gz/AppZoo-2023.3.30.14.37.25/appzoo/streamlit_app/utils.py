#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : utils
# @Time         : 2022/10/18 下午1:29
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import textwrap
import streamlit as st
from streamlit.components.v1 import html
from streamlit.elements.image import image_to_url

_set_html = lambda h: st.markdown(h, unsafe_allow_html=True)


def hide_st_style(footer_content='🔥'):
    _ = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    _ = f"""
        <style>.css-18e3th9 {{padding-top: 2rem;}}
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        footer:after {{content:"{footer_content}";visibility: visible;display: block;position: 'fixed';}}
        </style>
        """
    _set_html(_)


def set_footer(prefix="Made with 🔥 by ", author='Betterme', url='http://q6e9.cn/Hm40w2'):  # 链接门户、微信
    _ = f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #F5F5F5;
        color: #000000;
        text-align: center;
        border-style: solid;
        border-width: 1px;
        border-color: #DDDDDD;
        padding: 8px;
        }}
    </style>
    <div class="footer">
    <p>{prefix}<a href="{url}" target="_blank">{author}</a></p> 
    </div>
    """
    _set_html(_)


# 设置文本字体
def set_font():
    _ = f"""
    <style>
    h1,h2,h3,h4,h5,h6 {{
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-weight: 400;
    }}
    </style>
    """
    _set_html(_)


# 设置页面背景色
def set_background_color(color='#f1f1f1'):
    _ = f"""
    <style>
    body {{
        background-color: {color};
    }}
    </style>
    """
    _set_html(_)


def set_background_image(image=get_module_path('./pics/夕阳.png', __file__)):
    image_url = image_to_url(image, width=-1, clamp=False, channels="RGB", output_format="auto", image_id="")
    _ = f'''
        <style>
            .css-fg4pbf {{
            background-image:url({image_url});
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center center;
            height: 100vh;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            }}
        </style>
    '''
    _set_html(_)


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def columns_placed(bins=2, default_position=0, gap='small'):  # ("small", "medium", or "large")
    _ = st.columns(spec=bins, gap=gap)
    if len(_) < default_position:
        default_position = -1
    return _[default_position]


def show_code(func):
    """Showing the code of the demo."""
    _ = st.sidebar.checkbox("Show code", False)
    if _:
        # Showing the code of the demo.
        st.markdown("---")
        st.markdown("## Main Code")
        sourcelines, _ = inspect.getsourcelines(func)
        st.code(textwrap.dedent("".join(sourcelines[1:])))
        st.markdown("---")


def st_form(before_submit, after_submit, label='Submit', key='Form', ):
    with st.form(key):
        before_submit
    submitted = st.form_submit_button(label)
    if submitted:
        after_submit


def display_pdf(base64_pdf, width='100%', height=1000):
    pdf_display = f"""<embed src="data:application/pdf;base64,{base64_pdf}" width="{width}" height="{height}" type="application/pdf">"""

    st.markdown(pdf_display, unsafe_allow_html=True)


def display_html(text='会飞的文字'):  # html("""<marquee bgcolor="#00ccff" behavior="alternate">这是一个滚动条</marquee>""")
    _ = f"""
        <marquee direction="down" width="100%" height="100%" behavior="alternate" style="border:solid"  bgcolor="#00FF00">

          <marquee behavior="alternate">

            {text}

          </marquee>

        </marquee>
        """
    st.markdown(_, unsafe_allow_html=True)
