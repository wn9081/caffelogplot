本地直接绘图
=========
入口就是 `plot_training_log.py`。
用例：
  `./plot_training_log.py 6 ./output.png ./faster_rcnn_end2end_VGG16_.txt.2016-11-18_16-08-37.log`


网络服务
======
支持直接上传log文件
也支持直接绘制网络上获取log文件绘制，如`http://192.168.1.2/plotlog/?logurl=http://192.168.1.2/traintask/73/py-faster-rcnn-caffe.log`将直接把`http://192.168.1.2/traintask/73/py-faster-rcnn-caffe.log`这个log文件的图绘制出来。

本地启动网络服务
-------------
使用命令 `python plot.wsgi` 即可在本地端口8000启动一个网络服务，访问 http://localhost:8000/ 接口。

部署到Apache服务器
---------------
把下面配置信息添加到apache的配置文件中
```
<VirtualHost *:80>
    WSGIScriptAlias /caffelogplot/ /path/to/caffelogplot/plot.wsgi
</VirtualHost>
<Directory /path/to/caffelogplot>
    Require all granted
</Directory>
```

