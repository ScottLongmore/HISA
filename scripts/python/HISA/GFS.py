#!/usr/bin/python
"""
GFS.py - GFS GRIB2 class 
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
        "hour":{ "type":"string" },
        "fhour":{ "type":"string" },
        "runDTG":{ "type":"string" },
    }
}

class gfs(dataset):

    def __init__(self,properties):

        self.fileFieldsSchema=fileFieldsSchema

        super(gfs,self).__init__(properties)

        self._properties['hour']=int(self._properties['hour'])
        self._properties['fhour']=int(self._properties['fhour'])
        DTS="{}{}".format(self._properties['runDTG'],self._properties['hour'])
        self._properties['runDTG']=datetime.datetime.strptime(DTS,"%Y%m%d%H")

def latestGFS(config,metadata,dataname):

    try:
        latestGFS=metadata[dataname].pop(0)
        for gfs in metadata[dataname]: 
    
            runDTG=gfs.get('runDTG')
            if runDTG > latestGFS.get('runDTG'):
                latestGFS=gfs
    except:
        msg="Problem filtering dataname object list".format(dataname)
        utils.error(LOG,msg,error_codes.EX_DATAERR)
    
    return([latestGFS])
 
