# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 20:28:41 2022

@author: ThiruKuzhal
"""

import pandas as pd
from collections import Counter

def DF_fs_method(feature_list,dtm_df):
	DF={}
	for fs in feature_list:
		DF[fs]=len(dtm_df.loc[(dtm_df[fs]>0)])
	return DF

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
    DF=DF_fs_method(feature_list,dtm_df)
    print(DF)
    fs_wt = pd.DataFrame(data=DF, index=['fs_score']).T
    fs_wt.to_excel("DF_wt.xlsx")
    print("*****\n Done\n*****")
