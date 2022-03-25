#!/bin/env python3

import os
import sys
import itertools

date = os.getcwd().split("/")[-1]

spike_variants_dict = {"Alpha" : ['203-208Del(IHV68-70I--)', '429-431Del(VY143-144V-)', 'A1501T(N501Y)', 'C1709A(A570D)', 'A1841G(D614G)', 'C2042A(P681H)', 'C2147T(T716I)', 'T2944G(S982A)', 'G3352C(D1118H)'],
                    "Beta"      :   ['A239C(D80A)', 'A644G(D215G)', '719-727Del(TLLA240-243T---)', 'G1251T(K417N)', 'G1450A(E484K)', 'A1501T(N501Y)', 'A1841G(D614G)', 'C2102T(A701V)'],
                    "Gamma"     :   ['C52T(L18F)', 'C59A(T20N)', 'C76T(P26S)', 'G412T(D138Y)', 'G570T(R190S)', 'A1250C(K417T)', 'G1450A(E484K)', 'A1501T(N501Y)', 'A1841G(D614G)', 'C1963T(H655Y)', 'C3080T(T1027I)', 'G3526T(V1176F)'],
                    "Delta"     :   ['C56G(T19R)', '467-472Del(EFR156-158G--)', 'T1355G(L452R)', 'C1433A(T478K)', 'A1841G(D614G)', 'C2042G(P681R)', 'G2848A(D950N)'],
                    "Omicron(BA.1)"   :   ['C200T(A67V)', '203-208Del(IHV68-70I--)', 'C284T(T95I)', '425-433Del(GVYY142-145D---)', '632-634Del(NL211-212I-)', '643-insertGAGCCAGAA(215EPE)', 'G1016A(G339D)', 'TCC1111CTC(S371L)', 'T1117C(S373P)', 'C1124T(S375F)', 'G1251T(K417N)', 'T1320G(N440K)', 'G1430A(S477N)', 'C1433A(T478K)', 'A1451C(E484A)', 'A1478G(Q493R)', 'G1486A(G496S)', 'A1493G(Q498R)', 'A1501T(N501Y)', 'T1513C(Y505H)', 'C1640A(T547K)', 'A1841G(D614G)', 'C1963T(H655Y)', 'T2037G(N679K)', 'C2042A(P681H)', 'C2292A(N764K)', 'G2386T(D796Y)', 'C2568A(N856K)', 'A2862T(Q954H)', 'T2907A(N969K)', 'C2941T(L981F)'],
                    "Omicron(BA.2)"   :   ['C56T(T19I)', '71-79Del(LPPA24-27S---)', 'G425A(G142D)', 'T638G(V213G)', 'G1016A(G339D)', 'C1112T(S371F)', 'T1117C(S373P)', 'C1124T(S375F)', 'A1126G(T376A)', 'G1213A(D405N)', 'A1224C(R408S)', 'G1251T(K417N)', 'T1320G(N440K)', 'G1430A(S477N)', 'C1433A(T478K)', 'A1451C(E484A)', 'A1478G(Q493R)', 'A1493G(Q498R)', 'A1501T(N501Y)', 'T1513C(Y505H)', 'A1841G(D614G)', 'C1963T(H655Y)', 'T2037G(N679K)', 'C2042A(P681H)', 'C2292A(N764K)', 'G2386T(D796Y)', 'A2862T(Q954H)', 'T2907A(N969K)']
            }

collect_dict = {}
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('_unique_seqs.tsv'):
            coverage_dict = {}
            try:
                nt_call_fh = open(os.path.join(subdir, (file[:-15]+'nt_calls.tsv')), 'r')
            except:
                print("can't open "+os.path.join(subdir, (file[:-15]+'nt_calls.tsv')))
            else:
                for line in nt_call_fh:
                    splitline = line.split("\t")
                    try:
                        splitline[9]
                    except:
                        pass
                    else:
                        if not splitline[2] == "AA POS":
                            coverage_dict[splitline[0]] = splitline[9]
                nt_call_fh.close()
            in_file = open(os.path.join(subdir, file), 'r')
            samp_dict = {}
            samp_line = ''
            for variant in spike_variants_dict:
                samp_dict[variant] = {}
            for line in in_file:
                splitline = line.split("\t")
                try:
                    splitline[2]
                except:
                    samp_line = line
                else:
                    if not splitline[1] == "Count":
                        var_line = []
                        for variant in spike_variants_dict:
                            for PM in spike_variants_dict[variant]:

                                if PM in splitline[0]:
                                    try:
                                        samp_dict[variant][PM] += int(splitline[1])
                                    except:
                                        samp_dict[variant][PM] = int(splitline[1])
            out_fh = open(file[:-16]+"_variants.tsv", 'w')
            out_fh.write(samp_line+"\n")
            for variant in spike_variants_dict:
                out_fh.write(variant+"\n")
                covered_percentages = []
                covered = 0
                for PM in spike_variants_dict[variant]:
                    coverage = 0
                    cov_pos = 0
                    if 'Del' in PM:
                        cov_pos = PM.split('-')[0]
                    elif 'insert' in PM:
                        cov_pos = PM.split('-')[0]
                    else:
                        cov_pos = PM.split('(')[0].strip('ATGC')

                    try:
                        coverage = int(coverage_dict[cov_pos])
                        covered += 1
                    except:
                        pass
                    try:
                        percent = samp_dict[variant][PM] / coverage
                        out_fh.write(f"\t{PM}\t{str(percent)}\t{str(samp_dict[variant][PM])}\t{coverage}\n")
                        covered_percentages.append(percent)
                    except:
                        try:
                            out_fh.write(f"\t{PM}\tx\t{str(samp_dict[variant][PM])}\t{coverage}\n")
                        except:
                            out_fh.write(f"\t{PM}\t0\t0\t{coverage}\n")
                out_fh.write("\n")
                if covered_percentages:
                    if sum(covered_percentages)/len(covered_percentages) > .05 and len(covered_percentages)/covered > .85:
                        try:
                            collect_dict[samp_line][variant] = sum(covered_percentages)/len(covered_percentages)
                        except:
                            collect_dict[samp_line] = {variant : sum(covered_percentages)/len(covered_percentages)}
                

            out_fh.close()
            in_file.close()

if collect_dict:
    out_fh = open("Collected_Variants.tsv", "w")
    for samp in collect_dict:
        out_fh.write(samp+"\n")
        for var in collect_dict[samp]:
            out_fh.write(f"{var}\t{collect_dict[samp][var]}\n")
        out_fh.write("\n")