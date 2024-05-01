
import cv2 as cv
import os
import api


def break_image(img):
    #    img=cv.imread(r"Cheque120615.jpg")
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, img = cv.threshold(img, 150, 255, cv.THRESH_BINARY)
    edged = cv.Canny(img, 150, 500)
    contours, hierarchy = cv.findContours(edged,
                                          cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(img, contours, -1, (0, 255, 0), 2)
    size = img.shape
    # datebox=img[0:size[0]//5,size[1]-(size[1]//4):size[1]]
    payee_name = img[size[0]//5:size[0]//2, 50:(size[1]-(size[1]//5)-50)]
    # bottom_box=img[size[0]-(size[0]//5):size[0],size[1]//5:size[1]-size[1]//5]
    # amt_box=img[size[0]//3:size[0]//2,size[1]-(size[1]//3):size[1]]
    # bank_name=img[0:size[0]//5,0:size[1]-(size[1]//3)]
    # ac_no=img[size[0]//2:size[0]-(size[0]//5*2),0:size[1]]
    ac_no = img[size[0]//2-25:size[0]-(size[0]//5*2), 0:size[1]-(size[1]//3)]
    sign_box = img[size[0]//2:size[0] -
                   (size[0]//6), size[1]-(size[1]//3):size[1]]

    parent_dir = os.getcwd()
    image_dir = "Images"
    path = os.path.join(parent_dir, image_dir)
    if (not os.path.exists(path)):
        os.mkdir(path)

    # cv.imwrite(os.path.join(path , 'Date.jpeg'), datebox)
    # Date = m.azure_ocr_api("Date.jpeg")

    cv.imwrite(os.path.join(path, 'sign.jpeg'), sign_box)
    # sign = m.azure_ocr_api("sign.jpeg")

    # cv.imwrite(os.path.join(path , 'Payee_name.jpeg'),payee_name)
    # Payee_name = m.azure_ocr_api("Payee_name.jpeg")

    # cv.imwrite(os.path.join(path , 'Account_no.jpeg'),ac_no)
    # Account_no = m.azure_ocr_api("Account_no.jpeg")

    # cv.imwrite(os.path.join(path , 'Bank_name.jpeg'),bank_name)
    # Bank_name = m.azure_ocr_api("Bank_name.jpeg")

    # cv.imwrite(os.path.join(path , 'Bottom_digits.jpeg'),bottom_box)
    # Bottom_digits = m.azure_ocr_api("Bottom_digits.jpeg")

    # cv.imwrite(os.path.join(path , 'Amount.jpeg'),amt_box)
    # Amount = m.azure_ocr_api("Amount.jpeg")

    cv.imwrite(os.path.join(path, 'finals.jpeg'), img)
    cv.imwrite(os.path.join(path, 'payee.jpeg'), payee_name)
    cv.imwrite(os.path.join(path, 'acc_no.jpeg'), ac_no)
    final = []
    final3 = []
    final, final3 = api.azure_ocr_api("finals.jpeg")
    payee_ocr, payee_detect = api.azure_ocr_api("payee.jpeg")
    ac_ocr, ac_detect = api.azure_ocr_api("acc_no.jpeg")
    return final, final3, payee_ocr, payee_detect, ac_ocr, ac_detect


def break_back_image(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, img = cv.threshold(img, 150, 255, cv.THRESH_BINARY)
    edged = cv.Canny(img, 150, 500)
    contours, hierarchy = cv.findContours(edged,
                                          cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(img, contours, -1, (0, 255, 0), 2)
    size = img.shape
    parent_dir = os.getcwd()
    image_dir = "Images"
    path = os.path.join(parent_dir, image_dir)
    if (not os.path.exists(path)):
        os.mkdir(path)
    cv.imwrite(os.path.join(path, 'back.jpeg'), img)
    final, final3 = api.azure_ocr_api("back.jpeg")
    return final, final3


def process_back_image(img, size):
    back_ocr = []
    back_detect = []
    back_ocr, back_detect = break_back_image(img)
    return back_ocr, back_detect


def process_image(img, size):
    final1 = []
    fianl4 = []
    payee_ocr = []
    payee_detect = []
    ac_ocr = []
    ac_detect = []
    final1, final4, payee_ocr, payee_detect, ac_ocr, ac_detect = break_image(
        img)
    return final1, final4, payee_ocr, payee_detect, ac_ocr, ac_detect


def back_process(img, size):
    back_ocr = []
    back_detect = []
    back_ocr, back_detect = process_back_image(img, size)
    return back_ocr, back_detect


def front_process(img, size):
    cheque_ocr = []
    cheque_detect = []
    payee_ocr = []
    payee_detect = []
    ac_ocr = []
    ac_detect = []

    cheque_ocr, cheque_detect, payee_ocr, payee_detect, ac_ocr, ac_detect = process_image(
        img, size)
    date_list, amount_list, bottom, bank_name = create_partitions(
        cheque_ocr, cheque_detect, size)
    date, amount, bank, ifsc, payee_name, payee_amt, ac, leaf_no = extract_details(
        payee_ocr, ac_ocr, cheque_ocr, date_list, amount_list, bottom, bank_name)
    return date, amount, bank, ifsc, payee_name, payee_amt, ac, leaf_no


def create_partitions(cheque_ocr, cheque_detect, size):
    date_list = []
    amount_list = []
    bottom = []
    bank_name = []
    for i in cheque_detect:
        x, w, y, h = int(i[0]), int(i[1]), int(i[4]), int(i[5])
        if (i[4] > size[0]//5 and i[2] > size[1]-(size[1]//4) and i[7] < size[0]//5):
            date_list.append(cheque_ocr[cheque_detect.index(i)])
        if (i[4] > size[0]//5 and i[2] > size[1]-(size[1]//4) and i[7] > size[0]//5):
            amount_list.append(cheque_ocr[cheque_detect.index(i)])
        if (i[1] > size[0]-(size[0]//5)):
            bottom.append(cheque_ocr[cheque_detect.index(i)])
        if (i[7] < size[0]//5 and i[4] < size[1]-(size[1]//3)):
            bank_name.append(cheque_ocr[cheque_detect.index(i)])
        # if(i[1]>size[0]//6 and i[7]<size[0]//2):
        #     payee.append(final2[final5.index(i)])
    return date_list, amount_list, bottom, bank_name


def extract_details(payee_ocr, ac_ocr, cheque_ocr, date_list, amount_list, bottom, bank_name):
    bank = []
    date = []
    finaldigit = []
    finalamount = []
    finalifsc = []
    amount = []
    ifsc = []
    payee_name = []
    payee_amt = []
    flag = 0
    l = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    ac = []
    d = 0
    # date_list,amount_list,bottom,bank_name=create_partitions()
    for i in date_list:
        if (len(i) == 1):
            if (i.isdigit()):
                date.append(i)
        elif (len(i) > 1):
            for j in i:
                if (j.isdigit()):
                    date.append(j)
    date = (''.join(date))
    for i in date:
        for j in i:
            if (j.isdigit()):
                finaldigit.append(j)
    date = (''.join(finaldigit))
    for i in amount_list:
        if ("₹" in i):
            if (len(i) == 1):
                amount.append(amount_list[amount_list.index(i)+1])
            else:
                amount.append(amount_list[amount_list.index(i)])
    for i in amount:
        for j in i:
            if (j.isdigit()):
                finalamount.append(j)
        amount = (''.join(finalamount))
    for i in bank_name:
        if ("bank" in i.lower()):
            bank.append(i)
        elif ("ifsc" in i.lower() or "ifs" in i.lower()):
            ifsc.append(i)
    bank = (''.join(bank))
    for i in payee_ocr:
        if ("pay" in i.lower()):
            for j in range(payee_ocr.index(i)+1, len(payee_ocr)):
                x = payee_ocr[j]
                if ("rupees" in x.lower()):
                    break
                elif (x in l):
                    break
                payee_name.append(x)
        if ("rupees" in i.lower() and "रुपये" not in payee_ocr[payee_ocr.index(i)+1].lower()):
            payee_amt.append(payee_ocr[payee_ocr.index(i)+1])
        elif ("रुपये" in i.lower()):
            payee_amt.append(payee_ocr[payee_ocr.index(i)+1])
    # for i in cheque_ocr:
    #     if("rupees" in i.lower()):
    #         payee_amt.append(cheque_ocr[cheque_ocr.index(i)+1])
    #         break
    for i in ac_ocr:
        for j in i:
            if (j.isdigit()):
                ac.append(j)
    ac = (''.join(ac))
    ifsc = (''.join(ifsc))
    if (":" in ifsc.lower()):
        d = ifsc.index(':')
    if ("-" in ifsc.lower()):
        d = ifsc.index('-')
    finalifsc.append(ifsc[d+1:len(ifsc)])
    ifsc = (''.join(finalifsc))
    ifsc = ifsc.strip()
    if (not amount):
        for i in amount_list:
            for j in i:
                if (j.isdigit()):
                    amount.append(j)
        amount = (''.join(amount))
    for i in bottom:
        if ("⑈" in i):
            d = i.index("⑈", 1, len(i))
            leaf_no = i[1:d]
            break
    if (not payee_name):
        d = cheque_ocr.index("Pay")
        payee_name.append(cheque_ocr[d+1])
    # finalpayee=[]
    # if(len(payee_name)>1):
    #     temp=payee_name[0]
    #     d=cheque_ocr.index(temp)
    #     for i in range(d,len(cheque_ocr)):
    #         if("bearer" in cheque_ocr[i].lower()):
    #             break
    #         finalpayee.append(cheque_ocr[i])
    payee_name = (''.join(payee_name))
    payee_amt = (''.join(payee_amt))
    if ("only" in payee_amt.lower()):
        payee_amt = payee_amt.replace("only", "")
    if ("." in payee_amt.lower()):
        payee_amt = payee_amt.replace(".", "")
    payee_amt = payee_amt.strip()
    payee_name = payee_name.lower()
    return int(date), int(amount), bank, ifsc, payee_name, payee_amt, int(ac), int(leaf_no)

# date=[]
# amount=[]
# bank=[]
# ifsc=[]
# payee_name=[]
# payee_amt=[]
# ac=[]
# date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no=extract_details()
# print(date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no)
