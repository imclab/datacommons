

from datetime import datetime
import unittest
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from dcdata.contribution.models import Contribution, sql_names
from dcdata.models import Import
from models import Entity, EntityAlias, EntityAttribute, Normalization
from queries import _prepend_pluses
from matchbox_scripts.support.build_entities import populate_entities
from matchbox_scripts.support.normalize_database import normalize
from strings.normalizer import basic_normalizer
from matchbox.queries import search_entities_by_name



class TestQueries(unittest.TestCase):

    def save_contribution(self, org_name):
        c = Contribution(organization_name=org_name, 
                     datestamp=datetime.now(),
                     cycle='09', 
                     import_reference=self.import_)
        c.save()
        

    def setUp(self):
        """ 
        to do: set up some basic transactions, the run the build_entities and normalize scripts.
        
        Also add an entity with no corresponding transactions.
        """
        
        print("Setting up database...")
        Import.objects.all().delete()
        Contribution.objects.all().delete()
        Entity.objects.all().delete()
        EntityAlias.objects.all().delete()
        EntityAttribute.objects.all().delete()
        Normalization.objects.all().delete()
        
        self.import_ = Import()
        self.import_.save()
        
        for org_name in ['Apple', 'Apple', 'Apricot']:
            self.save_contribution(org_name)

        populate_entities(sql_names['contribution'], 
                          sql_names['contribution_organization_name'], 
                          sql_names['contribution_organization_entity'], 
                          [sql_names['contribution_organization_name']])
        
        orphan = Entity(name=u'Avacado')
        orphan.aliases.create(alias=u'Avacado')
        orphan.save()
        
        normalize([('entityalias', ['entityalias_alias'])], basic_normalizer)
        
        
    def test_populate_entities(self):
        self.assertEqual(3, Entity.objects.count())
        
        apple = Entity.objects.get(name="Apple")
        self.assertEqual(2, apple.organization_transactions.count())
        
        apple_alias = EntityAlias.objects.get(alias="Apple")
        self.assertEqual(apple.id, apple_alias.entity.id)

        apricot = Entity.objects.get(name="apricot")
        self.assertEqual(1, apricot.organization_transactions.count())
        
        apricot_alias = EntityAlias.objects.get(alias="apricot")
        self.assertEqual(apricot.id, apricot_alias.entity.id)
        
        avacado = Entity.objects.get(name='avacado')
        self.assertEqual(0, avacado.organization_transactions.count())
        

    def test_search_entities_by_name(self):
        rows = search_entities_by_name(u'a')
        
        expected = [['Apple', 2], ['Apricot', 1], ['Avacado', 0]]
        
        for ((expected_name, expected_count), (id, name, count)) in zip(expected, rows):
            self.assertEqual(expected_name, name)
            self.assertEqual(expected_count, count)
    
    
class TestUtils(unittest.TestCase):
    def test_prepend_pluses(self):
        self.assertEqual("", _prepend_pluses(""))
        self.assertEqual("", _prepend_pluses("   "))
        
        self.assertEqual("+a", _prepend_pluses("a"))
        self.assertEqual("+apple +computer", _prepend_pluses("apple computer"))
        self.assertEqual("+apple +computer, +inc.", _prepend_pluses("apple computer, inc."))
        self.assertEqual("+Procter +& +Gamble", _prepend_pluses("Procter & Gamble"))
        self.assertEqual("+Emily's +List", _prepend_pluses("Emily's List"))
        