import streamlit as st
import pandas as pd

# form openpyxl import load_workbook

st.set_page_config(page_title='人力资源调查统计', layout='wide')
hide_streamlit_style = '''
    <style>
        #MainMenu  {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid ="stAppViewContaine"']{
            width:100%;
            height:100%;
            background-size:cover;
            backgroud-position:center center;
            backgroud-repeat:repeat;
            backgroud-image:url(""
            }
        [data-testid = "stHeader"]{
            background-color:rgba(0,0,0,0)
        }
	</style>
'''
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def get_data_from_excel(excel_file):
    return (pd.read_excel(excel_file))


uploaded_file = st.file_uploader("请选择花名册", type=['xls', 'xlsx'])
if uploaded_file is not None:
    # hmc = get_data_from_excel(uploaded_file)
    # s = pd.Series(f'{hmc["姓名"].count()}', index=['总人数'])
    # st.write(s)
    # s = pd.DataFrame(['总人数', hmc["姓名"].count()])
    # # st.write(s.dtypes)
    # # st.write(f'在职总人数：{hmc["姓名"].count()}')
    # st.write(s)
    # df_sex = hmc['性别'].value_counts()
    # st.write(df_sex.dtypes)
    # st.write(df_sex)
    # st.write(hmc['性别'].value_counts())
    # df_Political_Status = hmc['政治面貌'].value_counts()
    # st.write(hmc['政治面貌'].value_counts())
    # df_education = hmc['学历'].value_counts()
    # st.write(hmc['学历'].value_counts())
    #
    #
    #
    # hmc_nl = hmc[(hmc['年龄'] <= 35)]
    # st.write(f'35及以下：{hmc_nl["年龄"].count()}')
    #
    # hmc_nl = hmc[(hmc['年龄'] > 35) & (hmc['年龄'] <= 40)]
    # st.write(f'36至40岁：{hmc_nl["年龄"].count()}')
    #
    # hmc_nl = hmc[(hmc['年龄'] > 40) & (hmc['年龄'] <= 45)]
    # st.write(f'41至45岁：{hmc_nl["年龄"].count()}')
    #
    # hmc_nl = hmc[(hmc['年龄'] > 45) & (hmc['年龄'] <= 50)]
    # st.write(f'46至50岁：{hmc_nl["年龄"].count()}')
    #
    # hmc_nl = hmc[(hmc['年龄'] > 50) & (hmc['年龄'] <= 54)]
    # st.write(f'51至54岁：{hmc_nl["年龄"].count()}')
    #
    # hmc_nl = hmc[(hmc['年龄'] >= 55)]
    # st.write(f'55岁及以上：{hmc_nl["年龄"].count()}')

    hmc = get_data_from_excel(uploaded_file)

    # 大专以下列表
    under_degree = ['大专', '中专', '中技', '高中', '初中', '职高']

    st.header('全体人员统计表')
    data = hmc
    df_a = pd.DataFrame({'人数': [data['身份证号码'].count(),
                                data['性别'][data.性别 == '男'].count(),
                                data['性别'][data.性别 == '女'].count(),
                                data['民族'][(data.民族 != '汉') & (data.民族 is not None)].count(),
                                data['政治面貌'][data.政治面貌 == '中共党员'].count(),
                                data['政治面貌'][(data.政治面貌 != '中共党员') & (data.性别 is not None)].count(),
                                data['学历'][data.学历 == '博士'].count(),
                                data['学历'][data.学历 == '研究生'].count(),
                                data['学历'][data.学历 == '本科'].count(),
                                data['学历'][(data.学历 != '博士') & (data.学历 != '研究生') & (data.学历 != '本科')].count(),
                                # data['学历'].count(x) for x in under_degree,
                                # grouped_data.get(x) for x in ['<=35', '36~40', '41~45', '46~50', '51~55', '56~60']
                                data['年龄'][data.年龄 <= 35].count(),
                                data['年龄'][(data.年龄 > 35) & (data.年龄 <= 40)].count(),
                                data['年龄'][(data.年龄 > 40) & (data.年龄 <= 45)].count(),
                                data['年龄'][(data.年龄 > 45) & (data.年龄 <= 50)].count(),
                                data['年龄'][(data.年龄 > 50) & (data.年龄 <= 55)].count(),
                                data['年龄'][data.年龄 > 55].count(),
                                ]
                         },
                        index=['总人数', '男', '女', '少数民族', '中共党员', '其他党派', '博士', '研究生', '本科', '大专以下', '35岁以下', '36~40岁', '41~45岁', '46~50岁', '51~55岁', '55岁以上']).T

    df_a

    st.header('专业技术人员统计表')
    data = hmc[hmc['专业技术职称等级'].notnull()]  #统计专业技术职称等级
    data
    # df_a = pd.DataFrame({'学历': [data['学历'][data.学历 == '博士'].count(),
    #                             data['学历'][data.学历 == '研究生'].count(),
    #                             data['学历'][data.学历 == '本科'].count(),
    #                             data['学历'][data.学历 != '博士' & data.学历 != '研究生' & data.学历 != '本科'].count()]
    #                     },
    #                     index=['博士', '研究生', '本科', '大专以下'])

    # # 根据年龄分组并计算人员结构统计表
    # grouped_data = data.groupby(['年龄']).count()
    # # grouped_data
    #
    # # 绘制不同年龄段的人员数量柱状图
    # df = pd.DataFrame({'Group': ['35岁以下', '36~40', '41~45', '46~50', '51~55', '56~60'],
    #                    'Count': [grouped_data.get(x) for x in ['<=35', '36~40', '41~45', '46~50', '51~55', '56~60']]},
    #                   index=['人员结构'])
    # df

    # # plotly.offline.plot({
    # #     'data': [df],
    # #     'layout': go.Bar(x=df['Count'], y=df['Group'])
    # # }, filename='人员结构统计图')
    # df
#
# '''
# 学习用，供参考
# book = load_workbook('人员花名册.xlsx')
# write = pd.ExcelWriter(r'人员花名册', engine='openpyxl')
# write.book = book
# write.sheets = {ws.title: ws for ws in book.worksheets}
# df_a.to_excel(write, sheet_name='人员花名册', header=False, index=False, startrow= 4, startcol = 7)
# write.save()
# write.close()
# '''

