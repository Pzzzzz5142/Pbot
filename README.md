![Pbot](https://socialify.git.ci/Pzzzzz5142/Pbot/image?description=1&font=Source%20Code%20Pro&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FPzzzzz5142%2FPbot%2Fmaster%2FPbot%2Favatar.JPG&owner=1&pattern=Signal&stargazers=1&theme=Light)

# Pbot

一个相对不那么xjb写的，并基于Nonebot2的QQ🤖。

功能很杂，代码风格很要命。

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

| 版本   | 发布时间或 Milestone 截至时间            | Key Feature             |
| ------ | ---------------------------------------- | ----------------------- |
| v0.1.0 | 2020-11-24                               | 老Bot的关键功能迁移完成 |
| v0.2.0 | 咕                                       | 老Bot的全部功能迁移完成 |
| v0.3.0 | 估                                       | 配置方式优化            |
| v0.4.0 | 沽                                       | 可迁移部署及文档完善    |
| ？     | 咕咕咕                                   | 没想好                  |
| ---    | （可能永远无法完成（真的不大可能有（（（ | web UI                  |

> 现在 wiki 还在 Working 中。可以先看 [这里](https://github.com/Pzzzzz5142/xjbx-QQ-group-bot) 了解老 bot 的相关功能介绍！（毕竟正在迁移到 Nonebot2 ）

## 安装

### 安装 Pbot 本体

*Working 中*

### 安装数据库

由于本 bot 使用的是一个异步框架，同时由于 sqlite 本身不支持异步的操作（~~或者说我没找到~~）。因此涉及到持久化的功能都使用到了 postgreSQL 数据库。

使用到数据库的功能包括：`rss`记录推送及订阅信息、`功能开关`和`今日人品`。

如果你想使用上述功能，则**必须**安装 postgreSQL 和 alembic。其中 alembic 用于数据库的迁移。

当然如果你觉得这部分比较复杂或者不需要上述三个功能，这可以无视掉这一步。

*Working 中*

## 配置

*Working 中*