import check 
import pk

question="yadang的出生年月"
entity,att=pk.seg(question)

print(entity,' ',att)


def answer(entity,att):
    if '地址' in att:
         check.find_add_by_col(entity)
    if '类型' in att:
         check.find_cat_by_col(entity)
    if '类别' in att:
         check.find_typ_by_col(entity)
    if '英文名'in att:
        check.find_eng_by_col(entity)
    if '缩写'in att:
        check.find_abb_by_col(entity)
    if '校长'in att:
        check.find_cur_by_col(entity)
    if '奖项'in att:
        check.find_maj_by_col(entity)
    if '论文'in att:
        check.find_rep_by_per(entity)
    if '毕业院校'in att:
        check.find_col_by_per(entity)
    if '从属机构'in att:
        check.find_aff_by_per(entity)
    if '成就'in att:
        check.find_ach_by_per(entity)
    if'中文名字'in att:
        check.find_chi_by_per(entity)
    if '地位'in att:
        check.find_sta_by_per(entity)
    if '所有信息'in att:
        check.find_all_by_per(entity)
    if'经济学家' in att:
        check.find_per_by_col(entity)
    if '建立时间' in att:
        check.find_est_by_col(entity)
    if'年诺贝尔经济学奖'in entity:
        check.find_per_by_ach(entity)

    if '诺贝尔经济学奖' == entity:
        check.find_per_by_ach(entity)

    if'新古典学派'in entity:
        print("萨伊, 马尔萨斯,约翰．穆勒, 庞巴维克, 马歇尔")
    if'当前' in entity:
        print("BBVA Foundation Frontiers of Knowledge Award in Economics,Fi-nance and Management"+'\n'+"MSSANZ"+'\n'+
        "Frisch Medal"+'\n'+"Global Economy Prize for Economics"+'\n'+"Prize in Economic Sciences in Memory of Alfred Nobel"
        +'\n'+"First Monograph Prize" +'\n'+"IZA Prize"+'\n'+"T.S.Ashton Prize "+'\n'+"Nemmers Prizes in economics "+'\n'+
        "EIB Prize Outstanding Contribution Award"+'\n'+"John von Neumann Award"+'\n'+"Schumpeter Prize "+'\n'+"Erik Kempe Award"+'\n'+
        "Hicks-Tinbergen Award ")
    if'出生年月' in att:
         print("对不起，你所要找的信息并不存在哦！")

answer(entity,att)