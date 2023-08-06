# import requests
# import json



# def login(apiKEY):
#     R = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": apiKEY})})
#     return R.json()['session']



# def sendURL(session, url):
#     R = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": session, "url": url})})
#     print(R.text)
    

# def sendFile(session, path):
#     dataheader = json.dumps({"session": session})
#     datafile = json.dumps({"filename": "upload.fits"})
#     with open('./x.png', 'rb') as f:
#         file = f.read()
    
#     res = requests.post(url='http://nova.astrometry.net/api/upload',
#         data=data,
#         headers={'Content-Type': 'application/octet-stream'})


# print(sendURL(login("sefgjpowjimxjkqo"), "http://apod.nasa.gov/apod/image/1206/ldn673s_block1123.jpg"))





from astroquery.astrometry_net import AstrometryNet

ast = AstrometryNet()
ast.api_key = 'sefgjpowjimxjkqo'

wcs_header = ast.solve_from_image('/Users/josia/workspace/ExoScanner/dataForTesting/20200624_Transit_Wasp52b-Gornergrat/light/Wasp52-b-002Light.fit')

print(wcs_header)