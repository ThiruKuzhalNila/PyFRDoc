# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 14:46:07 2022

@author: ThiruKuzhal
"""
import pandas as pd
from collections import Counter
def TRDL_fs_method(cls_prob,tf_i,tf_ik,NDM):
    TRDL={}
    for fs in feature_list:
        TRDL[fs]=0
        for cls in cls_prob.keys():
            TRDL[fs]=TRDL[fs]+(1-cls_prob[cls])*(tf_ik[cls][fs]/tf_i[fs])*NDM[fs]
    return TRDL
def NDM_fs_method(cls_prob,fs_prob_given_class,fs_prob_given_inverse_class,feature_list):
	NDM={}
	for fs in feature_list:
		NDM[fs]=0
		for cls in cls_prob.keys():
			x=abs(fs_prob_given_class[fs][cls]-fs_prob_given_inverse_class[fs][cls])
			y=min(fs_prob_given_class[fs][cls],fs_prob_given_inverse_class[fs][cls])
			if y==0:
				y=0.1
			NDM[fs]=NDM[fs]+(cls_prob[cls]*(x/y))
	return 	NDM

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
    tf_i={}
    tf_ik={}
    cls_prob={}
    for keys in cls_cnt:
        cls_prob[keys]=cls_cnt[keys]/tot_doc
        tf_ik[keys]=dtm_df.loc[dtm_df['Category']==keys].sum()
    tf_i=dtm_df.sum()
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

    NDM=NDM_fs_method(cls_prob,fs_prob_given_class,fs_prob_given_inverse_class,feature_list)
    TRDL=TRDL_fs_method(cls_prob,tf_i,tf_ik,NDM)
    fs_wt = pd.DataFrame(data=TRDL, index=['fs_score']).T
    fs_wt.to_excel("TRDL_wt.xlsx")
    print("*****\n Done\n*****")
