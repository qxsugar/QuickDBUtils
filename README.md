快速使用DBUtils开发python mysql程序
================================

### 描述
> 大部分时间我们使用py+mysql时候都是简单操作。
> 
> 现在的库都要自己处理异常。维护链接
> 
> 所以基于DBUtils封装一下。把日常操作mysql的封装起来
>
> 只需要定义好db. 然后query, exec_sql就好
>
> 这样就可以快速开发py脚本了

### setup
> pip install git+https://github.com/qxsugar/QuickDBUtils.git

### 使用
```python
import pymysql
from pymysql.cursors import DictCursor
from QuickDBUtils import SimplePolledDB, SqlTools
db = SimplePolledDB(pymysql, host='xx.xx.xx.xx', user='xxx', password='xxx')
db = SimplePolledDB(pymysql, host='xx.xx.xx.xx', user='xxx', password='xxx', cursorclass=DictCursor)

sql = """
    select
        xxx
    from
        xxx
"""
sql = SqlTools.normalize_sql(sql=sql)

db.query("show databases")
db.query("show databases", cursor=DictCursor)
db.fetchall("show databases")
db.fetchone("show databases")
db.exec_sql("insert into xxx values xxx")
```
