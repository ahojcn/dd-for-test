## 基本说明

main.go 为一个 go HTTP 服务器。

test.py 为测试代码。

### 接口说明

#### request

url: `url:8383/dd`

method: `POST`

content-type: `application/json`

data:
```json
Name,     // 姓名: 最短2位，最长20位
Height,   // 身高: [50, 300]cm
Weight,   // 体重: [20, 1k] kg
Gender,   // 性别: 男/女/保密
Age,      // 年龄: [6, 110]岁
Email,    // 邮箱
```

#### response

参数校验成功：
```json
{
    "status": 0,
    "message": "ok",
    "data": {
        "Name": "ahojcn",
        "Height": 175,
        "Weight": 85,
        "Gender": "male",
        "Age": 21,
        "Email": "ahojcn@qq.com"
    }
}
```

参数校验失败：
```json
{
    "status": -2,
    "message": "params error",
    "data": null
}
```
```json
{
    "status": -1,
    "message": "Email is not a email address",
    "data": {
        "Name": "ahojcn",
        "Height": 175,
        "Weight": 85,
        "Gender": "male",
        "Age": 21,
        "Email": ""
    }
}
```

### 测试说明

`TestBase` 进行了基础测试，包括接口地址、响应头、响应体类型的测试。

`TestParams` 对参数进行测试，不传参、传递参数为空、缺少必要参数、参数类型错误、参数越界、参数边界。

压力测试:

```bash
siege -c 100 -r 1000 -H "Content-Type:application/json" "http://127.0.0.1:8383/DD POST <./1.json"
```

```json
{	
    "transactions":			       99542,
	"availability":			       99.54,
	"elapsed_time":			      231.09,
	"data_transferred":		       12.25,
	"response_time":		        0.10,
	"transaction_rate":		      430.75,
	"throughput":			        0.05,
	"concurrency":			       41.02,
	"successful_transactions":	       99542,
	"failed_transactions":		         458,
	"longest_transaction":		       20.04,
	"shortest_transaction":		        0.00
}
```


---

End Of File README.

@author: [ahojcn](https://ahoj.cc) ahojcn@qq.com