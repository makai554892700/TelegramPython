# 安装相关工具
    pip3 install -r requirements.txt

# 错误解决方案
    * pip3 install -r requirements.txt时出现OSError: mysql_config not found错误

        yum install mysql-devel gcc gcc-devel python-devel -y

    * python3 manage.py db init 时出现 sqlite3.DatabaseError: malformed database schema (sent_files) - near "without": syntax error
        * 更新sqlite3到3.8+

            wget http://www.sqlite.org/snapshot/sqlite-snapshot-201804241859.tar.gz
            tar -zxvf sqlite-snapshot-201804241859.tar.gz
            cd sqlite-snapshot-201804241859
            ./configure
            make
            make install
            vim /etc/profile
                export LD_LIBRARY_PATH=/root/sqlite-snapshot-201804241859/.libs
            source /etc/profile

# 初始化

    # 安装mysql
    yum install mysql-server -y
    # 登录后创建telegram数据库
    create database telegram
    # 安装必要插件
    pip3 install -r requirements.txt
    # 初始化迁移文件
    python3 manage.py bd init
    # 将模型映射添加到文件中
    python3 manage.py db migrate
    # 将映射文件真正映射到数据库中
    python3 manage.py db upgrade

# 启动项目

    python3 manage.py runserver



