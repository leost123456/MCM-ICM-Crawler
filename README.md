# :bug:**2024年美赛成绩爬虫和可视化分析**

:arrow_heading_down:**你可以通过以下两种方式运行本程序**

 #### :golf:**1.一键运行安装包**

1. 去release中解压MCM-ICM-Crawler文件，其中已经帮你配置好tesseract目录中的**tesseract.exe文件和**和**tessdata语言包**，你只需要更改config.yaml文件中的比赛年份、爬取序号范围、线程数、代理IP。
2. 进入终端输入指令 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt安装依赖。
3. 输入指令python run.py即可运行程序。

#### :computer:**2.源码运行**

需要python版本>=3.8

1. git clone https://github.com/leost123456/MCM-ICM-Crawler.git 到本地仓库，或者直接下载源码。
2. 下载tesseract和其语言包，windows用户可去[**链接**](https://digi.bib.uni-mannheim.de/tesseract/)进行下载，并完成安装。
3. 完成安装后，在config.yaml文件中填写tesseract目录中的**tesseract.exe文件的路径**、**tessdata语言包**的路径、比赛年份、爬取序号范围、线程数、代理IP。
4. 在终端中输入指令 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt安装依赖。
5. 最后输入指令python run.py 程序即可运行。

#### :o:**3.输出结果**

1. 所有成绩奖状图片（将存放在result目录下的Award picture目录中）
2. 文件数据（包括队伍号、队员名称、指导老师名称、学校、奖项，存放在result目录下的data.csv文件中）
3. 可视化图片（8张分析图片）

---

### :black_flag:**结果展示**

**最终一共获得了28480条数据，可视化如下所示：**

**1.美赛各奖项计数情况**

[![image.png](https://i.postimg.cc/GmLkWBzt/image.png)](https://postimg.cc/56rYv2hW)

**2.美赛各参加学校计数前十五名**

[![image.png](https://i.postimg.cc/cLvJt0LT/image.png)](https://postimg.cc/4YTGrCth)

**3.获得Successful Participant奖项最多前十五名学校名称**

[![Successful-Participant.png](https://i.postimg.cc/P53xY5p7/Successful-Participant.png)](https://postimg.cc/RWt4z9T1)

**4.获得Honorable Mention奖项最多前十五名学校名称**

[![Honorable-Mention.png](https://i.postimg.cc/0j05Qk1c/Honorable-Mention.png)](https://postimg.cc/ct6GkNHn)

5**.获得Meritorious Winner奖项最多前十五名学校名称**

[![Meritorious-Winner.png](https://i.postimg.cc/2515wNnS/Meritorious-Winner.png)](https://postimg.cc/TyXGdSkz)

6.**获得Finalist奖项最多前十五名学校名称**

[![Finalist.png](https://i.postimg.cc/2S8y1Z6v/Finalist.png)](https://postimg.cc/8j9N3sLP)

**7.获得Outstanding Winner奖项最多前十五名学校名称**

[![Outstanding-Winner.png](https://i.postimg.cc/D0TynWHS/Outstanding-Winner.png)](https://postimg.cc/VrKcFNYw)

---

### :key:**免责声明**

**本项目仅供学习参考，如用于其他违法行为，后果自负，本人概不负责。**