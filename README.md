![python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![micro](https://img.shields.io/badge/Microsoft_Learn-258ffa?style=for-the-badge&logo=microsoft&logoColor=white)![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white) ![Microsoft](https://img.shields.io/badge/Microsoft-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)![Stack Overflow](https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white)![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Contents

<img align="right" width="100" height="100" src="https://github.com/Shailly0502/Tech-Diwane/blob/c782ca5a86027019f1d2ae484e0fdac4afe6c1e3/content.webp">  
<ul>  
   <li> <a href="#11"> Provided Problem Statement(Automated Cheque Processing) </a> </li>
   <li> <a href="#12"> Expected Solution </a> </li>
   <li> Proposed Solution </li>
   <ul> <li>  Workflow </li> 
   <ul> <li>  <a href="#2"> Input & Transformation </a> </li>
      <li> <a href="#3"> Extraction </a>  </li>
      <li> <a href="#4">Verification </a> </li>
      <li> <a href="#5"> Processing & Diagrametic Representation of Complete Workflow </a> </li> </ul>
   <li> <a href="#7"> Database </a> </li>
      <li> <a href="#8"> Features </a> </li> </ul>
   
# Provided Problem Statement(Automated Cheque Processing)<a id="11">

Bank handles large volumes of cheques in the clearing process. The process involves many technical verifications including signature verification. Some of these steps are manual and require human intervention to complete the process. The current process requires the high human capital deployment and longer processing time.

</a>

# Expected Solution<a id="12">

Using rule-based and AI/ML/ICR/ OCR (Optical Character Recognition) capabilities for automation and doing technical and signature verification of the cheques.

- Automation of the clearing process using AI/ML/ICR/OCR techniques
- Automatic Data Entry & Technical verification
- Signature Verification
- Support Multilingual
- Reduce Human Efforts
- Reduce Processing time
- Detecting Potential Frauds
  </a>

# Proposed Solution

## Workflow

- <a id="2"> A cheque image is taken as an input & scanned. Then this scanned image is transformed into many different small part where every part contain seperate useful information like signature,amount,account number,payee name,bank name,etc.
- These parts are extracted by drawing boxes on those parts of the scanned cheque image that contain useful information, with help of **OpenCV** and **Geometry.**
- With the help of **Azure APIs** these small different parts of the scanned images are sent to **OCR(Optical Character Recognition)** for processing information written in these small images. </a>
- <a id="3"> OCR model returns a list of detections and then among that list, there are both useful information and additional informations. Among complete list, detections of only required information are considered(this is known as **text cleaning or extracting of useful information**).

_Please make a note that Useful information here mean that only that information that is relevant or required for cheque verification and processing._

**Useful information includes:** _Payee Name, Amount in words, Amount in numbers, Date, IFSC Code, Bank Name, Account Number, MICR Code, Signature._

![cheque image](https://github.com/Shailly0502/Tech-Diwane/blob/f6b6ac386f94a1ac83bbad23283a2805e63eccee/cheque.jpeg)

- _To ensure the genuinity or correctiveness of cheque, extracted Amount in words is converted into numerical form and then that numerical form is compared with Amount in numbers, if it matches then, cheque information is correct and then further process is done_.

**Transaction Type detection**: _If 'self' or 'myself' is written in payee name then that transaction is NEFT otherwise it is a RTGS Transaction._

- _After cleaning or extracting useful detection from OCR list, the extracted information of the payer is used to compare with it's existing record information in database **so as to verify if payer is genuine or not** and \_this process is known as **Verification Process** & is the most crucial part of the whole process._
  </a>

 <a id="4">
* For complete verification of payer, verification of different extracted information takes place with the help of ML modules.

- **Signature Verification** is done with the help of **signver module** that contains **sub-modules** such that:

  - _Cleaner module_ returns a list of cleaned signature images (removal of background lines and text), given a list of signature images.
  - _Extactor module_ returns a list of vector representations, given a list of image tensors/np arrays.
  - _Matcher module_ returns a distance measure given a pair of signatures (where one signature image is the image of payee's signature extracted from input cheque image and other image is the image present in payee's existing records in the database). _If both images match, then signature is verified otherwise signature on input cheque is a forgery or fake signature of payee._

#### _Diagrametic Representation of signver module_

![signature verification](https://raw.githubusercontent.com/fastforwardlabs/signver/main/docs/images/signature_pipeline.png)

- Extracted **Account Number** is verified by checking if any information of payer with this extracted account number exists.
- Extracted **MICR Code** is verifed by checking if leaf number is less than leaf left.
- **Amount Verification** is done to check if account contains sufficient amount such that transaction of mentioned amount could take place in future after successful verification of cheque details because _If sufficient amount is present in account then only transaction will take place._

_Only after the successful verification, any processes or transactions(as instructed on cheque like transferring of money to the intended user bank account) takes place._

 </a>
 
 <a id="5">
* __After successful cheque processing, the details of the sender gets further updated in the database as per the transaction took place successfully.__
 
 #### _Diagrametic Representation of Complete Workflow_

![cheque verification](https://github.com/Shailly0502/Tech-Diwane/blob/69f23f6342bee3c180b161ec4146ce7174276da8/astha.png)

 </a>

## Database <a id="7">

 <img align="right" width="100" height="100" src="https://github.com/Shailly0502/Tech-Diwane/blob/c782ca5a86027019f1d2ae484e0fdac4afe6c1e3/database.png">  
Information of different payers are stored in the database. 
It includes:
   <ul> <li> Cheque ID </li>
      <li>  Account Number </li> 
      <li> MICR </li> 
   <li> Current Amount </li>
 <li> Signature Image </li> </ul>

![database image](https://github.com/Shailly0502/Tech-Diwane/blob/b4fef312819a8182b7e3c97a19e105d2d96ccf4f/database.png)

  </a>

## Features <a id="8">

   <img align="right" width="100" height="100" src="https://github.com/Shailly0502/Tech-Diwane/blob/c782ca5a86027019f1d2ae484e0fdac4afe6c1e3/features.webp">  
   <ul> <li> Back of the Cheque is also proposed </li>
   <li> Supports Multilingual <i> (Hindi,English)</i> </li>
      <li> MICR Verification </li>
      <li> Azure API(named as Azure database for MySQL) is used for database connectivity</li>
<li> Checks the correctiveness of cheque information by matching amount in words match with amount in number so as to ensure correctiveness of mentioned information of cheque. </li>
      <li> Checks if a transaction is NEFT or RTGS(Transaction type detection) </li>
<li> Reduce Human Efforts <i> (By automating process of verification and data updation after processing)</i> </li>
<li> Reduce Processing time <i>(Machine take less time than humans so it fastens the cheque processing time )</i> </li>
<li> Detecting Potential Frauds <i>(Through verification processing).</i> </li>
   </ul> 
  </a>
