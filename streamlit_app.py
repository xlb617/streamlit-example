import streamlit as st
import pandas as pd
import re
from datetime import date


def generate_css(language):
    if language == 'en':

        before_content = "Drag files here"

        after_content = "The maximum limit for each file is 200MB."

        button_content = "Browse file"

    else:

        before_content = "将文件拖放到此处"

        after_content = "每个文件最大限制200MB"

        button_content = "浏览文件"

    css = f'''
<style>
    [data-testid="stFileUploaderDropzone"] div div::before {{
        content: "{before_content}";
    }}
    [data-testid="stFileUploaderDropzone"] div div span {{
        display: none;
    }}
    [data-testid="stFileUploaderDropzone"] div div::after {{
        color: rgba(49, 51, 63, 0.6);
        font-size: .8em;
        content: "{after_content}";
    }}
    [data-testid="stFileUploaderDropzone"] div div small {{
        display: none;
    }}
    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {{
        font-size: 0px;
    }}
    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]::after {{
        content: "{button_content}";
        font-size: 17px !important;
    }}
    #MainMenu  {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid ="stAppViewContaine"']{{
            width:100%;
            height:100%;
            background-size:cover;
            backgroud-position:center center;
            backgroud-repeat:repeat;
            backgroud-image:url(""
            }}
        [data-testid = "stHeader"]{{
            background-color:rgba(0,0,0,0)
        }}

</style>
'''

    return css

st.set_page_config(page_title='HR数据统计系统', page_icon="📊", layout='wide')
st.title("📊 人力资源数据统计 - 文件上传")
# hide_streamlit_style = '''
#     <style>
#         #MainMenu  {visibility: hidden;}
#         footer {visibility: hidden;}
#         [data-testid ="stAppViewContaine"']{
#             width:100%;
#             height:100%;
#             background-size:cover;
#             backgroud-position:center center;
#             backgroud-repeat:repeat;
#             backgroud-image:url(""
#             }
#         [data-testid = "stHeader"]{
#             background-color:rgba(0,0,0,0)
#         }
# 	</style>
# '''
st.markdown(generate_css('cn'), unsafe_allow_html=True)

if 'show_items' not in st.session_state:
    st.session_state.show_items = []

def update_show_items(columns):
    for column in columns:
        checkbox_key = f'{column}_checkbox'
        if checkbox_key not in st.session_state:
            st.session_state[checkbox_key] = False
        checkbox = st.checkbox(column, key=checkbox_key)

        if checkbox and column not in st.session_state.show_items:
            st.session_state.show_items.append(column)
        elif not checkbox and column in st.session_state.show_items:
            st.session_state.show_items.remove(column)


def get_data_from_excel(excel_file, header=0):
    return (pd.read_excel(excel_file, header=header))


# 从字符串中取出数字
def extract_numbers(text):
    numbers = []
    current_number = ''
    for char in text:
        if char.isdigit():
            current_number += char
        elif current_number:
            numbers.append(int(current_number))
            current_number = ''
    if current_number:
        numbers.append(int(current_number))
    return numbers

# 用折叠面板优化界面，添加详细中文指引
with st.expander("📁 点击上传数据文件", expanded=True):
    st.markdown("""
    **支持格式**：Excel(.xlsx)、CSV(.csv)  
    **数据要求**：需包含所属公司、部门、科室名称、岗位、姓名、性别、民族、在职人员明细、籍贯、身份证出生年月等字段  
    **上传说明**：单次仅支持一个文件，文件大小不超过200MB
    """)
    uploaded_file = st.file_uploader(
        label="选择文件",  # 简化提示文本
        type=["xlsx", "csv", "xls"],
        label_visibility="collapsed"  # 隐藏默认标签，避免重复
    )


# uploaded_file = st.file_uploader("请选择花名册", type=['xls', 'xlsx'])
if uploaded_file is not None:
    hmc = get_data_from_excel(uploaded_file)
    # 清洗excel表头里不规范的非汉字字符
    for column in hmc.columns:
        # new_column = column.replace(r'[\W_]+', '')
        new_column = re.sub('([^\u4e00-\u9fa5])', '', column)
        if column != new_column:
            rename_dict = {column: new_column}
            hmc = hmc.rename(columns=rename_dict)

    data = hmc
    show_items = []
    TongJi_Item = ['性别', '年龄', '学历类型', '学习形式', '政治面貌', '民族', '取得专业技术职务等级', '取得工人技术职务等级', '职业资格', '职务级别', '合同类型', '身份', '合同类别', '用工形式']
    # 大专以下列表
    under_degree = ['大专', '中专', '中技', '高中', '初中', '职高', '专科']
    #大专列表
    degree = ['大专', '专科']

    # 研究生以上列表
    up_degree = ['研究生', '博士']
    # 性别列表
    genders = {'男': '性别 == "男"', '女': '性别 == "女"'}
    #年龄范围
    age_ranges = ['100~200岁', '90~100岁', '80~90岁',  '70~80岁', '60~70岁', '60~200岁',  '0~60岁', '56~60岁', '51~55岁', '46~50岁', '41~45岁', '36~40岁', '31~35岁', '30岁以下']
    # 年龄段
    age_groups = {}
    for age_range in age_ranges:
        if '~' in age_range:
            start, end = age_range.split('~')
            start = int(start.replace('岁', ''))
            end = int(end.replace('岁', ''))
            age_groups[age_range] = f"(年龄 >= {start}) & (年龄 <= {end})"
        else:
            # 处理没有 '~' 的情况，例如返回错误或使用默认值
            age_groups[age_range] = f"年龄 <= {extract_numbers(age_range)[0]}"
    # 政治面貌
    Political_Status = {'中共党员': '政治面貌 == "中共党员"', '共青团员': '政治面貌 == "共青团员"', '中共预备党员': '政治面貌 == "中共预备党员"', '群众': '政治面貌 == "群众"',
                        '其他党派': '(政治面貌 == "民革会员") & (政治面貌 == "民盟盟员") & (政治面貌 == "民建会员") & (政治面貌 == "民建会员") & (政治面貌 == "民进会员") & (政治面貌 == "农工党党员") & (政治面貌 == "致公党党员") & (政治面貌 == "九三学社社员") & (政治面貌 == "台盟盟员") & (政治面貌 == "无党派民主人士")'}

    # 民族
    Nations = {'汉族': '民族 == "汉族"', '少数民族': '(民族 != "汉族") & (民族 !="")'}
    # 学习形式  全日制和非全日制
    divided_time_full_or_parts = {
        '全日制博士': '((学历类型 == "博士")  | (学历类型 == "博士学位研究生") | (学历类型 == "博士研究生")) & (学习形式 == "全日制")',
        '全日制研究生': '((学历类型 == "研究生") | (学历类型 == "硕士学位研究生") | (学历类型 == "硕士研究生")) & (学习形式 == "全日制")',
        '全日制本科': '(学历类型 == "本科") & (学习形式 == "全日制")',
        '全日制大专以下': '(学历类型 != "博士") & (学历类型 != "研究生") & (学历类型 != "本科") & (学历类型 != "硕士学位研究生") & (学习形式 == "全日制")',
        '全日制大专': '学历类型.isin(@degree) & (学习形式 == "全日制")',
        '全日制中专': '(学历类型 == "中专") & (学习形式 == "全日制") ',
        '全日制中技': '(学历类型 == "中技") & (学习形式 == "全日制")',
        '全日制高中': '(学历类型 == "高中") & (学习形式 == "全日制")',
        '全日制初中': '(学历类型 == "初中") & (学习形式 == "全日制")',
        '全日制职高': '(学历类型 == "职高") & (学习形式 == "全日制")',
        '非全日制博士': '((学历类型 == "博士")  | (学历类型 == "博士学位研究生") | (学历类型 == "博士研究生")) & (学习形式 == "非全日制")',
        '非全日制研究生': '((学历类型 == "研究生") | (学历类型 == "硕士学位研究生") | (学历类型 == "硕士研究生")) & (学习形式 == "非全日制")',
        '非全日制本科': '(学历类型 == "本科") & (学习形式 == "非全日制")',
        '非全日制大专以下': '((学历类型 != "博士") & (学历类型 != "研究生") & (学历类型 != "本科") & (学历类型 != "硕士学位研究生"))& (学习形式 == "非全日制")',
        '非全日制大专': '(学历类型.isin(@degree)) & (学习形式 == "非全日制")',
        '非全日制中专': '(学历类型 == "中专") & (学习形式 == "非全日制") ',
        '非全日制中技': '(学历类型 == "中技") & (学习形式 == "非全日制")',
        '非全日制高中': '(学历类型 == "高中") & (学习形式 == "非全日制")',
        '非全日制初中': '(学历类型 == "初中") & (学习形式 == "非全日制")',
        '非全日制职高': '(学历类型 == "职高") & (学习形式 == "非全日制")'
    }
    # 学历类型
    educations = {'博士': '学历类型 == "博士"  | (学历类型 == "博士学位研究生") | (学历类型 == "博士研究生")', '研究生': '(学历类型 == "研究生") | (学历类型 == "硕士学位研究生") | (学历类型 == "硕士研究生")', '本科': '学历类型 == "本科"',
                  '大专以下': '(学历类型 != "博士") & (学历类型 != "研究生") & (学历类型 != "本科") & (学历类型 != "硕士学位研究生")', '大专': '学历类型.isin(@degree)',
                  '中专': '学历类型 == "中专"',
                  '中技': '学历类型 == "中技"', '高中': '学历类型 == "高中"', '初中': '学历类型 == "初中"', '职高': '学历类型 == "职高"'}

    # #学习形式 Full time and Part time  全日制与非全日制
    # full_time_and_part_time ={}
    # 取得专业技术职务等级
    # 初级专业技术等级列表
    junior_professional_technical_level = ['助埋会计师', '助理政工师', '助理经济师', '助埋工程师', '程序员', '电子商务技术员',
                                           '信息处理技术员', '信息系统运行管理员', '助理编辑', '助理审计师',
                                           '助理工程师', '系统规划与管理师', '软件设计师']
    # 中级专业技术等级列表
    intermediate_professional_technical_level = ['会计师', '政工师', '经济师', '多媒体应用设计师' '计算机辅助设计师',
                                                 '电子商务师', '信息安全工程师', '数据库系统工程师', '数据库系统工程师',
                                                 '信息系统管理工程师', '计算机硬件工程师', '信息技术支持工程师', '编辑',
                                                 '审计师', '工程师', '中级软件设计师', '中级系统规划与管理师']
    # 高级专业技术等级列表
    advanced_professional_technical_level = ['高级会计师', '高级经济师', '信息系统项目管理师', '高级政工师',
                                             '高级工程师', '高级软件设计师', '高级系统规划与管理师']
    # 专业技术等级
    Professional_technical_levels = {'高级': '取得专业技术职务等级.isin(@advanced_professional_technical_level)',
                                     '中级': '取得专业技术职务等级.isin(@intermediate_professional_technical_level)',
                                     '初级': '取得专业技术职务等级.isin(@junior_professional_technical_level)'}
    # Professional_technical_levels = {'高级': '取得专业技术职务等级.isin(@advanced_professional_technical_level)', '副高': '专业技术等级 == "副高"', '中级': '取得专业技术职务等级.isin(@intermediate_professional_technical_level)'',
    #                                  '初级': '取得专业技术职务等级.isin(@junior_professional_technical_level)' }
    # 工人技术等级
    Worker_technical_levels = {'技师': '取得工人技术职务等级 == "技师"', '高级工': '取得工人技术职务等级 == "高级工"', '中级工': '取得工人技术职务等级 == "中级工"',
                               '初级工': '取得工人技术职务等级 == "初级工"'}
    # '普通工': ('工人技术等级 == ""') & (专业技术等级 !="")
    # 出版物发行员职业资格
    PVQEs = {'二级/技师': '职业资格 == "出版物发行员二级"', '三级/高级': '职业资格 == "出版物发行员三级"', '四级/中级': '职业资格 == "出版物发行员四级"',
             '五级/初级': '职业资格 == "出版物发行员五级"', }

    # 职务级别    职务级别 == '正科'
    job_levelS = {'正处': '职务级别 == "正处"', '副处': '职务级别 == "副处"', '正科': '职务级别 == "正科"', '副科': '职务级别 == "副科"'}

    # 合同类型
    type_of_contracts = {'固定期限': '合同类型 =="固定期限"', '无固定期限': '合同类型 =="无固定期限"'}

    # 合同类别     分劳务派遣合同制  劳动合同制
    Contract_types = {'劳动合同制': '合同类别 =="劳动合同制"', '劳务派遣合同制': '合同类别 =="劳务派遣合同制"'}

    # 身份
    identitys = {'新人': '身份 =="“新人”"', '老人': '身份 =="“老人”"', '其他':'身份 =="其他"'}

    #用工形式
    Employment_forms ={'劳动合同':'用工形式 == "劳动合同"', '劳务派遣':'用工形式 == "劳务派遣"', '劳务合同':'用工形式 == "劳务合同"', '非全日制':'用工形式 == "非全日制"','季节工':'用工形式 == "季节工"'}


    st.markdown('# 全体人员统计表')
    st.markdown('#### 请选择显示项(数据来源：以集团eHR人事系统的导出excel为准) ')

    # 统计对象
    Statistical_objects = ['公司', '部门']
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        radio_list = hmc['人员类别'].value_counts().keys().tolist()
        my_radio = st.radio("①人员类别", radio_list, help="请注意在职需要再统计异地交流干部和精诚、异地任职在龙岩退休等情况", )
        if my_radio:
            data = data[data.人员类别 == my_radio]
    with c2:
        # 先显示公司勾选框
        company_checked = st.checkbox('公司', key='select_company')

        # 如果勾选了公司
        if company_checked:
            # 显示公司选择
            companys = data['所属公司'].value_counts().keys()
            selected_company = st.radio('请选择公司', companys, key='company_choice')

            if selected_company:
                # 应用公司筛选
                company_name = f'"{selected_company}"'
                data = hmc.query(f'所属公司 == {company_name}')

                # 只有选择了公司后，才显示部门勾选框
                department_checked = st.checkbox('部门', key='select_department')

                # 如果勾选了部门
                if department_checked:
                    # 显示部门选择
                    departments = data['部门'].value_counts().keys()
                    selected_department = st.radio('请选择部门', departments, key='department_choice')

                    if selected_department:
                        # 应用部门筛选
                        department_name = f'"{selected_department}"'
                        data = hmc.query(f'部门 == {department_name}'+'&' + f'所属公司 == {company_name}')
        # # 先显示所有统计对象的勾选框
        # selected_objects = []
        # for obj in Statistical_objects:
        #     if obj in TongJi_Item:
        #         continue
        #     if st.checkbox(obj, key=f'select_{obj}'):
        #         selected_objects.append(obj)
        #
        # # 根据选择的统计对象显示具体选项
        # for obj in selected_objects:
        #     st.markdown(f"**{obj}选择**")
        #     if obj == '公司':
        #         companys = data['所属公司'].value_counts().keys()
        #         company = st.radio('请选择公司', companys, key='company_choice')
        #         if company:
        #             company_name = f'"{company}"'
        #             data = hmc.query(f'所属公司 == {company_name}')
        #
        #     elif obj == '部门':
        #         departments = data['部门'].value_counts().keys()
        #         department = st.radio('请选择部门', departments, key='department_choice')
        #         if department:
        #             department_name = f'"{department}"'
        #             data = hmc.query(f'部门 == {department_name}')
        # # pass
        # for Statistical_object in Statistical_objects:
        #     if Statistical_object in TongJi_Item:
        #         continue
        #     if st.checkbox(Statistical_object, key =f'c2{Statistical_object}+{Statistical_object}'):
        #         if Statistical_object == '公司':
        #             companys =data['所属公司'].value_counts().keys()
        #             company = st.radio('请选择公司', companys)
        #             # st.write(Statistical_object)
        #             company_name = f'"{company}"'
        #             data = hmc.query(f'所属公司 == {company_name}')
        #         if Statistical_object == '部门':
        #             departments =data['部门'].value_counts().keys()
        #             department = st.radio('请选择部门', departments)
        #             # st.write(department)
        #             department_name = f'"{department}"'
        #             data = hmc.query(f'部门 == {department_name}')

                # if Statistical_object == '比照管理':
                #     departments = data['职务级别'].value_counts().keys()
                #     department = st.radio('请选择职务级别', departments)
                #     # st.write(department)
                #     department_name = f'"{department}"'
                #     data = hmc.query(f'职务级别 == {department_name}')


                    # for department in departments:
                    #     if st.checkbox(department, key=f'c2{Statistical_object}+{department}'):
                    #         department_name = f'"{department}"'
                    #         # st.write(department_name)
                    #         data = hmc.query(f'部门 == {department_name}')
                    #         # data

    with c3:
        age_range =st.radio('按各年龄段统计指标', age_ranges)
        # st.write(age_range)
        # st.write(age_groups[age_range])
        data = data.query(age_groups[age_range])
        # with st.expander("显示内容选择"):
        #     update_show_items(hmc.columns)
        # show_items = st.session_state.show_items
        # data[show_items]

    with c4:
        with st.expander("显示内容选择"):
            update_show_items(hmc.columns)
        show_items = st.session_state.show_items
        if len(show_items) > 0:
            data[show_items]



    dict_dataframe = {'人数': [data['人员类别'].count()]}
    dataframe_index = [f'{age_range}总人数']
    df = pd.DataFrame(dict_dataframe, index=dataframe_index)

    for checkbox_item in hmc.columns:
        if checkbox_item in TongJi_Item:
            if st.sidebar.checkbox(checkbox_item, key=f'{checkbox_item}'):
                if checkbox_item == '性别':
                    for gender in genders:
                        df[gender] = data.query(genders[gender])[checkbox_item].count()
                if checkbox_item == '民族':
                    for Nation in Nations:
                        df[Nation] = data.query(Nations[Nation])[checkbox_item].count()
                if checkbox_item == '年龄':
                    for age in age_groups.keys():
                        df[age] = data.query(age_groups[age])[checkbox_item].count()
                if checkbox_item == '政治面貌':
                    for ps in Political_Status.keys():
                        df[ps] = data.query(Political_Status[ps])[checkbox_item].count()
                if checkbox_item == '学历类型':
                    for education in educations.keys():
                        df[education] = data.query(educations[education])[checkbox_item].count()

                if checkbox_item == '学习形式':
                    for divided_time_full_or_part in divided_time_full_or_parts.keys():
                        df[divided_time_full_or_part] = data.query(divided_time_full_or_parts[divided_time_full_or_part])[checkbox_item].count()

                if checkbox_item == '取得专业技术职务等级':
                    for Professional_technical_level in Professional_technical_levels.keys():
                        df[Professional_technical_level] = \
                        data.query(Professional_technical_levels[Professional_technical_level])[
                            checkbox_item].count()

                if checkbox_item == '取得工人技术职务等级':
                    for Worker_technical_level in Worker_technical_levels.keys():
                        df[Worker_technical_level] = data.query(Worker_technical_levels[Worker_technical_level])[
                            checkbox_item].count()

                if checkbox_item == '职业资格':
                    for PVQE in PVQEs.keys():
                        df[PVQE] = data.query(PVQEs[PVQE])[
                            checkbox_item].count()

                if checkbox_item == '职务级别':
                    for job_level in job_levelS.keys():
                        df[job_level] = data.query(job_levelS[job_level])[
                            checkbox_item].count()

                if checkbox_item == '合同类型':
                    for type_of_contract in type_of_contracts.keys():
                        df[type_of_contract] = data.query(type_of_contracts[type_of_contract])[
                            checkbox_item].count()

                if checkbox_item == '合同类别':
                    for Contract_type in Contract_types.keys():
                        df[Contract_type] = data.query(Contract_types[Contract_type])[
                            checkbox_item].count()

                if checkbox_item == '身份':
                    for identity in identitys.keys():
                        df[identity] = data.query(identitys[identity])[
                            checkbox_item].count()

                if checkbox_item == '用工形式':
                    for Employment_form in Employment_forms.keys():
                        df[Employment_form] = data.query(Employment_forms[Employment_form])[
                            checkbox_item].count()
    df

    df.to_excel('output.xlsx', index=False)

    st.download_button(
        label='导出excel',
        data=open('output.xlsx', 'rb'),
        file_name=f'人员统计汇总表（{date.today()}）_导出{uploaded_file.name}',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
