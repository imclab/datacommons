from dcapi.aggregates.handlers import execute_top
from dcentity.models import Entity, EntityAttribute, OrganizationMetadata
from piston.handler import BaseHandler
from piston.utils import rc
from urllib import unquote_plus

import time
import sys


get_totals_stmt = """
    select cycle, contributor_count, recipient_count, contributor_amount, recipient_amount, l.count as lobbying_count, firm_income, non_firm_spending
    from agg_entities c
    full outer join agg_lobbying_totals l using (entity_id, cycle)
    where
        entity_id = %s
"""

def get_totals(entity_id):
    totals = dict()
    for row in execute_top(get_totals_stmt, entity_id):
        totals[row[0]] = dict(zip(EntityHandler.totals_fields, row[1:]))
    return totals


def get_type_specific_metadata(entity):
    if entity.type == 'organization':
        return {'lobbying_firm': bool(OrganizationMetadata.objects.filter(entity=entity.id, lobbying_firm=True))}
    else:
        return {}


class EntityHandler(BaseHandler):
    allowed_methods = ('GET',)

    totals_fields = ['contributor_count', 'recipient_count', 'contributor_amount', 'recipient_amount', 'lobbying_count', 'firm_income', 'non_firm_spending']
    ext_id_fields = ['namespace', 'id']

    def read(self, request, entity_id):

        t1 = time.time()
        entity = Entity.objects.select_related().get(id=entity_id)

        t2 = time.time()
        totals = get_totals(entity_id)

        t3 = time.time()
        external_ids = [{'namespace': attr.namespace, 'id': attr.value} for attr in entity.attributes.all()]

        t4 = time.time()
        metadata = get_type_specific_metadata(entity)

        t5 = time.time()

        sys.stdout.write("EntityHandler(): (%s, %s, %s, %s)\n" % (t2-t1, t3-t2, t4-t3, t5-t4))

        result = {'name': entity.name,
                  'id': entity.id,
                  'type': entity.type,
                  'totals': totals,
                  'external_ids': external_ids,
                  'metadata': metadata}

        return result


class EntityAttributeHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ['id']

    def read(self, request):
        namespace = request.GET.get('namespace', None)
        id = request.GET.get('id', None)

        if not id or not namespace:
            error_response = rc.BAD_REQUEST
            error_response.write("Must include a 'namespace' and an 'id' parameter.")
            return error_response

        attributes = EntityAttribute.objects.filter(namespace = namespace, value = id, verified = 't')

        return [{'id': a.entity_id} for a in attributes]


class EntitySearchHandler(BaseHandler):
    allowed_methods = ('GET',)

    fields = [
        'id', 'name', 'type',
        'count_given', 'count_received', 'count_lobbied',
        'total_given','total_received', 'firm_income', 'non_firm_spending',
        'state', 'party', 'seat', 'lobbying_firm'
    ]

    stmt = """
        select
            e.id, e.name, e.type,
            a.contributor_count, a.recipient_count, coalesce(l.count, 0),
            a.contributor_amount, a.recipient_amount, l.firm_income, l.non_firm_spending,
            pm.state, pm.party, pm.seat, om.lobbying_firm
        from matchbox_entity e
        left join matchbox_politicianmetadata pm
            on e.id = pm.entity_id
        left join matchbox_organizationmetadata om
            on e.id = om.entity_id
        left join agg_lobbying_totals l
            on e.id = l.entity_id
        left join agg_entities a
            on e.id = a.entity_id
        where
            a.cycle = -1
            and (l.cycle is null or l.cycle = -1)
            and to_tsvector('datacommons', e.name) @@ to_tsquery('datacommons', %s)
    """

    def read(self, request):
        query = request.GET.get('search', None)
        if not query:
            error_response = rc.BAD_REQUEST
            error_response.write("Must include a query in the 'search' parameter.")
            return error_response

        parsed_query = ' & '.join(unquote_plus(query).split(' '))

        raw_result = execute_top(self.stmt, parsed_query)

        return [dict(zip(self.fields, row)) for row in raw_result]


