import os
import sys
import urllib
from datetime import datetime

VERSION = 1
base_url = 'https://raw.githubusercontent.com/alekseystryukov/vk_audio_player/master/'
cur_dir = os.path.dirname(os.path.abspath(__file__))
cur_file = os.path.abspath(__file__)


def update():
    file_handle = urllib.urlopen(os.path.join(base_url, __file__))
    for line in file_handle.readlines():
        if line.startswith('VERSION'):
            _, new_version = line.split('=')
            print(line)
            print(float(new_version.strip()))
            if float(new_version.strip()) > VERSION:
                print(new_version)
            break


def update_code():
    for f in os.listdir(cur_dir):
        print(f)
        full_f = os.path.join(cur_dir, f)
        print(full_f)
        if os.path.isfile(os.path.join(cur_dir, f)):

            statbuf = os.stat(full_f)
            print("Modification time: {}".format(statbuf.st_mtime))

            req = urllib2.Request(base_url + f)
            req.add_header("If-Modified-Since", 'Thu, 19 Nov 2015 16:13:19 GMT') #datetime.fromtimestamp(statbuf.st_mtime)).strftime()

            class NotModifiedHandler(urllib2.BaseHandler):
                def http_error_304(self, req, fp, code, message, headers):
                    addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
                    addinfourl.code = code
                    print('hi')
                    print(addinfourl.code)
                    return addinfourl

            opener = urllib2.build_opener(NotModifiedHandler())
            url_handle = opener.open(req)
            headers = url_handle.info()
            print(headers)
            input('hi')

    if 'restart' in sys.argv:
        print(sys.argv)
        print(sys.executable)
        os.execl(sys.executable, *([sys.executable] + sys.argv[:1]))