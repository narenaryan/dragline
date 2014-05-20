import argparse
from zipfile import ZipFile
import os
import runner
import MySQLdb
import defaultsettings
import shutil

connection = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="passme",
    db="dragline")
cursor = connection.cursor()
logger = defaultsettings.get_logger("dragd")


def start(run_id):
    qry = "SELECT spider_id FROM spider_run WHERE id=%d" % int((run_id))
    logger.info("started run %s", run_id)
    cursor.execute(qry)
    connection.commit()
    row = cursor.fetchall()
    if row:
        spider_id = row[0][0]
        qry = "SELECT zipfile FROM spider_spider WHERE id=%d" % int((spider_id))
        cursor.execute(qry)
        connection.commit()
        result = cursor.fetchall()
        if result:
            zipfile = result[0][0]
            f = open("zipfile.zip", "w")
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
        zf = ZipFile("zipfile.zip")
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
