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

尚未实现：和微信小程序前端页面的请求通道建立，对于表中的数据进行查找的方式尚待研究。

以及如何快速高效的部署数据库和Django框架，（ngix？？？）

### 3. 运行方式

#### （1）下载conda，使用conda构建环境：

    conda init
    conda create -n your_env_name python=3.9
    conda activate your_env_name

执行 ``conda info`` ， 显示 ``active environment : koko``  即为成功。

#### （2）配置

在backend文件夹下，执行：

    pip install -r requirements.txt

#### （3）Mysql数据库

安装8.2.0的Mysql数据库，注册root用户且修改密码或settings.py使用户登陆时密码匹配。运行Mysql并建立test数据库。

#### （4）数据库合并

在backend文件夹下，执行：

    python manage.py makemigrations
    python manage.py migrate

会在app/migrations中出现0001_initial.py，算是数据库建立成功。

前往http://127.0.0.1:8000/，看到 ``Hello, world! get content: Add information``成功。

### 4. 説明

在koko/settings.py中，数据库名称为test，使用用户为root，密码为""。所以你的数据库用户和密码要和配置文件中匹配。

数据库的建立：app文件夹下的models.py中每一个类决定了数据库中的一个表。
models详见 <a>https://blog.csdn.net/happygjcd/article/details/102649947

建立数据库时，应该在app/migrations下看到0001_initial.py，如果没有，请执行：

    python manage.py makemigrations app

然后再执行

    python manage.py migrate
