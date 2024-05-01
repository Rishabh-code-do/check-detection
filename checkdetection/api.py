from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json
import csv


subscription_key = "f03026222f7c425e9fd1cd5db6dfa3e5"
endpoint = "https://checkdetection.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key))


def azure_ocr_api(image_url):  # image_url
    # local_image_url = r"E:\Bank of Baroda\BOB IMAGE\Cheque309086.jpeg"
    read_response = computervision_client.read_in_stream(
        open("./Images/" + image_url, 'rb'),  raw=True)
    # read_response = computervision_client.read_in_stream(open(local_image_url,'rb'),  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    list1 = []
    list2 = []
    if read_result.status == OperationStatusCodes.succeeded:
        jsonFile = open("data.json", "w")
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                linestrbb = line.bounding_box
                linestrtt = line.text
                stringjsonbb = json.dumps(linestrbb)
                stringjsontt = json.dumps(linestrtt)
                jsonFile.write(stringjsonbb)
                jsonFile.write(stringjsontt)
                list1.append(line.text)
                list2.append(line.bounding_box)
        jsonFile.close()
    # print(list)
    # pass
    return list1, list2


# azure_ocr_api()
print("End of Computer Vision quickstart.")
