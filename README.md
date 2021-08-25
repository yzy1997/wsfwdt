# 网上服务大厅每日健康填报自动打卡程序使用指南
## 1.首先电脑中要安装python: [python](https://zhuanlan.zhihu.com/p/45608443)
## 2.接着要安装pip: [pip教程](https://jingyan.baidu.com/article/7c6fb428d84f9480642c90d1.html)
pip官网：[pip官网](https://pypi.org/project/pip/#files)
## 3.安装所需要的依赖包
(1) 进入cmd(Win+R键，输入cmd，回车)  
(2) 安装selenium: `pip install selenium`
## 4.配置chromedriver
(1) 打开chrome浏览器，地址栏输入`chrome://version/`，在第一行查看版本信息  
(2) 下载对应chrome版本的chromedriver: 
[chromedrvier下载](http://chromedriver.storage.googleapis.com/index.html)  
(3) 把chromedriver拷贝到chrome的安装文件夹下：
[chromedriver配置教程](https://blog.csdn.net/qq_40604853/article/details/81388078)
## 5.修改程序中的参数
### (1) 修改浏览器位置信息：
在程序第12行
 `"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222`
把引号中的位置改成你的chrome位置，一般对着桌面的chrome右键属性，就可以查看安装位置，改成这个位置就可以了  
### (2) 修改chromedriver位置信息
代码第41行，修改
`driver_path = r' C:\Program Files (x86)\Google\Chrome\Application\chromedrdriver.exe ' `和刚才类似修改成你的chromedriver位置就可以了, chromedriver和chrome放在同一目录下  
### (3) 修改邮箱配置信息
我用的是163邮箱，如果没有的话可以注册一个，也不难  
代码119行：`mail_user = 'xxx' `，xxx改成你的163邮箱用户名  
代码121行：`mail_pass = 'ABC'` ，ABC改成163邮箱授权码  
[163邮箱授权码](https://jingyan.baidu.com/article/e6c8503c3e01f6a44f1a18c5.html)  
**注意！！！授权码一定要记得保存，现在获取授权码好像要短信验证，而且只显示一次，记得要保存好（我们选的协议是SMTP，经验里给的是POP3，这个要注意勾选SMTP）**  
代码122行：`sender = 'xxx@163.com'`  # 发送邮箱的地址   
代码123行：`receivers = ['xxx@xx.com']`  # 接收邮箱的地址
### (4) 改名字
在代码154行：`name = '张三'`  # 这里填你的名字  
填了名字可以发邮件通知你哦
## 6.运行程序
说了这么多，赶紧看看效果吧:  
(1) ***首先关闭所有打开的chrome浏览器，否则可能运行不成功***
(2) 打开命令行（Win+R键，输入cmd，回车），把程序12行的代码（第5步修改过的代码）`"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222`   
**注意！！！不要#键和前面的空格，回车，就可以打开chrome**  
(3) 进入网上服务大厅，自己登陆一下：[网上服务大厅地址](https://eportal.uestc.edu.cn/new/index.html)  
(4) 保持浏览器别关（以后也别关，电脑也保持开机）  
(5) 运行python代码，如果你有任意一款python IDE，点击运行就可；
如果你没有python IDE，只需要在命令行敲入：
`python D:\xxx\wsfwdt.py` 也就是改成你的python文件路径就可以了
