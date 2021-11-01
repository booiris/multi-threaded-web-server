# 多线程服务器

## 运行步骤

运行 "python server.py"

下面显示的 ip 地址和端口 为服务器地址和端口

浏览器输入 

host : port

host : port/index.html

host : port/cal.html

host : port/query.html

查看效果

## 目录结构

```bash
.
├── cgi-bin              // cgi程序文件夹
│   ├── cal.py           // 计算器程序 
│   ├── cal_res.html     // 计算结果页面
│   ├── query.html       // 查询结果页面
│   └── query.py         // 查询数据程序
├── css                  // 页面css文件夹
│   ├── img              // 网页图片文件夹
│   │   ├── head.png     
│   │   ├── p1.jpg
│   │   └── p2.jpg
│   ├── index.css
│   └── temp.css
├── data                 // 数据库初始化 
│   └── Student_data.sql
├── log                  // 日志文件夹
│   └── null
├── 400.html             // 400错误页面
├── 403.html             // 403错误页面
├── 404.html             // 404错误页面
├── cal.html             // 计算器页面
├── index1.html          // 主页1（测试css）
├── index.html           // 主页2（测试图片）
├── query.html           // 数据查询界面
├── readme.md
├── server.py            // 服务器主函数，用于绑定端口，和启动线程池管理
└── worker.py            // 服务线程的具体实现，在 worker 类中
```



