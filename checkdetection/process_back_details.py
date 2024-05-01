import os
import cv2 as cv
import pandas as pd

def pr(ocr):
    account=[]
    phone=[]
    name=[]
    for i in ocr:
        if('ac' in i.lower() or 'account' in i.lower()):
            for j in i:
                if(j.isdigit()):
                    account.append(j)
        elif('phone' in i.lower()):
            for j in i:
                if(j.isdigit()):
                    phone.append(j)
        elif('name' in i.lower()):
            if(":" in i.lower()):
                d=i.index(':')
            if("-" in i.lower()):
                d=i.index('-')
            name.append(ocr[d+1:len(i)])
    name=(''.join(name))
    name=name.strip()
    account=(''.join(account))
    phone=(''.join(phone))
    return int(account),int(phone),name

