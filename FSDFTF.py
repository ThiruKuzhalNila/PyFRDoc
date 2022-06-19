# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 02:45:32 2022

@author: ThiruKuzhal
"""
import pandas as pd
from collections import Counter

def newDDFS_fs_method(cls_prob,cls_prob_given_fs,feature_list,inverse_fs_prob_given_class,fs_prob_given_inverse_class,cls_prob_given_inv_fs):
	newDDFS={}
	for fs in feature_list:
		newDDFS[fs]={}
		for cls in cls_prob.keys():
			x,y,z,x1=cls_prob_given_fs[cls][fs],inverse_fs_prob_given_class[fs][cls],fs_prob_given_inverse_class[fs][cls],cls_prob_given_inv_fs[cls][fs]
			newDDFS[fs][cls]=(x-x1)/(y+z+1)
	return newDDFS

def TF_fs_method(dtm_df,feature_list,cls_prob,cls_cnt):
    tot_doc=sum(cls_cnt.values())
    N_ik={}
    N_k={}
    N_i={}
    mean_i={}
    mean_ik={}
    var_i={}
    var_ik={}
    tf_i={}
    tf_ik={}
    IDFS={}
    for keys in cls_cnt:
        cls_prob[keys]=cls_cnt[keys]/tot_doc
        N_k[keys]=cls_cnt[keys]
        mean_ik[keys]=dtm_df.loc[dtm_df['Category']==keys].mean()
        var_ik[keys]=dtm_df.loc[dtm_df['Category']==keys].std()
        tf_ik[keys]=dtm_df.loc[dtm_df['Category']==keys].sum()
    mean_i=dtm_df.mean()
    var_i=dtm_df.std()
    tf_i=dtm_df.sum()
    for fs in feature_list:
        N_i[fs]=len(dtm_df.loc[dtm_df[fs]>0])
        N_ik[fs]={}
        for cls in cls_prob.keys():
            no_of_present_doc=len(dtm_df.loc[(dtm_df[fs]>0)&(dtm_df['Category']==cls)])
            N_ik[fs][cls]=no_of_present_doc
  
    
    max_BC={}
    for cls in cls_prob.keys():
        max_BC[cls]=-1
        for fs in feature_list:
            x=(N_ik[fs][cls]/N_i[fs])*(tf_ik[cls][fs]/tf_i[fs])
            if(x>max_BC[cls]):
                max_BC[cls]=x
    BC={}
    for fs in feature_list:
        BC[fs]={}
        for cls in cls_prob.keys():
            if(var_i[fs]==0):
                BC[fs][cls]=0
            else:
                BC[fs][cls]=(N_ik[fs][cls]/N_i[fs])*(tf_ik[cls][fs]/tf_i[fs])
                
    max_WC={}          
    for cls in cls_prob.keys():
        max_WC[cls]=-1
        for fs in feature_list:
            x=N_ik[fs][cls]*mean_ik[cls][fs]/N_k[cls]
            if(x>max_WC[cls]):
                max_WC[cls]=x
    WC={}
    for fs in feature_list:
        WC[fs]={}
        for cls in cls_prob.keys():
            if(var_i[fs]==0):
                WC[fs][cls]=0
            else:
                WC[fs][cls]=(N_ik[fs][cls]*mean_ik[cls][fs]/N_k[cls])/max_WC[cls]
                #if(var_ik[cls][fs]!=0):
                 #   WC[fs][cls]=(1/var_ik[cls][fs])* WC[fs][cls]    
    return (BC,WC)
def FS_DFTF_fs_method(feature_list,cls_prob,DDFS,WC,BC):
    FS_DFTF={}
    for fs in feature_list:
        FS_DFTF[fs]=0
        for cls in cls_prob.keys():
            FS_DFTF[fs]=FS_DFTF[fs]+(cls_prob[cls]*DDFS[fs][cls]*WC[fs][cls]*BC[fs][cls])
    return FS_DFTF

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
                
    (BC,WC)=TF_fs_method(dtm_df,feature_list,cls_prob,cls_cnt)   
    newDDFS=newDDFS_fs_method(cls_prob,cls_prob_given_fs,feature_list,inv_fs_prob_given_class,fs_prob_given_inverse_class,cls_prob_given_inv_fs)
    FS_DFTF=FS_DFTF_fs_method(feature_list,cls_prob,newDDFS,WC,BC)
    fs_wt = pd.DataFrame(data=FS_DFTF, index=['fs_score']).T
    fs_wt.to_excel("FS_DFTF.xlsx")
    print("*****\n Done\n*****")