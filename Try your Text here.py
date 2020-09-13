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
dataset=pd.read_csv("emails.csv",low_memory=False)
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
print("Enter the text:::")
input_text = string(input())
input_text = Parser().parsestr(input_text).get_payload()
regex = r"-{4,}(.*)(\d{2}:\d{2}:\d{2})\s*(PM|AM)"
match = min(re.search(regex,input_text),re.search("---------------------- Forwarded by ",input_text))
input_text_final=input_text[0:match]
temp_dict = {}
text_tokenize_just_words = word_tokenize(i.translate(str.maketrans('', '', string.punctuation)))
tokens_len = len(text_tokenize_just_words)
characters_based_features={'number_of_whitespaces':0,'number_of_letters':0,'number_of_characters':0,'number_of_uppercase':0,'number_of_lowercase':0,'number_of_digits':0,
                           'number_of_quotation':0,'number_of_numbersigns':0,'number_of_dollar':0,'number_of_percent':0,'number_of_ampersand':0,'number_of_pair_paranthesis':0,
                           'number_of_asterisk':0,'number_of_plus':0,'number_of_minus':0,'number_of_solidus':0,'number_of_lessthan':0,'number_of_equal':0,
                           'number_of_greaterthan':0,'number_of_at':0,'number_of_reverseSolidus':0,'number_of_pair_squareBracket':0,'number_of_circumflexAccent':0,
                           'number_of_lowerLine':0,'number_of_pair_curlyBracket':0,'number_of_verticalLine':0,'number_of_tile':0,'number_of_open_squareBracket':0,
                           'number_of_close_squareBracket':0,'number_of_open_paranthesis':0,'number_of_close_paranthesis':0,'number_of_open_curlyBracket':0,'number_of_close_curlyBracket':0}

for j in input_text_final:
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
characters_based_features['number_of_characters'] = textstat.char_count(input_text_final, ignore_spaces=False)
characters_based_features['number_of_quotation'] = len(re.compile(r"\"").findall(input_text_final))
characters_based_features['number_of_numbersigns'] = len(re.compile(r"\#").findall(input_text_final))
characters_based_features['number_of_dollar'] = len(re.compile(r"\$").findall(input_text_final))
characters_based_features['number_of_percent'] = len(re.compile(r"\%").findall(input_text_final))
characters_based_features['number_of_ampersand'] = len(re.compile(r"\&").findall(input_text_final))
characters_based_features['number_of_asterisk'] = len(re.compile(r"\*").findall(input_text_final))
characters_based_features['number_of_plus'] = len(re.compile(r"\+").findall(input_text_final))
characters_based_features['number_of_minus'] = len(re.compile(r"\-").findall(input_text_final))
characters_based_features['number_of_solidus'] = len(re.compile(r"\/").findall(input_text_final))
characters_based_features['number_of_lessthan'] = len(re.compile(r"\<").findall(input_text_final))
characters_based_features['number_of_equal'] = len(re.compile(r"\=").findall(input_text_final))
characters_based_features['number_of_greaterthan'] = len(re.compile(r"\>").findall(input_text_final))
characters_based_features['number_of_at'] = len(re.compile(r"\@").findall(input_text_final))
characters_based_features['number_of_reverseSolidus'] = len(re.compile(r"\\").findall(input_text_final))
characters_based_features['number_of_circumflexAccent'] = len(re.compile(r"\^").findall(input_text_final))
characters_based_features['number_of_lowerLine'] = len(re.compile(r"\_").findall(input_text_final))
characters_based_features['number_of_verticalLine'] = len(re.compile(r"\|").findall(input_text_final))
characters_based_features['number_of_tile'] = len(re.compile(r"\~").findall(input_text_final))
    
for z in characters_based_features:
    temp_dict[z] = characters_based_features[z]
    
    
###### count of structural_based_features
    
structural_based_features = {'number_of_sentences':0,'number_of_paragraphs':0,'average_number_of_sentences_per_paragraph':0,
                             'average_number_of_words_per_paragraph':0,'average_number_of_characters_per_paragraph':0,
                             'average_number_of_words_per_sentence':0,'total_number_of_blank_lines':0}
    
structural_based_features['number_of_sentences'] = len(sent_tokenize(input_text_final))
structural_based_features['number_of_paragraphs'] = count_para(input_text_final)
structural_based_features['average_number_of_sentences_per_paragraph'] = structural_based_features['number_of_sentences']/structural_based_features['number_of_paragraphs']
structural_based_features['average_number_of_words_per_paragraph'] = tokens_len/structural_based_features['number_of_paragraphs']
structural_based_features['average_number_of_characters_per_paragraph'] = textstat.char_count(input_text_final, ignore_spaces=False)/structural_based_features['number_of_paragraphs']
structural_based_features['average_number_of_words_per_sentence'] = tokens_len/len(sent_tokenize(input_text_final))
for j in input_text_final:
    if j.split() == []:
        structural_based_features['total_number_of_blank_lines'] += 1
                      
    
for z in structural_based_features:
    temp_dict[z] = structural_based_features[z]

###### count of syntactic_based_features
        
syntactic_based_features = {'number_of_single_quotes':0,'number_of_comma':0,'number_of_period_counter':0,'number_of_colons':0,
                            'number_of_semicolons':0,'number_of_question_marks':0,'number_of_multiple_question_marks':0,
                            'number_of_exclaimation_marks':0,'number_of_multiple_exclaimation_marks':0,'number_of_ellipsis':0}
        
syntactic_based_features['number_of_single_quotes'] = len(re.compile(r"\'").findall(input_text_final))
syntactic_based_features['number_of_comma'] = len(re.compile(r"\,").findall(input_text_final))
syntactic_based_features['number_of_period_counter']= len(re.compile(r"\.").findall(input_text_final))
syntactic_based_features['number_of_colons'] = len(re.compile(r"\:").findall(input_text_final))
syntactic_based_features['number_of_semicolons'] = len(re.compile(r"\;").findall(input_text_final))
syntactic_based_features['number_of_question_marks'] = len(re.compile(r"\"").findall(input_text_final))
syntactic_based_features['number_of_exclaimation_marks'] = len(re.compile(r"\!").findall(input_text_final))
multiple_ques_mark=0
multiple_exclaim_mark=0
for k in input_text_final:
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
    
###### count of words_based_features
     #####   parameters  #####
    
email_words_freq = {}
for k in text_tokenize_just_words:
    if k not in email_words_freq:
        email_words_freq[k]= text_tokenize_just_words.count(k)
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
sigmaV,sympsonD,entropy,yuleK,honoreR=0,0,0,0,0
for k in range(0, len(Vm)):
    sigmaV = sigmaV + (Vm[k]*(((k+1)/tokens_len)**2))
    sympsonD = sympsonD +(Vm[k]*((k+1)/tokens_len)*(k/(tokens_len-1)))
    entropy = entropy + (Vm[k]*((k+1)/tokens_len)*math.log10(tokens_len/(k+1)))
yuleK = (10**(-4) * (-1/tokens_len)) + sigmaV
if hepaxlegomena!=max_freq:
    honoreR = (100 * math.log10(tokens_len))/(1-(hepaxlegomena/max_freq))
else:
    honoreR = numpy.finfo(numpy.float64).max - 1000
        
########
    
words_based_features={'total_number_of_words':0,'average_length_for_words':0,'vocabulary_richness':vocabulary_richness,'number_of_long_words':0,
                      'number_of_short_words':0,'hepaxlegomena':hepaxlegomena,'hepaxdislegomena':hepaxdislegomena,'yuleK':yuleK,
                      'sympsonD':sympsonD,'honoreR':honoreR,'entropy':entropy}
        
words_based_features['total_number_of_words'] = tokens_len
for k in text_tokenize_just_words:
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
    
words = ['all','everybody','his','most','other','that','what','your','another','everyone','I','much','others','theirs','whatever','yours',
         'any','everything','it','myself','ours','them','which','yourself','anybody','few','its','neither','ourselves','themselves','whichever',
         'yourselves','anyone','he','itself','no','one','several','these','who','anything','her','little','nobody','she','hey','whoever','both',
         'hers','many','none','some','this','whom','each','herself','me','nothing','somebody','those','whomever','him','mine','someone','us','whose',
         'either','himself','more','something','we','you','yes','okay','OK','amen','Ok','a','an','the','Him','my','no one','our','their','Be','am',
         'is ','are','was','were','being','can','could','dare','do','does','did','have','has','had','having','may','might','must','need','ought',
         'shall','should','will','would','they','a','Yes','No','Okay','Amen','The','A','An','Aah','aha','ahem','ahh','argh','aww','aw','bah','boo',
         'booh','brr','duh','eek','eep','eh','eww','gah','gee','grr','hmm','humph','harumph','huh','hurrah','ich','yuck','yak','meh','mhm uh-hu','mm',
         'mmh','muahaha','mwahaha','nah','nuh-uh','oh','ooh-la-la','oh-lala','ooh','oomph','umph','oops','ow','oy','pew','pff','phew','psst','sheesh',
         'jeez','shh','shoo','tsk-tsk','uh-uh','oh-oh','uhh','err','wee','whee','whoa','wow','yahoo','yay','yeah','yee-haw','yoo-yoo','yah-uh','mwah',
         'neener-neener','zowie','zoinks','yow','yikes','va-va-voom','ugh','tchah','rah','sis-boom-bah','ole','lah-de-dah','hup','hubba-hubba','ho-hum',
         'be','been','and','or','though','now','if','while','in','order','case','because','yet','unless','even','whereas','nor','so','when','although',
         'only','whether','not','until','adios','dear','Ha-ha','howdy','tush','whoosh','ah','begorra','doh','hail','hoy','ouch','tut','behold',
         'hallelujah','Tutetut','bejesus','heigh-ho','phooey','ahoy','bingo','encore','hello','hurray','pipepip','uh-huh','yippee','alack','bleep',
         'eureka','hem','hush','pooh','uh-oh','yo','alas','fie','indeed','pshaw','uheuh','yoicks','bravo','presto','jeepers','creepers','rats','viva',
         'yoo-hoo','alleluia','bye','whiz','hi','righto','voila','yuk','aloha','cheerio','gesundheit','hip','lo','scat','wahoo','yummy','cheers',
         'goodness','man','well','zap','attaboy','ciao','gosh','ho','word','shoot','crikey','great','hum','long','whoopee','ay','cripes','hah','hot',
         'dog','Touch','whoops','aboard','astride','down','of','through','worth','on','to','front','about','at','during','off','throughout',
         'according','onto','lieu','above','athwart','except','till','ahead','out','from','place','absent','atop','failing','as','spite','across',
         'barring','following','opposite','toward','aside','outside','account','after','before','for','towards','owing','behalf','against','behind',
         'under','close','prior','top','along','below','over','underneath','due','pursuant','versus','alongside','beneath','inside','past','unlike',
         'regardless','concerning','amid','beside','into','per','far','subsequent','considering','amidst','besides','like','plus','up','regarding',
         'among','between','mid','upon','apart','amongst','beyond','minus','round','via','by','means','around','but','near','save','with','instead',
         'accordance','next','since','within','addition']
    
for j in words:
    function_based_features['number_of_'+j] = 0
    function_based_features['number_of_'+j] = count_given_word(i.translate(str.maketrans('', '', string.punctuation)),j)
        
for z in function_based_features:
    temp_dict[z] = function_based_features[z]

y_pred=model.predict(temp_dict)