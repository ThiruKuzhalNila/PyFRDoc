# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 19:51:24 2022

@author: ThiruKuzhal
"""

import pandas as pd
from collections import Counter

def ACC2_fs_method_max(cls_prob,fs_prob_given_class,fs_prob_given_inverse_class,feature_list):
	ACC2={}
	for fs in feature_list:
		ACC2[fs]=0
		for cls in cls_prob.keys():
			x=abs(fs_prob_given_class[fs][cls]-fs_prob_given_inverse_class[fs][cls])
			ACC2[fs]=ACC2[fs]+(cls_prob[cls]*x)
	return 	ACC2

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
    fs_prob_given_class={}
    fs_prob_given_inverse_class={}
    
    
    
    for fs in feature_list:
        

        fs_prob_given_class[fs]={}
        fs_prob_given_inverse_class[fs]={}
        
        
        for cls in cls_prob.keys():
            #fs_prob_given_inverse_class
            no_of_present_doc=len(dtm_df.loc[(dtm_df[fs]>0)&(dtm_df['Category']!=cls)])
            fs_prob_given_inverse_class[fs][cls]=no_of_present_doc/len(dtm_df.loc[dtm_df['Category']!=cls])
        
            #fs_prob_given_class
            no_of_present_doc=len(dtm_df.loc[(dtm_df[fs]>0)&(dtm_df['Category']==cls)])
            fs_prob_one_class=no_of_present_doc/len(dtm_df.loc[dtm_df['Category']==cls])
            fs_prob_given_class[fs][cls]=fs_prob_one_class

    ACC2=ACC2_fs_method_max(cls_prob,fs_prob_given_class,fs_prob_given_inverse_class,feature_list)
    print(ACC2)
    fs_wt = pd.DataFrame(data=ACC2, index=['fs_score']).T
    fs_wt.to_excel("ACC2_wt.xlsx")
    print("*****\n Done\n*****")
