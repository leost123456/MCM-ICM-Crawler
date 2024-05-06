import random
import requests
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
from pdf2image import convert_from_bytes
from plugin.pytesseract import pytesseract #用于OCR识别
from PIL import Image
import os
from loguru import logger
from matplotlib import rcParams

config = {"font.family":'Times New Roman'}  # 设置画图字体类型
rcParams.update(config)    #进行更新配置

#下面发送请求并将pdf文件转化为png图片格式
def request_data(url,image_path,proxy): #其中url是传入的url
    team_number = url.split('/')[-1].split('.')[0]  # 拿到队伍号
    # user_agent列表
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
    ]
    # refere
    # 先构造请求头
    User_Agent = random.choice(user_agent_list)  # 获取随机生成user_agent和referer用于伪装
    headers = {
        "User-Agent": User_Agent,
    }
    # 发送请求
    try:
        response = requests.get(url, headers=headers,proxies={'https':proxy,'http':proxy})  # 发送请求（注意这里的代理）
        team_number = url.split('/')[-1].split('.')[0]  # 拿到队伍号
        if not str(response.status_code).startswith('4'): #不是返回4开头的状态码
            # 下面进行将读取的二进制pdf数据存储为png图片格式
            image = convert_from_bytes(response.content)  # 将读取二进制数据并转化为图片
            # 进行读取pdf内容并保存到本地
            image[0].save(f'{image_path}\\{str(team_number)}.png', 'PNG')  # 将图片进行保存到对应的文件中（png格式，注意只有1页）
            image = Image.open(os.path.join(image_path, f'{team_number}.png'))  # 导入图像
            #logger.success('转化图片成功')
            return image
        else:
            logger.error(f'号码为{team_number}的队伍不存在')
            pass
    except Exception as e: #网页打不开
        logger.error(f'号码为{team_number}的队伍不存在',str(e))
        return None

#下面进行OCR识别并进行提取需要的数据
def extract_data(tessdata,image,team_number,detect_advisor,student_name_re,faculty_name_re,school_re,awards_re): #输入图像
    try:
        #进行OCR识别
        tessdata_dir_config = f'--tessdata-dir "{tessdata}"' #语言包地址（外部导入）
        text=pytesseract.image_to_string(image,config=tessdata_dir_config,lang='eng') #进行OCR识别（英语）
        #进行匹配
        if detect_advisor.findall(text): #如果是有advisor的
            student_name=list(filter(None,student_name_re.search(text).group(1).strip('\n').strip().split('\n'))) #列表形式,并过滤空字符串 学生
            faculty_name=faculty_name_re.search(text).group(1).strip('\n') #字符串形式 老师
            school = school_re.search(text).group(1).strip('\n')  # 字符串形式 学校
        else: #有些奖状错误（要重新匹配学生和老师、学校）
            # 匹配姓名
            name_re1 = re.compile(r'.*The Team [0|O]f(.*)[0|O]f.+Was Designated', re.I | re.S)
            name_list = list(filter(None, name_re1.search(text).group(1).strip('\n').strip().split('\n')))
            index=name_list.index('Of') if 'Of' in name_list else name_list.index('of') #查找of的序号
            student_name=name_list[:index-1]
            faculty_name=name_list[index-1]
            school=name_list[index+1]

        awards=awards_re.search(text).group(1).strip('\n').split(sep='\n')[0] #字符串形式

        #对学生列表确保长度为3（添加空白字符串）
        student_name+=['']*(3-len(student_name))

        #logger.success('OCR识别成功，数据提取成功')

        return student_name,faculty_name,school,awards
    except Exception as e:
        logger.error(f'队伍号为{team_number}的OCR识别和数据提取出错',str(e))
        pass

#进行保存数据到csv文件中
def save_data(Team_number_list,Team_members_1_list,Team_members_2_list,Team_members_3_list,Instructor_list,
              School_list,Awards_list):
    result_csv=pd.DataFrame()
    result_csv['Team number']=Team_number_list
    result_csv['Team members 1'] = Team_members_1_list
    result_csv['Team members 2'] = Team_members_2_list
    result_csv['Team members 3'] = Team_members_3_list
    result_csv['Instructor'] =Instructor_list
    result_csv['School'] = School_list
    result_csv['Awards'] = Awards_list
    result_csv.sort_values(by='Team number',inplace=True,ascending=True) #按队伍号升序
    result_csv.to_csv('result\\data.csv',index=None,encoding='utf-8')
    return result_csv

#进行数据分析出图(如果有数据可以单独调用)
def plot_data(result_csv):
    result_csv['School'] = result_csv['School'].str.upper()  # 全部变为大写
    # 奖项名称
    Awards_name = ['Not Judged', 'Disqualified - P', 'Unsuccessful - I', 'Successful Participant', 'Honorable Mention',
                   'Meritorious Winner', 'Finalist', 'Outstanding Winner']
    # 进行统计各奖项(降序)
    values_count = result_csv['Awards'].value_counts()  # 字典形式
    num_list = []
    for name in Awards_name:
        num_list.append(len(result_csv[result_csv['Awards'] == name]))

    # 1绘制奖状数量条形图
    height=0.25 #高度（每个条形之间）
    index=np.arange(len(num_list))      #特征类别个数
    plt.figure(figsize=(8, 6))
    plt.rcParams['axes.unicode_minus']=False #用来正常显示正负号
    plt.style.use('seaborn-whitegrid')
    plt.tick_params(size=5, labelsize=13)  # 坐标轴
    plt.barh(index,num_list,height=height,color='#F21855',alpha=1) #从下往上
    for i,data in enumerate(num_list):
        plt.text(data,index[i]-0.11,round(data,1),fontsize=13,family='Times New Roman')
    plt.yticks(index,Awards_name) #设置y轴的标签
    plt.xlabel('计数',fontsize=13,family='SimHei') #注意这个还是横轴的
    plt.ylabel('奖项',fontsize=13,family='Times New Roman') #竖轴的标签
    plt.title('美赛各奖项计数',fontsize=15,family='SimHei')
    plt.savefig(r'result/美赛各奖项计数条形图.svg',format='svg',bbox_inches='tight')
    plt.show()

    # 2绘制参赛学校数量的条形图（从高到底）
    school_count=result_csv['School'].value_counts()
    school_name=school_count.keys().tolist()[:15][::-1] #显示前15所学校
    school_num=list(school_count.values[:15])[::-1]
    height=0.4 #高度（每个条形之间）
    index=np.arange(len(school_num))      #特征类别个数
    plt.figure(figsize=(8, 6))
    plt.rcParams['axes.unicode_minus']=False
    plt.style.use('seaborn-whitegrid')
    plt.tick_params(size=5, labelsize=13)  # 坐标轴
    plt.barh(index,school_num,height=height,color='#bf0000',alpha=1) #从下往上
    for i,data in enumerate(school_num):
        plt.text(data,index[i]-0.17,round(data,1),fontsize=13,family='Times New Roman')
    plt.yticks(index,school_name) #设置y轴的标签
    plt.xlabel('计数',fontsize=13,family='SimHei') #注意这个还是横轴的
    plt.ylabel('学校名称',fontsize=13,family='SimHei') #竖轴的标签
    plt.title('美赛各参加学校参赛计数前十五名',fontsize=15,family='SimHei')
    plt.savefig(r'result/美赛各参加学校计数前十五名条形图.svg',format='svg',bbox_inches='tight')
    plt.show()

    # 3队伍不同参加人数的计数柱形图（1人，2人，3人）
    # 计算每队参赛队员人数
    result_csv.fillna(0, inplace=True)  # 填补缺失值用于统计
    result_csv['total number'] = result_csv['Team members 1'].apply(lambda x: 1 if x != 0 else 0) + \
                                 result_csv['Team members 2'].apply(lambda x: 1 if x != 0 else 0) + \
                                 result_csv['Team members 3'].apply(lambda x: 1 if x != 0 else 0)
    member_num = result_csv['total number'].value_counts(ascending=True).values[:] if len(result_csv['total number'].value_counts(ascending=True).values) == 3 else result_csv['total number'].value_counts(ascending=True).values[1:4]
    index = np.arange(3)  # 横轴的特征数，这里有三特征，用于绘制簇状柱形图
    feature_index = ['1', '2', '3']  # 横轴x的特征名称
    # 进行绘制
    plt.figure(figsize=(8, 6))
    plt.style.use('seaborn-whitegrid')
    plt.tick_params(size=5, labelsize=13)  # 坐标轴
    width = 0.6
    # 注意下面可以进行绘制误差线，如果是计算均值那种的簇状柱形图的话(注意类别多的话可以用循环的方式搞)
    plt.bar(index, member_num, width=width, alpha=0.4, color='#52D896')
    for i, data in enumerate(member_num):
        plt.text(index[i], data + 0.1, data, horizontalalignment='center', fontsize=13, family='Times New Roman')
    plt.xlabel('队伍人数', fontsize=13, family='SimHei')
    plt.ylabel('计数', fontsize=13, family='SimHei')
    plt.title('队伍中队员人数统计', fontsize=15, family='SimHei')
    plt.xticks(index, feature_index)
    plt.savefig(f'result\\队伍中队员人数统计.svg', format='svg', bbox_inches='tight')
    plt.show()

    # 各个学校获得奖项数量的排名（S、H、M、F、O）（5张图）
    # 奖项选择
    choose_award = ['Successful Participant', 'Honorable Mention', 'Meritorious Winner', 'Finalist',
                    'Outstanding Winner']
    # 颜色列表
    color_list = ['#fb9489', '#a9ddd4', '#9ec3db', '#cbc7de', '#fdfcc9']  # 颜色列表
    for i, award in enumerate(choose_award):
        school_count = result_csv[result_csv['Awards'] == award]['School'].value_counts()  # 选出对应奖项的数据
        print(school_count)
        school_name = school_count.keys().tolist()[:15][::-1]  # 显示数量最多前15所学校
        school_num = list(school_count.values[:15])[::-1]
        height = 0.4  # 高度（每个条形之间）
        index = np.arange(len(school_num))  # 特征类别个数
        plt.figure(figsize=(8, 6))
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示正负号
        plt.style.use('seaborn-whitegrid')
        plt.tick_params(size=5, labelsize=13)  # 坐标轴
        plt.barh(index, school_num, height=height, color=color_list[i], alpha=1)  # 从下往上
        for i, data in enumerate(school_num):
            plt.text(data, index[i] - 0.17, round(data, 1), fontsize=13, family='Times New Roman')
        plt.yticks(index, school_name)  # 设置y轴的标签
        plt.xlabel('计数', fontsize=13, family='SimHei')  # 注意这个还是横轴的
        plt.ylabel('学校名称', fontsize=13, family='SimHei')  # 竖轴的标签
        plt.title(f'获得{award}奖项最多前十五名学校名称', fontsize=15, family='SimHei')
        plt.savefig(f'result\\获得{award}奖项最多前十五名学校名称.svg', format='svg', bbox_inches='tight')
        plt.show()





