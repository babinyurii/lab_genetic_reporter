from django.test import TestCase
from patients.models import PatientSample
import datetime


class TestPatientSampleModel(TestCase):
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
            #tests=None,
        )

    def test_patientsamplemodel(self):
        self.assertEqual(self.patient.first_name, 'test_first_name')
        self.assertEqual(self.patient.last_name, 'test_last_name')
        self.assertEqual(self.patient.middle_name, 'test_middle_name')
        self.assertEqual(self.patient.age, 42)
        self.assertEqual(self.patient.clinic_id, 'patient 404')
        self.assertEqual(self.patient.lab_id, 'aa67')
        self.assertEqual(self.patient.date_sampled, datetime.date(2023, 12, 31))
        self.assertEqual(self.patient.date_delivered, datetime.date(2024, 1, 1))
        self.assertEqual(self.patient.dna_concentration, 70)
        self.assertEqual(self.patient.dna_quality_260_280, 1.8)
        self.assertEqual(self.patient.dna_quality_260_230, 2.0)
        self.assertEqual(self.patient.notes, 'sample is not frozen')
        self.assertEqual(self.patient.created_by, None)
        #self.assertEqual(self.patient.tests, None)



