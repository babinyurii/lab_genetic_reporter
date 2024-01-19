from django.test import TestCase
from results.models import ResultSNP
from patients.models import PatientSample
from detection_kits.models import DetectionKit
import datetime


 
class TestResultSNPModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.patient = PatientSample.objects.create(
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            age=42,
            clinic_id='patient 404',
            lab_id='aa67',
            date_sampled=datetime.date(2023, 12, 31),
            date_delivered=datetime.date(2024, 1, 1),
            dna_concentration=70,
            dna_quality_260_280=1.8,
            dna_quality_260_230=2.0,
            notes='sample is not frozen',
            created_by=None,
        )  

        cls.detection_kit = DetectionKit.objects.create(
            name='GeneKit',
            date_created=datetime.date(2023, 12, 31),
            created_by=None,
        ) 

        cls.result_snp = ResultSNP.objects.create(
            patient_sample=cls.patient,
            test=cls.detection_kit,
            rs='rs1',
            result='GA',
        )

    def test_resultsnp_model(self):
        self.assertEqual(self.result_snp.patient_sample, self.patient)
        self.assertEqual(self.result_snp.test, self.detection_kit)
        self.assertEqual(self.result_snp.rs, 'rs1')
        self.assertEqual(self.result_snp.result, 'GA')
