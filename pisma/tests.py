from typing import List

from django.test import TestCase

from pisma.models import PegaNode
from pisma.views.services import get_default_context


class PegaNodeTestCase(TestCase):
    """
    Test PegaNode db interactions
    """
    def setUp(self) -> None:
        PegaNode.objects.create(name='SANDBOX', production_level=PegaNode.ProductionLevels.SANDBOX)
        PegaNode.objects.create(name='DEVELOPMENT', production_level=PegaNode.ProductionLevels.DEVELOPMENT)
        PegaNode.objects.create(name='QA', production_level=PegaNode.ProductionLevels.QA)
        PegaNode.objects.create(name='PRELIVE', production_level=PegaNode.ProductionLevels.PRELIVE)
        PegaNode.objects.create(name='PRODUCTION', production_level=PegaNode.ProductionLevels.PRODUCTION)

    def test_names(self):
        """
        Test PegaNode names
        """
        all_nodes: List[PegaNode] = PegaNode.objects.all()

        for node in all_nodes:
            self.assertEqual(node.name, str(node))

    def test_production_levels(self):
        """
        Test PegaNode production level choices
        """
        all_nodes: List[PegaNode] = PegaNode.objects.all()

        for node in all_nodes:
            if node.name == 'SANDBOX':
                self.assertEqual(node.production_level, 1)
                continue

            if node.name == 'DEVELOPMENT':
                self.assertEqual(node.production_level, 2)
                continue

            if node.name == 'QA':
                self.assertEqual(node.production_level, 3)
                continue

            if node.name == 'PRELIVE':
                self.assertEqual(node.production_level, 4)
                continue

            if node.name == 'PRODUCTION':
                self.assertEqual(node.production_level, 5)
                continue

    def test_get_default_context(self):
        """
        Test get_default_context() view service without node_id param
        """
        all_nodes: List[PegaNode] = PegaNode.objects.all()

        context = get_default_context()
        for node in all_nodes:
            self.assertIn(node, context['nodes'])

    def test_get_default_context_for_node(self):
        """
        Test get_default_context() view service with node_id param
        """
        all_nodes: List[PegaNode] = PegaNode.objects.all()

        for node in all_nodes:
            context = get_default_context(node_id=node.id)
            self.assertIn(node, context['nodes'])
            self.assertEqual(node, context['node'])
