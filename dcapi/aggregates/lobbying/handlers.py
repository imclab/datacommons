
from dcapi.aggregates.handlers import TopListHandler


class OrgRegistrantsHandler(TopListHandler):
    fields = ['registrant_name', 'registrant_entity', 'amount']
    
    stmt = """
        select registrant_name, registrant_entity, amount
        from agg_lobbying_registrants_for_client
        where
            client_entity = %s
            and cycle = %s
        order by amount desc
        limit %s
    """


class OrgIssuesHandler(TopListHandler):
    fields = ['issue', 'count']
    
    stmt = """
        select issue, count
        from agg_lobbying_issues_for_client
        where
            client_entity = %s
            and cycle = %s
        order by count desc
        limit %s
    """


class OrgLobbyistsHandler(TopListHandler):
    
    fields = ['lobbyist_name', 'lobbyist_entity', 'count']

    stmt = """
        select lobbyist_name, lobbyist_entity, count
        from agg_lobbying_lobbyists_for_client
        where
            client_entity = %s
            and cycle = %s
        order by count desc
        limit %s    
    """
    
class IndivRegistrantsHandler(TopListHandler):
    
    fields = ['lobbyist_entity', 'cycle', 'registrant_name', 'registrant_entity', 'count']
    
    stmt = """
        select lobbyist_entity, cycle, registrant_name, registrant_entity, count
        from agg_lobbying_registrants_for_lobbyist
        where
            lobbyist_entity = %s
            and cycle = %s
        order by count desc
        limit %s
    """
    
class IndivIssuesHandler(TopListHandler):
    
    fields = ['lobbyist_entity', 'cycle', 'issue', 'count']
    
    stmt = """
        select lobbyist_entity, cycle, issue, count
        from agg_lobbying_issues_for_lobbyist
        where
            lobbyist_entity = %s
            and cycle = %s
        order by count desc
        limit %s
    """
    
class IndivClientsHandler(TopListHandler):        
    
    fields = ['lobbyist_entity', 'cycle', 'client_name', 'client_entity', 'count']
    
    stmt = """
        select lobbyist_entity, cycle, client_name, client_entity, count
        from agg_lobbying_clients_for_lobbyist
        where
            lobbyist_entity = %s
            and cycle = %s
        order by count desc
        limit %s
    """        
    
    