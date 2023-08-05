import subprocess
import os
import sys
import time
import oss2
import http.client
import json
import logging
import calendar
from pathlib import Path
import shutil
import zipfile
import platform
import requests
import hashlib
from PIL import Image
from io import BytesIO

def getOssResource(rootDir, url, md5, name):
    localFile = os.path.join(rootDir, name)
    localFileIsRemote = False
    if os.path.exists(localFile):
        with open(localFile, 'rb') as fp:
                file_data = fp.read()
        file_md5 = hashlib.md5(file_data).hexdigest()
        if file_md5 == md5:
            localFileIsRemote = True

    if localFileIsRemote == False: #download
        if os.path.exists(localFile):
            os.remove(localFile)
        s = requests.session()
        s.keep_alive = False
        file = s.get(url, verify=False)
        with open(localFile, "wb") as c:
            c.write(file.content)
        s.close()

def updateBin(rootDir):
    getOssResource(rootDir, "http://mecord-m.2tianxin.com/res/ffmpeg.zip", "a9e6b05ac70f6416d5629c07793b4fcf", "ffmpeg.zip.py")
    for root,dirs,files in os.walk(rootDir):
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

    for root,dirs,files in os.walk(rootDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
                return
        if root != files:
            break

def videoInfo(file):
    w = 0
    h = 0
    bitrate = 0
    fps = 0

    ffmpeg = ffmpegBinary()
    command = f'{ffmpeg} -i {file}'
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        str = ""
        if result.returncode == 0:
            str = result.stdout.decode(encoding="utf8", errors="ignore")
        else:
            str = result.stderr.decode(encoding="utf8", errors="ignore")
        if str.find("yuv420p") > 0 and str.find("fps") > 0:
            s1 = str[str.find("yuv420p"):str.find("fps")+3].replace(' ', "")
            s1_split = s1.split(",")
            for s1_it in s1_split:
                s2 = s1_it
                if s2.find("[") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("(") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("x") > 0:
                    sizes = s2.split("x")
                    if len(sizes) > 1:
                        w = sizes[0]
                        h = sizes[1]
                if s2.find("kb/s") > 0:
                    bitrate = s2[0:s2.find("kb/s")]
                if s2.find("fps") > 0:
                    fps = s2[0:s2.find("fps")]
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        print(e)
        print("======================      end      ======================")
    return float(w),float(h),float(bitrate),float(fps)

def ffmpegBinary():
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    updateBin(binDir)
    binaryFile = ""
    if sys.platform == "win32":
        binaryFile = os.path.join(binDir, "ffmpeg", "win", "ffmpeg.exe")
    elif sys.platform == "linux":
        machine = platform.machine().lower()
        if machine == "x86_64" or machine == "amd64":
            machine = "amd64"
        else:
            machine = "arm64"
        binaryFile = os.path.join(binDir, "ffmpeg", "linux", machine, "ffmpeg")
    elif sys.platform == "darwin":
        binaryFile = os.path.join(binDir, "ffmpeg", "darwin", "ffmpeg")
    
    if len(binaryFile) > 0 and sys.platform != "win32":
        print(f"=================== chmod 755 {binaryFile} ==================")
        cmd = subprocess.Popen(f"chmod 755 {binaryFile}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while cmd.poll() is None:
            print(cmd.stdout.readline().rstrip().decode('utf-8'))
        print("===================             end              ==================")
        
    return binaryFile
    
def processMoov(file):
    tmpPath = f"{file}.mp4"
    binary = ffmpegBinary()
    command = f'{binary} -i {file} -movflags faststart -y {tmpPath}'
    logging.info(f"ffmpegProcess: {command}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            logging.info(result.stdout.decode(encoding="utf8", errors="ignore"))
            os.remove(file)
            os.rename(tmpPath, file)
        else:
            logging.error("====================== ffmpeg error ======================")
            logging.error(result.stderr.decode(encoding="utf8", errors="ignore"))
            logging.error("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logging.error("====================== process error ======================")
        logging.error(e)
        logging.error("======================      end      ======================")

def ffmpegTest():
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    testImage = os.path.join(binDir, "ffmpeg", "test.jpg")
    ffmpegProcess(f"-i {testImage}")
    
def ffmpegProcess(args):
    binary = ffmpegBinary()
    command = f'{binary} {args}'
    logging.info(f"ffmpegProcess: {command}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            logging.info(result.stdout.decode(encoding="utf8", errors="ignore"))
        else:
            logging.error("====================== ffmpeg error ======================")
            logging.error(result.stderr.decode(encoding="utf8", errors="ignore"))
            logging.error("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logging.error("====================== process error ======================")
        logging.error(e)
        logging.error("======================      end      ======================")

def getOssImageSize(p):
    try:
        s = requests.session()
        s.keep_alive = False
        res = s.get(p)
        image = Image.open(BytesIO(res.content), "r")
        s.close()
        return image.size
    except:
        return 0, 0

def getLocalImageSize(p):
    try:
        image = Image.open(BytesIO(p), "r")
        return image.size
    except:
        return 0, 0
    
def upload(file, bucketDiff):
    ALIYUN_OSS_ENDPOINT="https://oss-accelerate.aliyuncs.com"
    ALIYUN_OSS_ACCESS_KEY_ID="LTAI5tLnazpA2DNVsN8dhvR5"
    ALIYUN_OSS_ACCESS_SECRET_KEY="f9MB0CHlBBJU2wHlqoAglu3FLHzVUh"
    ALIYUN_OSS_BUCKET_NAME="mecord-web"
    ALIYUN_OSS_CDN="mecord-m.2tianxin.com"

    auth = oss2.Auth(ALIYUN_OSS_ACCESS_KEY_ID, ALIYUN_OSS_ACCESS_SECRET_KEY)
    bucket = oss2.Bucket(auth, ALIYUN_OSS_ENDPOINT, ALIYUN_OSS_BUCKET_NAME)
    with open(file, "rb") as f:
        byte_data = f.read()
    file_name = Path(file).name
    publish_name = f"mecord/crawler{bucketDiff}/{file_name}" 
    bucket.put_object(publish_name, byte_data)
    # domain = Endpoint.replace("http://", f"http://{BucketName}.").replace("https://", f"https://{BucketName}.")
    # return f"{domain}/{publish_name}"
    return f"http://{ALIYUN_OSS_CDN}/{publish_name}"

# #beta接口：
# #https://mecord-beta.2tianxin.com/proxymsg/get_oss_config
# #prod接口：
# #https://api.mecordai.com/proxymsg/get_oss_config
# #beta环境：8058e02b06b909b42f60841949a72af7
# #prod环境：f0463f490eb84133c0aab3a8576ed2fc
# AccessKeyId = ""
# AccessKeySecret = ""
# SecurityToken = ""
# BucketName = ""
# Expiration = 99999999999
# Endpoint = ""
# CallbackUrl = ""
# cdn = ""
# def upload(file, bucketDiff):
#     global AccessKeyId, AccessKeySecret, SecurityToken, BucketName, Expiration, Endpoint, CallbackUrl, cdn
#     if calendar.timegm(time.gmtime()) < (Expiration - 60):
#         conn = http.client.HTTPSConnection("api.mecordai.com")
#         payload = json.dumps({
#             "sign": "f0463f490eb84133c0aab3a8576ed2fc"
#         })
#         headers = {
#             'Content-Type': 'application/json'
#         }
#         conn.request("POST", "/proxymsg/get_oss_config", payload, headers)
#         res = conn.getresponse()
#         data = json.loads(res.read().decode("utf-8"))
#         if data["code"] == 0:
#             AccessKeyId = data["data"]["AccessKeyId"]
#             AccessKeySecret = data["data"]["AccessKeySecret"]
#             SecurityToken = data["data"]["SecurityToken"]
#             BucketName = data["data"]["BucketName"]
#             Expiration = data["data"]["Expiration"]
#             Endpoint = data["data"]["Endpoint"]
#             CallbackUrl = data["data"]["CallbackUrl"]
#             cdn = data["data"]["cdn"]
#         else:
#             logging.error(f"get_oss_config fail: response={data}")
    
#     if len(AccessKeyId) <= 0:
#         logging.error(f"get_oss_config error?")
#         logging.error(f"=== calendar.timegm(time.gmtime()) = {calendar.timegm(time.gmtime())}")
#         logging.error(f"=== Expiration = {Expiration}")
        
#         return
    
#     auth = oss2.StsAuth(AccessKeyId, AccessKeySecret, SecurityToken)
#     bucket = oss2.Bucket(auth, Endpoint, BucketName, connect_timeout=600)
#     with open(file, "rb") as f:
#         byte_data = f.read()
#     file_name = Path(file).name
#     publish_name = f"mecord/crawler{bucketDiff}/{file_name}" 
#     bucket.put_object(publish_name, byte_data)
#     # domain = Endpoint.replace("http://", f"http://{BucketName}.").replace("https://", f"https://{BucketName}.")
#     # return f"{domain}/{publish_name}"
#     return f"{cdn}{publish_name}"