import sys
import os
import time
import requests
import json
from mecord_crawler import utils
import logging
import urllib3
import datetime
import shutil
import random
from urllib.parse import *
from PIL import Image
from fake_useragent import UserAgent

rootDir = ""
env = ""
def domain():
    if env == "test":
        return "beta.2tianxin.com"
    else:
        return "api.mecordai.com"
def bucket_diff():
    if env == "test":
        return "_test"
    else:
        return ""
curGroupId = 0
allCount = 0
successCount = 0
notifyServer = True

def notifyMessage(success, msg):
    try:
        param = {
            "task_id": curGroupId,
            "finish_desc": msg
        }
        s = requests.session()
        s.keep_alive = False
        res = s.post(f"https://{domain()}/common/admin/mecord/update_task_finish", json.dumps(param), verify=False)
        resContext = res.content.decode(encoding="utf8", errors="ignore")
        logging.info(f"notifyMessage res:{resContext}")
        s.close()
    except Exception as e:
        logging.info(f"notifyMessage exception :{e}")

def publish(media_type, post_text, ossurl, cover_url):
    type = 0
    if media_type == "video":
        type = 2
    elif media_type == "image":
        type = 1
    elif media_type == "audio":
        type = 3
    param = {
        "task_id": curGroupId,
        "content": ossurl,
        "content_type": type,
        "info": post_text,
        "cover_url": cover_url
    }
    s = requests.session()
    s.keep_alive = False
    res = s.post(f"https://{domain()}/common/admin/mecord/add_crawler_post", json.dumps(param), verify=False)
    resContext = res.content.decode(encoding="utf8", errors="ignore")
    logging.info(f"publish success {successCount}/{allCount}")
    print(f"publish success {successCount}/{allCount}")
    s.close()
    
def ossPathWithSize(path):
    w = 0
    h = 0
    if "http" in path:
        w,h = utils.getOssImageSize(path)
    
    if w > 0 and h > 0:
        if "?" in path:
            return f"{path}&width={w}&height={h}"
        else:
            return urljoin(path, f"?width={w}&height={h}")
    return path

def pathWithSize(path, w, h):    
    if w > 0 and h > 0:
        if "?" in path:
            return f"{path}&width={w}&height={h}"
        else:
            return urljoin(path, f"?width={w}&height={h}")
    return path

def localFileWithSize(type, path):
    width = 0
    height = 0
    if type == "image":
        img = Image.open(path)
        imgSize = img.size
        width = img.width
        height = img.height
    elif type == "video":
        w,h,bitrate,fps = utils.videoInfo(path)
        width = w
        height = h
    
    return int(width), int(height)
    
def download(name, media_type, post_text, media_resource_url, audio_resource_url):
    ext = ".mp4"
    if media_type == "image":
        ext = ".jpg"
    elif media_type == "audio":
        ext = ".mp3"
    savePath = os.path.join(rootDir, f"{name}{ext}")
    if os.path.exists(savePath):
        os.remove(savePath)
    #download
    logging.info(f"download: {media_resource_url}, {audio_resource_url}")
    s = requests.session()
    s.keep_alive = False
    ua = UserAgent()
    file = s.get(media_resource_url, verify=False, headers={'User-Agent': ua.random})
    with open(savePath, "wb") as c:
        c.write(file.content)
    #merge audio & video
    if len(audio_resource_url) > 0:
        audioPath = os.path.join(rootDir, f"{name}.mp3")
        file1 = s.get(audio_resource_url)
        with open(audioPath, "wb") as c:
            c.write(file1.content)
        tmpPath = os.path.join(rootDir, f"{name}.mp4.mp4")
        utils.ffmpegProcess(f"-i {savePath} -i {audioPath} -vcodec copy -acodec copy -y {tmpPath}")
        if os.path.exists(tmpPath):
            os.remove(savePath)
            os.rename(tmpPath, savePath)
            os.remove(audioPath)
        logging.info(f"merge => {file}, {file1}")
    #cover
    coverPath = ""
    if media_type == "video":
        utils.processMoov(savePath)
        tttempPath = f"{savePath}.jpg"
        utils.ffmpegProcess(f"-i {savePath}  -ss 00:00:00.02 -frames:v 1 -y {tttempPath}")
        if os.path.exists(tttempPath):
            coverPath = tttempPath
    elif media_type == "image":
        # tttempPath = f"{savePath}.jpg"
        # shutil.copyfile(savePath, tttempPath)
        coverPath = savePath
        
    #upload
    savePathW, savePathH = localFileWithSize(media_type, savePath)
    url = utils.upload(savePath,bucket_diff())
    if url == None:
        logging.info(f"oss url not found")
        return
    ossurl = pathWithSize(url, savePathW, savePathH)
    cover_url = ""
    if os.path.exists(coverPath) and media_type == "video":
        coverW, coverH = localFileWithSize("image", coverPath)
        coverossurl = utils.upload(coverPath,bucket_diff())
        cover_url = pathWithSize(coverossurl, coverW, coverH)
        os.remove(coverPath)
    elif os.path.exists(coverPath) and media_type == "image":
        cover_url = ossurl
        
    #publish
    logging.info(f"upload success, url = {ossurl}, cover = {cover_url}")
    s.close()
    os.remove(savePath)
    if notifyServer:
        publish(media_type, post_text, ossurl, cover_url)
    
def processPosts(uuid, data):
    global allCount
    global successCount

    post_text = data["text"]
    medias = data["medias"]
    idx = 0
    for it in medias:
        media_type = it["media_type"]
        media_resource_url = it["resource_url"]
        audio_resource_url = ""
        if "formats" in it:
            formats = it["formats"]
            quelity = 0
            for format in formats:
                if format["quality"] > quelity and format["quality"] <= 1080:
                    quelity = format["quality"]
                    media_resource_url = format["video_url"]
                    audio_resource_url = format["audio_url"]
        try:
            allCount += 1
            download(f"{uuid}_{idx}", media_type, post_text, media_resource_url, audio_resource_url)
            successCount += 1
            time.sleep(1)
        except Exception as e:
            print("====================== download+process+upload error! ======================")
            print(e)
            print("======================                                ======================")
            time.sleep(10) #maybe Max retries
        idx += 1

def aaaapp(multiMedia, url, cursor, page):
    param = {
        "userId": "D042DA67F104FCB9D61B23DD14B27410",
        "secretKey": "b6c8524557c67f47b5982304d4e0bb85",
        "url": url,
        "cursor": cursor,
    }
    requestUrl = "https://h.aaaapp.cn/posts"
    if multiMedia == False:
        requestUrl = "https://h.aaaapp.cn/single_post"
    logging.info(f"=== request: {requestUrl} cursor={cursor}")
    s = requests.session()
    s.keep_alive = False
    res = s.post(requestUrl, params=param, verify=False)
    logging.info(f"=== res: {res.content}")
    if len(res.content) > 0:
        data = json.loads(res.content)
        if data["code"] == 200:
            idx = 0
            if multiMedia == False:
                processPosts(f"{curGroupId}_{page}_{idx}", data["data"])
                if allCount > 1000:
                    print("stop mission with out of cnt=1000")
                    return
            else:
                posts = data["data"]["posts"]
                for it in posts:
                    processPosts(f"{curGroupId}_{page}_{idx}", it)
                    if allCount > 1000:
                        print("stop mission with out of cnt=1000")
                        return
                    idx+=1
            if "has_more" in data["data"] and data["data"]["has_more"] == True:
                next_cursor = ""
                if "next_cursor" in data["data"] and len(data["data"]["next_cursor"]) > 0:
                    if "no" not in data["data"]["next_cursor"]:
                        next_cursor = data["data"]["next_cursor"]
                if len(next_cursor) > 0:
                    aaaapp(multiMedia, url, next_cursor, page+1)
        else:
            if notifyServer:
                notifyMessage(False, data["msg"])
            print(f"=== error aaaapp, context = {res.content}")
            logging.info(f"=== error aaaapp, context = {res.content}")
            if data["code"] == 300:
                print("=== no money, exit now!")
                logging.info("=== no money, exit now!")
                exit(-1)
    else:
        print("=== error aaaapp, context = {res.content}, eixt now!")
        logging.info("=== error aaaapp, context = {res.content}, eixt now!")
        if notifyServer:
            notifyMessage(False, "无法抓取")
        exit(-1)
    s.close()

def dosom(gid, multiMedia, url):
    global rootDir
    global curGroupId
    global env
    global allCount
    global successCount
    global notifyServer

    curGroupId = gid
    allCount = 0
    successCount = 0
    notifyServer = False
    env = "test"
    print(f"=== begin {curGroupId}")
    right_s = url.replace("\n", "").replace(";", "").replace(",", "").strip()
    aaaapp(multiMedia, right_s, "", 0)
    if allCount > 1000:
        print("stop mission with out of cnt=1000")
        return
    print(f"complate => {curGroupId} rst={successCount}/{allCount}")


def main():    
    global rootDir
    global curGroupId
    global env
    global allCount
    global successCount
    global notifyServer
    
    urllib3.disable_warnings()
    d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(filename=f"{thisFileDir}/mecord_crawler_{d}.log", 
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        encoding="utf-8",
                        level=logging.DEBUG)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test_request":
            curGroupId = 0
            aaaapp(False, "https://www.instagram.com/meowbot_iv/", "", 0)
            return
        elif sys.argv[1] == "test_ffmpeg":
            utils.ffmpegTest()
            return
        elif sys.argv[1] == "upload":
            datas = [
                ["207","","191","1"],
                ["191","","37","1"],
                ["190","https://www.youtube.com/@RedAldino/shorts","1","1"],
                ["189","https://www.instagram.com/quang.media/","589","1"],
                ["188","https://www.youtube.com/@ZazeRP/shorts","8","1"],
                ["187","https://www.instagram.com/nft_wrap/","237","1"],
                ["186","https://www.instagram.com/uki_hajime/;https://www.instagram.com/miko_aiart/;https://www.instagram.com/smitzpandya/;","2065","1"],
                ["185","https://www.instagram.com/retrowaviest/;https://www.instagram.com/oslilith/;https://www.instagram.com/pixelatry/;","211","1"],
                ["184","https://www.instagram.com/aimotorized/;https://www.instagram.com/ai_arch_ref/;https://www.instagram.com/enterlink_art/;","390","1"],
                ["183","https://instagram.com/jimmyssunshinereport?igshid=YmMyMTA2M2Y=;https://instagram.com/cutecats_n?igshid=YmMyMTA2M2Y=;https://instagram.com/aipetshome?],[igshid=YmMyMTA2M2Y=;","160","1"],
                ["182","https://www.instagram.com/v3_dall_e/;https://www.instagram.com/cheefcuts/;https://www.instagram.com/cristancho_ai/;","38","1"],
                ["181","https://www.instagram.com/ai.fs.fantasy/;https://www.instagram.com/ai_characters/;https://www.instagram.com/bee__ai/;","109","1"],
                ["180","https://www.instagram.com/kenmar1986/;https://www.instagram.com/ossso.concept/;https://www.instagram.com/starwars.galaxy_/;","904","1"],
                ["179","https://www.instagram.com/enterdreamlands/;https://www.instagram.com/atiras_h_arts/;https://www.instagram.com/nohumanpaintinglandscapes/","148","1"],
                ["178","https://www.instagram.com/funnylolmemes4humans/","63","1"],
                ["176","https://www.instagram.com/i_am__barbara/","157","1"],
                ["175","https://www.instagram.com/aiartsplunge/","225","1"],
                ["174","https://www.instagram.com/graffbomb.ai/","72","1"],
                ["173","https://www.instagram.com/banzai_universe/","275","1"],
                ["172","https://www.instagram.com/virtualgf_ai/","248","1"],
                ["171","","172","1"],
                ["170","","176","1"],
                ["169","","273","1"],
                ["168","","585","1"],
                ["167","https://www.instagram.com/runrun_ac/","1916","1"],
                ["166","https://www.instagram.com/daxar123_builds/","187","1"],
                ["165","https://www.instagram.com/graysun.builds","473","1"],
                ["164","https://www.instagram.com/mrmattranger/","53","1"],
                ["163","https://www.instagram.com/rememorie_service/","77","1"],
                ["162","https://www.instagram.com/alternatehistory.ai/","224","1"],
                ["161","https://www.instagram.com/morrodocastelo/","759","1"],
                ["160","https://www.instagram.com/smitzpandya/","528","1"],
                ["159","https://www.instagram.com/bluekitsune.ai/","960","1"],
                ["158","https://www.instagram.com/rasputin.64/","97","1"],
                ["157","https://www.instagram.com/idreamhouse/","627","1"],
                ["156","https://www.instagram.com/raasch.motorshots/","188","1"],
                ["155","https://www.instagram.com/midoaiart/","282","1"],
                ["154","https://www.instagram.com/akithefull/","467","1"],
                ["153","https://www.instagram.com/nftzone_/","483","1"],
                ["152","https://www.instagram.com/artificial_fantasies/","262","1"],
                ["151","","323","1"],
                ["150","https://www.instagram.com/nftrai/","115","1"],
                ["149","https://www.instagram.com/thecomicgalaxy/","210","1"],
                ["148","https://www.instagram.com/anandhups360/","181","1"],
                ["146","https://www.instagram.com/josemartingomez2022/","709","1"],
                ["145","https://www.instagram.com/transformers.ai/","47","1"],
                ["144","https://www.instagram.com/starlord.ai/","5","1"],
                ["143","https://www.instagram.com/batmanthedefender/","39","1"],
                ["142","https://www.instagram.com/monstermachina/","12","1"],
                ["139","https://www.instagram.com/artedobatmannomundo/","2657","1"],
                ["138","https://www.instagram.com/batman_gotham_forever/","20","1"],
                ["137","https://www.instagram.com/lynnsquared__/","31","1"],
                ["136","https://www.instagram.com/sybercreations/","43","1"],
                ["135","https://www.instagram.com/arti.fictional/","120","1"],
                ["134","https://www.instagram.com/artzoneai/","1345","1"],
                ["133","https://www.instagram.com/diskret.ark/","174","1"],
                ["132","https://www.instagram.com/diskret.ark/","194","1"],
                ["131","https://www.instagram.com/alesandrome_ai/","172","1"],
                ["130","https://www.instagram.com/aiconceptfurniture/","90","1"],
                ["128","https://www.instagram.com/digital_download_farm/","101","1"],
                ["127","","260","1"],
                ["126","","24","1"],
                ["125","https://www.instagram.com/jurjen74.ai.art/","120","1"],
                ["124","https://www.instagram.com/nextgen_autobot_art/","108","1"],
                ["123","https://www.instagram.com/nextgen_autobot_art/","156","1"],
                ["122","https://www.instagram.com/ai_design_concepts/","277","1"],
                ["121","https://www.instagram.com/luma_girl_ai/","101","1"],
                ["120","https://www.instagram.com/ai_collector_/","125","1"],
                ["119","https://www.instagram.com/mlnima/","39","1"],
                ["118","https://www.instagram.com/proto.craftsman/","20","1"],
                ["117","https://www.tiktok.com/@exosfeer","39","1"],
                ["116","https://www.instagram.com/diegopaulvillavicencio/","431","1"],
                ["115","https://www.instagram.com/luma_girl_ai/","102","1"],
                ["114","https://www.instagram.com/manuel_gual/","363","1"],
                ["113","https://www.instagram.com/ai_forart/","17","1"],
                ["112","https://www.instagram.com/ai.artimage/","94","1"],
                ["111","https://www.instagram.com/eko2000_ai/","156","1"],
                ["110","https://www.instagram.com/nickocreates.ai/","1094","1"],
                ["109","https://www.instagram.com/ka_loc_a.i/","284","1"],
                ["108","https://www.tiktok.com/@ai_animation_and_art","144","1"],
                ["107","","83","1"],
                ["106","https://www.instagram.com/uki_hajime/","1508","1"],
                ["105","https://www.instagram.com/haroshi_mirukami/","75","1"],
                ["104","https://www.instagram.com/albonich/","152","1"],
                ["103","https://www.instagram.com/meowbot_iv/","54","1"],
                ["102","https://www.instagram.com/mooncryptowow/","1684","1"],
                ["101","https://www.instagram.com/theairevolution/","562","1"],
                ["100","https://www.instagram.com/unwdef/","475","1"],
                ["99","https://www.tiktok.com/@funx.arts","403","1"],
                ["98","https://www.tiktok.com/@starcoxel","26","1"],
                ["97","https://www.tiktok.com/@morph_ai","22","1"],
                ["96","https://www.tiktok.com/@heyseia2","41","1"],
                ["95","https://www.tiktok.com/@proteinique","66","1"],
                ["94","https://www.tiktok.com/@fareedafabriani","139","1"],
                ["93","https://www.tiktok.com/@ai_animation_and_art","135","1"],
                ["92","https://www.tiktok.com/@sheldrickstudio","26","1"],
                ["91","https://www.tiktok.com/@_ai_generating","95","1"],
                ["90","https://www.tiktok.com/@masouschka","40","1"],
                ["89","https://www.tiktok.com/@johnwolf_1","57","1"],
                ["88","https://www.tiktok.com/@arvizu__la","192","1"],
                ["87","https://www.tiktok.com/@deep_nya","206","1"],
                ["86","https://www.tiktok.com/@almarazjourney","36","1"],
                ["85","https://www.tiktok.com/@_cyberframe_","33","1"],
                ["84","https://www.tiktok.com/@kamiotaku.art","33","1"],
                ["83","https://www.instagram.com/unwdef/","148","1"]
            ]
            if sys.argv[2].isdigit():
                for it in range(int(sys.argv[2]) * 20, (int(sys.argv[2]) + 1) * 20):
                    if it < len(datas):
                        groupid = datas[it][0]
                        urls = datas[it][1].split(';')
                        for url in urls:
                            if len(url) > 0:
                                dosom(groupid, True, url)
            return
        elif sys.argv[1] == "test":
            env = sys.argv[1]
        else:
            print(f"not found {sys.argv[1]}")
            return

    rootDir = thisFileDir
    print(f"current domain is {domain()}")
    while(os.path.exists(os.path.join(thisFileDir, "stop.now")) == False):
        try:
            s = requests.session()
            s.keep_alive = False
            res = s.get(f"https://{domain()}/common/admin/mecord/get_task?t={random.randint(100,99999999)}", verify=False)
            s.close()
            if len(res.content) > 0:
                data = json.loads(res.content)
                curGroupId = data["id"]
                allCount = 0
                successCount = 0
                notifyServer = True
                logging.info(f"================ begin {curGroupId} ===================")
                logging.info(f"========== GetTask: {res.content}")
                print(f"=== begin {curGroupId}")
                link_url_list = data["link_url_list"]
                multiMedia = False
                if "is_set" in data:
                    multiMedia = data["is_set"]
                for s in link_url_list:
                    right_s = s.replace("\n", "").replace(";", "").replace(",", "").strip()
                    aaaapp(multiMedia, right_s, "", 0)
                    if allCount > 1000:
                        print("stop mission with out of cnt=1000")
                        break
                notifyMessage(True, "成功")
                print(f"complate => {curGroupId} rst={successCount}/{allCount}")
                logging.info(f"================ end {curGroupId} ===================")
        except Exception as e:
            notifyMessage(False, str(e))
            logging.error("====================== uncatch Exception ======================")
            logging.error(e)
            logging.error("======================      end      ======================")
        time.sleep(10)
    os.remove(os.path.join(thisFileDir, "stop.now"))
    print(f"stoped !")
        
if __name__ == '__main__':
        main()

# urllib3.disable_warnings()
# d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# thisFileDir = os.path.dirname(os.path.abspath(__file__))
# logging.basicConfig(filename=f"{thisFileDir}/mecord_crawler_{d}.log", 
#                         format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         encoding="utf-8",
#                         level=logging.DEBUG)
# aaaapp(True, "https://www.youtube.com/@ZazeRP/shorts", "", 0)