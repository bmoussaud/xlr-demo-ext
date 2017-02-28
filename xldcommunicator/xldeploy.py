#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import httplib
import urllib
from urlparse import urlparse
import xml.etree.ElementTree as ET
from xml.dom.minidom import Document

class XLDeployCommunicator:
    """ XL Deploy Communicator using http & XML"""

    # TODO Manage 'context'

    def __init__(self, endpoint='http://localhost:4516', username='admin', password='admin', context='deployit'):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.context = context

    def do_get(self, path):
        return self.do_it("GET", path, "")

    def do_put(self, path, doc):
        return self.do_it("PUT", path, doc)

    def do_post(self, path, doc):
        return self.do_it("POST", path, doc)

    def do_delete(self, path):
        return self.do_it("DELETE", path, "", False)

    def do_it(self, verb, path, doc, parse_response=True):
        # print "DO %s %s on %s " % (verb, path, self.endpoint)

        parsed_url = urlparse(self.endpoint)
        if parsed_url.scheme == "https":
            conn = httplib.HTTPSConnection(parsed_url.hostname, parsed_url.port)
        else:
            conn = httplib.HTTPConnection(parsed_url.hostname, parsed_url.port)

        try:
            auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            headers = {"Content-type": "application/xml", "Accept": "application/xml", "Authorization": "Basic %s" % auth}

            conn.request(verb, "/deployit/%s" % path, doc, headers)
            response = conn.getresponse()
            # print response.status, response.reason
            if response.status != 200 and response.status != 204:
                raise Exception("Error when requesting XL Deploy Server [%s]:%s" % (response.status, response.reason))

            if parse_response:
                xml = ET.fromstring(str(response.read()))
                return xml

            return None
        finally:
            conn.close()


    def property_descriptors(self, typename):
        doc = self.do_get("metadata/type/%s" % typename)
        return dict((pd.attrib['name'], pd.attrib['kind']) for pd in doc.getiterator('property-descriptor'))

    def __str__(self):
        return "[endpoint=%s, username=%s]" % (self.endpoint, self.username)


class RepositoryService:
    """ Access to the repository REST service"""

    def __init__(self, communicator=None):
        self.communicator = communicator

    def read(self, id):
        doc = self.communicator.do_get('repository/ci/%s' % id)
        return ConfigurationItem.from_xlm(doc, self.communicator)

    def mread(self, ids):
        return map(self.read, ids)

    def exists(self, id):
        doc = self.communicator.do_get('repository/exists/%s' % id)
        return "true" in doc.text

    def update(self, ci):
        doc = ConfigurationItem.to_xml(ci, self.communicator)
        updated = self.communicator.do_put('repository/ci/%s' % ci.id, doc)
        return ConfigurationItem.from_xlm(updated, self.communicator)

    def create(self, ci):
        doc = ConfigurationItem.to_xml(ci, self.communicator)
        updated = self.communicator.do_post('repository/ci/%s' % ci.id, doc)
        return ConfigurationItem.from_xlm(updated, self.communicator)

    def delete(self, id):
        self.communicator.do_delete("repository/ci/%s" % id)

    def search(self, ci_type, ci_parent):
        parameters = { "type" : ci_type, "parent" : ci_parent }
        doc = self.communicator.do_get("repository/query?%s" % urllib.urlencode(parameters))
        return map(lambda line:  line.attrib['ref'], doc)


class ConfigurationItem:
    """ an XL Deploy Configuration item"""

    def __init__(self, type, id, properties):
        self.id = id
        self.name = id.split('/')[-1]
        self.type = type
        self.properties = properties

    def __getattr__(self, name):
        if name == "id":
            return self.id
        elif name == "name":
            return self.name
        elif name == "type":
            return self.type
        else:
            return self.properties[name]

    def __str__(self):
        return "%s %s %s" % (self.id, self.type, dict(map(lambda t: (t[0], "********") if t[0] == "password" else t, self.properties.iteritems())))

    def __eq__(self, other):
        return self.id == other.id and self.type == other.type and self.properties == other.properties

    def __contains__(self, item):
        print "###################################################### %s "% item
        # TODO: use DictDiffer https://github.com/hughdbrown/dictdiffer/blob/master/dictdiffer/__init__.py
        # TODO: manage Password

        if not self.id == item.id:
            return False
        if not self.type == item.type:
            return False
        #if not len(self.properties) == len(item.properties):
        #    return False

        for k, v in item.properties.iteritems():
            if k not in self.properties:
                return False
            if type(self.properties[k]) is str:
                if not str(self.properties[k]) == str(v):
                    return False
            elif type(self.properties[k]) is list:
                if not set(v).issubset(set(self.properties[k])):
                    return False

        return True

    def properties(self):
        return self.properties

    def update_with(self, other):
        for k, v in other.properties.iteritems():
            if k in self.properties:
                if isinstance( self.properties[k], list):
                    self.properties[k] = list(set( self.properties[k] + v))
                else:
                    self.properties[k] = v
            else:
                self.properties[k]=v

    @staticmethod
    def from_xlm(doc, communicator):
        descriptors = communicator.property_descriptors(doc.tag)

        def collection_of_string(xml):
            return map(lambda e: e.text, xml)

        def collection_of_ci(xml):
            return map(lambda e: e.attrib['ref'], xml)

        def map_string_string(xml):
            return dict((child.attrib['key'], child.text) for child in xml)

        def ci(xml):
            return xml.attrib['ref']

        def default(xml):
            return xml.text

        properties = dict((xml.tag, {'SET_OF_STRING': collection_of_string,
                                'LIST_OF_STRING': collection_of_string,
                                'SET_OF_CI': collection_of_ci,
                                'LIST_OF_CI': collection_of_ci,
                                'MAP_STRING_STRING': map_string_string,
                                'CI': ci
        }.get(descriptors[xml.tag], default)(xml)) for xml in doc)

        return ConfigurationItem(doc.tag, doc.attrib['id'], properties)

    @staticmethod
    def to_xml(item, communicator):
        descriptors = communicator.property_descriptors(item.type)
        doc = Document()
        base = doc.createElement(item.type)
        base.attributes['id'] = item.id
        doc.appendChild(base)

        def collection_of_string(doc, key, value):
            node = doc.createElement(key)
            for s in value:
                value = doc.createElement('value')
                value.appendChild(doc.createTextNode(s))
                node.appendChild(value)
            return node

        def collection_of_ci(doc, key, value):
            node = doc.createElement(key)
            for ci in value:
                cinode = doc.createElement('ci')
                cinode.attributes['ref'] = ci
                node.appendChild(cinode)
            return node

        def map_string_string(doc, key, value):
            node = doc.createElement(key)
            for k, v in value.iteritems():
                entry = doc.createElement('entry')
                entry.attributes['key'] = k
                entry.appendChild(doc.createTextNode(v))
                node.appendChild(entry)
            return node

        def ci(doc, key, value):
            node = doc.createElement(key)
            node.attributes['ref'] = value
            return node

        def default(doc, key, value):
            node = doc.createElement(key)
            node.appendChild(doc.createTextNode(str(value)))
            return node

        for key, value in item.properties.iteritems():
            if not key in descriptors:
                raise Exception("'%s' is not a property of '%s'" % (key, item.type))

            base.appendChild(
                {'SET_OF_STRING': collection_of_string,
                 'LIST_OF_STRING': collection_of_string,
                 'SET_OF_CI': collection_of_ci,
                 'LIST_OF_CI': collection_of_ci,
                 'MAP_STRING_STRING': map_string_string,
                 'CI': ci
                }.get(descriptors[key], default)(doc, key, value))

        return doc.toxml()


