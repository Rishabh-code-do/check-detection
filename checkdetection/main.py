from process_cheque import front_process,back_process
import os
import cv2 as cv
import pandas as pd
from words2num import parse_int
from process_back_details import pr
import time

def verify(db1,amount,payee_name,leaf_no,payee_amt):
    curr_amt=int(db1['current_amount'].values)
    leaves_left=int(db1['cheque_issued'].values)
    verify_dict={
        'sufficient_funds' : 0,
        'MICR CODE' :0,
        'NFT/RTGS':0,
        'amount_in_words':0,
        'valid':0,
        'invalid':0
    }
    x=['self','myself']
    if(curr_amt>=amount):
        # print("Cannot proceed transaction : INSUFFINIENT FUNDS")
        # return 0
        verify_dict['sufficient_funds']=1
    else:
        verify_dict['invalid']=1
    if(leaves_left>=leaf_no):
        # print("Invalid Cheque Number")
        # return 0
        verify_dict['MICR CODE']=1
    else:
        verify_dict['invalid']=1
    if(payee_name in x):
        # print("This cheque is for NEFT/RTGS transaction")
        # return 0
        verify_dict['NFT/RTGS']=1
    y=parse_int(payee_amt)
    if(y=="invalid"):
        verify_dict['invalid']=1
    elif(y==amount):
        # print("Invalid amount : Amount in words does not match given amount")
        # return 0
        verify_dict['amount_in_words']=1
    else:
        verify_dict['invalid']=1
    if(verify_dict['invalid']==0):
        verify_dict['valid']=1
    return verify_dict
    

def FUN(str,str3):

    print('Hello shailly')
    t1=time.time()
    str1=str[1:]
    raw_s=r'{}'.format(str1)
    print(raw_s)
    img=cv.imread(raw_s)
    size=img.shape

    date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no=front_process(img,size)
    db=pd.read_csv(r"chequedb12.csv")
    db1=db.loc[db['account_no']==ac]



    front_ver=verify(db1,amount,payee_name,leaf_no,payee_amt)
    if(front_ver['valid']==1):
        print("Front of the cheque is verified")
        print("Date : ",date,"\nAmount : ",amount,"\nBank Name : ",bank,"\nIFSC code : ",ifsc,"\nPayee Name : ",payee_name,"\nPayee Amount : ",payee_amt,"\nAcount Number : ",ac,"\nMICR code : ",leaf_no)
        str2=str3[1:]
        raw_s1=r'{}'.format(str2)
        back=cv.imread(raw_s1)
        size=img.shape
        back_ocr,back_detect=back_process(back,size)
        account,phone,name=pr(back_ocr)
        flag=int(0)
        payee_db=pd.read_csv(r"Payee_Database.csv")
        back_ver={
            'back_account' : 0,
            'back_phone':0,
            'back_name':0,
            'invalid':0,
            'valid':0
        }
        if(account and name):
            db2=payee_db.loc[payee_db['account number']==account]
            if(db2['Name'].values==payee_name):
                back_ver['back_account']=1
            else:
                back_ver['invalid']=1
        if(phone and name):
            db2=payee_db.loc[payee_db['Phone Number']==phone]
            if(db2['Name'].values==payee_name):
                back_ver['back_phone']=1
            else:
                back_ver['invalid']=1
        if(back_ver['invalid']==0):
            print("Back of the cheque is Verified.")
        else:
            print("Back of the cheque is not verified")
        print("Name : ",name,"\nAccount Number of Payee : ",account,"\nPhone Number of Payee : ",phone)
        # if(flag==0):
        #     print("Back of the cheque is not verified.")
        #     print("Name : ",name,"\nAccount Number of Payee : ",account,"\nPhone Number of Payee : ",phone)
    t2=time.time()
    print("Time Taken : ",t2-t1)
    return front_ver,date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no,back_ver,account,phone,name