import pandas as pd
from email.parser import Parser
from nltk.tokenize import word_tokenize,sent_tokenize
import re
import csv
import math
import string
import textstat
import numpy as np
from sklearn import preprocessing
#dataset=pd.read_csv("emails.csv",low_memory=False)
def count_given_word(input_string, test_word):
    count=0
    tokens = word_tokenize(input_string)
    for i in tokens:
        if i == test_word:
            count += 1
    return count
def count_para(input_text):
    
    lines = sent_tokenize(input_text)
    paragraph=0
    for idx, line in enumerate(lines):
        if not line == '\n':
            m = re.match(r'\w', line)
            if m != None:
                str = m.group(0)
            else:
                break
    
        try:
            if line == '\n' and str in lines[idx-1]: 
                paragraph +=1
        except:
            pass
    
    if lines[-1] != '\n':
        paragraph = paragraph + 1
    return paragraph


### Divide the original Enron dataset into Emails of Male and Emails of Female
    

male_dataset=pd.read_csv('male_authors.csv')
female_dataset=pd.read_csv('female_authors.csv')
male_temp_mssg=[]
female_temp_mssg=[]
male_authors=[]
female_authors=[]
male_authors=male_dataset['author']
female_authors=female_dataset['author']
regex = r"-{4,}(.*)(\d{2}:\d{2}:\d{2})\s*(PM|AM)"
for i in range(517401):
    s=''
    for j in dataset['file'][i]:
        if j.isalpha():
            s=s+j
            continue
        else:
            break
    for j in female_authors:
        if s == j:
            female_temp_mssg.append(dataset['message'][i])
'''    for j in female_authors:
        if s == j:
            male_temp_mssg.append(dataset['message'][i])'''
male_mssg_non_forwarded=[]
female_mssg_non_forwarded=[]
### Remove the frowarded emails and small emails or very large emails 
for i in male_temp_mssg:
    match1=re.search(regex,i)
    match2=re.search("---------------------- Forwarded by ",i)
    if (match1 or match2):
        continue
    else:
        temp = Parser().parsestr(i).get_payload()
        if (len(word_tokenize(temp.translate(str.maketrans('', '', string.punctuation)))) > 5 and 
            len(word_tokenize(temp.translate(str.maketrans('', '', string.punctuation)))) < 600):
            male_mssg_non_forwarded.append(temp)
        
'''
first compile all dictionaries(characters_based_features, structural_based_features, etc), then the below section for inserting headers            
header=[]
for i in characters_based_features:
    if i not in header:
        header.append(i)
for i in structural_based_features:
    if i not in header:
        header.append(i)
for i in syntactic_based_features:
    if i not in header:
        header.append(i)
for i in words_based_features:
    if i not in header:
        header.append(i)
for i in function_based_features:
    if i not in header:
        header.append(i)
with open("Final_male_normalized_dataset.csv",'w') as file:
    writer = csv.DictWriter(file, fieldnames = header)
    writer.writeheader()
    file.close()
 '''   
    

        
        ### count characters_based_features
for i in male_mssg_non_forwarded:
    temp_dict = {}
    male_mssg_tokenize_just_words = word_tokenize(i.translate(str.maketrans('', '', string.punctuation)))
    tokens_len = len(male_mssg_tokenize_just_words)
    characters_based_features={'number_of_whitespaces':0,'number_of_letters':0,'number_of_characters':0,'number_of_uppercase':0,'number_of_lowercase':0,'number_of_digits':0,
                               'number_of_quotation':0,'number_of_numbersigns':0,'number_of_dollar':0,'number_of_percent':0,'number_of_ampersand':0,'number_of_pair_paranthesis':0,
                               'number_of_asterisk':0,'number_of_plus':0,'number_of_minus':0,'number_of_solidus':0,'number_of_lessthan':0,'number_of_equal':0,
                               'number_of_greaterthan':0,'number_of_at':0,'number_of_reverseSolidus':0,'number_of_pair_squareBracket':0,'number_of_circumflexAccent':0,
                               'number_of_lowerLine':0,'number_of_pair_curlyBracket':0,'number_of_verticalLine':0,'number_of_tile':0,'number_of_open_squareBracket':0,
                               'number_of_close_squareBracket':0,'number_of_open_paranthesis':0,'number_of_close_paranthesis':0,'number_of_open_curlyBracket':0,'number_of_close_curlyBracket':0}

    for j in i:
        for k in j:
            if k.isspace():
                characters_based_features['number_of_whitespaces'] += 1
            if k.isalpha():
                characters_based_features['number_of_letters'] += 1
            if k.isdigit():
                characters_based_features['number_of_digits'] += 1
            if k.isupper():
                characters_based_features['number_of_uppercase'] +=1
            if k.islower():
                characters_based_features['number_of_lowercase'] +=1
            if k == '(':
                characters_based_features['number_of_open_paranthesis'] +=1
            if k == ')':
                characters_based_features['number_of_close_paranthesis'] +=1
            if k == '()':
                characters_based_features['number_of_pair_paranthesis'] +=1
            if k == '[':
                characters_based_features['number_of_open_squareBracket'] +=1
            if k == ']':
                characters_based_features['number_of_close_squareBracket'] +=1
            if k == '[]':
                characters_based_features['number_of_pair_squareBracket'] +=1
            if k == '{':
                characters_based_features['number_of_open_curlyBracket'] +=1
            if k == '}':
                characters_based_features['number_of_close_curlyBracket'] +=1
            if k == '{}':
                characters_based_features['number_of_pair_curlyBracket'] +=1
    characters_based_features['number_of_characters'] = textstat.char_count(i, ignore_spaces=False)
    characters_based_features['number_of_quotation'] = len(re.compile(r"\"").findall(i))
    characters_based_features['number_of_numbersigns'] = len(re.compile(r"\#").findall(i))
    characters_based_features['number_of_dollar'] = len(re.compile(r"\$").findall(i))
    characters_based_features['number_of_percent'] = len(re.compile(r"\%").findall(i))
    characters_based_features['number_of_ampersand'] = len(re.compile(r"\&").findall(i))
    characters_based_features['number_of_asterisk'] = len(re.compile(r"\*").findall(i))
    characters_based_features['number_of_plus'] = len(re.compile(r"\+").findall(i))
    characters_based_features['number_of_minus'] = len(re.compile(r"\-").findall(i))
    characters_based_features['number_of_solidus'] = len(re.compile(r"\/").findall(i))
    characters_based_features['number_of_lessthan'] = len(re.compile(r"\<").findall(i))
    characters_based_features['number_of_equal'] = len(re.compile(r"\=").findall(i))
    characters_based_features['number_of_greaterthan'] = len(re.compile(r"\>").findall(i))
    characters_based_features['number_of_at'] = len(re.compile(r"\@").findall(i))
    characters_based_features['number_of_reverseSolidus'] = len(re.compile(r"\\").findall(i))
    characters_based_features['number_of_circumflexAccent'] = len(re.compile(r"\^").findall(i))
    characters_based_features['number_of_lowerLine'] = len(re.compile(r"\_").findall(i))
    characters_based_features['number_of_verticalLine'] = len(re.compile(r"\|").findall(i))
    characters_based_features['number_of_tile'] = len(re.compile(r"\~").findall(i))
    
    for z in characters_based_features:
        temp_dict[z] = characters_based_features[z]
    
    
    ### count of structural_based_features
    
    structural_based_features = {'number_of_sentences':0,'number_of_paragraphs':0,'average_number_of_sentences_per_paragraph':0,
                                 'average_number_of_words_per_paragraph':0,'average_number_of_characters_per_paragraph':0,
                                 'average_number_of_words_per_sentence':0,'total_number_of_blank_lines':0}
    
    structural_based_features['number_of_sentences'] = len(sent_tokenize(i))
    structural_based_features['number_of_paragraphs'] = count_para(i)
    structural_based_features['average_number_of_sentences_per_paragraph'] = structural_based_features['number_of_sentences']/structural_based_features['number_of_paragraphs']
    structural_based_features['average_number_of_words_per_paragraph'] = tokens_len/structural_based_features['number_of_paragraphs']
    structural_based_features['average_number_of_characters_per_paragraph'] = textstat.char_count(i, ignore_spaces=False)/structural_based_features['number_of_paragraphs']
    structural_based_features['average_number_of_words_per_sentence'] = tokens_len/len(sent_tokenize(i))
    for j in i:
        if j.split() == []:
            structural_based_features['total_number_of_blank_lines'] += 1
                      
    
    for z in structural_based_features:
        temp_dict[z] = structural_based_features[z]

    ### count of syntactic_based_features
        
    syntactic_based_features = {'number_of_single_quotes':0,'number_of_comma':0,'number_of_period_counter':0,'number_of_colons':0,
                                'number_of_semicolons':0,'number_of_question_marks':0,'number_of_multiple_question_marks':0,
                                'number_of_exclaimation_marks':0,'number_of_multiple_exclaimation_marks':0,'number_of_ellipsis':0}
        
    syntactic_based_features['number_of_single_quotes'] = len(re.compile(r"\'").findall(i))
    syntactic_based_features['number_of_comma'] = len(re.compile(r"\,").findall(i))
    syntactic_based_features['number_of_period_counter']= len(re.compile(r"\.").findall(i))
    syntactic_based_features['number_of_colons'] = len(re.compile(r"\:").findall(i))
    syntactic_based_features['number_of_semicolons'] = len(re.compile(r"\;").findall(i))
    syntactic_based_features['number_of_question_marks'] = len(re.compile(r"\"").findall(i))
    syntactic_based_features['number_of_exclaimation_marks'] = len(re.compile(r"\!").findall(i))
    multiple_ques_mark=0
    multiple_exclaim_mark=0
    for k in i:
        if k in ["??","???","????","?????","??????","???????","????????","?????????","??????????","???????????","????????????","?????????????","??????????????",
             "???????????????","????????????????","???????????????????","??????????????????","???????????????????","????????????????????"]:
            multiple_ques_mark += 1
        if k in ["!!","!!!","!!!!","!!!!!","!!!!!!","!!!!!!!","!!!!!!!!","!!!!!!!!!","!!!!!!!!!!","!!!!!!!!!!!","!!!!!!!!!!!!","!!!!!!!!!!!!!","!!!!!!!!!!!!!!",
             "!!!!!!!!!!!!!!!","!!!!!!!!!!!!!!!!","!!!!!!!!!!!!!!!!!","!!!!!!!!!!!!!!!!!!","!!!!!!!!!!!!!!!!!!!","!!!!!!!!!!!!!!!!!!!!"]:
            multiple_exclaim_mark +=1
    syntactic_based_features['number_of_multiple_exclaimation_marks'] = multiple_exclaim_mark
    syntactic_based_features['number_of_multiple_question_marks'] = multiple_ques_mark
    
    for z in syntactic_based_features:
        temp_dict[z] = syntactic_based_features[z]
    
    ### count of words_based_features
        #####   parameters  #####
    
    email_words_freq = {}
    for k in male_mssg_tokenize_just_words:
        if k not in email_words_freq:
            email_words_freq[k]= male_mssg_tokenize_just_words.count(k)
    vocabulary_richness = len(email_words_freq)     
    hepaxlegomena=0
    hepaxdislegomena=0
    for key in email_words_freq:
        if email_words_freq[key] == 1:
            hepaxlegomena += 1
        if email_words_freq[key] == 2:
            hepaxdislegomena += 1
    max_freq=max(email_words_freq, key=lambda x:email_words_freq[x])
    Vm=[]
    for k in range(1,email_words_freq[max_freq]):
        occ=0
        for words in email_words_freq:
            if email_words_freq[words]==k:
                occ += 1
        Vm.append(occ)
    max_freq = email_words_freq[max_freq]
    sigmaV=0
    sympsonD=0
    entropy=0
    yuleK=0
    honoreR=0
    for k in range(0, len(Vm)):
        sigmaV = sigmaV + (Vm[k]*(((k+1)/tokens_len)**2))
        sympsonD = sympsonD +(Vm[k]*((k+1)/tokens_len)*(k/(tokens_len-1)))
        entropy = entropy + (Vm[k]*((k+1)/tokens_len)*math.log10(tokens_len/(k+1)))
    yuleK = (10**(-4) * (-1/tokens_len)) + sigmaV
    if hepaxlegomena!=max_freq:
        honoreR = (100 * math.log10(tokens_len))/(1-(hepaxlegomena/max_freq))
    else:
        honoreR = math.inf
        
    ########
    
    words_based_features={'total_number_of_words':0,'average_length_for_words':0,'vocabulary_richness':vocabulary_richness,'number_of_long_words':0,
                          'number_of_short_words':0,'hepaxlegomena':hepaxlegomena,'hepaxdislegomena':hepaxdislegomena,'yuleK':yuleK,
                          'sympsonD':sympsonD,'honoreR':honoreR,'entropy':entropy}
        
    words_based_features['total_number_of_words'] = tokens_len
    for k in male_mssg_tokenize_just_words:
        words_based_features['average_length_for_words'] += len(k)
        if len(k)>6:
            words_based_features['number_of_long_words'] +=1
        if len(k)<4:
            words_based_features['number_of_short_words'] +=1
    words_based_features['average_length_for_words'] /= tokens_len 
    
    for z in words_based_features:
        temp_dict[z] = words_based_features[z]    
    
    ### count of function_based_features
    function_based_features={}
    
    words=[]
    with open("Vocabulary_words.txt",'r') as file:
        for lines in file:
            for w in lines.split(','):
                words.append(w)
    
    for j in words:
        function_based_features['number_of_'+j] = 0
        function_based_features['number_of_'+j] = count_given_word(i.translate(str.maketrans('', '', string.punctuation)),j)
        
    for z in function_based_features:
        temp_dict[z] = function_based_features[z]
        
    with open("Final_dataset.csv",'a') as file:
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writerow(temp_dict)
        file.close()
        
male_unnormalized_dataset = pd.read_csv("Final_male_dataset_Unnormailzed.csv")     
male_normalized_dataset = (male_unnormalized_dataset-male_unnormalized_dataset.min())/(male_unnormalized_dataset.max()-male_unnormalized_dataset.min())
male_normalized_dataset.to_csv("Final_male_normalized_dataset.csv",index=False)

combined_normalized_dataset=pd.merge(male_normalized_dataset,male_normalized_dataset,on=header,how='outer')
combined_normalized_dataset.to_csv("Final_combined_normalized_dataset.csv",index=False)
