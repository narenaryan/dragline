
import os
import inspect
import zipfile
import sys
from json import dumps
from httplib2 import Http
from urllib import urlencode
import logging
#logger = logging.getLogger("dragd:deploy")


h = Http()


def deploy(username,password,foldername):

    #check whether the folder is a spider
    if "main.py" in os.listdir(foldername):
        pass
    else:
        print "Not a valid spider"
        return

    #check if the main.py contain a spider class
    module = load_module(foldername,"main")
    #check if main.py contain a spider class
    spider=None
    try:

        spider = getattr(module,"Spider")
    except Exception as e:
        pass

    if spider:
        pass
        #check if spider is a class
    else:
        print "Spider class not found"
        return

    if inspect.isclass(spider):
        pass
    else:
        print "Spider class not found"
        return

    #create a spider object and check whether it contain required attributes

    spider_object=spider(None)

    try:
        if spider_object._name and spider_object._start_url and spider_object._allowed_urls_regex and spider_object.parse:
            spider_name=spider_object._name
            pass
        else:
            print "required attributes not found in spider"
            return

    except Exception as e:
        print "Spider deploying failed"
        return

    #zip the folder



    zipf = zipfile.ZipFile('%s.zip'%spider_name, 'w')
    zipdir('spider_2', zipf)
    zipf.close()

    zipf=open("%s.zip"%spider_name,"rb").read()



    post_data = {'username' : username,'password' : password,'spider_name' : spider_name,'zipfile' :  zipf}






    resp, content = h.request("http://192.168.0.11:8000/deploy/",
        "POST", body=urlencode(post_data),
        headers={'content-type':'application/x-www-form-urlencoded'} )
        #read zip file
    print resp,content






     #upload the spider into database





















def load_module(path, filename):
    try:

        sys.path.insert(0, path)


        module = __import__(filename)
        del sys.path[0]
        return module
    except Exception as e:
        print e.message
        #logger.exception("Failed to load module %s" % filename)
        raise ImportError





def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))




if __name__ == "__main__":
    deploy("manu","passme","../../samplespider/NetaPorter/")



