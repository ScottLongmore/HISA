# System
import sys
import os
import unittest
import json
import datetime
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
import dataset
import ADECK
import GFS
import ATMS 
import setup_logging
 
class TestDatasets(unittest.TestCase):
 
    def setUp(self):
        LOG = logging.getLogger(__file__) #create the logger for this file
        setup_logging.setup_logging("test_datasets","test_datasets.log")
        self.pp=pprint.PrettyPrinter(indent=4)
 
    def test_adeck(self):
        
        properties={
            "regexp":"^(?P<source>jtwc|nhc)_a(?P<stormId>(?P<basinId>\\w{2})(?P<stormNum>\\d{2})(?P<year>\\d{4}))\\.dat\\.?(?P<createDTG>\\d{12})$",
            "filepath":"fixtures/adeck/nhc_aep142018.dat.201808240319",
        }

        # Create adeck object
        dataObj=ADECK.adeck(properties)

        properties={
            "regexp":"^(?P<source>jtwc|nhc)_a(?P<stormId>(?P<basinId>\\w{2})(?P<stormNum>\\d{2})(?P<year>\\d{4}))\\.dat\\.?(?P<createDTG>\\d{12})$",
            "filepath":"fixtures/adeck/nhc_aep142018.dat.201808240319",
            "filename":"nhc_aep142018.dat.201808240319",
            "path":"fixtures/adeck",
            "source":"nhc",
            "stormId":"ep142018",
            "basinId":"ep",
            "jtwcId":"14E",
            "stormNum":14,
            "year":2018,
            "createDTG":datetime.datetime.strptime("201808240319","%Y%m%d%H%M")
        }

        # Test adeck object
        self.assertIsInstance(dataObj,ADECK.adeck)
        self.assertEqual(properties['filepath'],dataObj.get('filepath'))
        self.assertEqual(properties['regexp'],dataObj.get('regexp'))
        self.assertDictEqual(properties,dataObj.getProperties())

    def test_gfs(self):

        properties={
            "regexp":"^gfs\\.t(?P<hour>\\d{2})z\\.pgrb2\\.1p00\\.f(?P<fhour>\\d{3})\\.(?P<runDTG>\\d{8})$",
            "filepath":"fixtures/gfs/gfs.t18z.pgrb2.1p00.f000.20180823",
        }

        # Create GFS object 
        dataObj=GFS.gfs(properties)

        properties={
            "regexp":"^gfs\\.t(?P<hour>\\d{2})z\\.pgrb2\\.1p00\\.f(?P<fhour>\\d{3})\\.(?P<runDTG>\\d{8})$",
            "filepath":"fixtures/gfs/gfs.t18z.pgrb2.1p00.f000.20180823",
            "filename":"gfs.t18z.pgrb2.1p00.f000.20180823",
            "path":"fixtures/gfs",
            "hour":18,
            "fhour":0,
            "runDTG":datetime.datetime.strptime("2018082318","%Y%m%d%H")
        }

        # Test GFS object
        self.assertIsInstance(dataObj,GFS.gfs)
        self.assertEqual(properties['filepath'],dataObj.get('filepath'))
        self.assertEqual(properties['regexp'],dataObj.get('regexp'))
        self.assertDictEqual(properties,dataObj.getProperties())

    def test_atms(self):

        properties={
            "regexp":"^NPR-MIRS-(?P<type>SND|IMG)_(?P<version>\\w+)_(?P<satellite>\\w+)_s(?P<startDT>\\d{14,15})_e(?P<endDT>\\d{14,15})_c(?P<createDT>\\d{14,15})\\.nc$",
            "filepath":"fixtures/atms/NPR-MIRS-IMG_v11r1_npp_s201808232352586_e201808232353303_c201808240048140.nc"
        }

        # Create ATMS object 
        dataObj=ATMS.atms(properties)

        properties={
            "regexp":"^NPR-MIRS-(?P<type>SND|IMG)_(?P<version>\\w+)_(?P<satellite>\\w+)_s(?P<startDT>\\d{14,15})_e(?P<endDT>\\d{14,15})_c(?P<createDT>\\d{14,15})\\.nc$",
            "filepath":"fixtures/atms/NPR-MIRS-IMG_v11r1_npp_s201808232352586_e201808232353303_c201808240048140.nc",
            "filename":"NPR-MIRS-IMG_v11r1_npp_s201808232352586_e201808232353303_c201808240048140.nc",
            "path":"fixtures/atms",
            "type":"IMG",
            "version":"v11r1",
            "satellite":"npp",
            "startDT":datetime.datetime.strptime("20180823235258","%Y%m%d%H%M%S"),
            "endDT":datetime.datetime.strptime("20180823235330","%Y%m%d%H%M%S"),
	    "createDT":datetime.datetime.strptime("20180824004814","%Y%m%d%H%M%S")
	}

        # Test ATMS object
        self.maxDiff=None
        self.assertIsInstance(dataObj,ATMS.atms)
        self.assertEqual(properties['filepath'],dataObj.get('filepath'))
        self.assertEqual(properties['regexp'],dataObj.get('regexp'))
        self.assertDictEqual(properties,dataObj.getProperties())

 
 
if __name__ == '__main__':
    unittest.main()
