# koko 日语发音学习小程序 后端

## 说明

### 1. 版本与平台
    Django: 4.1
    pyhton: 3.9
    mysqlclient: 2.2.0
    mysql: 8.2.0

平台为Win10平台

### 2. 目前实现与未完成

已经实现Django后端对应的数据库的建立，以及从数据库中读取数据的功能。

尚未实现：和微信小程序前端页面的请求通道建立，没有测试向数据库中写入数据的功能，对于表中的数据进行查找的方式尚待研究。

以及如何快速高效的部署数据库和Django框架，（nigx？？？）

### 3. 説明

在koko/settings.py中，数据库名称为test，使用用户为root，密码为""。（？？？）

数据库的建立：app文件夹下的models.py中每一个类决定了数据库中的一个表。
models详见 <a>https://blog.csdn.net/happygjcd/article/details/102649947

关于Mysql：如果你真的想本机跑（），请安装对应版本的MySql之后创建test数据库，然后在backend文件夹下运行如下代码：

    python manage.py makemigrations
    python manage.py migrate

会在app/migrations中出现0001_initial.py，算是数据库建立成功。
