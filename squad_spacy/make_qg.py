import json
import spacy
import string
import re
from tqdm import tqdm
def tokenize(t):
    t = re.sub("\"","",t)
    t = re.sub("' ","'",t)
    t = re.sub(" '","'",t)
    t = re.sub(" -","-",t)
    t = re.sub("- ","-",t)
    t = re.sub(", ",",",t)
    return t
def concatenate(tokens):
    return " ".join(tokens)
with open('train_result_squad_spacy_train.json','r') as readfile:
    read = json.load(readfile)
result = {}
result['data'] = []
for d in tqdm(read['data']):
    sentence_num = 0
    ans_index = 0
    temp = {}
    temp['context'] = d['context']
    temp['input'] = []
    sentence_num += 1
    while ans_index < len(d['tokens'])-1:
        detokenized_sentence = ''
        ans = {}
        for i in range(ans_index,len(d['tokens'])):
            length = 0
            index = i
            while d['labels'][index] == 'A':
                index += 1
                length += 1
                if index >= len(d['tokens']):
                    break

            if length > 0:
                detokenized_sentence += concatenate(d['tokens'][:i])
                detokenized_sentence += '[HL]'
                string = tokenize(concatenate(d['tokens'][i:i+length]))
                detokenized_sentence += tokenize(string)
                detokenized_sentence += '[HL]'
                detokenized_sentence += concatenate(d['tokens'][i+length:])
                ans_index = i + length + 1
                ans['answer'] = string

                break
            else:
                ans_index += 1
        if detokenized_sentence:
            ans['sentence'] = detokenized_sentence
            temp['input'].append(ans)
    result['data'].append(temp)
with open('qg_train_squad_spacy_train.json','w') as writefile:
    json.dump(result,writefile)