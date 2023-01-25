#!/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
from plotnine import *
import re

VOCs = {
"Omicron BF.14"     :   "G1251T(K417N) T1320G(N440K) A1348G(N450D) T1355G(L452R) G1430A(S477N) C1433A(T478K) A1451C(E484A) T1456G(F486V) A1493G(Q498R) A1501T(N501Y) T1513C(Y505H)",
"Omicron BQ.1.1"    :   "G1251T(K417N) T1320G(N440K) A1331C(K444T) T1355G(L452R) T1380A(N460K) G1430A(S477N) C1433A(T478K) A1451C(E484A) T1456G(F486V) A1493G(Q498R) A1501T(N501Y) T1513C(Y505H)",
"Omicron BA.4/5"    :   "G1251T(K417N) T1320G(N440K) T1355G(L452R) G1430A(S477N) C1433A(T478K) A1451C(E484A) T1456G(F486V) A1493G(Q498R) A1501T(N501Y) T1513C(Y505H)",
"Omicron BA.2.12.1" :   "G1251T(K417N) T1320G(N440K) T1355A(L452Q) G1430A(S477N) C1433A(T478K) A1451C(E484A) A1478G(Q493R) A1493G(Q498R) A1501T(N501Y) T1513C(Y505H)",
"Omicron BA.2"      :   "G1251T(K417N) T1320G(N440K) G1430A(S477N) C1433A(T478K) A1451C(E484A) A1478G(Q493R) A1493G(Q498R) A1501T(N501Y) T1513C(Y505H)",
"Omicron BA.1"      :   "G1251T(K417N) T1320G(N440K) G1336A(G446S) G1430A(S477N) C1433A(T478K) A1451C(E484A) A1478G(Q493R) G1486A(G496S) A1493G(Q498R) A1501T(N501Y) T1513C(Y505H) C1640A(T547K)",
"Delta"     :  "T1355G(L452R) C1433A(T478K)",
# "Mu/Theta"  :  "G1450A(E484K) A1501T(N501Y)",
"Gamma"     :  "A1250C(K417T) G1450A(E484K) A1501T(N501Y)",
"Beta"      :  "G1251T(K417N) G1450A(E484K) A1501T(N501Y)",
"Alpha"     :  "A1501T(N501Y) C1709A(A570D)",
}

VOCs_by_hap = {y: x for x, y in VOCs.items()}

omicron_mutations = [ ## Original From Rose
    'T19I',
    'LPPA24-27S---',
    'A67V',
    'IHV68-70I--',
    'T95I',
    'GVYY142-145D---',
    'G142D',
    'NL211-212I-',
    'V213G',
    '215EPE',
    'G339D',
    'S371L',
    'S373P',
    'S375F',
    'K417N',
    'N440K',
    'N450D',
    'L452Q',
    'L452R',
    'G446S',
    'S477N',
    'T478K',
    'E484A',
    'F486V',
    'Q493R',
    'G496S',
    'Q498R',
    'N501Y',
    'Y505H',
    'T547K'
]

omicron_positions = [
    '19',
    '24',
    '25',
    '26',
    '27',
    '67',
    '68',
    '69',
    '70',
    '95',
    '142',
    '143',
    '144',
    '145',
    '211',
    '212',
    '213',
    '215',
    '339',
    '371',
    '373',
    '375',
    '417',
    '440',
    '450',
    '452',
    '446',
    '452',
    '477',
    '478',
    '484',
    '486',
    '493',
    '496',
    '498',
    '501',
    '505',
    '547'
    ]

for VOC in VOCs:
    if "Omicron" in VOC:
        for mut in VOCs[VOC].split(" "):
            AAmut = mut.split("(")[-1].strip(")")
            if not AAmut in omicron_mutations:
                omicron_mutations.append(AAmut)
            if not AAmut[1:-1] in omicron_positions:
                omicron_positions.append(AAmut[1:-1])

def mut_pos_stringer(muts):
    mut_pos_string = ''
    for mut in muts.split(' '):
        mut_pos = ''
        for c in mut.split('(')[0].strip('ATCGN'):
            if c.isdigit():
                mut_pos += c
            else:
                break
        mut_pos_string += f"{int(mut_pos):06d} "
    return(mut_pos_string)

def load_deconv(file_name): ## From Rose
    '''ingest file and change column names, add seq IDs,
    filter out sequences with fewer than 5 mutations, melt to long format
    returns the filtered raw file with frequencies and the long format file'''
    # load data, rename columns, drop the rows called "Covariant" and "Reference"
    df_raw = pd.read_csv(file_name, sep='\t', header=None, names=('Sample', 'Sequence'))
    # df_raw = df_raw.rename(columns={'Unnamed: 1' : 'Sequence'})
    # df_raw = df_raw[~df_raw.mutations.isin(['Covariant', 'Reference'])]

    # make column with count of mutations and then filter out seqs with < 5 mutations
    # df_raw['mutations_count'] = df_raw.mutations.apply(lambda x: len(x.split(' ')))
    # df_raw = df_raw[df_raw.mutations_count >= 5]
    # df_raw = df_raw.drop(columns='mutations_count') # now drop this col

    # drop columns that are all NA
    # df_raw = df_raw.dropna('columns', how='all')

    # print(df_raw)
    # df_raw['mut_poses'] = df_raw.Sequence.apply(lambda x: mut_pos_stringer(x))
    # df_raw = df_raw.sort_values(by='mut_poses').reset_index().drop(columns=['index'])
    # df_raw = df_raw.drop(columns=['mut_poses'])

    # pat_E484 = re.compile(r'\(E484(\D)\)')
    # pat_N440 = re.compile(r'\(N440(\D)\)')
    # df_raw['E484'] = df_raw.mutations.apply(lambda x: bool(pat_E484.search(x)))
    # df_raw['N440'] = df_raw.mutations.apply(lambda x: bool(pat_N440.search(x)))

    # df_raw = df_raw.sort_values(by='E484').reset_index().drop(columns=['index'])
    # df_raw = df_raw.drop(columns=['E484'])
    # df_raw = df_raw.sort_values(by='N440').reset_index().drop(columns=['index'])
    # df_raw = df_raw.drop(columns=['N440'])
    # print(df_raw)


    df_raw.insert(0,'seq_id', range(0,len(df_raw)))


    return df_raw # , df

for file in os.listdir(os.getcwd()):
    if file.endswith('.tsv'): #.endswith('_trimmedv2.tsv'):

        ####
        ####  Original plotting from Rose
        ####
        df_raw = load_deconv(file)
        # print(df_raw)
        seq_num = df_raw.shape[0]

        df_raw['PMs'] = df_raw.Sequence.apply(lambda x: x.split(' '))
        df = df_raw.drop(columns=['Sequence'])

        pat_SCP = re.compile(r'\(((\D)(\d+)(\w))\)')
        pat_ins = re.compile(r'insert\w+\(((\d+)(\w+))\)')
        pat_ins1 = re.compile(r'\w+insert\(((\w)(\d+)(\w+))insert\)')
        pat_del = re.compile(r'\(((\w)(\d+))del\)')
        pat_MCP = re.compile(r'\(((\D+)(\d+)-(\d+)(\D+))\)')
        new_entries = []
        for row in df.itertuples():
            for pm in row.PMs:
                Omi = 'Non-Omicron'

                # if ':' in pm:
                    # print(pm)
                    # continue
                if pat_ins.search(pm):
                    exp = pat_ins.search(pm).groups()
                    position = exp[1]
                    wt = '-'
                    wt_pos = '-'+exp[1]
                    mut = exp[2]
                    if exp[0] in omicron_mutations:
                        Omi = 'Omicron Mutation'
                    elif exp[1] in omicron_positions:
                        Omi = 'Omicron Position'
                    if len(mut) > 1:
                        i = 0
                        for AA in mut:
                            new_entries.append([row.seq_id, row.Sample, wt_pos+'.'+str(i), int(position), wt, mut[i], Omi])
                            i += 1
                        continue
                elif pat_SCP.search(pm):
                    exp = pat_SCP.search(pm).groups()
                    position = exp[2]
                    wt = exp[1]
                    wt_pos = exp[1]+exp[2]
                    mut = exp[3]
                    if wt == mut:
                        continue
                    if exp[0] in omicron_mutations:
                        Omi = 'Omicron Mutation'
                    elif exp[2] in omicron_positions:
                        Omi = 'Omicron Position'
                elif pat_ins1.search(pm):
                    exp = pat_ins1.search(pm).groups()
                    position = exp[2]
                    wt = exp[1]
                    mut = exp[3]
                    if not wt == mut[0]:
                        if wt+position+mut[0] in omicron_mutations:
                            Omi = 'Omicron Mutation'
                        elif exp[2] in omicron_positions:
                            Omi = 'Omicron Position'
                        new_entries.append([row.seq_id, row.Sample, exp[1]+exp[2], int(position), wt, mut[0], Omi])
                    Omi = 'Non-Omicron'
                    wt = '-'
                    mut = mut[1:]
                    
                    if position+mut in omicron_mutations:
                        Omi = 'Omicron Mutation'
                    elif position in omicron_positions:
                        Omi = 'Omicron Position'
                    i = 1
                    for AA in mut:
                        newposition = str(int(position)) +'.'+str(i)
                        new_entries.append([row.seq_id, row.Sample, '-'+newposition, float(newposition), wt, AA, Omi])
                        i += 1
                    continue

                elif pat_del.search(pm):
                    exp = pat_del.search(pm).groups()
                    position = exp[2]
                    wt = exp[1]
                    wt_pos = exp[1]+exp[2]
                    mut = 'Δ'
                    if (exp[0]+'-') in omicron_mutations:
                        Omi = 'Omicron Mutation'
                    elif exp[2] in omicron_positions:
                        Omi = 'Omicron Position'
                elif pat_MCP.search(pm):
                    exp = pat_MCP.search(pm).groups()
                    position = exp[2]
                    wt = exp[1]
                    wt_pos = 'x'
                    mut = exp[4]
                    if 'del' in mut:
                        mut = mut.strip("del")
                    # if len(mut) == len(wt):
                    for i in range(0, len(wt)):
                        try:
                            if wt[i] == mut[i]:
                                continue
                            Omi = 'Non-Omicron'
                            if (wt[i]+str(int(position)+i)+mut[i]) in omicron_mutations:
                                Omi = 'Omicron Mutation'
                            elif str(int(position)+i) in omicron_positions:
                                Omi = 'Omicron Position'
                            new_entries.append([row.seq_id, row.Sample, wt[i]+str(int(position)+i), int(position)+i, wt[i], mut[i].replace('-', 'Δ'), Omi])
                        except:
                            if Omi == 'Non-Omicron':
                                if (wt[i]+str(int(position)+i)+'-') in omicron_mutations:
                                    Omi = 'Omicron Mutation'
                                elif str(int(position)+i) in omicron_positions:
                                    Omi = 'Omicron Position'
                            new_entries.append([row.seq_id, row.Sample, wt[i]+str(int(position)+i), int(position)+i, wt[i], 'Δ', Omi])
                            #print(pm)
                        # print(new_entries[-1])
                        Omi = 'Non-Omicron'
                    if len(mut) > len(wt):
                        print(pm)
                        mut = mut[i+1:]
                        wt = '-'
                        position = int(position) + i + 1 
                        if str(position)+mut in omicron_mutations:
                            Omi = 'Omicron Mutation'
                        elif str(position) in omicron_positions:
                            Omi = 'Omicron Position'
                        i = 1
                        for AA in mut:
                            newposition = str(int(position)+1) +'.'+str(i)
                            new_entries.append([row.seq_id, row.Sample, '-'+newposition, float(newposition), wt, AA, Omi])
                            i += 1

                    continue
                else:
                    print(pm)
                    continue
                new_entries.append([row.seq_id, row.Sample, wt_pos, int(position), wt, mut, Omi])
        #try:
        df_long = pd.DataFrame.from_records(new_entries, columns = ['seq_id', 'Sample', 'wt_pos', 'position', 'wildtype_aa', 'mutation_aa', 'Omicron Residues'])

        # order the data by wildtype position for plotting nicely, From Rose
        sorting = df_long[['position', 'wt_pos']].copy()
        sorting.position = pd.to_numeric(sorting.position)
        ordered_list = list(sorting.sort_values('position')['wt_pos'].unique())
        df_long.wt_pos = pd.Categorical(df_long.wt_pos, ordered=True, categories=ordered_list)


        sorting = df_long[['seq_id', 'Sample']].copy()
        sorting.seq_id = pd.to_numeric(sorting.seq_id)
        ordered_list = list(sorting.sort_values('seq_id')['Sample'].unique())
        df_long.Sample = pd.Categorical(df_long.Sample, ordered=True, categories=ordered_list)

        pm_num = df_long.wt_pos.nunique()
        colors = ['#111111', '#d55e00', '#009e73']

        fig = (ggplot(df_long, aes(x='wt_pos', y='Sample', color='Omicron Residues'))+ # , limitsize=False
         geom_tile(aes(width=.9, height=.9), size=1, linetype='solid', fill='white')+ # , color='black'
         geom_text(aes(label='mutation_aa'), color='black', size=7)+
         scale_color_manual(values=colors, drop=False, breaks=['Non-Omicron', 'Omicron Mutation', 'Omicron Position'])+
         xlab("Position")+
         ylab('')+
         theme_classic()+
         theme(legend_position='right', figure_size=((pm_num+1)/6,(seq_num+1)/6), dpi=600, axis_text_x=element_text(angle=90, hjust=0.5), axis_text_y=element_text(color='black'), axis_line_y=element_line(color='white'), axis_ticks_major_y=element_line(color='white'),axis_ticks_minor_y=element_line(color='white'))) # , panel_grid=element_line(color='#111111', linetype='solid', size=0.1)

        fig.save(filename = file[:-4]+'1.svg')