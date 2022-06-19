# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 22:02:40 2022

@author: ThiruKuzhal
"""

import pandas as pd
from collections import Counter

def DFS_fs_method(cls_prob,cls_prob_given_fs,feature_list,inverse_fs_prob_given_class,fs_prob_given_inverse_class):
	DFS={}
	for fs in feature_list:
		DFS[fs]=0
		for cls in cls_prob.keys():
			x,y,z=cls_prob_given_fs[cls][fs],inverse_fs_prob_given_class[fs][cls],fs_prob_given_inverse_class[fs][cls]
			DFS[fs]=DFS[fs]+(x/(y+z+1))	
	return DFS

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
    
        
    cls_prob_given_fs={}
    cls_prob_given_inv_fs={}
    for cls in cls_prob.keys():
        cls_prob_given_fs[cls]={}
        cls_value=0
        cls_prob_given_inv_fs[cls]={}
        for fs in feature_list:
            cls_prob_given_fs[cls][fs]=cls_prob[cls]*fs_prob_given_class[fs][cls]/fs_prob[fs]
            if inv_fs_prob[fs]==0:
                cls_prob_given_inv_fs[cls][fs]=0
            else:
                cls_prob_given_inv_fs[cls][fs]=cls_prob[cls]*inv_fs_prob_given_class[fs][cls]/inv_fs_prob[fs]
                
    DFS=DFS_fs_method(cls_prob,cls_prob_given_fs,feature_list,inv_fs_prob_given_class,fs_prob_given_inverse_class)
    print(DFS)
    fs_wt = pd.DataFrame(data=DFS, index=['fs_score']).T
    fs_wt.to_excel("DFS_wt.xlsx")
    print("*****\n Done\n*****")
