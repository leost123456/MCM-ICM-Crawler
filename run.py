import re
import threading #用于多线程操作
import queue
import os
from loguru import logger
from Universal import request_data,extract_data,save_data,plot_data
import yaml

#主运行函数
def main():
    while not q.empty(): #队列不为空
        url_index=q.get() #拿到序号

        if (url_index+1)%1000 ==0: #每进行1000轮保存一次数据
            save_data(Team_number_list,Team_members_1_list,Team_members_2_list,Team_members_3_list,Instructor_list,
              School_list,Awards_list)

        url=base_url+str(url_index)+'.pdf' #构造url

        #发送请求并转化成图片
        image=request_data(url,image_path)

        #OCR识别并进行数据提取
        if image != None : #如果可以正确读取数据
            try:
                student_name,faculty_name,school,awards=extract_data(tessdata,image,url_index,detect_advisor,student_name_re,faculty_name_re,school_re,awards_re)
            except Exception as e:
                continue
            #下面进行申请获取锁(防止多线程写入混乱)
            muti_lock.acquire()

            #存入列表（队伍号、队员1、队员2、队员3、指导教师、学校、奖项）
            Team_number_list.append(url_index)
            Team_members_1_list.append(student_name[0])
            Team_members_2_list.append(student_name[1])
            Team_members_3_list.append(student_name[2])
            Instructor_list.append(faculty_name)
            School_list.append(school)
            Awards_list.append(awards)

            #释放锁
            muti_lock.release()
            logger.success(f'成功提取号码为{url_index}的数据')
        else:
            continue

if __name__ == '__main__':
    # 导入poppler到系统变量中(用户变量)
    # 获取当前系统变量
    env = os.environ
    # 导入
    if 'PATH' in env:
        env['PATH'] += f";{os.path.abspath('.')}\\plugin\\poppler-0.68.0\\bin"
    else:
        env['PATH'] = f"{os.path.abspath('.')}\\plugin\\poppler-0.68.0\\bin"
    # 更新(注意只会注入其中一次，运行完毕后删除)
    os.environ = env

    # 创建存储目录
    os.makedirs('result', exist_ok=True) #存储图片、数据和数据分析结果
    os.makedirs('result\\Award Picture',exist_ok=True) #存储奖状图片
    image_path='result\\Award Picture' #存储图片的地址
    base_url=r'https://www.comap-math.com/mcm/2023Certs/' #基础url

    #下面进行读取配置文件
    logger.info('正在读取配置文件')
    try:
        with open('config.yaml','r',encoding='utf-8') as f:
            config=yaml.safe_load(f)
            n=config['n'] #总共爬取的队伍数量（设置较大的一个数）
            n_thread=config['n_thread'] #线程数量
        try:
            tessdata=config['tessdata'] #语言包路径
        except:
            logger.error('tessdata语言包路径有误')
            exit()
        logger.success('成功读取配置文件，开始进行爬取')
    except Exception as e:
        logger.error('配置文件有误，请检查')
        exit()
    # 下面设置正则表达式用于文本匹配
    detect_advisor = re.compile(r'.*With.*[Student|Faculty].*Advisor.*', re.I | re.S ) #检测文本是否正确
    # 1进行匹配学生姓名
    student_name_re = re.compile(r'.*The Team [0|O]f(.*)With [Student|Faculty]', re.I | re.S)
    # 2进行匹配老师姓名
    faculty_name_re = re.compile(r'.*With.*Advisor(.+?)[0|O]f.*Was Designated',re.I | re.S)
    # 3进行匹配学校
    school_re = re.compile(r'With.*Advisor.*[0|O]f\n(.+?)Was Designated As.*',re.I | re.S | re.DOTALL)
    # 4进行匹配奖项
    awards_re = re.compile(r'Was Designated As(.*)\n+.+',re.I | re.S | re.DOTALL)
    #创建队列
    q=queue.Queue(maxsize=n)
    #将url数据存入队列中
    for i in range(n):
        q.put(2300000+i)

    # 下面创建一个线程锁对象，防止多线程存入结果中发生错乱（通过后续调用acquire和release方法来使用）,全局变量用于main()
    muti_lock = threading.Lock()

    # 创建存储列表
    Team_number_list=[] #存储队伍号
    Team_members_1_list=[] #队员1
    Team_members_2_list = [] #队员2
    Team_members_3_list = [] #队员3
    Instructor_list=[] #指导老师
    School_list=[] #学校
    Awards_list=[] #奖项

    # 下面进行创建多线程操作
    thread = []  # 存储所有线程对象
    for i in range(n_thread):  # 50个线程
        t = threading.Thread(target=main, name='LoopThread' + str(i + 1))  # 其中target就是每个线程运行的程序，name就是标记下名字
        t.start()
        thread.append(t)

    #下面设置等待所有进行结束再运行下一步
    for t in thread:
        t.join()

    #进行最后一次存储数据
    result_csv=save_data(Team_number_list,Team_members_1_list,Team_members_2_list,Team_members_3_list,Instructor_list,
              School_list,Awards_list)
    logger.success(f'已完成所有数据的爬取，总共爬取到{len(result_csv)}份有效数据，文字信息数据已保存在result/data.csv中，奖状图片已保存在result/Award Picture文件夹下')
    logger.info('下面进行数据可视化分析')
    plot_data(result_csv)
    logger.success('已完成所有数据可视化分析，结果图片保存在result文件夹下')





















