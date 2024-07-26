

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
        if report['conc'] is not None:
            text += report['conc']
        else:
            text += 'None, no conclusion in db'
        text += sep * 2 
        text += snp_sep * 50 + sep
    text += category_sep * 50 + sep
    
    #print(one_snp_conc, flush=True)
    for category in one_snp_conc.keys():
        if category is not None:
            text += category
        # TODO logging: if category not chosen before - into warning
        else:
            text += 'None, no category selected'
        text += sep * 2
        reports = one_snp_conc[category]
        for report in reports:
            text += f"{report['rs']} {space}{report['gene']} {space}{report['genotype']}"
            text += sep * 1
            if report['conc'] is not None:
                text += report['conc']
            # TODO logging: if conclusion was not created by user not chosen before - into warning
            else:
                text += 'None, no conclusion is db'
            text += sep * 2
            text += snp_sep * 50 + sep
            
    return text