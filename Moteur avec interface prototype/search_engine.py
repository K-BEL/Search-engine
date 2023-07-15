import os
import sys
import re
from time import time

def split_text(text):
    text = re.compile("[^\w]|_").sub(" ", text)
    word_list = re.findall("\w+", text.lower())    
    return word_list

def sp_text(text):
    word_list = re.split('\s+', text.lower())
    punctuation = re.compile(r'[-.?!,":;()|0-9]')
    
    for i, word in enumerate(word_list):
        word_list[i] = punctuation.sub("", word)
    
    return word_list


def create_dict(base_dir):
    file_list = os.listdir(base_dir)
    global_dict = {}
    
    start = time()
    for file in file_list:
        filename = os.path.join(base_dir, file)
        f = open(filename, "r", encoding='utf8')
        text = f.read()
        f.close()
        words = split_text(text)
        
        for i, word in enumerate(words):
            local_dict = {}
            local_list = []
            
            if word in global_dict:
                local_dict = global_dict[word]
                
                if file in local_dict:
                    local_list = local_dict[file]
                    local_list.append(i)
                else:
                    local_list.append(i) 
                local_dict[file] = local_list
                
            else:
                local_list.append(i)
                local_dict[file] = local_list
            
            global_dict[word] = local_dict
           
        
    print ("Temps de création du dictionnaire global : ", (time()-start))
            
    return global_dict
            

def boolean_query(dict, query_terms):
    result = []
    
    for term in query_terms:
        temp = {}
        if term in dict:
            temp = dict[term]
            if len(result) == 0:
                result = temp.keys()
            else:
                result = [x for x in result if x in temp.keys()]
        else:
            result = []
            break
            
    return result
        
  
def phrase_query(dict, query):
    keys = dict.keys()
    temp_query = query
    query = split_text(query)
    bool_query_res = boolean_query(dict, query)
    result = []
    
    for res in bool_query_res:
        list = []
        for term in query:
            if term in keys:
                temp_dict = dict[term]
                
                if res in temp_dict:
                    list.append(temp_dict[res])
                    
        for index in range(len(list)):
            list[index] = [x-index for x in list[index]]
            
        intersect = set(list[0]).intersection(*list)
        if len(intersect) != 0:
            result.append(res)
            
    return result
               

def rotate(str,n):
    return str[n:] + str[:n]


def create_permuterm(word_list):
    dict = {}
    
    strt = time()
    for word in word_list:
        temp = word + '$'
        for i in range(len(temp)):
            temp = rotate(temp, 1)
            dict[temp] = word
            
    print ("Le temps nécessaire à la création de l'indice permuterm est de: ", (time()-strt))            
    return dict
        

def wc_query(dict, pdict, query_terms):
    pkeys = pdict.keys()
    result = []
    
    for term in query_terms:
        term = term + '$'
        while(term[-1] != '*'):
            term = rotate(term, 1)
            
        term = term[:-1]
        temp_list = []
        
        for pkey in pkeys:
            if term in pkey:
                pk = pdict[pkey]
                if pk in temp_list:
                    continue
                else:
                    temp_list.append(pk)
                
        temp_result = []
        for temp in temp_list:
            t_list = []
            t_list.append(temp)
            temp_result = temp_result + boolean_query(dict, t_list)
            
        if len(result) == 0:
            result = temp_result
        else:
            result = [x for x in result if x in temp_result]
        
    result_set = set(result)
    result = list(result_set)
        
    return result

base_dir = r"C:\Users\LENOVO\Desktop\Projet\projectCorpus"
file_list = os.listdir(base_dir)

dict = create_dict(base_dir)
pdict = create_permuterm(dict.keys())

def search(input_query:str):
    result = []
    if input_query == "":
        return False, "Saisissez une requête non-vide :"
    else:
        input_terms = sp_text(input_query)
        
        w_query_terms = []
        b_query_terms = []
        for w in input_terms:
            if '*' in w:
                w_query_terms.append(w)
            else:
                b_query_terms.append(w)
                
        if len(w_query_terms) > 0:
            result1 = wc_query(dict, pdict, w_query_terms) 
            result.append(result1)  

        matches = re.findall(r'\"(.+?)\"', input_query)
        ph_query = ",".join(matches)
        p_query_list = ph_query.split(",")
        
        result2 = []
        if ph_query != "":
            for p_query in p_query_list:
                temp = phrase_query(dict, p_query)
                
                if len(result2) == 0:
                    result2 = temp
                else:
                    result2 = [x for x in result2 if x in temp]
            result.append(result2)
            
        if len(b_query_terms) > 0:
            result3 = boolean_query(dict, b_query_terms)
            result.append(result3)
            
    if len(result) > 0:       
        result_set = set(result[0]).intersection(*result)
        result = list(result_set)
    
        if len(result) > 0:
            result = [x[:-4] for x in result]
            return True, result
        else:
            return False, "Désolé pas de correspondance :("
