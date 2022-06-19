# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 02:24:17 2022

@author: ThiruKuzhal
"""
import pandas as pd
import math
from collections import Counter

def MI_fs_method(feature_list,fs_prob,fs_prob_given_class,cls_prob):
    MI={}
    for fs in feature_list:
        mi_log=0
        for cls in cls_prob.keys():
            if(fs_prob_given_class[fs][cls]!=0):
                mi_log=mi_log+(cls_prob[cls]*math.log(fs_prob_given_class[fs][cls]/fs_prob[fs],2))
        MI[fs]=mi_log
    return MI

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
    
    for fs in feature_list:
        fs_value=0
        fs_prob_given_class[fs]={}
        
        for cls in cls_prob.keys():
            
            #fs_prob_given_class
            no_of_present_doc=len(dtm_df.loc[(dtm_df[fs]>0)&(dtm_df['Category']==cls)])
            fs_prob_one_class=no_of_present_doc/len(dtm_df.loc[dtm_df['Category']==cls])
            fs_prob_given_class[fs][cls]=fs_prob_one_class
            fs_value=fs_value+(cls_prob[cls]*fs_prob_one_class)

        fs_prob[fs]=fs_value
                    
    MI=MI_fs_method(feature_list,fs_prob,fs_prob_given_class,cls_prob)
    print(MI)
    fs_wt = pd.DataFrame(data=MI, index=['fs_score']).T
    fs_wt.to_excel("MI_wt.xlsx")
    print("*****\n Done\n*****")
