import argparse
from zipfile import ZipFile
import os
import runner
import MySQLdb
import defaultsettings
import shutil
import logging
import logging.config

connection = MySQLdb.connect(
    host="192.168.0.20",
    user="root",
    passwd="passme",
    db="dragline")
cursor = connection.cursor()
logging.config.dictConfig(defaultsettings.LOGCONFIG)
logger = logging.getLogger("dragd")


def start(run_id):
    qry = "SELECT spider_id FROM spider_run WHERE id=%d" % int((run_id))
    logger.info("started run %s", run_id)
    cursor.execute(qry)
    connection.commit()
    row = cursor.fetchall()
    if row:
        spider_id = row[0][0]
        qry = "SELECT zipfile FROM spider_spider WHERE id=%d" % int(
            (spider_id))
        cursor.execute(qry)
        connection.commit()
        result = cursor.fetchall()
        if result:
            zipfile = result[0][0]
            filename = "/tmp/zip_%s" % (spider_id)

            f = open(filename, "w")
            f.write(zipfile)
            f.close()
        else:
            raise Exception
        # unzip("zipfile.zip","spiders")
        directory = "/tmp/spider_%s" % (str(spider_id))
        try:
            shutil.rmtree(directory)
        except Exception as e:
            pass
        if not os.path.exists(directory):
            os.makedirs(directory)
        zf = ZipFile(filename)
        zf.extractall(directory)
        zf.close()
        files = os.walk(directory)
        for folder in files:
            pass
        spider_dir = folder[0]
        runner.main("main.py", spider_dir, False, defaultsettings)
        shutil.rmtree(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('run_id', type=int)
    args = parser.parse_args()
    start(args.run_id)
