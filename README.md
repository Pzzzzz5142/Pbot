![Pbot](https://socialify.git.ci/Pzzzzz5142/Pbot/image?description=1&font=Source%20Code%20Pro&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FPzzzzz5142%2FPbot%2Fmaster%2FPbot%2Favatar.JPG&owner=1&pattern=Signal&stargazers=1&theme=Light&forks=1)

# Pbot

一个相对不那么xjb写的，并基于Nonebot2的QQ🤖。

功能很杂，代码风格很要命。

试用 QQ 群：1037557679

## 功能概览

> 蓝色字体的功能表示有使用帮助！点击它即可跳转！

+ [**搜图**](https://github.com/Pzzzzz5142/Pbot/wiki/功能使用帮助#st) - st：包括以图搜图及关键字搜图。
+ [**机器翻译**](https://github.com/Pzzzzz5142/Pbot/wiki/功能使用帮助#wm) - wm
+ **Rss订阅及查看** - rss
+ [**点歌**](https://github.com/Pzzzzz5142/Pbot/wiki/功能使用帮助#点歌) - 点歌
+ **戳一戳**
+ **切噜一下** - 切噜一下 | 切噜～♪ ：（抄自[Hoshino](https://github.com/Ice-Cirno/HoshinoBot)
+ **根据 P 站 id 看原图** - cat
+ **复读**
+ **每日早上好**
+ [**今日人品**](https://github.com/Pzzzzz5142/Pbot/wiki/功能使用帮助#jrrp) - jrrp
+ **能不能好好说话** - hhsh

## RoadMap

| 版本   | 发布时间或 Milestone 截至时间            | Key Feature               |
| ------ | ---------------------------------------- | ------------------------- |
| v0.1.0 | 2020-11-24                               | 老 Bot 的关键功能迁移完成 |
| v0.2.0 | 2021-5-27                                | 老 Bot 迁移完成           |
| v0.3.0 | 估                                       | 配置方式优化              |
| v0.4.0 | 沽                                       | 可迁移部署及文档完善      |
| ？     | 咕咕咕                                   | 没想好                    |
| ---    | （可能永远无法完成（真的不大可能有（（（ | web UI                    |

> 现在 wiki 还在 Working 中。（毕竟我太摸了）

## 安装

### 安装 Pbot 本体

安装的步骤主要是装依赖、装收消息的东西（mirai之类的，推荐用go-cqhttp），然后就可以跑了。

#### 安装收消息的东西

现在收消息的东西很多，mirai、mirai-ok、go-cqhttp等等。因为 go-cqhttp 非常傻瓜无脑，一键安装，所以我就用的是他了。

#### 安装依赖

由于 nonebot2 本身就是使用poetry管理环境，因此这里也同样使用 poetry 管理环境。

+ `clone` 本仓库并切到该文件夹：

    `git clone https://github.com/Pzzzzz5142/Pbot.git && cd Pbot`

+ 安装 poetry

    你喜欢怎么装就怎么装

+ 安装依赖：

    `poetry install`

    如果是国内的服务器，安装的时候可能速度比较慢。而 poetry 本质上还是依赖于 pip 进行安装，所以给 pip 换上国内源就可以加速了。
    
#### （~~可选~~必选！）安装数据库

由于本 bot 使用的是一个异步框架，同时由于 sqlite 本身不支持异步的操作（~~或者说我没找到~~）。因此涉及到持久化的功能都使用到了 postgreSQL 数据库。

使用到数据库的功能包括：`rss`记录推送及订阅信息、`功能开关`和`今日人品`。

如果你想使用上述功能，则**必须**安装 postgreSQL 和 alembic。其中 alembic 用于数据库的迁移。

~~当然如果你觉得这部分比较复杂或者不需要上述三个功能，则可以无视掉这一步。~~（由于技术力，不够pro这个是必要的！

+ 安装 postgreSQL 和 alembic

    你想怎么装就怎么装

+ 安装数据库相关的依赖

    `poetry install -E [db]`

+ 迁移数据库

    详见[配置](##配置)一节。（yysy，没写完）
    
#### 安装 RSSHub

同样的，本 bot 所使用的诸如 rss 订阅等功能都是依赖于 RSSHub 完成的。由于docker实在是太方便了，因此本 bot 建议的安装方式为使用 docker 安装，其他安装方式详见[这里](https://docs.rsshub.app/install/#docker-jing-xiang)（需翻墙）。

+ 安装 RSSHub

    `docker pull diygod/rsshub`

+ 运行它！

    `docker run -d --name rsshub -p 1200:1200 diygod/rsshub`

*Working 中*

## 配置

~~（这里要写的好多啊淦）~~

*Working 中*
