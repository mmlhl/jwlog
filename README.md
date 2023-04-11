# jw-log
**nnnu教务系统登录实现。**
***
## 1.文件解析



## 2.启用加密
###### 环境要求

- node.js


###### 进入加密模块目录

~~~ shell
cd encode
~~~

###### 运行加密端口

~~~ shell
npm run encode
~~~

###### 加密数据

请求运行起来的加密链接，得到加密内容，然后就可以拿着加密后的内容提交登录请求。

| 键   | 可能的值    | 说明                                               |
| ---- | ----------- | -------------------------------------------------- |
| key  | jC8cm2LseQg | 登录主界面中id为login-croypto的p标签里面的文本内容 |
| psw  | password    | 用户密码                                           |

示例：

~~~shell
curl 'http://127.0.0.1:5715/encode?key=jC8cm2LseQg&psw=password'
~~~

