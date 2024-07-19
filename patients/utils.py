

def generate_text_for_conclusion(two_snp_conc, one_snp_conc):
        sep = '\n'
        space = ' '
        text = ''
        category_sep = '='
        snp_sep = '-'
        
        for report in two_snp_conc['two_snp_reports']:
            text += f"SNP1: {report['snp_1_rs']} {space} {report['snp_1_gene']}{space} \
                {report['snp_1_result']}{space} {sep} SNP2:  {report['snp_2_rs']}{space} {report['snp_2_gene']}{space}\
                     {report['snp_2_result']}"
            text += sep * 2
            text += report['conc']
            text += sep * 2 
            text += snp_sep * 50 + sep
        text += category_sep * 50 + sep

        for category in one_snp_conc.keys():
            text += category
            text += sep * 2
            reports = one_snp_conc[category]
            for report in reports:
                text += f"{report['rs']} {space}{report['gene']} {space}{report['genotype']}"
                text += sep * 1
                text += report['conc']
                text += sep * 2
                text += snp_sep * 50 + sep
                
        return text