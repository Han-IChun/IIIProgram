# -*- coding: utf-8 -*-


attribute_list=[]
opinion_list=[]

attribute_set=set()
opinion_set=set()

f=open('CRF_output_acer.txt','r')


for line in f.readlines():
    if len(line)>1:
        if line.split('\t')[2].strip()=='B_A':
            attribute_list.append(line.split('\t')[0])
        if line.split('\t')[2].strip()=='I_A':
            attribute_list.append(line.split('\t')[0])
        if line.split('\t')[2].strip()=='E_A':
            attribute_list.append(line.split('\t')[0])
            if ''.join(attribute_list) not in attribute_set:
                attribute_set.add(''.join(attribute_list))
                attribute_list=[]
            else:
                attribute_list=[]
        if line.split('\t')[2].strip()=='A':
            if line.split('\t')[0] not in attribute_set:
                attribute_set.add(line.split('\t')[0])



        if line.split('\t')[2].strip()=='B_O':
            opinion_list.append(line.split('\t')[0])
        if line.split('\t')[2].strip()=='I_O':
            opinion_list.append(line.split('\t')[0])
        if line.split('\t')[2].strip()=='E_O':
            opinion_list.append(line.split('\t')[0])
            if ''.join(opinion_list) not in opinion_set:
                opinion_set.add(''.join(opinion_list))
                opinion_list=[]
            else:
                opinion_list=[]
        if line.split('\t')[2].strip()=='O':
            if line.split('\t')[0] not in opinion_set:
                opinion_set.add(line.split('\t')[0])
f.close()


fid=open('attribute.txt','w')
for word in attribute_set:
    fid.write(word+'\n')
fid.close()


fid=open('opinion.txt','w')

for word in opinion_set:
    fid.write(word+'\n')
fid.close()
