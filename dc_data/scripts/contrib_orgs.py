#!/usr/bin/env python
from hashlib import md5
from saucebrush import run_recipe
from saucebrush.sources import CSVSource
from saucebrush.filters import YieldFilter
from saucebrush.emitters import CSVEmitter, DebugEmitter
from strings.normalizer import basic_normalizer
import saucebrush
import datetime
import sys
import os
"""
    python contrib_orgs.py < [path to denorm csv]
    *** just writes to . directory for now ***
"""

FILENAME = u"contrib_orgs_%s.csv"

class OrgSplitter(YieldFilter):
    def process_record(self, record):
        org_name = record['organization_name'].strip()
        if org_name:
            yield {
                'organization_entity': None,
                'organization_name': org_name,
                'type': 'child',
            }
        org_name = record['parent_organization_name'].strip()
        if org_name:
            yield {
                'organization_entity': None,
                'organization_name': org_name,
                'type': 'parent',
            }

class EntityEmitter(CSVEmitter):
    
    fields = ('id','name','type','timestamp','reviewer')
    
    def __init__(self, csvfile, timestamp):
        super(EntityEmitter, self).__init__(csvfile, self.fields)
        self._timestamp = timestamp
        self._cache = { }
        
    def emit_record(self, record):
        org_name = record['organization_name']
        urn = 'urn:matchbox:name:%s' % basic_normalizer(org_name.decode('utf-8', 'ignore'))
        entity_id = md5(urn).hexdigest()
        if entity_id not in self._cache:
            self._cache[entity_id] = None
            record['organization_entity'] = md5(urn).hexdigest()
            super(EntityEmitter, self).emit_record(dict(zip(self.fields, (
                record['organization_entity'],
                org_name,
                'organization',
                self._timestamp,
                'basic entity script - jcarbaugh',
            ))))

class EntityAttributeEmitter(CSVEmitter):
    
    fields = ('entity','namespace','value')
    
    def __init__(self, csvfile):
        super(EntityAttributeEmitter, self).__init__(csvfile, self.fields)
        
    def emit_record(self, record):
        super(EntityAttributeEmitter, self).emit_record(dict(zip(self.fields, (
            record['organization_entity'],
            'urn:matchbox:entity',
            record['organization_entity'],
        ))))


class EntityAliasEmitter(CSVEmitter):
    
    fields = ('entity','alias')
    
    def __init__(self, csvfile):
        super(EntityAliasEmitter, self).__init__(csvfile, self.fields)
        
    def emit_record(self, record):
        super(EntityAliasEmitter, self).emit_record(dict(zip(self.fields, (
            record['organization_entity'],
            record['organization_name'],
        ))))


def extract_organizations(infile):
    
    now = datetime.datetime.utcnow().isoformat()
    
    run_recipe(
        CSVSource(infile),
        OrgSplitter(),
        EntityEmitter(open(FILENAME % 'entity', 'w'), now),
        EntityAttributeEmitter(open(FILENAME % 'entity_attribute', 'w')),
        EntityAliasEmitter(open(FILENAME % 'entity_alias', 'w')),
    )


if __name__ == "__main__":
    extract_organizations(sys.stdin)