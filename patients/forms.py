
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
        if not self.instance.pk:
            for kit in kits:
                #if ReportRuleTwoSNP.objects.filter(order_in_conclusion=order_in_conclusion).exists():
                #    raise ValidationError(f'the report rule with the value {order_in_conclusion} of order in conclusion already exists. Choose another one')
                if ReportRuleTwoSNP.objects.filter(snp_1=snp_1, snp_2=snp_2, tests=kit).exists() or \
                    ReportRuleTwoSNP.objects.filter(snp_1=snp_2, snp_2=snp_1, tests=kit).exists():
                    raise ValidationError(f'the database already has the record with the kit:  "{kit}",  snp 1:  "{snp_1}",  snp 2:  "{snp_2}"')

            for snp in snps:
                if not kit.markers.filter(rs=snp.rs).exists():
                    raise ValidationError(f'snp : "{snp}" is not in the kit: "{kit}"')
        
        return data
    