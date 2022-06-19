# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 15:07:48 2022

@author: ThiruKuzhal
"""
import math
import pandas as pd
from collections import Counter
def TFDM_fs_method(cls_prob,TFR,TDR):
    TFDM={}
    for fs in feature_list:
        TFDM[fs]=0
        for cls in cls_prob.keys():
            TFDM[fs]=TFDM[fs]+cls_prob[cls]*TFR[cls][fs]*TDR[cls][fs]
    return TFDM

if __name__ == '__main__':
    
    dtm_df = pd.read_excel('DTM_TFDM.xlsx')
    print("##############\nDocument Term Matrix")
    print(dtm_df)
    features=list(dtm_df.columns)[1:]
    print(features)
    class_list=list(dtm_df['Category'])
    print(class_list)
    cls_cnt=Counter(class_list)
    tot_doc=sum(cls_cnt.values())
    tf_i={}
    tf_ik={}
    mu_i={}
    mu_ik={}
    cls_prob={}
    tf_i=dtm_df.sum()
    mu_i=dtm_df.mean()
    feature_list=features    
    TFR={}
    TDR={}
    N_k={}
    N=tot_doc
    for keys in cls_cnt:
        TFR[keys]={}
        TDR[keys]={}
        cls_prob[keys]=cls_cnt[keys]/tot_doc
        N_k[keys]=cls_cnt[keys]
        tf_ik[keys]=dtm_df.loc[dtm_df['Category']==keys].sum()
        mu_ik[keys]=dtm_df.loc[dtm_df['Category']==keys].mean()
        for fs in feature_list:
            TFR[keys][fs]=tf_ik[keys][fs]/tf_i[fs]
            TDR[keys][fs]= abs( mu_ik[keys][fs]-mu_i[fs])/math.sqrt((N-N_k[keys])/N_k[keys])
    
    TFDM=TFDM_fs_method(cls_prob,TFR,TDR)
    
    fs_wt = pd.DataFrame(data=TFDM, index=['fs_score']).T
    fs_wt.to_excel("TFDM_wt.xlsx")
    print("*****\n Done\n*****")
