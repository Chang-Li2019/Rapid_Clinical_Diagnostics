# start pipeline tier 1 & 2    
for key,value in var_list.items():
    if key in clinvar:
        cur_clinvar[key] = clinvar[key] 
    if key in hgmd:
        cur_hgmd[key] = hgmd[key] 
    if key not in clinvar and key not in hgmd:
        no_var_list[key] = 0

for key,value in cur_clinvar.items():
    if value[2].lower() in phenotype:
        yes_var_list[key] = 0
    else:
        no_var_list[key] = 0
for key,value in cur_hgmd.items():
    if value[3].lower() in phenotype:
        yes_var_list[key] = 0
    else:
        no_var_list[key] = 0
        
if len(yes_var_list)>0:
    for key,value in yes_var_list.items():
        if key in parents_var:
            tier1.write(key+'\n')
        else:
            tier2.write(key+'\n')
tier1.close()
tier2.close()
# damaging

def damaging(position_identifier):
    key = position_identifier
    if key in dbnsfp_damaging:
        return True
    if (key in anno_conseq and anno_conseq[key]==1) or (key in snpeff_conseq and snpeff_conseq[key]==1) or (key in vep_conseq and vep_conseq[key]==1):
        return True
# tier 3
for key,value in no_var_list.items():
    if key in dbnsfp_gene and dbnsfp_gene[key] in r_gene:
        if damaging(key):
            print('single:',key)
            tier3.write(key+'\n')
            entries_to_remove(key,no_var_list)
    elif key in indel_gene:
        anno_genes = indel_gene[key][0].split('|')
        snpeff_genes = indel_gene[key][1].split('|')
        vep_genes = indel_gene[key][2].split('|')
        for genes in r_gene:
            if (genes in anno_genes or genes in snpeff_genes or genes in vep_genes):
                if damaging(key):
                    print('indel:',key)
                    tier3.write(key+'\n')
                    entries_to_remove(key,no_var_list)
tier3.close()
