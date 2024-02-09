
from django import forms
from django.core.exceptions import ValidationError
from patients.models import ReportRuleTwoSNP, ResultSNP
from detection_kits.models import DetectionKit

class ReportRuleForm(forms.ModelForm):

    class Meta:
        model = ReportRuleTwoSNP
        fields = ('name', 'snp_1', 'snp_2', 'order_in_conclusion', 'tests')
        widgets = {
            'tests': forms.CheckboxSelectMultiple(),
        }
    
  
    def clean(self):
        data = self.cleaned_data
        snp_1 = data.get('snp_1')
        snp_2 = data.get('snp_2')
        snps = [snp_1, snp_2]
        kits = data.get('tests')
        order_in_conclusion = data.get('order_in_conclusion')


        if snp_1 == snp_2:
            raise ValidationError(f'field snp_1 {snp_1} and field snp_2 {snp_2} are the same. Choose different markers')

        if not kits:
            raise ValidationError('choose kit')
        for kit in kits:

            if ReportRuleTwoSNP.objects.filter(snp_1=snp_1, snp_2=snp_2, tests=kit, order_in_conclusion=order_in_conclusion).exists() or \
                ReportRuleTwoSNP.objects.filter(snp_1=snp_2, snp_2=snp_1, tests=kit, order_in_conclusion=order_in_conclusion).exists():
                raise ValidationError(f'the database already has the record with "{kit}", "{snp_1}", "{snp_2}", and order: "{order_in_conclusion}"')

            for snp in snps:
                if not kit.markers.filter(rs=snp.rs).exists():
                    raise ValidationError(f'snp : "{snp}" is not in the kit: "{kit}"')
        
        return data
    