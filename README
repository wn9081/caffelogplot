本地直接使用
=========
入口就是 `plot_training_log.py`, 其他文件如`parse_log.sh`/`parse_log.py`/`extract_seconds.py`都会被直接或间接调用。
用例：
  `./plot_training_log.py 6 ./output.png ./faster_rcnn_end2end_VGG16_.txt.2016-11-18_16-08-37.log`

部署到WSGI服务器
=============
```
<VirtualHost *:80>
    WSGIScriptAlias /caffelogplot/ /path/to/caffelogplot/plot.wsgi
</VirtualHost>
<Directory /path/to/caffelogplot>
    Require all granted
</Directory>
```
支持直接上传log文件
也支持直接绘制网络上获取log文件绘制，如`http://192.168.1.2/plotlog/?logurl=http://192.168.1.2/traintask/73/py-faster-rcnn-caffe.log`将直接把`http://192.168.1.2/traintask/73/py-faster-rcnn-caffe.log`这个log文件的图绘制出来。

