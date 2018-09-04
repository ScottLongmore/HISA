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
import libHISA as hisa
import setup_logging
 
class TestLibHISA(unittest.TestCase):
 
    def setUp(self):
        LOG = logging.getLogger(__file__) #create the logger for this file
        setup_logging.setup_logging("test_libHISA","test_libHISA.log")
        self.pp=pprint.PrettyPrinter(indent=4)
 
    def test_scaleOffsetThreshPoolTextFile(self):
        
        scale=0.01
        offset=0.0
        lowThresh=0.0
        highThresh=500.0
        inputMissing=-999.0
        outputMissing=-999.0
        filename="fixtures/pool/LWP.txt"
        newfilename="output/new_LWP.txt"
        # Test LWP
        status=hisa.scaleOffsetThreshPoolTextFile(scale,offset,lowThresh,highThresh,inputMissing,outputMissing,filename,newfilename)
        self.assertTrue(status)
 
 
if __name__ == '__main__':
    unittest.main()
