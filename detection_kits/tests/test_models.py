from django.test import TestCase
from detection_kits.models import (DetectionKit, 
                                   DetectionKitMarkers,
                                   ConclusionsForSNP)
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
            #date_created=datetime.date(2023, 12, 31),
            created_by=None,
            kit_type='SNP', 
        )

        cls.detection_kit.linked_markers.add(cls.snp) 


    def test_detectionkit_model(self):
        self.assertEqual(self.detection_kit.name, 'GeneKit')
        #self.assertEqual(self.detection_kit.date_created, datetime.date(2023, 12, 31))
        self.assertEqual(self.detection_kit.created_by, None)
        self.assertEqual(self.detection_kit.linked_markers.get(pk=self.snp.pk), self.snp)
        self.assertEqual(self.detection_kit.kit_type, 'SNP')


    def test_conc_for_snp_table_creation(self):

        #print('*' * 100, self.detection_kit.linked_markers.all(), flush=True)
        det_kit_marker = DetectionKitMarkers.objects.all()[0]
        #print('*' * 100, det_kit_marker, flush=True)
        det_kit_marker.save()
        concs = ConclusionsForSNP.objects.all()
        genotypes_in_concs = ConclusionsForSNP.objects.values_list('genotype', flat=True)
        #print("=" * 100, genotypes_in_concs, flush=True)

        self.assertEqual(len(concs), 3)
        for genotype in ['CC', 'CA', 'AA']:
            self.assertIn(genotype, genotypes_in_concs)





    





