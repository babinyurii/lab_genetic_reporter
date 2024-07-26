
from django import forms
from django.core.exceptions import ValidationError
from patients.models import ReportRuleTwoSNP, ResultSNP


class ResultSNPForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResultSNPForm, self).__init__(*args, **kwargs)
      
        CHOICES = [(self.instance.rs.nuc_var_1 + self.instance.rs.nuc_var_1,) * 2,
                    (self.instance.rs.nuc_var_1 + self.instance.rs.nuc_var_2,) * 2,
                    (self.instance.rs.nuc_var_2 + self.instance.rs.nuc_var_2,) * 2,]
        self.fields['result'] = forms.ChoiceField(
            choices=CHOICES)

 

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

        if snp_1 == snp_2:
            raise ValidationError(f'field snp_1 {snp_1} and field snp_2 \
                {snp_2} are the same. Choose different markers')
        if not kits:
            raise ValidationError('choose kit')
        if not self.instance.pk:
            for kit in kits:
                if ReportRuleTwoSNP.objects.filter(
                    snp_1=snp_1, snp_2=snp_2, tests=kit).exists() or \
                    ReportRuleTwoSNP.objects.filter(
                        snp_1=snp_2, snp_2=snp_1, tests=kit).exists():
                    raise ValidationError(
                        f'the database already has the record with the kit:\
                             "{kit}",  snp 1:  "{snp_1}",  snp 2:  "{snp_2}"')

            for snp in snps:
                if not kit.linked_markers.filter(rs=snp.rs).exists():
                    raise ValidationError(
                        f'snp : "{snp}" is not in the kit: "{kit}"')

        return data
