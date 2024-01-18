from django.test import TestCase
from detection_kits.models import DetectionKit
from markers.models import SingleNucPol
import datetime


class TestDetectionKitModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snp = SingleNucPol.objects.create(
            rs = 'rs1800012',
            gene_name_short = 'COL1A1', 
            gene_name_full = 'first type collagen',
            nuc_var_1 = 'C',
            nuc_var_2 = 'A',
            nuc_var_1_freq = 0.83,
            nuc_var_2_freq = 0.17,
            db_snp_link = 'https://www.ncbi.nlm.nih.gov/snp/rs1800012',

        )

        cls.detection_kit = DetectionKit.objects.create(
            name='GeneKit',
            date_created=datetime.date(2023, 12, 31),
            created_by=None,
            
        )

        cls.detection_kit.markers.add(cls.snp) 


    def test_detectionkit_model(self):
        self.assertEqual(self.detection_kit.name, 'GeneKit')
        self.assertEqual(self.detection_kit.date_created, datetime.date(2023, 12, 31))
        self.assertEqual(self.detection_kit.created_by, None)
        self.assertEqual(self.detection_kit.markers.get(pk=self.snp.pk), self.snp)

