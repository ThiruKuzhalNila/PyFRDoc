# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 15:59:25 2022

@author: ThiruKuzhal
"""

import pandas as pd
from collections import Counter

def EFS_fs_method(cls_prob,EFS_P1,EFS_P2,feature_list):
	EFS={}
	for fs in feature_list:
		EFS[fs]=0
		for cls in cls_prob.keys():
			EFS[fs]=EFS[fs]+(EFS_P1[cls][fs]*EFS_P2[cls][fs])
	return 	EFS

if __name__ == '__main__':
    
    dtm_df = pd.read_excel('DTM.xlsx')
    print("##############\nDocument Term Matrix")
    print(dtm_df)
    features=list(dtm_df.columns)[1:]
    print(features)
    class_list=list(dtm_df['Category'])
    print(class_list)
    cls_cnt=Counter(class_list)
    tot_doc=sum(cls_cnt.values())
    cls_prob={}
    for keys in cls_cnt:
        cls_prob[keys]=cls_cnt[keys]/tot_doc
    
    feature_list=features    
    fs_prob={}
    fs_prob_given_class={}
    inverse_fs_prob_given_class={}
    fs_prob_given_inverse_class={}
    inv_fs_prob={}
    inv_fs_prob_given_class={}
    
    
    for fs in feature_list:
        
        fs_value=0
        inv_fs_value=0
        
        inv_fs_prob_given_class[fs]={}
        fs_prob_given_inverse_class[fs]={}
        fs_prob_given_class[fs]={}
        
        for cls in cls_prob.keys():
            #inverse_fs_prob_given_class
            no_of_present_doc=len(dtm_df.loc[(dtm_df[fs]==0)&(dtm_df['Category']==cls)])
            inv_fs_prob_one_class=no_of_present_doc/len(dtm_df.loc[dtm_df['Category']==cls])
            inv_fs_prob_given_class[fs][cls]=inv_fs_prob_one_class
            inv_fs_value=inv_fs_value+(cls_prob[cls]*inv_fs_prob_one_class)
            
            #fs_prob_given_inverse_class
            no_of_present_doc=len(dtm_df.loc[(dtm_df[fs]>0)&(dtm_df['Category']!=cls)])
            fs_prob_given_inverse_class[fs][cls]=no_of_present_doc/len(dtm_df.loc[dtm_df['Category']!=cls])
            #fs_prob_given_class
            no_of_present_doc=len(dtm_df.loc[(dtm_df[fs]>0)&(dtm_df['Category']==cls)])
            fs_prob_one_class=no_of_present_doc/len(dtm_df.loc[dtm_df['Category']==cls])
            fs_prob_given_class[fs][cls]=fs_prob_one_class
            fs_value=fs_value+(cls_prob[cls]*fs_prob_one_class)

        inv_fs_prob[fs]=inv_fs_value
        fs_prob[fs]=fs_value
    print(inverse_fs_prob_given_class)

    cls_prob_given_fs={}
    inv_cls_prob_given_fs={}
    cls_prob_given_inv_fs={}
    for cls in cls_prob.keys():
        cls_prob_given_fs[cls]={}
        inv_cls_prob_given_fs[cls]={}
        cls_value=0
        cls_prob_given_inv_fs[cls]={}
        for fs in feature_list:
            inv_cls_prob_given_fs[cls][fs]=len(dtm_df.loc[(dtm_df[fs]>0)&(dtm_df['Category']!=cls)])/len(dtm_df.loc[dtm_df[fs]>0])
            cls_prob_given_fs[cls][fs]=cls_prob[cls]*fs_prob_given_class[fs][cls]/fs_prob[fs]
            if inv_fs_prob[fs]==0:
                cls_prob_given_inv_fs[cls][fs]=0
            else:
                cls_prob_given_inv_fs[cls][fs]=cls_prob[cls]*inv_fs_prob_given_class[fs][cls]/inv_fs_prob[fs]

    EFS_P1={}
    EFS_P2={}
    for cls in cls_prob.keys():
        EFS_P1[cls]={}
        EFS_P2[cls]={}
        for fs in feature_list:
            EFS_P1[cls][fs]=fs_prob_given_class[fs][cls]/(inv_fs_prob_given_class[fs][cls]+fs_prob_given_inverse_class[fs][cls]+1)
            EFS_P2[cls][fs]=cls_prob_given_fs[cls][fs]/( inv_cls_prob_given_fs[cls][fs]+ cls_prob_given_inv_fs [cls][fs]+1)
    EFS=EFS_fs_method(cls_prob,EFS_P1,EFS_P2,feature_list)
    print(EFS)
    fs_wt = pd.DataFrame(data=EFS, index=['fs_score']).T
    fs_wt.to_excel("EFS_wt.xlsx")
    print("*****\n Done\n*****")
