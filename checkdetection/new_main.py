from process_cheque import front_process,back_process
import os
import cv2 as cv
import pandas as pd
from words2num import parse_int
from sign import signv
import argparse
import process_back_details
import time
from process_back_details import pr

t1=time.time()
ap=argparse.ArgumentParser()
ap.add_argument("-f","--f_image",required=True,help="path to input image")
ap.add_argument("-b","--b_image",required=True,help="path to input image")
args=vars(ap.parse_args())
img=cv.imread(args["f_image"])
size=img.shape

date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no=front_process(img,size)

db=pd.read_csv(r"chequedb12.csv")
db1=db.loc[db['account_no']==ac]

def verify():
    curr_amt=int(db1['current_amount'].values)
    leaves_left=int(db1['cheque_issued'].values)
    x=['self','myself']
    if(curr_amt<amount):
        print("Cannot proceed transaction : INSUFFINIENT FUNDS")
        return 0
    if(leaves_left<leaf_no):
        print("Invalid Cheque Number")
        return 0
    if(payee_name in x):
        print("This cheque is for NEFT/RTGS transaction")
        return 0
    y=parse_int(payee_amt)
    if(y!=amount):
        print("Invalid amount : Amount in words does not match given amount")
        return 0
    else:
        return 1

x=verify()
if(x==1):
    print("Front of the cheque is verified")
    print("Date : ",date,"\nAmount : ",amount,"\nBank Name : ",bank,"\nIFSC code : ",ifsc,"\nPayee Name : ",payee_name,"\nPayee Amount : ",payee_amt,"\nAcount Number : ",ac,"\nMICR code : ",leaf_no)
    back=cv.imread(args["b_image"])
    size=img.shape
    back_ocr,back_detect=back_process(back,size)
    account,phone,name=pr(back_ocr)
    flag=int(0)
    payee_db=pd.read_csv(r"Payee_Database.csv")
    if(account and name):
        db2=payee_db.loc[payee_db['account number']==int(account)]
        verify_name=db2['Name'].values
        verify_name=(''.join(verify_name))
        if(verify_name==name):
            flag+=1
    if(phone and name):
        db2=payee_db.loc[payee_db['Phone Number']==int(phone)]
        verify_name=db2['Name'].values
        verify_name=(''.join(verify_name))
        if(verify_name==name):
            flag+=1
    if(flag!=0):
        print("Back of the cheque is Verified.")
        print("Name : ",name,"\nAccount Number of Payee : ",account,"\nPhone Number of Payee : ",phone)
    if(flag==0):
        print("Back of the cheque is not verified.")
        print("Name : ",name,"\nAccount Number of Payee : ",account,"\nPhone Number of Payee : ",phone)
    
t2=time.time()

print("Time Taken : ",t2-t1)
    

#sign section
imgs2 = cv.imread("r"+"str1")
path=r'sign_directory'
dir_path=os.path.join(path,str(ac))

print(signv(r"Images\sign.jpeg",dir_path+('.jpeg')))
