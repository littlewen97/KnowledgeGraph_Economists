from config import graph
import codecs
import os
import json
import base64


def get_json_data(data):
    json_data={'data':[],"links":[]}
    d=[]


    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.name']+"_"+i['p.label'])
        d.append(i['n.name']+"_"+i['n.label'])
        d=list(set(d))
    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")
    
        data_item={}
        name_dict[j_array[0]]=count
        count+=1
        data_item['name']=j_array[0]
        data_item['category']=CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
   
        link_item = {}
        
        link_item['source'] = name_dict[i['p.name']]
        
        link_item['target'] = name_dict[i['n.name']]
        link_item['value'] = i['r.property1']
        json_data['links'].append(link_item)

    return json_data

def find_rep_by_per(e1):
        cypher = graph.run('match(p:person{person:"%s"})-[r:publish]-(c) return c.report'% (e1)) 
        res = (cypher).data()
        my_set = set()
        for item in res:
            my_set.add(item['c.report'])
        print(list(my_set))


def find_col_by_per(e1):
        cypher = graph.run('match(p:person{person:"%s"})-[r:graduate_from]-(c) return c.chinesename'% (e1)) 
        print((cypher).data()[0]['c.chinesename'])

def find_aff_by_per(e1):
        cypher = graph.run('match(p:person{person:"%s"})-[r:belong_to]-(c) return c.affiliation'% (e1)) 
        print((cypher).data()[0]['c.affiliation'])

def find_ach_by_per(e1):
        cypher = graph.run('match(p:person{person:"%s"}) return p.achievement'% (e1)) 
        print((cypher).data()[0]['p.achievement'])

def find_chi_by_per(e1):
        cypher = graph.run('match(p:person{person:"%s"}) return p.chinesename1'% (e1)) 
        print((cypher).data()[0]['p.chinesename1'])

def find_sta_by_per(e1):
        cypher = graph.run('match(p:person{person:"%s"}) return p.status'% (e1)) 
        print((cypher).data()[0]['p.status'])

def find_add_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.address'% (e1))
        print((cypher).data()[0]['c.address'])     

def find_abb_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.abbreviation'% (e1))
        print((cypher).data()[0]['c.abbreviation'])

def find_cat_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.category'% (e1))
        print((cypher).data()[0]['c.category'])

def find_typ_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.type1'% (e1))
        print((cypher).data()[0]['c.type1'])

def find_eng_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.college'% (e1))
        print((cypher).data()[0]['c.college'])

def find_cur_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.currentleader'% (e1))
        print((cypher).data()[0]['c.currentleader'])

def find_maj_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.majorawards'% (e1))
        print((cypher).data()[0]['c.majorawards'])

def find_est_by_col(e1):
        cypher = graph.run('match(c:college{chinesename:"%s"}) return c.established'% (e1))
        print((cypher).data()[0]['c.established'])

def find_per_by_col(e1):
        cypher = graph.run('match(p)-[r:graduate_from]-(c:college{chinesename:"%s"}) return p.person'% (e1))
        res = (cypher).data()
        my_set = set()
        for item in res:
            my_set.add(item['p.person'])
        print(list(my_set))

def find_all_by_per(e1):
        cypher = graph.run('match(p:person{person:"%s"}) return p.chinesename1,p.status,p.achievement'%(e1))
        res = (cypher).data()
        for item in res:
            print('中文名:'+item['p.chinesename1']+'  '+'社会地位:'+item['p.status']+'  '+'主要成就:'+item['p.achievement'])
           
def find_per_by_ach(e1):
        cypher = graph.run("match (n:person) where n.achievement =~ '.*%s.*'  return n.person"%(e1))
        res = (cypher).data()
        my_set = set()
        for item in res:
            my_set.add(item['n.person'])
        print(list(my_set))

# def find_rep_by_per(e1):
#         data_array=[]
#         cypher = graph.run('match(p:person{person:"%s"})-[r:publish]-(c) return c.affiliation'% (e1)) 
#         cypher = list(cypher)
#         data_array.extend(cypher)
#         print(data_array[0])
# find_per_by_ach('dsd')