# System
import sys
import os
import unittest
import json
import logging
import pprint

try:
    exePath=os.path.dirname(os.path.abspath(__file__))
    parentPath,childDir=os.path.split(exePath)
    sys.path.insert(1,os.path.join(parentPath,"lib"))
    sys.path.insert(2,os.path.join(parentPath,"HISA"))
except:
   print "Unable to load local library paths"
   sys.exit(1)

# Local
import utils
import setup_logging
 
class TestUtils(unittest.TestCase):
 
    def setUp(self):
        LOG = logging.getLogger(__file__) #create the logger for this file
        setup_logging.setup_logging("test_utils","test_utils.log")
        self.pp=pprint.PrettyPrinter(indent=4)
 
    def test_textFileRecordsFilter(self):

        inputFile='fixtures/adeck/nhc_aep142018.dat.201808240319'
        outputFile='/tmp/nhc_aep142018.dat.201808240319'
        
        recordREs=['^.*CARQ.*$','^.*OFCL.*$','^.*OFCI.*$','^.*TABM.*$','^.*JTWC.*$','^.*JTWI.*$','^.*MBAM.*$']
        status=utils.textFileRecordFilter(inputFile,outputFile,recordREs)
        self.assertTrue(status)
 
 
if __name__ == '__main__':
    unittest.main()
