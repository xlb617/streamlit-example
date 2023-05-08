from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Streamlit App应用程序',layout = 'wide')

def get_data_from_excel(excel_file):
    return(pd.read_excel(excel_file))

st.title("标题：欢迎加入Streamlit")
# st.write('Hello World!')
# st.text('st.text输出内容！')

uploaded_file = st.file_uploader("选择文件")
if uploaded_file is not None:
    st.write(f'上传文件为：{uploaded_file.name}')
    st.write(get_data_from_excel(uploaded_file))

st.sidebar.title('页面导航： ')
menu = ['菜单1','菜单2','菜单3','菜单4','菜单5','菜单6','菜单7']
choice = st.sidebar.selectbox('菜单选项',menu)
st.sidebar.text(f'你选择了【{choice}】选项')
