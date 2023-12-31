import os
import re
import time

import requests
from ..config import DOWNLOAD_CONFIG, NETWORK_CONFIG, OUTPUT_CONFIG
from ..utils import printError, printInfo, printWarn, writeFailLog


def downloadImage(url: str) -> float:
    """[summary]
    download image

    Returns: image size (MB)

    NOTE: url sample "https://i.pximg.net/
        img-original/img/2022/05/11/00/00/12/98259515_p0.jpg"
    """

    image_name = url[url.rfind("/") + 1:]
    result = re.search("/(\d+)_", url)
    printError(result is None, "bad url in image downloader")
    image_id = result.group(1)
    headers = {
        "Referer": f"https://www.pixiv.net/artworks/{image_id}",
        "x-user-id": "56405112",
        "COOKIE": "first_visit_datetime_pc=2022-03-23+09%3A05%3A13; p_ab_id=2; p_ab_id_2=6; p_ab_d_id=496637752; yuid_b=FnRJY4g; _fbp=fb.1.1647993926346.868094683; privacy_policy_notification=0; a_type=0; b_type=1; _im_vid=01FYT7DA0M1MG08GJSVD70BA7M; adr_id=lTzPqgTf6xmkSZZddeH8LhLHDKfx8OJsbbCpSa4F8n6kESK0; login_ever=yes; _td=e09e84b3-b5d0-4284-8cbc-fe6a9605154a; _ga_692MXKN5XF=GS1.1.1665973029.1.0.1665973029.0.0.0; cto_bundle=MeOqNl9aSyUyRkklMkJFcFJ5WCUyQlNzZkozQTFYSVpESHZCRiUyRm83QWZ3aTdmNEVIbG9FRWkxUUlIbDl0eiUyQnZlRmU3SWo0d1VLMGFFMks1M0dXWnA4OFBhMkNhcjJGQ3Rjakl3JTJGc3lwcU5ZV1NiY0RMbSUyQmQ0aEVZY0J4TnM0RiUyRnBEJTJGcVJPeSUyQkwyWTAwUmFvNmQyV3R5QlRnN2RXSFFYUSUzRCUzRA; _im_uid.3929=i.HNTUXPphRC6Tos5lngHwCA; c_type=21; privacy_policy_agreement=6; __gads=ID=e032ebe84fc5b362:T=1696335939:RT=1696335939:S=ALNI_MYk8hTGJ0JVZ08XHPJ1chcTiPcYZQ; __gpi=UID=00000c56c30e862e:T=1696335939:RT=1696335939:S=ALNI_MZ0J6EZLNM_IHlenurDDcoh0qn7tw; _ga_ZQEKG3EF2C=GS1.1.1696335939.1.0.1696335941.58.0.0; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=56405112=1^9=p_ab_id=2=1^10=p_ab_id_2=6=1^11=lang=zh=1; _gcl_au=1.1.2068989696.1697797468; PHPSESSID=56405112_5F6NwBp0ibUH6FuPbdq8P8dKXRrJiakY; device_token=d9e66683eee3c683671ce6dd45961915; _ga_MZ1NL4PHH0=GS1.1.1698243034.3.1.1698243060.0.0.0; __utmz=235335808.1698489562.713.11.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.73441192.1699788507; __utma=235335808.740189076.1647993924.1699936938.1699944133.746; _ga_ZPL8LPMDK3=GS1.1.1699945764.19.1.1699945776.0.0.0; __cf_bm=o75a_dxEYYH.70c_3Bc9l9kcnQ21g9q8qLYL8Cwim7E-1699947948-0-Ado847VODjuEbsuWh1d73rDUAUzc7NV4HSqPNkf4uDbtOq43lk4n0Iadho7XiG9BJqfShmOiyQ0SBKCLFsD9oftUNIV83XaDN3sMnjCMy9C9; __utmc=235335808; __utmt=1; cf_clearance=tKGeitoxfXwmrHstKob0LLLWi8vTys7CS5e3PwnggmI-1699948192-0-1-631cd866.945ac2d7.341d8786-0.2.1699948192; __utmb=235335808.54.10.1699944133; _ga_75BBYNYN9J=GS1.1.1699944133.496.1.1699948282.0.0.0; _ga=GA1.2.740189076.1647993924"
       }
    headers.update(NETWORK_CONFIG["HEADER"])

    verbose_output = OUTPUT_CONFIG["VERBOSE"]
    error_output = OUTPUT_CONFIG["PRINT_ERROR"]
    if verbose_output:
        printInfo(f"downloading {image_name}")
    time.sleep(DOWNLOAD_CONFIG["THREAD_DELAY"])

    image_path = DOWNLOAD_CONFIG["STORE_PATH"] + image_name
    if os.path.exists(image_path):
        printWarn(verbose_output, f"{image_path} exists")
        return 0

    wait_time = 10
    for i in range(DOWNLOAD_CONFIG["N_TIMES"]):
        try:
            response = requests.get(
                url, headers=headers,
                proxies=NETWORK_CONFIG["PROXY"],
                timeout=(4, wait_time))

            if response.status_code == 200:
                image_size = int(
                    response.headers["content-length"])
                # deletc incomplete image
                if len(response.content) != image_size:
                    time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])
                    wait_time += 2
                    continue

                with open(image_path, "wb") as f:
                    f.write(response.content)
                if verbose_output:
                    printInfo(f"{image_name} complete")
                return image_size / (1 << 20)

        except Exception as e:
            printWarn(error_output, e)
            printWarn(error_output,
                      f"This is {i} attempt to download {image_name}")

            time.sleep(DOWNLOAD_CONFIG["FAIL_DELAY"])

    printWarn(error_output, f"fail to download {image_name}")
    writeFailLog(f"fail to download {image_name} \n")
    return 0
