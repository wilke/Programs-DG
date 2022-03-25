#!/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
from plotnine import *
import re

# omicron_mutations = [ ## Original From Rose
# 'T19I',
# 'LPPA24-27S---',
# 'L24S',
# 'P25--',
# 'P26-',
# 'A27-',
# 'A67V',
# 'IHV68-70I--',
# 'I68I',
# 'H69-',
# 'V70-',
# 'T95I',
# 'GVYY142-145D---',
# 'G142D',
# 'V143-',
# 'Y144-',
# 'Y145-',
# 'G142D',
# 'NL211-212I-',
# 'N211I',
# 'L212-',
# 'V213G',
# '215EPE',
# 'G339D',
# 'S371L',
# 'S373P',
# 'S375F',
# 'K417N',
# 'N440K',
# 'G446S',
# 'S477N',
# 'T478K',
# 'E484A',
# 'Q493R',
# 'G496S',
# 'Q498R',
# 'N501Y',
# 'Y505H',
# 'T547K'
# ]
# omicron_positions = [
# '19',
# '24',
# '25',
# '26',
# '27',
# '67',
# '68',
# '69',
# '70',
# '95',
# '142',
# '143',
# '144',
# '145',
# '211',
# '212',
# '213',
# '215',
# '339',
# '371',
# '373',
# '375',
# '417',
# '440',
# '446',
# '477',
# '478',
# '484',
# '493',
# '496',
# '498',
# '501',
# '505',
# '547'
# ]

# def mut_pos_stringer(muts):
    # mut_pos_string = ''
    # for mut in muts.split(' '):
        # mut_pos = ''
        # for c in mut.split('(')[0].strip('ATCGN'):
            # if c.isdigit():
                # mut_pos += c
            # else:
                # break
        # mut_pos_string += f"{int(mut_pos):06d} "
    # return(mut_pos_string)

def load_deconv(file_name): ## From Rose
    '''ingest file and change column names, add seq IDs,
    filter out sequences with fewer than 5 mutations, melt to long format
    returns the filtered raw file with frequencies and the long format file'''
    # load data, rename columns, drop the rows called "Covariant" and "Reference"
    df_raw = pd.read_csv(file_name, sep='\t')
    # df_raw = df_raw.rename(columns={'Unnamed: 0':'mutations'})
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


    # df_raw.insert(0,'seq_id', range(0,len(df_raw)))


    return df_raw # , df

for file in os.listdir(os.getcwd()):
    if file.endswith('_NTtable.tsv'):

        ####
        ####  Original plotting from Rose
        ####
        df_raw = load_deconv(file)

        mut_num = df_raw.shape[0]
        sample_num = df_raw.shape[1]
        
        df_long = df_raw.melt(id_vars=['mut'], var_name='sample_id', value_name='abundance')
        
        # print(df_long.head())
        fig = (ggplot(df_long, aes(x='sample_id', y='mut', fill='abundance'))+
         geom_tile(color='white')+
         xlab('')+
         scale_fill_cmap(limits=[0, 1])+ #, breaks=[0, .5, 1])+
         ylab('')+
         theme_classic()+
         theme(figure_size=((sample_num+1)/4,(mut_num+1)/4), dpi=600, axis_text_x=element_text(angle=45, hjust=.75), axis_text_y=element_text(color='black')))
         
        fig.save(filename = file[:-4]+'.png')
        
        
        # print(df_raw.head())
        # print(mut_num)
        # print(sample_num)
        
        # df_raw['PMs'] = df_raw.Sequence.apply(lambda x: x.split(' '))
        # df = df_raw.drop(columns=['Sequence'])

        # pat_SCP = re.compile(r'\(((\w)(\d+)(\w))\)')
        # pat_ins = re.compile(r'insert\(((\d+)(\w+))\)')
        # pat_ins1 = re.compile(r'insert\w+\(((\w)(\d+)(\w+))\)')
        # pat_del = re.compile(r'\(((\w)(\d+))-\)')
        # pat_MCP = re.compile(r'\(((\D+)(\d+)-(\d+)(\D+))\)')
        # new_entries = []
        # for row in df.itertuples():
            # for pm in row.PMs:
                # Omi = 'Non-Omicron'

                # # if ':' in pm:
                    # # print(pm)
                    # # continue
                # if pat_SCP.search(pm):
                    # exp = pat_SCP.search(pm).groups()
                    # position = exp[2]
                    # wt = exp[1]
                    # wt_pos = exp[1]+exp[2]
                    # mut = exp[3]
                    # if wt == mut:
                        # continue
                    # if exp[0] in omicron_mutations:
                        # Omi = 'Omicron Mutation'
                    # elif exp[2] in omicron_positions:
                        # Omi = 'Omicron Position'
                # elif pat_ins.search(pm):
                    # exp = pat_ins.search(pm).groups()
                    # position = exp[1]
                    # wt = '-'
                    # wt_pos = '-'+exp[1]
                    # mut = exp[2]
                    # if exp[0] in omicron_mutations:
                        # Omi = 'Omicron Mutation'
                    # elif exp[1] in omicron_positions:
                        # Omi = 'Omicron Position'
                # elif pat_ins1.search(pm):
                    # exp = pat_ins1.search(pm).groups()
                    # position = exp[2]
                    # wt = exp[1]
                    # mut = exp[3]
                    # if not wt == mut[0]:
                        # if wt+position+mut[0] in omicron_mutations:
                            # Omi = 'Omicron Mutation'
                        # elif exp[2] in omicron_positions:
                            # Omi = 'Omicron Position'
                        # new_entries.append([row.seq_id, row.Sample, exp[1]+exp[2], int(position), wt, mut[0], Omi])
                    # Omi = 'Non-Omicron'
                    # wt = '-'
                    # mut = mut[1:]
                    
                    # if position+mut in omicron_mutations:
                        # Omi = 'Omicron Mutation'
                    # elif position in omicron_positions:
                        # Omi = 'Omicron Position'
                    # i = 1
                    # for AA in mut:
                        # newposition = str(int(position)+1) +'.'+str(i)
                        # new_entries.append([row.seq_id, row.Sample, '-'+newposition, float(newposition), wt, AA, Omi])
                        # i += 1
                    # continue

                # elif pat_del.search(pm):
                    # exp = pat_del.search(pm).groups()
                    # position = exp[2]
                    # wt = exp[1]
                    # wt_pos = exp[1]+exp[2]
                    # mut = 'Δ'
                    # if exp[0] in omicron_mutations:
                        # Omi = 'Omicron Mutation'
                    # elif exp[2] in omicron_positions:
                        # Omi = 'Omicron Position'
                # elif pat_MCP.search(pm):
                    # exp = pat_MCP.search(pm).groups()
                    # position = exp[2]
                    # wt = exp[1]
                    # wt_pos = 'x'
                    # mut = exp[4]
                    # # if len(mut) == len(wt):
                    # for i in range(0, len(wt)):
                        # try:
                            # if wt[i] == mut[i]:
                                # continue
                            # Omi = 'Non-Omicron'
                            # if (wt[i]+str(int(position)+i)+mut[i]) in omicron_mutations:
                                # Omi = 'Omicron Mutation'
                            # elif str(int(position)+i) in omicron_positions:
                                # Omi = 'Omicron Position'
                            # new_entries.append([row.seq_id, row.Sample, wt[i]+str(int(position)+i), int(position)+i, wt[i], mut[i].replace('-', 'Δ'), Omi])
                        # except:
                            # if Omi == 'Non-Omicron':
                                # if (wt[i]+str(int(position)+i)+'-') in omicron_mutations:
                                    # Omi = 'Omicron Mutation'
                                # elif str(int(position)+i) in omicron_positions:
                                    # Omi = 'Omicron Position'
                            # new_entries.append([row.seq_id, row.Sample, wt[i]+str(int(position)+i), int(position)+i, wt[i], 'Δ', Omi])
                            # #print(pm)
                        # # print(new_entries[-1])
                        # Omi = 'Non-Omicron'
                    # if len(mut) > len(wt):
                        # mut = mut[i+1:]
                        # wt = '-'
                        # position = int(position) + i + 1 
                        # if str(position)+mut in omicron_mutations:
                            # Omi = 'Omicron Mutation'
                        # elif str(position) in omicron_positions:
                            # Omi = 'Omicron Position'
                        # i = 1
                        # for AA in mut:
                            # newposition = str(int(position)+1) +'.'+str(i)
                            # new_entries.append([row.seq_id, row.Sample, '-'+newposition, float(newposition), wt, AA, Omi])
                            # i += 1

                    # continue
                # else:
                    # print(pm)
                    # continue
                # new_entries.append([row.seq_id, row.Sample, wt_pos, int(position), wt, mut, Omi])
        # #try:
        # df_long = pd.DataFrame.from_records(new_entries, columns = ['seq_id', 'Sample', 'wt_pos', 'position', 'wildtype_aa', 'mutation_aa', 'Omicron Residues'])

        # # order the data by wildtype position for plotting nicely, From Rose
        # sorting = df_long[['position', 'wt_pos']].copy()
        # sorting.position = pd.to_numeric(sorting.position)
        # ordered_list = list(sorting.sort_values('position')['wt_pos'].unique())
        # df_long.wt_pos = pd.Categorical(df_long.wt_pos, ordered=True, categories=ordered_list)


        # sorting = df_long[['seq_id', 'Sample']].copy()
        # sorting.seq_id = pd.to_numeric(sorting.seq_id)
        # ordered_list = list(sorting.sort_values('seq_id')['Sample'].unique())
        # df_long.Sample = pd.Categorical(df_long.Sample, ordered=True, categories=ordered_list)

        # pm_num = df_long.wt_pos.nunique()
        # colors = ['#111111', '#d55e00', '#009e73']

        # fig = (ggplot(df_long, aes(x='wt_pos', y='Sample', color='Omicron Residues', limitsize=False))+
         # geom_tile(aes(width=.9, height=.9), size=1, linetype='solid', fill='white')+ #
         # geom_text(aes(label='mutation_aa'), color='black', size=7)+
         # scale_color_manual(values=colors, drop=False, breaks=['Non-Omicron', 'Omicron Mutation', 'Omicron Position'])+
         # xlab("Position")+
         # ylab('')+
         # theme_classic()+
         # theme(legend_position='right', figure_size=((pm_num+1)/6,(seq_num+1)/6), dpi=600, axis_text_x=element_text(angle=90, hjust=0.5), axis_text_y=element_text(color='black'), axis_line_y=element_line(color='white'), axis_ticks_major_y=element_line(color='white'),axis_ticks_minor_y=element_line(color='white'))) # , panel_grid=element_line(color='#111111', linetype='solid', size=0.1)

        # fig.save(filename = file[:-4]+'1.png')