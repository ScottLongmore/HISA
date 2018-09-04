# System
import os
import sys
import unittest
import json
import logging
import traceback
import pprint

try:
    exePath=os.path.dirname(os.path.abspath(__file__))
    parentPath,childDir=os.path.split(exePath)
    sys.path.insert(1,os.path.join(parentPath,"lib"))
    sys.path.insert(2,os.path.join(parentPath,"HISA"))
except:
   print "Unable to load local library paths"
   traceback.print_exc()
   sys.exit(1)

# Local
import NDE
import setup_logging
 
class TestNDE(unittest.TestCase):
 
    def setUp(self):
        LOG = logging.getLogger(__file__) #create the logger for this file
        setup_logging.setup_logging("test_NDE","test_NDE.log")

    def test_getInput(self):
        pcfFile="fixtures/NDE/HISA.PCF"

        pcfDict=NDE.getInput(pcfFile)
        self.assertIsInstance(pcfDict,dict)
 
 
if __name__ == '__main__':
    unittest.main()
