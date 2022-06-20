doc = """
## 安装 Redis

拉取镜像：

```bash
docker pull redis
```

准备 redis 配置文件，先从 redis 官网下载一个 redis 配置文件

```bash
wget http://download.redis.io/redis-stable/redis.conf
```

修改 redis 配置文件：

```bash
bind 127.0.0.1 # 注释掉这部分，使redis可以外部访问
daemonize no # 用守护线程的方式启动
requirepass 你的密码 # 给redis设置密码
appendonly yes # redis持久化　　默认是no
tcp-keepalive 300 # 防止出现远程主机强迫关闭了一个现有的连接的错误 默认是300
logfile "/data/redis.log" # 存放日志文件
dir /data # 存放持久化文件
```

接下来创建本地与 docker 映射的目录，即本地存放目录，将配置文件拷贝到该目录。

```bash
sudo mkdir /usr/local/docker/redis
sudo mkdir /usr/local/docker/redis/data
sudo mv /tmp/redis.conf /usr/local/docker/redis
sudo touch /usr/local/docker/redis/data/redis.log # 日志文件
```

启动

```bash
docker run -itd -p 6379:6379 --name redis -v /usr/local/docker/redis/redis.conf:/etc/redis/redis.conf -v /usr/local/docker/redis/data:/data redis redis-server /etc/redis/redis.conf
```



## 安装 Elasticsearch

拉取指定版本的镜像：

```bash
docker pull elasticsearch:7.1
```

运行：

```bash
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms64m -Xmx256m" --name es elasticsearch:7.6.2
```



## 安装 RabbitMQ

拉取镜像

```bash
docker pull rabbitmq
```

运行

```bash
docker run -itd --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq
```



## 安装 MongoDB

拉取镜像：

```
docker pull mongo
```

运行：

```bash
docker run -d -p 27017:27017 -v /usr/local/docker/mconfigdb:/data/configdb -v /usr/local/docker/mongo/db:/data/db --name mongo mongo
```

如果要以认证模式运行，在最后加上 ` --auth`。运行，进入容器：

```bash
docker exec -it mongo mongo admin
```

创建用户名和密码：

```bash
db.createUser({ user: 'mongo', pwd: '123456', roles: [{ role: "userAdminAnyDatabase", db: "admin" }]});
```



## 安装 MySQL

拉取镜像：

```bash
docker pull mysql
```

新建需要映射的目录，运行：

```bash
docker run -p 3306:3306 --name mysql \
-v /usr/local/docker/mysql/conf:/etc/mysql \
-v /usr/local/docker/mysql/logs:/var/log/mysql \
-v /usr/local/docker/mysql/data:/var/lib/mysql-files \
-e MYSQL_ROOT_PASSWORD=123456 \
-id mysql
```



"""


import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        except Exception:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)

def MarkdownConvertToHtmlWithMistune(content: str):
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(content)

print(MarkdownConvertToHtmlWithMistune(doc))