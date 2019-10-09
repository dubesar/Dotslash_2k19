import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
subscription_key = '280c7bc04130439ab461e5ed4175c872'
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the "westus" region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

text_recognition_url = vision_base_url + "recognizeText"

# Set image_url to the URL of an image that you want to analyze.
image_url = "https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fderiv.nls.uk%2Fdcn30%2F9464%2F94643850.30.jpg&f=1"
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
# Note: The request parameter changed for APIv2.
# For APIv1, it is 'handwriting': 'true'.
params  = {'mode': 'Handwritten'}
data    = {'url': image_url}
response = requests.post(
    text_recognition_url, headers=headers, params=params, json=data)
response.raise_for_status()

# Extracting handwritten text requires two API calls: One call to submit the
# image for processing, the other to retrieve the text found in the image.

# Holds the URI used to retrieve the recognized text.
operation_url = response.headers["Operation-Location"]

# The recognized text isn't immediately available, so poll to wait for completion.
analysis = {}
poll = True
while (poll):
    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    analysis = response_final.json()
    time.sleep(1)
    if ("recognitionResult" in analysis):
        poll= False 
    if ("status" in analysis and analysis['status'] == 'Failed'):
        poll= False

polygons=[]
if ("recognitionResult" in analysis):
    # Extract the recognized text, with bounding boxes.
    polygons = [(line["boundingBox"], line["text"])
        for line in analysis["recognitionResult"]["lines"]]

s=''
for i in range(len(polygons)):
  s+=polygons[i][1]
print(s)

#with open('test.txt',mode = 'rb') as file:
  #post_body = file.read()
post_body = s
api_url = "https://www.summarizebot.com/api/summarize?apiKey=748baf41ec7d4b5a853dedecaa4b5a41&size=30&keywords=10&fragments=15&filename=New Text Document.txt"

header = {'Content-Type': "application/octet-stream"}
r = requests.post(api_url, headers = header, data = post_body)
json_res = r.json()
s = json_res

k=''
for i in range(len(s[0]['summary'])):
  k+=s[0]['summary'][i]['sentence']
  
print(k)
