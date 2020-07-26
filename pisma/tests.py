from typing import List

from django.test import TestCase

from pisma.models import PegaNode


class PegaNodeTestCase(TestCase):
    def setUp(self) -> None:
        PegaNode.objects.create(name='SANDBOX', production_level=PegaNode.ProductionLevels.SANDBOX)
        PegaNode.objects.create(name='DEVELOPMENT', production_level=PegaNode.ProductionLevels.DEVELOPMENT)
        PegaNode.objects.create(name='QA', production_level=PegaNode.ProductionLevels.QA)
        PegaNode.objects.create(name='PRELIVE', production_level=PegaNode.ProductionLevels.PRELIVE)
        PegaNode.objects.create(name='PRODUCTION', production_level=PegaNode.ProductionLevels.PRODUCTION)

    def test_production_levels(self):
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
