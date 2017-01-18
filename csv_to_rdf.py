#!/usr/bin/env python3
#  -*- coding: UTF-8 -*-
"""
Convert Prisoners of War from CSV to RDF using CIDOC CRM.
"""

import argparse
import datetime
import logging
import re

import pandas as pd
from rdflib import URIRef, Namespace, Graph, RDF, Literal
from rdflib import XSD

from converters import convert_int, convert_dates, convert_person_name
from mapping import PRISONER_MAPPING

CIDOC = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
DC = Namespace('http://purl.org/dc/elements/1.1/')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
BIOC = Namespace('http://ldf.fi/schema/bioc/')

DATA_NS = Namespace('http://ldf.fi/warsa/prisoners/')
SCHEMA_NS = Namespace('http://ldf.fi/schema/warsa/prisoners/')
EVENTS_NS = Namespace('http://ldf.fi/warsa/events/')


class RDFMapper:
    """
    Map tabular data (currently pandas DataFrame) to RDF. Create a class instance of each row.
    """

    def __init__(self, mapping, instance_class, loglevel='WARNING'):
        self.mapping = mapping
        self.instance_class = instance_class
        self.table = None
        self.data = Graph()
        self.schema = Graph()
        logging.basicConfig(filename='rdfmapper.log',
                            filemode='a',
                            level=getattr(logging, loglevel),
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.log = logging.getLogger(__name__)

    def read_column_with_sources(self, orig_value):
        # Split value to value and sources
        sourcematch = re.search(r'(.+) \(([^()]+)\)(.*)', orig_value)
        (value, sources, trash) = sourcematch.groups() if sourcematch else (orig_value, None, None)

        if sources:
            self.log.debug('Found sources: %s' % sources)
            sources = (Literal(s.strip()) for s in sources.split(','))

        if trash:
            self.log.warning('Found some content after sources: %s' % trash)

        return value, sources

    def map_row_to_rdf(self, entity_uri, row):
        """
        Map a single row to RDF.

        :param entity_uri: URI of the instance being created
        :param row: tabular data
        :return:
        """

        row_rdf = Graph()

        (firstnames, lastname, fullname) = convert_person_name(row[0])

        if firstnames:
            row_rdf.add((entity_uri, FOAF.givenName, Literal(firstnames)))

        row_rdf.add((entity_uri, FOAF.familyName, Literal(lastname)))
        row_rdf.add((entity_uri, URIRef('http://www.w3.org/2004/02/skos/core#prefLabel'), Literal(fullname)))

        for column_name in self.mapping:

            mapping = self.mapping[column_name]

            value = row[column_name]

            row_rdf.add((entity_uri, RDF.type, self.instance_class))

            slash_separated = mapping.get('slash_separated')

            # Make an iterable of all values in this field
            # TODO: Handle columns separated by ;

            values = (val.strip() for val in re.split(r'\s/\s', str(value))) if slash_separated else \
                [str(value).strip()]

            for value in values:

                sources = None
                if slash_separated:
                    value, sources = self.read_column_with_sources(value)

                if sources:
                    # TODO: Write sources in reified statements
                    pass

                converter = mapping.get('converter')
                value = converter(value) if converter else value

                if value:
                    liter = Literal(value, datatype=XSD.date) if type(value) == datetime.date else Literal(value)
                    row_rdf.add((entity_uri, mapping['uri'], liter))

        return row_rdf

    def read_csv(self, input):
        """
        Read in a CSV files using pandas.read_csv

        :param input: CSV input (filename or buffer)
        """
        csv_data = pd.read_csv(input, encoding='UTF-8', index_col=False, sep='\t', quotechar='"',
                               # parse_dates=[1], infer_datetime_format=True, dayfirst=True,
                               na_values=[' '], converters={'ammatti': lambda x: x.lower(), 'lasten lkm': convert_int})

        self.table = csv_data.fillna('').applymap(lambda x: x.strip() if type(x) == str else x)

    def serialize(self, destination_data, destination_schema):
        """
        Serialize RDF graphs

        :param destination_data: serialization destination for data
        :param destination_schema: serialization destination for schema
        :return: output from rdflib.Graph.serialize
        """
        self.data.bind("p", "http://ldf.fi/warsa/prisoners/")
        self.data.bind("ps", "http://ldf.fi/schema/warsa/prisoners/")
        self.data.bind("skos", "http://www.w3.org/2004/02/skos/core#")
        self.data.bind("cidoc", 'http://www.cidoc-crm.org/cidoc-crm/')
        self.data.bind("foaf", 'http://xmlns.com/foaf/0.1/')
        self.data.bind("bioc", 'http://ldf.fi/schema/bioc/')

        self.schema.bind("ps", "http://ldf.fi/schema/warsa/prisoners/")
        self.schema.bind("skos", "http://www.w3.org/2004/02/skos/core#")
        self.schema.bind("cidoc", 'http://www.cidoc-crm.org/cidoc-crm/')
        self.schema.bind("foaf", 'http://xmlns.com/foaf/0.1/')
        self.schema.bind("bioc", 'http://ldf.fi/schema/bioc/')

        data = self.data.serialize(format="turtle", destination=destination_data)
        schema = self.schema.serialize(format="turtle", destination=destination_schema)

        return data, schema  # Mainly for testing purposes

    def process_rows(self):
        """
        Loop through CSV rows and convert them to RDF
        """
        # column_headers = list(self.table)
        #
        for index in range(len(self.table)):
            prisoner_uri = DATA_NS['prisoner_' + str(index)]
            self.data += self.map_row_to_rdf(prisoner_uri, self.table.ix[index])

        for prop in PRISONER_MAPPING.values():
            if 'name_fi' in prop:
                self.schema.add((prop['uri'], SKOS.prefLabel, Literal(prop['name_fi'], lang='fi')))
                self.schema.add((prop['uri'], RDF.type, RDF.Property))


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Process war prisoners CSV", fromfile_prefix_chars='@')

    argparser.add_argument("input", help="Input CSV file")
    argparser.add_argument("output", help="Output location to serialize RDF files to")
    argparser.add_argument("--loglevel", default='INFO', help="Logging level, default is INFO.",
                           choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])


    args = argparser.parse_args()

    output_dir = args.output + '/' if args.output[-1] != '/' else args.output

    mapper = RDFMapper(PRISONER_MAPPING, SCHEMA_NS.PrisonerOfWar, loglevel=args.loglevel.upper())
    mapper.read_csv(args.input)

    mapper.process_rows()

    mapper.serialize(output_dir + "prisoners.ttl", output_dir + "schema.ttl")
