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




# OCX xsd schema parser functionality
class OCXSchema:
    def __init__(self):
        self.schema_changes = []
        self.dom_tree = None
        self.model = None
        self.attributes = []  # the schema global attributes
        self.elements = []  # the schema global elements
        self.complex = []  # the schema global complex types
        self.enums = {} # Dictionary of global enums
        self.dict = {}  # The schema element dictionary of legal types
        self.uri = ''
        self.namespace = {}  # The namespaces used by the OCX
        self.version = 'No version'  # The schema version of the parsed xsd
        self.logger = logging.getLogger('schema_validation')
        self.ns = ET.FunctionNamespace(None)
        self.ns['description'] = self.description

    def load_schema(self, schema) -> bool:
        self.uri = schema  # The uri or the file name of the xsd schema
        # Check the schema uri
        uri = Path(schema)
        if uri.exists():
            # initialize the name space and parse the xsd
            self.parse_name_space()
            self.create_dom_tree(schema)
            self.parse_schema_version()
            self.parse_schema_changes()
            self.xmlschema = ET.XMLSchema(self.get_dom_tree())
            root = self.dom_tree.getroot()
            # Retreive all global elements
            self.elements = root.findall('xs:element', self.namespace)
            # Retrieve all complex types (we need this as the schemaVersion is part of DocumentBase_T)
            self.complex = root.findall('xs:complexType', self.namespace)
            # Retrieve all global attributes
            self.attributes = root.findall('xs:attribute', self.namespace)
            self.parse_attribute_enumerations()
            self.make_schema_dictionary()
            return True
        else:
            self.logger.error('Wrong schema location: {}'.format(uri))
            return False

    def parse_name_space(self):
        # open the schema uri and read the namespaces
        pattern = 'xmlns'
        with open(self.uri, mode='r') as fd:
            for line in fd:
                if re.search(pattern, line):
                    break  # Break when pattern is found & close the file
        fd.close()
        # Extract the name spaces
        # Example namespace string:   xmlns:xs=\http://www.w3.org/2001/XMLSchema"
        ns = re.findall(r'xmlns:\w+="\S+', line)
        # create the name space dict:
        namespace = dict()
        for str in ns:
            k = re.findall(r'xmlns:\w+', str)
            key = re.sub(r'xmlns:', "", k[0])
            v = re.findall(r'=\S+', str)
            value = re.sub(r'[="]+', "", v[0])
            self.namespace[key] = value
        return

    def create_dom_tree(self, schema_file):
        self.dom_tree = ET.parse(schema_file)  # Create the DOM tree

    def get_dom_tree(self):
        return self.dom_tree

    def get_schema_root(self):
        if self.dom_tree is None:
            self.logger.error('Call load_schema() first')
            return None
        else:
            return self.dom_tree.getroot()

    def get_name_space(self):
        return self.namespace

    def get_version(self)->str:
        return self.version

    def get_schema_changes(self):
        return self.schema_changes

    def parse_schema_changes(self):
        if self.dom_tree is None:
            self.logger.error('Call load_schema() first')
        else:
            self.schema_changes = []
            root = self.get_schema_root()
            changes = root.findall('.//ocx:SchemaChange', self.namespace)
            for change in changes:
                version = change.get('version')
                if version == self.get_version(): #Only include changes for this schema version
                    schemachange = [change.get('version'), change.get('author'), change.get('date')]
                    regex = '\w+'
                    description = ET.tostring(change,  method='text', inclusive_ns_prefixes=None).decode('UTF-8')
                    text =  re.sub('[\n\t\r]','', description )
                    schemachange.append(text)
                    self.schema_changes.append(schemachange)
        return

    def get_elements(self):
        return self.elements

    def get_dictionary(self):
        return self.dict

    def get_attributes(self):
        return self.attributes

    def get_complex(self):
        return self.complex

    def get_enumerations(self):
        return self.enums

    # Attributes enumerators
    def parse_attribute_enumerations(self):
        for attr in self.attributes:
            evalues = []
            aname = attr.get('name')
            enumerations = attr.findall('.//*xs:enumeration', self.namespace)
            if  len(enumerations) == 0:
                self.enums[aname] = []
            else:
                for enum in enumerations:
                    value = enum.get('value')
                    evalues.append(value)
                self.enums[aname] = evalues

    def make_schema_dictionary(self):
        self.type = {}

        # Global ocx element and type
        for e in self.elements:
            name = e.get('name')
            typ = e.get('type')
            self.type[name] = typ  # Lookup table for type
        # Global ocx attribute and type
        for e in self.attributes:
            name = e.get('name')
            typ = e.get('type')
            self.type[name] = typ  # Lookup table for type
        # Create static name dictionary
        for e in sorted(self.type.keys()):
            key = e.lower()
            self.dict[key] = e
        # Wrap namespace declaration
 #       for e in self.dict:
 #           value = self.dict[e]
 #           self.dict[e] = '{' + self.namespace['ocx'] + '}' + value


    def parse_schema_version(self) -> bool:
        if (len(self.namespace)) == 0:
            self.logger.error('Call method "parse_name_space()"  first')
            return False
        if self.dom_tree is None:
            self.logger.error('Call method "load_schema()"  first')
            return False
        else:
            root = self.dom_tree.getroot()
            # Retrieve all complex types (we need this as the schemaVersion is part of DocumentBase_T)
            self.complex = root.findall('xs:complexType', self.namespace)
            # Get the schema version
            for cmplx in self.complex:
                name = cmplx.get('name')
                if name == 'DocumentBase_T':
                    attr = cmplx.findall('xs:attribute', self.namespace)
                    for a in attr:
                        name = a.get('name')
                        if name == 'schemaVersion':
                            self.version = a.get('fixed')
                            break
        return True

    def description(self, context, arg):
        regex = re.search(':Description>\n*(.*)\n', arg)
        return regex[1]

