import cgi
import os
import sys
import base64
import re
import urllib
import tempfile
import os.path as osp
from string import Template

sys.path.insert(0, osp.dirname(__file__))
from plot_training_log import plot_chart

root= tempfile.gettempdir()

htmlbody = Template(u"""
<html>
<head><title>plot caffe log</title></head>
<body>
${IMGCONT}
<form name="plot" action="" ${FORMPARAM}>
<table>
<thead></thead>
<tfoot></tfoot>
<tbody>
<tr>
<td>chart type</td><td>
<select name="type">
    <option value="0">0: Test accuracy  vs. Iters</option>
    <option value="1">1: Test accuracy  vs. Seconds</option>
    <option value="2">2: Test loss  vs. Iters</option>
    <option value="3">3: Test loss  vs. Seconds</option>
    <option value="4">4: Train learning rate  vs. Iters</option>
    <option value="5">5: Train learning rate  vs. Seconds</option>
    <option value="6" selected="selected">6: Train loss  vs. Iters</option>
    <option value="7">7: Train loss  vs. Seconds</option>
</select>
</td>
</tr>
<tr>
<td>logfile</td>
<td>${FILEINPUTTAG}</td>
</tr>
<tr>
<td colspan="2"><input type="submit" value="Submit" /></td>
</tr>
</form>
</body>
</html>
""")

# plot
def _plot_chart(chart_type, file_path):
    #_, path_to_png = tempfile.mkstemp(suffix='.png')
    pngfile = tempfile.NamedTemporaryFile(suffix='.png')
    path_to_png = pngfile.name
    path_to_logs = [ file_path,]
    os.chdir(root)
    plot_chart(chart_type, path_to_png, path_to_logs)

    # Injection attack possible on the filename - should escape!
    return u"<img src=\"data:image/png;base64,%s\">"%(
                base64.b64encode(open(path_to_png,"rb").read())
            )


def _plot_url(chart_type, file_url):
    filename = osp.basename(file_url)
    file_path = osp.join(root, filename)
    if osp.exists(file_path): os.unlink(file_path)
    urllib.urlretrieve(file_url,file_path)

    return htmlbody.substitute(IMGCONT=_plot_chart(chart_type, file_path),
                               FILEINPUTTAG='<input type="text" name="logurl" value="{}" readonly="readonly"/>'.format(file_url),
                               FORMPARAM='method="get"')


def _plot_upload(environ):
            post = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=environ,
                keep_blank_values=True
            )
            fileitem = post["userfile"]
            chart_type = int(post.getvalue("type",4))
            if fileitem.file:
                filename = fileitem.filename.decode('utf8').replace('\\','/').split('/')[-1].strip()
                if not filename:
                    raise Exception('No valid filename specified')
                file_path = osp.join(root, filename)
                # Using with makes Python automatically close the file for you
                counter = 0
                with open(file_path, 'wb') as output_file:
                    while 1:
                        data = fileitem.file.read(1024)
                        # End of file
                        if not data:
                            break
                        output_file.write(data)
                        counter += 1
                        if counter == 100:
                            counter = 0
            # plot
            return _plot_chart(chart_type, file_path)


def application(environ, start_response):
        if environ['REQUEST_METHOD'] == 'POST':
            body = _plot_upload(environ)
        else:
          logurl = environ.get("QUERY_STRING", None)
          pr = None
          if logurl:
            pr = re.match('type=(.*)&logurl=(.*)', logurl)
            if not pr:
                pr = re.match('logurl=(.*)', logurl)
          if pr:
              chart_type = 6 if len(pr.groups())<2 else int(pr.groups()[0])
              body = _plot_url(chart_type, urllib.unquote(pr.groups()[-1]))
          else:
            body = htmlbody.substitute(IMGCONT='',
                               FILEINPUTTAG='<input type="file" name="userfile" />',
                               FORMPARAM='method="post" enctype="multipart/form-data"')
        start_response(
            '200 OK', 
            [
                ('Content-type', 'text/html; charset=utf8'),
                ('Content-Length', str(len(body))),
            ]
        )
        return [body.encode('utf8')]


