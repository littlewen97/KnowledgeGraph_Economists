import pkuseg
def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def seg(question):
    lexicon = ['诺贝尔经济学奖','克拉克奖','经济学奖']
    seg_pos = pkuseg.pkuseg(postag=True,user_dict=lexicon)
    text = seg_pos.cut(question)
    entity = ''
    att = []

    if text[0][1]=='t':
        entity=entity+text[0][0]
        if text[1][1]=='nz':
            entity=entity+text[1][0]
        return entity, att

    if text[0][1]=='nz':
        entity=entity+text[0][0]
        return entity, att

    i=0
    res=[]
    for i, val in enumerate(text) :
        i=i+1
        if val[1]=='u' or val[1]=='c' or val[1]=='w':
            res.append(i)

    if len(res)==0:
        for t in text:
            if not check_contain_chinese(text[0][1]):
                entity = entity + t[0]+' '
            else:
                entity = entity + t[0]
    elif len(res)!=0:
        for t in text[:res[0]-1]:
            if not check_contain_chinese(t[1]):
                entity = entity + t[0]+' '
            else:
                entity = entity + t[0]
        for i in range(1,len(res)+1):
            temp=''
            if i==len(res):
                for t in text[res[i - 1]:]:
                    temp = temp + t[0]
            else:
                for t in text[res[i-1]:res[i]-1]:
                    temp=temp+t[0]
            att.append(temp)

    #哈佛大学的经济学家有哪些
    for i in range(0, len(att)):
        if '经济学家' in att[i]:
            att[i] = '经济学家'

    #货币学派的代表人物
    if '学派' in entity:
        att=[]

    #美国的经济学家有哪些
    if '国' in entity:
        att=[]

    # 经济学奖有哪些
    if '经济学奖' in entity:
        entity='经济学奖'
        att=[]

    return entity, att


#哈佛大学的经济学家有哪些
#哈佛大学   ['经济学家']
question="哈佛大学的经济学家有哪些"
print(question)
entity,att=seg(question)
print(entity,' ',att,'\n')

#实体
#亚当·斯密   []
question2="亚当·斯密"
print(question2)
entity2,att2=seg(question2)
print(entity2,' ',att2,'\n')

#2017年诺贝尔经济学奖的获得者有哪些
#2017年诺贝尔经济学奖   []
question3="2017年诺贝尔经济学奖的获得者"
print(question3)
entity3,att3=seg(question3)
print(entity3,' ',att3,'\n')

#实体的属性1，属性2，属性3和属性4
#亚当·斯密   ['英文名', '成就']
question4="亚当·斯密的英文名，成就"
print(question4)
entity4,att4=seg(question4)
print(entity4,' ',att4,'\n')

#诺贝尔经济学奖的获得者有哪些
#诺贝尔经济学奖   []
question5="诺贝尔经济学奖的获得者"
print(question5)
entity5,att5=seg(question5)
print(entity5,' ',att5,'\n')

#货币学派的代表人有哪些
#货币学派   []
question6="货币学派的代表人物"
print(question6)
entity6,att6=seg(question6)
print(entity6,' ',att6,'\n')

#美国的经济学家有哪些
#美国   []
question7="美国的经济学家有哪些"
print(question7)
entity7,att7=seg(question7)
print(entity7,' ',att7,'\n')

#经济学奖有哪些
#经济学奖   []
question8="经济学奖有哪些"
print(question8)
entity8,att8=seg(question8)
print(entity8,' ',att8,'\n')

#Andrei Shleifer的作品
#Andrei Shleifer    ['作品']
question9="Andrei Shleifer的作品"
print(question9)
entity9,att9=seg(question9)
print(entity9,' ',att9,'\n')

#Andrei Shleifer
#Andrei Shleifer    []
question10="Andrei Shleifer"
print(question10)
entity10,att10=seg(question10)
print(entity10,' ',att10,'\n')

