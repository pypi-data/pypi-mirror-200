# Project description

The most elegant mysql ORM in history.

# Installation and documentation

Install：`pip install coolmysql`

[Documentation](https://github.com/lcctoor/lccpy/blob/main/coolmysql/docs/doc.md)

[中文文档](https://github.com/lcctoor/lccpy/blob/main/coolmysql/docs/doc_zh.md)

# Bug submission and feature proposal

You can contact me through [Github-Issues](https://github.com/lcctoor/lccpy/issues), [WeChat](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg), [Technology exchange group on WeChat](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg) .

# About the author

Author：许灿标

Email：lcctoor@outlook.com

[Home Page](https://github.com/lcctoor/me/blob/main/home.md) | [WeChat](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg) | [Python technology exchange group on WeChat](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg)

Open source projects：[Make Python simpler](https://github.com/lcctoor/lccpy#readme)

# Syntax Preview

Import：

```python
from pymysql import connect
from coolmysql import ORM, mc, mf
```

Create an ORM:

```python
def mkconn():
    return connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = '123456789'
    )

orm = ORM(mkconn=mkconn)  # account ORM
db = orm['city']  # db ORM
sheet = db['school']  # sheet ORM
```

Add data:

```python
line1 = {'name': 'tony 1', 'age':11, 'report_date':'2023-01-11'}
line2 = {'name': 'tony 2', 'age':12, 'report_date':'2023-01-12'}
line3 = {'name': 'tony 3', 'age':13, 'report_date':'2023-01-13'}
line4 = {'name': 'tony 4', 'age':14, 'report_date':'2023-01-14'}
line5 = {'name': 'tony 5', 'age':15, 'report_date':'2023-01-15'}
line6 = {'name': 'tony 6', 'age':16, 'report_date':'2023-01-16'}

r1 = sheet + line1  # Add a row of data
r2 = sheet + [line2, line3, line4, line5, line6]  # Add multiple rows of data
```

Query example:

```python
sheet[:]  # Query all data

sheet[3]  # Query Article 3 data

sheet[mc.age>13][mc.name=='tony 5'][1]  # Query the first data with the age greater than 13 and the name 'tony 5'
```

Modify Example:

```python
sheet[mc.age>10][2:5] = {
    'vision': 5.0,
    'gender': 'male',
    'like': 'football, basketball, painting, rope skipping'
}
```

Delete example:

```python
# Delete all data with age>=15
sheet[mc.age>=15][:] = None

# Delete the second data that is older than 10 and likes football
sheet[mc.age>10][mc.like.re('football')][2] = None

# Delete all data
sheet[:] = None
```

Slice example:

```python
sheet[filter]...[filter][:]  # Query all qualified data
sheet[filter]...[filter][:] = None  # Delete all eligible data
sheet[filter]...[filter][:] = {'grade':'junior 1'}  # Modify all eligible data

sheet[filter]...[filter][1]  # Query the first eligible item
sheet[filter]...[filter][1] = None  # Delete the eligible Article 1
sheet[filter]...[filter][1] = {'grade':'junior 1'}  # Modify Article 1 that meets the conditions

sheet[filter]...[filter][3:7]  # Query eligible items 3 to 7
sheet[filter]...[filter][3:7] = None  # Delete articles 3 to 7 that meet the conditions
sheet[filter]...[filter][3:7] = {'grade':'junior 1'}  # Modify articles 3 to 7 that meet the conditions
```

Filter：

| **Code** |
| -------------- |
| mc.age > 10    |
| mc.age >= 10   |
| mc.age < 10    |
| ...            |

| **Code**                       | **Explanation**                                             |
| ------------------------------------ | ----------------------------------------------------------------- |
| mc.grade.isin('grade 3', 'senior 2') | If the field value is a member of the input value, it matches     |
| mc.age.notin(10, 30, 45)             | If the field value is not a member of the input value, it matches |

| **Code**     |
| ------------------ |
| mc.name.re('tony') |

| **Code**                                                              | **Explanation** |
| --------------------------------------------------------------------------- | --------------------- |
| [ mc.age>3 ][ mc.age<100 ]                                                  | Intersection          |
| [ (mc.age==30)&#124; (mc.age>30) &#124; (mc.age<30) &#124; (mc.age==None) ] | Union                 |
| [ (mc.age>3) - (mc.age>100) ]                                               | Difference set        |
| [ ~(mc.age>100) ]                                                           | Complement            |

only the name and age fields are returned:

```python
sheet[mc.age>11][mc.age<30]['name','age'][:]
```

for all data with an age greater than 12, the first step is in descending order by age, and the second step is in ascending order by name. After sorting, the second to fourth data items are returned:

```python
sheet[mc.age>12].order(age=False, name=True)[2:4]
```

Statistics：

| **Project**       | **Syntax**        | **Return**                                        |
| ----------------------- | ----------------------- | ------------------------------------------------------- |
| All fields              | sheet.getColumns( )     | [{'name':'id', 'comment':'', 'type':'int'}, {...}, ...] |
| Total data              | len( sheet )            | 0                                                       |
| Data volume with age>10 | len( sheet[mc.age>10] ) | 0                                                       |

orm (account ORM):

| **Function**                | **Syntax**  | **Return**                                                     |
| --------------------------------- | ----------------- | -------------------------------------------------------------------- |
| Obtain the names of all libraries | orm.getDbNames( ) | ['information_schema', 'mysql', 'performance_schema', 'sys', 'city'] |
| check whether a library exists.   | 'city'  in  orm   | True                                                                 |
| Number of statistical databases   | len( orm )        | 5                                                                    |

db (database ORM):

| **Function**             | **Syntax**    | **Return** |
| ------------------------------ | ------------------- | ---------------- |
| obtain the names of all sheets | db.getSheetNames( ) | ['school']       |
| check whether a sheet exists.  | 'school'  in  db    | True             |
| Number of statistical sheets   | len( db )           | 1                |

Call mysql functions：

```python
sheet[mf.year('report_date') == 2023][:]
sheet[mf.year('report_date') == 2029][:] = None
sheet[mf.year('report_date') == 2023][2:5] = {'gender':'female'}
```

Execute native SQL statements：

```python
data, cursor = sheet.execute('select name from school limit 1')
data
# >>> [{'name': 'tony 1'}]

data, cursor = sheet.execute('update school set like="Python" limit 3')
cursor.rowcount
# >>> 3
```
