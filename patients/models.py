from django.db import models
from users.models import CustomUser
from detection_kits.models import DetectionKit
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from markers.models import SingleNucPol
from detection_kits.models import DetectionKitMarkers, ConclusionsForSNP
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from patients.constants import allowed_chars
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

def check_if_rs_exists(value):
    if not SingleNucPol.objects.filter(rs=value).exists():
        raise ValidationError('this rs id does not exist in the database.\
             please, check "MARKERS" application.')


class PatientSample(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                      MaxValueValidator(122)])
    clinic_id = models.CharField(max_length=255, blank=True, null=True)
    lab_id = models.CharField(max_length=255, unique=True)
    date_sampled = models.DateField(help_text='USE CALENDAR WIDGET')
    date_delivered = models.DateField(help_text='USE CALENDAR WIDGET')
    dna_concentration = models.FloatField(validators=[MinValueValidator(0)])
    dna_quality_260_280 = models.FloatField(
                                            validators=[MinValueValidator(0.0),
                                            MaxValueValidator(3.0)])
    dna_quality_260_230 = models.FloatField(
                                            validators=[MinValueValidator(0.0),
                                            MaxValueValidator(3.0)])
    notes = models.TextField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, null=True,
                                   blank=True, on_delete=models.PROTECT)
    tests = models.ManyToManyField(DetectionKit,
                                   through='PatientSampleDetectionKit')
    date_created = models.DateTimeField(auto_now_add=True, editable=False, )
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Sample'
        verbose_name_plural = '3. Samples'

    def clean(self):
        if not self.date_sampled or not self.date_delivered:
            raise ValidationError('please fill in both sampling and delivery dates')
            
        if self.date_sampled > date.today():
            raise ValidationError(
                 f'check sampling date: sample can not be\
                 sampled in the future. date sampled: {self.date_sampled} '
                 )
        if self.date_delivered > date.today():
            raise ValidationError(
                f'check delivery date: sample can not be\
                 delivered in the future. date delivered:\
                 {self.date_delivered}'
                 )
        if self.date_sampled > self.date_delivered:
            raise ValidationError(
                'check sampling date: sample can not be\
                 sampled after delivery date'
                 )
        for char in self.lab_id:
            if char not in allowed_chars:
                raise ValidationError(
                    'use only english characters,\
                    numbers, underscore and hyphen for lab id'
                    )


class PatientSampleDetectionKit(models.Model):
    patient_sample = models.ForeignKey(PatientSample, null=True, on_delete=models.SET_NULL)
    test = models.ForeignKey(DetectionKit, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        kit_markers = self.test.linked_markers.all()

        for marker in kit_markers:
            if not ResultSNP.objects.filter(
                rs=marker.pk,
                test=self.test.pk,
                patient_sample=self.patient_sample.pk).exists():

                ResultSNP.objects.create(patient_sample=self.patient_sample,
                                         test=self.test,
                                         rs=marker,
                                         result=None)

    def __str__(self):
        return f'{self.test}'

    class Meta:
        verbose_name = 'Detection kit'
        verbose_name_plural = 'Detection kits'
        constraints = [models.UniqueConstraint(
                       fields=['patient_sample', 'test',],
                       name='patient_and_test_unique_constraint')]


class ResultSNP(models.Model):

    patient_sample = models.ForeignKey(PatientSample, on_delete=models.CASCADE)
    test = models.ForeignKey(DetectionKit, on_delete=models.CASCADE)
    rs = models.ForeignKey(SingleNucPol, on_delete=models.CASCADE)
    result = models.CharField(
                            max_length=4, blank=True, null=True,
                            help_text="use only English characters for result.\
                            USE NUCLEOTIDE ORDER DESIGNATED ABOVE")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SNP result'
        verbose_name_plural = '4. SNP results'

    def __str__(self):
        return f'patient: {self.patient_sample}.  SNP: {self.rs}.  result: {self.result}'

    def save(self, *args, **kwargs):
        update_obj = False
        if self.pk:
            update_obj = True

        super().save(*args, **kwargs)

        # not created automatically after patient creation
        if update_obj:
            results_snp = ResultSNP.objects.filter(
                test=self.test,
                    patient_sample=self.patient_sample)

            results = [obj.result for obj in results_snp]

            if all(results):  # look for conclusion creation only when snp results are updated,
                two_snp_conc = self.create_two_snp_report(results_snp=results_snp)
                one_snp_conc = self.create_one_snp_report(results_snp=results_snp)

                text = self.generate_text_for_conclusion(two_snp_conc, one_snp_conc)
             
                self.create_conclusion(text=text)
                

    def generate_text_for_conclusion(self, two_snp_conc, one_snp_conc):
        sep = '\n'
        space = ' '
        text = ''
        
        for report in two_snp_conc['two_snp_reports']:
            text += f"{report['snp_1_rs']} {space} {report['snp_1_gene']}{space} {report['snp_1_result']}{space} {report['snp_2_rs']}{space} {report['snp_2_gene']}{space} {report['snp_2_result']}"
            text += sep * 2
            text += report['conc']
            text += sep * 2
        text += sep * 3

        for category in one_snp_conc.keys():
            text += category
            text += sep * 2
            reports = one_snp_conc[category]
            for report in reports:
                text += f"{report['rs']} {space}{report['gene']} {space}{report['genotype']}"
                text += sep * 2
                text += report['conc']
       
        return text
        

    def clean(self):
        nuc_vars = [self.rs.nuc_var_1 + self.rs.nuc_var_1,
                    self.rs.nuc_var_2 + self.rs.nuc_var_2,
                    self.rs.nuc_var_1 + self.rs.nuc_var_2,]
        if self.result not in nuc_vars:
            raise ValidationError(
                'genotype is not correct. check: only uppercase letter,\
                     look at the order of nucleotides above')

    def create_one_snp_report(self, results_snp):
        det_kit_markers = DetectionKitMarkers.objects.filter(
            detection_kit=self.test).order_by(
                'category_order_in_conclusion','marker_order_in_category')

        results = {}
        current_category_name = None

        for det_kit_marker in det_kit_markers:
            if det_kit_marker.marker_category_in_kit not in results.keys():
                results[det_kit_marker.marker_category_in_kit] = []
                current_category_name = det_kit_marker.marker_category_in_kit
           
            marker_result = results_snp.get(rs=det_kit_marker.marker)
            result_genotype = marker_result.result

            concs_variants = ConclusionsForSNP.objects.filter(det_kit_marker=det_kit_marker)
            try:
                conc_for_result_genotype = concs_variants.get(genotype=result_genotype)
            except ObjectDoesNotExist:
                continue


            results[current_category_name].append({'rs': det_kit_marker.marker.rs,
                                                    'gene': det_kit_marker.marker.gene_name_short, 
                                                    'genotype': result_genotype,
                                                    'conc': conc_for_result_genotype.conclusion})
           
        return results
                    

    def create_two_snp_report(self, results_snp):
        two_snp_report = {'two_snp_reports': []}
        rules = ReportRuleTwoSNP.objects.filter(tests=self.test).order_by('order_in_conclusion')
        for rule in rules:
            combs = ReportCombinations.objects.filter(
                report_rule_two_snp=rule)
            # don't forget, here we get objects
            snp_1_rs = rule.snp_1
            snp_2_rs = rule.snp_2
            snp_1_result = results_snp.get(rs=snp_1_rs).result
            snp_2_result = results_snp.get(rs=snp_2_rs).result

            try:
                conclusion_for_result = combs.get(
                                        genotype_snp_1=snp_1_result,
                                        genotype_snp_2=snp_2_result)
            except ObjectDoesNotExist:
                raise ValidationError(
                    'seems like genotypes in results are not correct')

            two_snp_report['two_snp_reports'].append({
                                        'snp_1_rs': snp_1_rs.rs, 
                                        'snp_2_rs': snp_2_rs.rs, 
                                        'snp_1_gene': snp_1_rs.gene_name_short,
                                        'snp_2_gene': snp_2_rs.gene_name_short,
                                        'snp_1_result': snp_1_result,
                                        'snp_2_result': snp_2_result, 
                                        'conc': conclusion_for_result.report})
        return two_snp_report
    

    def create_conclusion(self, text):
        if not ConclusionSNP.objects.filter(
                                        patient=self.patient_sample,
                                        test=self.test).exists():
            ConclusionSNP.objects.create(
                                    patient=self.patient_sample,
                                    test=self.test, conclusion=text)
        else:
            conc_obj = ConclusionSNP.objects.get(
                patient=self.patient_sample, test=self.test)
            conc_obj.conclusion = text
            conc_obj.save()



class ReportRuleTwoSNP(models.Model):
    ORDER_FOR_CONCLUSION = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
    )

    name = models.CharField(max_length=255, unique=True)
    tests = models.ManyToManyField(DetectionKit, related_name='report_rules')
    snp_1 = models.ForeignKey(SingleNucPol, on_delete=models.CASCADE,
                              related_name='report_rules_snp_1')
    snp_2 = models.ForeignKey(SingleNucPol, on_delete=models.CASCADE,
                              related_name='report_rules_snp_2')
    note = models.TextField(max_length=1000)
    order_in_conclusion = models.IntegerField(default=1,
                                              choices=ORDER_FOR_CONCLUSION)

    class Meta:
        verbose_name = 'Report rule for two SNP'
        verbose_name_plural = '1. Report rules for two SNP'

    def __str__(self):
        return f'report rule: {self.name}'

    def detection_kits(self):
        return "\n".join([kit.name for kit in self.tests.all()])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        snp_1 = self.snp_1
        snp_2 = self.snp_2
        genotypes_snp_1 = [snp_1.nuc_var_1 + snp_1.nuc_var_1,
                           snp_1.nuc_var_1 + snp_1.nuc_var_2,
                           snp_1.nuc_var_2 + snp_1.nuc_var_2]
        genotypes_snp_2 = [snp_2.nuc_var_1 + snp_2.nuc_var_1,
                           snp_2.nuc_var_1 + snp_2.nuc_var_2,
                           snp_2.nuc_var_2 + snp_2.nuc_var_2]

        genotypes_combs_in_list = []
        for genotype_snp_1 in genotypes_snp_1:
            for genotype_snp_2 in genotypes_snp_2:
                genotypes_combs_in_list.append((genotype_snp_1, genotype_snp_2))

        report_combinations = ReportCombinations.objects.filter(
            report_rule_two_snp=self).order_by('pk')
        if report_combinations:
            comb_counter = 0
            for report_comb in report_combinations:
                report_comb.genotype_snp_1 = genotypes_combs_in_list[
                                            comb_counter][0]
                report_comb.genotype_snp_2 = genotypes_combs_in_list[
                                            comb_counter][1]
                report_comb.save()
                comb_counter += 1
        else:
            for genotype_snp_1 in genotypes_snp_1:
                for genotype_snp_2 in genotypes_snp_2:

                    ReportCombinations.objects.create(
                            report_rule_two_snp=self,
                            genotype_snp_1=genotype_snp_1,
                            genotype_snp_2=genotype_snp_2
                            )


class ReportCombinations(models.Model):
    report_rule_two_snp = models.ForeignKey(ReportRuleTwoSNP,
                                            on_delete=models.CASCADE)
    genotype_snp_1 = models.CharField(max_length=2, blank=True, null=True)
    genotype_snp_2 = models.CharField(max_length=2, blank=True, null=True)
    report = models.TextField(max_length=10000, blank=True, null=True)

    class Meta:
        verbose_name = 'report rules: conclusions for genotype combinations'
        verbose_name_plural = '2. report rules: conclusions for genotype combinations'

    def __str__(self):
        return self.report_rule_two_snp.name


class ConclusionSNP(models.Model):
    patient = models.ForeignKey(PatientSample, on_delete=models.CASCADE)
    test = models.ForeignKey(DetectionKit, on_delete=models.CASCADE)
    conclusion = models.TextField(max_length=20000)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'conclusion for report'
        verbose_name_plural = '5. Conclusions for reports'
        constraints = [models.UniqueConstraint(
            fields=['patient', 'test', ],
            name='patient_and_test_unique_constraint_for_conclusion')]

    def __str__(self):
        return f'conclusion for: {self.patient}, test: {self.test}'
