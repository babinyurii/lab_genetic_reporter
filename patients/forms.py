
from django import forms
from django.core.exceptions import ValidationError
from patients.models import ReportRuleTwoSNP, ResultSNP
from detection_kits.models import DetectionKit

class ReportRuleForm(forms.ModelForm):

    class Meta:
        model = ReportRuleTwoSNP
        fields = ('name', 'snp_1', 'snp_2', 'tests',)
        widgets = {
            'tests': forms.CheckboxSelectMultiple(),
        }

   
    def clean(self):
        snp_1 = self.cleaned_data.get('snp_1')
        snp_2 = self.cleaned_data.get('snp_2')
        snps = [snp_1, snp_2]
        kits = self.cleaned_data.get('tests')


        if snp_1 == snp_2:
            raise ValidationError(f'field snp_1 {snp_1} and field snp_2 {snp_2} are the same. Choose different markers')
        for kit in kits:
            if ReportRuleTwoSNP.objects.filter(snp_1=snp_1, snp_2=snp_2, tests=kit).exists() or \
                ReportRuleTwoSNP.objects.filter(snp_1=snp_2, snp_2=snp_1, tests=kit).exists():
                raise ValidationError(f'the database already has the record with "{kit}", "{snp_1}", "{snp_2}"')

            for snp in snps:
                if not kit.markers.filter(rs=snp.rs).exists():
                    raise ValidationError(f'snp : "{snp}" is not in the kit: "{kit}"')
        
        return self.cleaned_data
    