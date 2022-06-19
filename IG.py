# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 02:28:29 2022

@author: ThiruKuzhal
"""
import math
import pandas as pd
from collections import Counter

def IG_fs_method(cls_prob,fs_prob,inv_fs_prob,cls_prob_given_fs,cls_prob_given_inv_fs,feature_list):
	cls_log=0
	for cls in cls_prob.keys():
		cls_log=cls_log+(cls_prob[cls]*math.log(cls_prob[cls],2))
		
	IG={}
	for fs in feature_list:
		IG[fs]=0
		p1,p2,p3=0,0,0
		temp2=0
		temp3=0
		for cls in cls_prob.keys():
			if(cls_prob_given_fs[cls][fs]!=0):
				temp2=temp2+(cls_prob_given_fs[cls][fs]*math.log(cls_prob_given_fs[cls][fs],2))
			if(cls_prob_given_inv_fs[cls][fs]!=0):
				temp3=temp3+(cls_prob_given_inv_fs[cls][fs]*math.log(cls_prob_given_inv_fs[cls][fs],2))
		p1=-cls_log
		p2=fs_prob[fs]*temp2
		p3=inv_fs_prob[fs]*temp3
		IG[fs]=p1+p2+p3
	return IG

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
                
    IG=IG_fs_method(cls_prob,fs_prob,inv_fs_prob,cls_prob_given_fs,cls_prob_given_inv_fs,feature_list)
    print(IG)
    fs_wt = pd.DataFrame(data=IG, index=['fs_score']).T
    fs_wt.to_excel("IG_wt.xlsx")
    print("*****\n Done\n*****")
