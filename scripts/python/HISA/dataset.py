#!/usr/bin/python
"""
dataset.py - parent class for dataset objects 
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

LOG = logging.getLogger(__name__)


propSchema={
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type":"object",
    "properties": {
        "filepath":{ "type":"string" },
        "regexp":{ "type":"string" }
    }
}

fileFieldsSchema={
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type":"object",
    "properties": {
        "DTG":{
            "type":"string"
        }
    }
}

class dataset(object):

    def __init__(self,properties):

        # Use dataset schemas if childs are not defined
        try: self.propSchema
        except: self.propSchema=propSchema
        try: self.fileFieldsSchema
        except: self.fileFieldsSchema=fileFieldsSchema

        self._properties={}
        self._setProperties(properties)
        return

    def get(self,prop):

        if prop in self._properties:
            return(self._properties[prop])
        else:
            msg="Property: {} not found".format(prop)
            utils.error(LOG,msg,error_codes.EX_IOERR)

    def getProperties(self):

        return(self._properties)


    def _setProperties(self,properties):

        # Validate properties against dataset object propSchema
        msg=utils.schemaValidate(properties,self.propSchema)
        if msg:
            msg="Problem finding required properties: {}".format(msg)
            utils.error(LOG,msg,error_codes.EX_IOERR)
        self._properties.update(properties)

        # Check filepath existence
        if os.path.isfile(self._properties['filepath']):
            path,filename=os.path.split(self._properties['filepath'])
            if not path: # Just the filename, CWD is path, since it exists)
               path=os.getcwd()
            self._properties['path']=path
            self._properties['filename']=filename
        else:
            msg="Filepath: {} does't exist".format(self._properties["filepath"])
            utils.error(LOG,msg,error_codes.EX_IOERR)

        # Check filename format against regexp 
        fields={}
        try:
            match=re.match(self._properties['regexp'],self._properties['filename'])
            fields=match.groupdict()
        except:
            msg="Filename: {} invalid filename format".format(self._properties["filename"])
            utils.error(LOG,msg,error_codes.EX_IOERR)

        # Validate file fields against dataset object fileFieldsSchema
        msg=utils.schemaValidate(fields,self.fileFieldsSchema)
        if msg:
            msg="Problem extracting file field properties from filename: {}".format(self._properties["filename"]) + msg
            utils.error(LOG,msg,error_codes.EX_IOERR)
        self._properties.update(fields)

        return
