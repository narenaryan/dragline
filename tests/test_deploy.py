#import os
#import unittest
#from dragline.deploy import deploy
#from httplib2 import Http
#import MySQLdb
#connection = MySQLdb.connect(
    #host="localhost", user="root", passwd="passme", db="dragline")
#cursor = connection.cursor()


#class DeployTest(unittest.TestCase):

    #def setUp(self):
        #self.parent_dir = os.getcwd()
        #os.chdir(str(os.getcwd()) + "/tests")

    #def tearDown(self):
        #try:
            #os.chdir(self.parent_dir)
        #except:
            #pass

    #def test_deploy_wrong(self):

        ## check whether the server is running
        #req = Http()
        #try:
            #status, content = req.request("http://192.168.0.20:8000/deploy/")
            #if status['status'] != "200":
                #return
        #except:
            #print "dragline server not running, quiting testing"
            #return
        #try:
            #connection = MySQLdb.connect(
                #host="localhost", user="root", passwd="passme", db="dragline")
            #cursor = connection.cursor()
        #except:
            #print "cannot connect to database, quitting further testing"
            #return

        #print os.listdir(os.getcwd())
        #result = deploy("http://192.168.0.20:8000/deploy/",
                        #"shimil", "passme", "Test_Boxoffice_wrong")
        #qry = "SELECT * FROM spiders_spider WHERE name='Test_Boxoffice_wrong'"
        #cursor.execute(qry)
        #connection.commit()
        #res = cursor.fetchall()
        #self.assertFalse(res)

        ## cleanup
        #qry = "DELETE FROM spiders_spider WHERE name ='Test_Boxoffice'"
        #cursor.execute(qry)
        #connection.commit()

        #qry = "DELETE FROM spiders_spider WHERE name ='Test_Boxoffice_wrong'"
        #cursor.execute(qry)
        #connection.commit()

    #def test_deploy(self):

        ## check whether the server is running
        #req = Http()
        #try:
            #status, content = req.request("http://192.168.0.20:8000/deploy/")
            #if status['status'] != "200":
                #return
        #except:
            #print "dragline server not running, quiting testing"
            #return
        #try:
            #connection = MySQLdb.connect(
                #host="localhost", user="root", passwd="passme", db="dragline")
            #cursor = connection.cursor()
        #except:
            #print "cannot connect to database, quitting further testing"
            #return

        #print os.listdir(os.getcwd())
        #result = deploy(
            #"http://192.168.0.20:8000/deploy/", "shimil", "passme", "Test_Boxoffice")
        #qry = "SELECT * FROM spiders_spider WHERE name='Test_Boxoffice'"
        #cursor.execute(qry)
        #connection.commit()
        #res = cursor.fetchall()
        #self.assertTrue(res)

        ## cleanup
        #qry = "DELETE FROM spiders_spider WHERE name ='Test_Boxoffice'"
        #cursor.execute(qry)
        #connection.commit()

        #qry = "DELETE FROM spiders_spider WHERE name ='Test_Boxoffice_wrong'"
        #cursor.execute(qry)
        #connection.commit()
#if __name__ == "__main__":
    #unittest.main()