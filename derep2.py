#!/bin/env python3

import os
import sys
import argparse


parser = argparse.ArgumentParser(
        description='Dereplicates fasta or fastq reads with counts'
)

parser.add_argument(
    'in_file',
    type=argparse.FileType('r'),
    help='fasta or fastq file'
)
parser.add_argument(
    'out_file',
    type=str,
    help='output fasta name'
)
parser.add_argument(
    'min_count',
    type=int,
    default=1,
    help='min count for a sequence to be included.  default 1'
)parser.add_argument(
    '--split',
    type=int,
    default=0,
    help='split large data sets into smaller sets.  default 0'
)

args = parser.parse_args()

def write_file(outfile, seqs_dict):
    counter = 1
    sorted_seqs = sorted(seqs_dict.items(), key=lambda x:x[1], reverse=True )
    with open(outfile, "w") as out_file:
        for seq in sorted_seqs:
            if seqs_dict[seq[0]] >= args.min_count:
                out_file.write(f">{counter}-{seqs_dict[seq[0]]}\n{seq[0]}\n")
                counter += 1
            else:
                break

# tmp_file_count = 0
# tmp_unique_seqs = 0
# seq_dict = {}
# total_reads = 0
# first_line = args.in_file.readline()
# args.in_file.seek(0)
# if first_line.startswith('>'):
    # cur_seq = ""
    # for line in args.in_file:
        # if line.startswith('>'):
            # if cur_seq:
                # try:
                    # seq_dict[cur_seq] += 1
                # except:
                    # seq_dict[cur_seq] = 1
                    # tmp_unique_seqs += 1
                # cur_seq = ''
            # total_reads += 1
        # else:
            # cur_seq += line.strip('\n\r')
        # if tmp_unique_seqs >= 10000000:
            # sorted_seqs = sorted(seq_dict.items(), key=lambda x:x[1], reverse=True )
            # write_file(str(tmp_file_count)+"_"+args.out_file, sorted_seqs, seq_dict)
            # tmp_file_count += 1
            # tmp_unique_seqs = 0
            # seq_dict = {}

    # if cur_seq:
        # try:
            # seq_dict[cur_seq] += 1
        # except:
            # seq_dict[cur_seq] = 1

# elif first_line.startswith("@"):

    # seq_id = ""
    # sequence = ""
    # seq_q_id = ""
    # qual = ""
    # file_reading = True
    # while(file_reading):
        # try:
            # seq_id = args.in_file.readline()
            # sequence = args.in_file.readline()
            # seq_q_id = args.in_file.readline()
            # qual = args.in_file.readline()
        # except Exception as e:
            # print(e)
            # print("Error in reading file")
            # file_reading = False
            # break
        # else:
            # if seq_id == "":
                # # EOF
                # file_reading = False
                # break
            # elif seq_id.startswith("@") and seq_q_id.startswith("+"):
                # try:
                    # seq_dict[sequence.strip("\n\r")] += 1
                # except:
                    # seq_dict[sequence.strip("\n\r")] = 1
                    # tmp_unique_seqs += 1
                # total_reads += 1
            # else:
                # print("Error in reading FASTQ format.")
                # file_reading = False
                # break


        # if tmp_unique_seqs >= 10000000:
            # sorted_seqs = sorted(seq_dict.items(), key=lambda x:x[1], reverse=True )
            # write_file(str(tmp_file_count)+"_"+args.out_file, sorted_seqs, seq_dict)
            # tmp_file_count += 1
            # tmp_unique_seqs = 0
            # seq_dict = {}

# else:
    # print('input file not recognized as fasta/q')
# args.in_file.close()




# print(f"{total_reads} sequences collected.  Dereplicated to {len(seq_dict)} unique sequences.  Writing output file")

# if tmp_file_count == 0:
    # write_file(args.out_file, seq_dict)
# else:
    # write_file(str(tmp_file_count)+"_"+args.out_file, seq_dict)

# for file in tmp_files:
file_list = []

for file in os.listdir(os.getcwd()):
    if "_"+args.out_file in file:
        print(file)
        file_list.append(file)

for i in range(0, len(file_list)-1):
    seq_dict = {}
    
    with open(file_list[i], "r") as in_file:
        cur_seq = ""
        count = 0
        print(file_list[i])
        for line in in_file:
            if line.startswith('>'):
                if cur_seq:
                    try:
                        seq_dict[cur_seq] += count
                    except:
                        seq_dict[cur_seq] = count
                    cur_seq = ''
                count = int(line.split("-")[-1])
            else:
                cur_seq += line.strip('\n\r')

        if cur_seq:
            try:
                seq_dict[cur_seq] += 1
            except:
                seq_dict[cur_seq] = 1
    for p in range(i+1, len(file_list)):
        not_collected = {}
        with open(file_list[p], "r") as in_file:
            cur_seq = ""
            count = 0
            for line in in_file:
                if line.startswith('>'):
                    if cur_seq:
                        try:
                            seq_dict[cur_seq] += count
                        except:
                            not_collected[cur_seq] = count
                        cur_seq = ''
                    count = int(line.split("-")[-1])
                else:
                    cur_seq += line.strip('\n\r')

            if cur_seq:
                try:
                    seq_dict[cur_seq] += count
                except:
                    not_collected[cur_seq] = count
        write_file(file_list[p], not_collected)
    write_file(file_list[i], seq_dict)
    
    