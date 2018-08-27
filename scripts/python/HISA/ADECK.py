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

fileFieldsSchema={ 
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type":"object",
    "properties": {
        "source":{ "type":"string" },
        "stormId":{ "type":"string" },
        "basinId":{ "type":"string" },
        "stormNum":{ "type":"string" },
        "year":{ "type":"string" },
        "createDTG":{ "type":"string" }
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

    def __init__(self,properties):

        self.fileFieldsSchema=fileFieldsSchema
        super(adeck,self).__init__(properties)

        self._properties['stormNum']=int(self._properties['stormNum'])
        self._properties['year']=int(self._properties['year'])

        checkBasin(self._properties['basinId'],self._properties['filename'])
        self._properties['jtwcId']="{}{}".format(self._properties['stormNum'],self._properties['basinId'][0].upper())
        
        if 'createDTG' in self._properties:
            self._properties['createDTG']=datetime.datetime.strptime(self._properties['createDTG'],"%Y%m%d%H%M")
        else:
            # Should replace this time with newest time entry within file, need Roberts python adeck reader
            LOG.info("Filename creation time field doesn't exist, using file modification time")
            self._properties['createDTG']=datetime.fromtimestamp(os.path.getmtime(self._properties('filename')))

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


 
