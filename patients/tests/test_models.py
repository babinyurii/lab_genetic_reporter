import datetime
from django.test import TestCase
from detection_kits.models import DetectionKit
from markers.models import SingleNucPol
from patients.models import (PatientSample, 
                            PatientSampleDetectionKit, 
                            ResultSNP, 
                            ReportRuleTwoSNP, 
                            ReportCombinations, 
                            ConclusionSNP)


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
        )

        cls.snp_1 = SingleNucPol.objects.create(rs='rs1', gene_name_short='GENE1',
            nuc_var_1='G', nuc_var_2='A') 
        cls.snp_2 = SingleNucPol.objects.create(rs='rs2', gene_name_short='GENE2',
            nuc_var_1='C', nuc_var_2='T')
        cls.snp_3 = SingleNucPol.objects.create(rs='rs3', gene_name_short='GENE3',
            nuc_var_1='T', nuc_var_2='A')


        cls.detection_kit = DetectionKit.objects.create(
            name='GeneKit',
            date_created=datetime.date(2023, 12, 31),
            created_by=None,
        )

        cls.detection_kit.markers.add(cls.snp_1)
        cls.detection_kit.markers.add(cls.snp_2)
        cls.detection_kit.markers.add(cls.snp_3)

        cls.patient.tests.add(cls.detection_kit) 


        cls.result_snp = ResultSNP.objects.create(
            patient_sample=cls.patient,
            test=cls.detection_kit,
            rs='rs1',
            result='GA',
        )

        cls.report_rule = ReportRuleTwoSNP.objects.create(
            name='COL1 and MMP1 report rule',
            snp_1='rs1',
            snp_2='rs2',
            note='test rule'
        )

        cls.report_rule.tests.add(cls.detection_kit)

        cls.conc = ConclusionSNP.objects.create(
            patient=cls.patient,
            test=cls.detection_kit,
            conclusion='test conclusion'
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
        self.assertEqual(self.patient.tests.get(pk=self.patient.pk), self.detection_kit)


    def test_patientsampledetectionkit_model(self):
        patientsample_detectionkit = PatientSampleDetectionKit.objects.get(patient_sample=self.patient)
        patientsample_detectionkit.save() # call explicitly to trigger results records generating and saving
        print('all records from results: ', patientsample_detectionkit)

        detection_kit = DetectionKit.objects.get(pk=patientsample_detectionkit.test.pk)
        print(detection_kit)
        markers = detection_kit.markers.all()
        print('markers: ', markers)
        
        rs_ids = []
        for marker in markers:
            rs_ids.append(marker.rs)
        print('rs_ids: ', rs_ids)
        # добавлять маркеры в другой список: сравнить после длину
        result_records = ResultSNP.objects.filter(patient_sample=self.patient.pk, test=self.detection_kit.pk)
        print('result records list from QUERY: ', result_records)
        rs_from_results_table = []
        for record in result_records:
            print('record in LOOP: ', record)
            self.assertEqual(record.test, self.detection_kit)
            self.assertEqual(record.patient_sample, self.patient)
            self.assertIn(record.rs, rs_ids)
            print('record.rs: ', record.rs)
            rs_from_results_table.append(record.rs)
        self.assertEqual(len(rs_ids), len(rs_from_results_table))
        print('rs_ids: ', rs_ids, flush=True)
        print('rs_from_through: ', rs_from_results_table, flush=True)

    def test_resultsnp_model(self):
        self.assertEqual(self.result_snp.patient_sample, self.patient)
        self.assertEqual(self.result_snp.test, self.detection_kit)
        self.assertEqual(self.result_snp.rs, 'rs1')
        self.assertEqual(self.result_snp.result, 'GA')

    def test_reportruletwosnp_model(self):
        self.assertEqual(self.report_rule.name, 'COL1 and MMP1 report rule')
        self.assertEqual(self.report_rule.snp_1, 'rs1')
        self.assertEqual(self.report_rule.snp_2, 'rs2')
        self.assertEqual(self.report_rule.note, 'test rule')


    def test_reportcombinations(self):
        report_rule = self.detection_kit.report_rules.all()[0]
        print('report rules: ', report_rule)
        report_combs = ReportCombinations.objects.filter(report_rule_two_snp=report_rule.pk)
        print(report_combs)
        self.assertEqual(len(report_combs), 9)

        genotypes_snp_1 = [self.snp_1.nuc_var_1 + self.snp_1.nuc_var_1,
                    self.snp_1.nuc_var_1 + self.snp_1.nuc_var_2,
                    self.snp_1.nuc_var_2 + self.snp_1.nuc_var_2]
        genotypes_snp_2 = [self.snp_2.nuc_var_1 + self.snp_2.nuc_var_1,
                    self.snp_2.nuc_var_1 + self.snp_2.nuc_var_2,
                    self.snp_2.nuc_var_2 + self.snp_2.nuc_var_2]

        # collect genotypes combinations from report combs objects
        genotypes_combinations = []
        for report_comb in report_combs:
            genotypes_combinations.append((report_comb.genotype_snp_1, 
                                            report_comb.genotype_snp_2,),)

        for genotype_snp_1 in genotypes_snp_1:
            for genotype_snp_2 in genotypes_snp_2:
                self.assertIn((genotype_snp_1, genotype_snp_2,), genotypes_combinations)


    def test_conclusionsnpmodel(self):
        self.assertEqual(self.conc.patient, self.patient)
        self.assertEqual(self.conc.test, self.detection_kit)
        self.assertEqual(self.conc.conclusion, 'test conclusion')



















