from time import time
import sys

from urllib import unquote_plus
from django.db.models import Q
from piston.handler import BaseHandler
from dcentity.models import Entity, Normalization
from dcdata.contribution.models import Contribution
from dcapi.contributions import filter_contributions
from dcentity.queries import search_entities_by_name

RESERVED_PARAMS = ('apikey','callback','limit','format','page','per_page','return_entities')
DEFAULT_PER_PAGE = 100
MAX_PER_PAGE = 1000

CONTRIBUTION_FIELDS = ['cycle', 'transaction_namespace', 'transaction_id', 'transaction_type', 'filing_id', 'is_amendment',
              'amount', 'date', 'contributor_name', 'contributor_ext_id', 'contributor_type', 'contributor_occupation', 
              'contributor_employer', 'contributor_gender', 'contributor_address', 'contributor_city', 'contributor_state',
              'contributor_zipcode', 'contributor_category', 'contributor_category_order', 'organization_name', 
              'organization_ext_id', 'parent_organization_name', 'parent_organization_ext_id', 'recipient_name',
              'recipient_ext_id', 'recipient_party', 'recipient_type', 'recipient_state', 'recipient_category', 'recipient_category_order',
              'committee_name', 'committee_ext_id', 'committee_party', 'election_type', 'district', 'seat', 'seat_status',
              'seat_result']

def load_contributions(params, nolimit=False, ordering=True):
    
    start_time = time()

    per_page = min(int(params.get('per_page', DEFAULT_PER_PAGE)), MAX_PER_PAGE)
    page = int(params.get('page', 1)) - 1
    
    offset = page * per_page
    limit = offset + per_page
    
    for param in RESERVED_PARAMS:
        if param in params:
            del params[param]
            
    unquoted_params = dict([(param, unquote_plus(quoted_value)) for (param, quoted_value) in params.iteritems()])
    result = filter_contributions(unquoted_params)
    if ordering:
        result = result.order_by('-cycle','-amount')
    if not nolimit:
        result = result[offset:limit]
          
    return result


class ContributionStatsLogger(object):
    def __init__(self):
        self.stats = { 'total': 0 }
    def log(self, record):
        if isinstance(record, dict):
            ns = record.get('transaction_namespace', 'unknown')
        else:
            ns = getattr(record, 'transaction_namespace', 'unknown')
        self.stats[ns] = self.stats.get(ns, 0) + 1
        self.stats['total'] += 1

class ContributionFilterHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = CONTRIBUTION_FIELDS
    model = Contribution
    statslogger = ContributionStatsLogger
    
    def read(self, request):
        params = request.GET.copy()
        return load_contributions(params)
