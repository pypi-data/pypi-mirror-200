# 项目描述

根据openai官方接口‘openai’改造的‘openai2’，比官方接口更好用一点。

# 安装

安装：`pip install openai2`

# 获取api_key

[获取链接1](https://platform.openai.com/account/api-keys)

[获取链接2](https://www.baidu.com/s?wd=%E8%8E%B7%E5%8F%96%20openai%20api_key)

# 文档

导入：

```python
from openai2 import Chat
```

创建会话：

```python
api_key = 'api_key'  # 更换成自己的api_key

talk_1 = Chat(api_key=api_key, model="gpt-3.5-turbo")
talk_2 = Chat(api_key=api_key, model="gpt-3.5-turbo")
```

对话：

```python
talk_1.request('数字1的后面是几?')
# >>> 2

talk_2.request('数字101的后面是几?')
# >>> 102

talk_1.request('再往后是几?')
# >>> 3

talk_2.request('再往后是几?')
# >>> 103
```

存档：

```python
talk_1.dump('./talk_record.json')
```

载入存档：

```python
new_talk = Chat(api_key=api_key, model="gpt-3.5-turbo")
new_talk.load('./talk_record.json')
new_talk.request('再往后呢?')
# >>> 4
```

对话回滚：

```python
talk_4 = Chat(api_key=api_key, model="gpt-3.5-turbo")

talk_4.request('数字1的后面是几?')
# >>> 2

talk_4.request('再往后是几?')
# >>> 3

talk_4.request('再往后呢?')
# >>> 4

# 回滚
talk_4.rollback()
# >>> [user]: 再往后是几?
# >>> [assistant]: 3

# 再回滚
talk_4.rollback()
# >>> [user]: 数字1的后面是几?
# >>> [assistant]: 2

talk_4.request('再往后是几?')
# >>> 3
```

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/lccpy/issues)、[微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg)、[技术交流群](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg) 与我联系。

# 关于作者

作者：许灿标

邮箱：lcctoor@outlook.com

[主页](https://github.com/lcctoor/me/blob/main/home.md) | [微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg) | [Python技术微信交流群](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg)

开源项目：[让 Python 更简单一点](https://github.com/lcctoor/lccpy#readme) | [史上最优雅的 mysql ORM](https://github.com/lcctoor/lccpy/blob/main/coolmysql/docs/doc_zh.md)