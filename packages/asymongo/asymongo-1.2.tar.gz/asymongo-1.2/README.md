# 项目描述

异步的 MongoDB ORM 。

# 安装与文档

安装：`pip install asymongo`

[文档](https://github.com/lcctoor/lccpy/blob/main/asymongo/docs/doc.md)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/lccpy/issues)、[微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg)、[技术交流群](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg) 与我联系。

# 关于作者

作者：许灿标

邮箱：lcctoor@outlook.com

[主页](https://github.com/lcctoor/me/blob/main/home.md) | [微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg) | [Python技术微信交流群](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg)

开源项目：[让 Python 更简单一点](https://github.com/lcctoor/lccpy#readme)

# 语法预览

导入：

```python
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import asymongo as mg
from asymongo import mc, mup
```

创建ORM:

```python
mkconn = lambda: MongoClient(host='localhost', port=27017)

orm = mg.ORM(mkconn=mkconn)  # 账户ORM
db = orm['泉州市']  # 库ORM
sheet = db['希望小学']  # 表ORM
```

新增数据:

```python
line1 = {'姓名': '小一', '年龄':11, '幸运数字':[1, 2, 3], '成绩':{'语文':81, '数学':82}}
line2 = {'姓名': '小二', '年龄':12, '幸运数字':[2, 3, 4], '成绩':{'语文':82, '数学':83}}
line3 = {'姓名': '小三', '年龄':13, '幸运数字':[3, 4, 5], '成绩':{'语文':83, '数学':84}}
line4 = {'姓名': '小四', '年龄':14, '幸运数字':[4, 5, 6], '成绩':{'语文':84, '数学':85}}
line5 = {'姓名': '小五', '年龄':15, '幸运数字':[5, 6, 7], '成绩':{'语文':85, '数学':86}}
line6 = {'姓名': '小六', '年龄':16, '幸运数字':[6, 7, 8], '成绩':{'语文':86, '数学':87}}

await sheet.insert(line1)  # 单条添加
await sheet.insert([ line2, line3, line4, line5, line6 ])  # 批量添加
```

查询示例:

```python
await sheet[:]  # 查询所有数据

await sheet[3]  # 查询第3条数据

await sheet[mc.成绩.语文 == 85][:]  # 查询语文成绩为85分的数据

await sheet[mc.年龄>13][mc.姓名=='小五'][1]  # 查询年龄大于13、且姓名叫'小五'的第1条数据
```

修改示例:

```python
data = {
    '视力': 5.0,
    '性别': '男',
    '爱好': ['足球','篮球','画画','跳绳'],
    '幸运数字': mup.push(15,16,17),  # 添加到列表
    '年龄': mup.inc(2)  # 自增
}

await sheet.update(data)[2:5]
```

删除示例:

```python
# 删除年龄>=15的数据
await sheet[mc.年龄>=15].delete()[:]

# 删除年龄大于10、且姓名包含'小'的第2条数据
await sheet[mc.年龄>10][mc.姓名 == mg.re('小')].delete()[2]

# 删除所有数据
await sheet.delete()[:]
```

成员运算:

| **代码**                           | **解释**                          |
| ---------------------------------------- | --------------------------------------- |
| mc.年级 == mg.isin('初三', '高二')       | 若字段值是传入值的成员，则符合          |
| mc.年龄 == mg.notin(10, 30, 45)          | 若字段值不是传入值的成员，则符合        |
| mc.爱好 == mg.containAll('画画', '足球') | 若字段值包含传入值的所有元素，则符合    |
| mc.爱好 == mg.containAny('画画', '足球') | 若字段值包含传入值的至少1个元素，则符合 |
| mc.爱好 == mg.containNo('画画', '足球')  | 若字段值不包含传入值的任何元素，则符合  |

正则运算:

| **代码**         |
| ---------------------- |
| mc.姓名 == mg.re('小') |

过滤器之间的集合运算:

| **代码**                                                                  | **解释** |
| ------------------------------------------------------------------------------- | -------------- |
| [ mc.年龄>3 ][ mc.年龄<100 ]                                                    | 交集           |
| [ (mc.年龄==30)&#124; (mc.年龄>30) &#124; (mc.年龄<30) &#124; (mc.年龄==None) ] | 并集           |
| [ (mc.年龄>3) - (mc.年龄>100) ]                                                 | 差集           |
| [ ~(mc.年龄>100) ]                                                              | 补集           |

限定返回字段:

只返回姓名、年龄这2个字段：

```python
await sheet[mc.年龄>11][mc.年龄<30]['姓名','年龄'][:]
```

特殊操作:

| **语法**   | **含义**                                     |
| ---------------- | -------------------------------------------------- |
| mup.inc(1)       | 自增1                                              |
| mup.inc(-1)      | 自减1                                              |
| mup.add(1, 2, 3) | 向列表字段添加元素，仅当被添加的元素不存在时才添加 |
| ...              | ...                                                |

统计:

| **项目**            | **语法**                 |
| ------------------------- | ------------------------------ |
| 某张表的数据总量          | await sheet.len( )             |
| 某张表中，年龄>10的数据量 | await sheet[mc.年龄>10].len( ) |
| 库的数量                  | await orm.len( )               |
| ...                       | ...                            |
