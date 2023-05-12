# :bug:**2023年美赛成绩爬虫和可视化分析**

:arrow_heading_down:**你可以通过以下两种方式运行本程序**

 #### :golf:**1.一键运行安装包**

1. 去release中解压MCM-ICM-Crawler文件，其中已经帮你配置好tesseract目录中的**tesseract.exe文件和****tessdata语言包**，你只需要更改config.yaml文件中的线程数和爬取数量。
2. 进入终端输入指令 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt安装依赖。
3. 输入指令python run.py即可运行程序。

#### :computer:**2.源码运行**

需要python版本>=3.8

1. git clone https://github.com/leost123456/MCM-ICM-Crawler.git到本地仓库，或者直接下载源码。
2. 下载tesseract和其语言包，windows用户可去[链接](**https://digi.bib.uni-mannheim.de/tesseract/)**进行下载，并完成安装。
3. 完成安装后，在config.yaml文件中填写tesseract目录中的**tesseract.exe文件的路径**、**tessdata语言包**的路径、线程数和爬取数量。
4. 在终端中输入指令 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt安装依赖。
5. 最后输入指令python run.py 程序即可运行。

---

### :black_flag:**结果展示**

**最终一共获得了20615条数据，可视化如下所示：**

**1美赛各奖项计数情况**

[![image.png](https://i.postimg.cc/VNfPFCpV/image.png)](https://postimg.cc/gxT7znYV)

**2美赛各参加学校计数前十五名**

[![image.png](https://i.postimg.cc/yNKsbNpw/image.png)](https://postimg.cc/210sqCDw)

**3获得Successful Participant奖项最多前十五名学校名称

[![Successful-Participant.png](https://i.postimg.cc/vHhb1yPy/Successful-Participant.png)](https://postimg.cc/JGs9gfVY)

**4获得Honorable Mention奖项最多前十五名学校名称**

[![Honorable-Mention.png](https://i.postimg.cc/1RTDkx09/Honorable-Mention.png)](https://postimg.cc/dD27CxSX)

5**获得Meritorious Winner奖项最多前十五名学校名称**

[![Meritorious-Winner.png](https://i.postimg.cc/vTRf6fZ4/Meritorious-Winner.png)](https://postimg.cc/CBNz3ZD0)

6**获得Finalist奖项最多前十五名学校名称**

[![Finalist.png](https://i.postimg.cc/ydnCDXPP/Finalist.png)](https://postimg.cc/jwWF9fBw)

**获得Outstanding Winner奖项最多前十五名学校名称**

[![Outstanding-Winner.png](https://i.postimg.cc/RV62mzjG/Outstanding-Winner.png)](https://postimg.cc/TpxtjB2W)

---

### :key:**免责声明**

**本项目仅供学习参考，如用于其他违法行为，后果自负，本人概不负责。**



