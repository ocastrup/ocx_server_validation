#  #!/usr/bin/env python3
#  GNU All-Permissive License
#  Copying and distribution of this file, with or without modification,
#  are permitted in any medium without royalty provided the copyright
#  notice and this notice are preserved.  This file is offered as-is,
#  without any warranty.

from lxml import etree as ET
from lxml.etree import XMLSyntaxError
import logging
import re
from pathlib import Path
from ocxSchema import OCXSchema


# xsd schema validation
class OCXValidate:
    def __init__(self, schema: OCXSchema):
        self.schema = schema # The instantiated xsd schema
        self.ocxfile ='No model' # OCX Model file name
        self.errors = [] # List of errors after validation
        self.logger = logging.getLogger('schema_validation')
        self.syntax_error = ''

    def validate(self, ocxfile):
        try:
            ocx_doc = ET.parse(ocxfile)
        except XMLSyntaxError as error:
            self.logger.error(error)
            self.syntax_error = error
            return False
        self.ocxfile = Path(ocxfile).name
        self.model = ocx_doc
        self.errors = []
        schema = self.schema.xmlschema
        self.logger.info('Validating OCX model: {}'.format(self.ocxfile))
        self.valid = schema.validate(ocx_doc)
        self.logger.info('Number of errors in model: {}'.format(len(schema.error_log)))
        for error in schema.error_log:
            msg = self.find_replace_multi(error.message, self.schema.get_name_space())
            self.logger.info('Line: {}, Error: {}'.format(error.line,msg))
            self.errors.append((error.line, msg))
        return True

    def get_number_of_errors(self):
        return len(self.errors)

    def get_errors(self):
        return self.errors

    def get_model_name(self):
        return self.ocxfile

    def find_replace_multi(self, string, dictionary):
        for item in dictionary.keys():
            # sub item for item's paired value in string
            string = re.sub('{' + dictionary[item] + '}', item + ':', string)
        return string
