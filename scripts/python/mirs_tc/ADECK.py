#!/usr/bin/python
"""
ADECK.py - automated tropical cyclone forcast (ATCF) ADECK class  
"""

# Stock modules
import sys
import os
import re
import logging
import traceback
import datetime
import collections
import operator

# Local modules
import error_codes
import utils
from dataset import dataset

LOG = logging.getLogger(__name__)

regexp="^(?P<source>jtwc|nhc)_a(?P<stormId>(?P<basinId>\\w{2})(?P<stormNum>\\d{2})(?P<year>\\d{4}))\\.dat\\.?(?P<createDTG>\\d{12})$"
schema={ 
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type":"object",
    "properties": {
        "source":{ "type":"string" },
        "stormId":{ "type":"string" },
        "basinId":{ "type":"string" },
        "stormNum":{ "type":"string" },
        "year":{ "type":"string" }
    }
}

basins={
   "al":"Atlantic",
   "ep":"Eastern Pacific",
   "cp":"Central Pacific",
   "wp":"Western Pacific",
   "io":"Indian Ocean",
   "sh":"Southern Hemisphere"
}

class adeck(dataset):

    def __init__(self,filepath):

        self.regexp=regexp
        self.schema=schema

        super(adeck,self).__init__(filepath)

        self.properties['stormNum']=int(self.properties['stormNum'])
        self.properties['year']=int(self.properties['year'])

        checkBasin(self.properties['basinId'],self.properties['filename'])
        self.properties['jtwcId']="{}{}".format(self.properties['stormNum'],self.properties['basinId'][0].upper())
        
        if 'createDTG' in self.properties:
            self.properties['createDTG']=datetime.datetime.strptime(self.properties['createDTG'],"%Y%m%d%H%M")
        else:
            # Should replace this time with newest time entry within file, need Roberts python adeck reader
            LOG.info("Filename creation time field doesn't exist, using file modification time")
            self.properties['createDTG']=datetime.fromtimestamp(os.path.getmtime(self.properties('filename')))

''' Filter routine for adeck object lists '''
def latestAdecks(config,metadata,dataname):

    try: 
        latestAdecks={}
        for adeck in metadata[dataname]: 
            stormId=adeck.get('stormId')
            createDTG=adeck.get('createDTG')
            if stormId in latestAdecks:
                 if createDTG > latestAdecks[stormId].get('createDTG'):
                    latestAdecks[stormId]=adeck
            else:
                latestAdecks[stormId]=adeck
        latestAdecks=latestAdecks.values()
    except:
        msg="Problem filtering {} object list".format(dataname)
        utils.error(LOG,msg,error_codes.EX_DATAERR)

    return(latestAdecks)

def checkBasin(basin,file):

    if basin in basins:
        LOG.info("Basin is {} ({}) for file: {}".format(basins[basin],basin,file))
    else:
        msg="Unknown basin {} ({}) for file: {}".format(basins[basin],basin,file)
        utils.error(LOG,msg,error_codes.EX_CONFIG)

    return


 
