# %% [markdown]
# # Pixiv Craw

# %% [markdown]
# > - ### import repos

# %%
import requests
import json
from tqdm import tqdm

import sys
import os

from downloader.downloader import Downloader

# %% [markdown]
# > - ### 按照artist的id来craw

# %%
artist_id = 63608651

url = f"https://www.pixiv.net/ajax/user/{artist_id}/profile/all?lang=zh"

additional_headers = {
    "Referer": f"https://www.pixiv.net/users/{artist_id}/illustrations",
    "x-user-id": "5640xxxx",
    "COOKIE": "first_visit_datetime_pc=2022-03-23+09%3A05%3A13; p_ab_id=2; p_ab_id_2=6; p_ab_d_id=496637752; yuid_b=FnRJY4g; _fbp=fb.1.1647993926346.868094683; privacy_policy_notification=0; a_type=0; b_type=1; _im_vid=01FYT7DA0M1MG08GJSVD70BA7M; adr_id=lTzPqgTf6xmkSZZddeH8LhLHDKfx8OJsbbCpSa4F8n6kESK0; login_ever=yes; _td=e09e84b3-b5d0-4284-8cbc-fe6a9605154a; _ga_692MXKN5XF=GS1.1.1665973029.1.0.1665973029.0.0.0; cto_bundle=MeOqNl9aSyUyRkklMkJFcFJ5WCUyQlNzZkozQTFYSVpESHZCRiUyRm83QWZ3aTdmNEVIbG9FRWkxUUlIbDl0eiUyQnZlRmU3SWo0d1VLMGFFMks1M0dXWnA4OFBhMkNhcjJGQ3Rjakl3JTJGc3lwcU5ZV1NiY0RMbSUyQmQ0aEVZY0J4TnM0RiUyRnBEJTJGcVJPeSUyQkwyWTAwUmFvNmQyV3R5QlRnN2RXSFFYUSUzRCUzRA; _im_uid.3929=i.HNTUXPphRC6Tos5lngHwCA; c_type=21; privacy_policy_agreement=6; __gads=ID=e032ebe84fc5b362:T=1696335939:RT=1696335939:S=ALNI_MYk8hTGJ0JVZ08XHPJ1chcTiPcYZQ; __gpi=UID=00000c56c30e862e:T=1696335939:RT=1696335939:S=ALNI_MZ0J6EZLNM_IHlenurDDcoh0qn7tw; _ga_ZQEKG3EF2C=GS1.1.1696335939.1.0.1696335941.58.0.0; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=56405112=1^9=p_ab_id=2=1^10=p_ab_id_2=6=1^11=lang=zh=1; _gcl_au=1.1.2068989696.1697797468; PHPSESSID=56405112_5F6NwBp0ibUH6FuPbdq8P8dKXRrJiakY; device_token=d9e66683eee3c683671ce6dd45961915; _ga_MZ1NL4PHH0=GS1.1.1698243034.3.1.1698243060.0.0.0; __utmz=235335808.1698489562.713.11.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.73441192.1699788507; _ga_ZPL8LPMDK3=GS1.1.1699930329.18.1.1699930357.0.0.0; __cf_bm=X67SFTFNe9KvEzK6AxS96ftfSVWEqcIgua.4.3EcMVc-1699935025-0-AfkUhf87pN2+siqG5r1YvGpphK/bajDCL09AvrYlnYhvxsux9sdfZQIN8W3Ha3ztxG0ErV0mnsKzNjCErKsxohNNrRGurEMD/KweXvYGAHlI; __utma=235335808.740189076.1647993924.1699930321.1699935028.744; __utmc=235335808; __utmt=1; cf_clearance=SJHsrjUq5DYhRK8AO2UWSsB.5pZbPWf68VmswfYjLVA-1699935773-0-1-631cd866.8b0b9526.341d8786-0.2.1699935773; _ga=GA1.2.740189076.1647993924; __utmb=235335808.16.10.1699935028; _ga_75BBYNYN9J=GS1.1.1699935028.495.1.1699936337.0.0.0"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
}

headers.update(additional_headers)

proxies = {
    "https": "127.0.0.1:7890"
}

response = requests.get(
                url, headers=headers,
                proxies=proxies,
                timeout=4)
if response.status_code == 200:
    id_group = set(response.json()["body"]["illusts"].keys())
    print(id_group)
    
artist_artworks_ids_path = "E:\\vscode_clustter\\code\\github\\Animate-Image-Bed\\utils\\crawler\\test\\jsons\\"

file_name = f"{artist_id}-artworksID-collect.json"

artist_dict = {artist_id: list(id_group)}

# 将字典保存到 JSON 文件中
with open(artist_artworks_ids_path + file_name, "w", encoding="utf-8") as json_file:
    json.dump(artist_dict, json_file, ensure_ascii=False, indent=4)



# %% [markdown]
# > - ### Download Images

# %%
print("===== collector start =====")

downloader = Downloader(capacity=1024)

with tqdm(total=len(id_group), desc="collecting urls") as pbar:
    urls = [f"https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=zh"
            for illust_id in id_group]
    additional_headers = [
        {
            "Referer": f"https://www.pixiv.net/artworks/{illust_id}",
            "x-user-id": "5640xxxx",
            "COOKIE": "first_visit_datetime_pc=2022-03-23+09%3A05%3A13; p_ab_id=2; p_ab_id_2=6; p_ab_d_id=496637752; yuid_b=FnRJY4g; _fbp=fb.1.1647993926346.868094683; privacy_policy_notification=0; a_type=0; b_type=1; _im_vid=01FYT7DA0M1MG08GJSVD70BA7M; adr_id=lTzPqgTf6xmkSZZddeH8LhLHDKfx8OJsbbCpSa4F8n6kESK0; login_ever=yes; _td=e09e84b3-b5d0-4284-8cbc-fe6a9605154a; _ga_692MXKN5XF=GS1.1.1665973029.1.0.1665973029.0.0.0; cto_bundle=MeOqNl9aSyUyRkklMkJFcFJ5WCUyQlNzZkozQTFYSVpESHZCRiUyRm83QWZ3aTdmNEVIbG9FRWkxUUlIbDl0eiUyQnZlRmU3SWo0d1VLMGFFMks1M0dXWnA4OFBhMkNhcjJGQ3Rjakl3JTJGc3lwcU5ZV1NiY0RMbSUyQmQ0aEVZY0J4TnM0RiUyRnBEJTJGcVJPeSUyQkwyWTAwUmFvNmQyV3R5QlRnN2RXSFFYUSUzRCUzRA; _im_uid.3929=i.HNTUXPphRC6Tos5lngHwCA; c_type=21; privacy_policy_agreement=6; __gads=ID=e032ebe84fc5b362:T=1696335939:RT=1696335939:S=ALNI_MYk8hTGJ0JVZ08XHPJ1chcTiPcYZQ; __gpi=UID=00000c56c30e862e:T=1696335939:RT=1696335939:S=ALNI_MZ0J6EZLNM_IHlenurDDcoh0qn7tw; _ga_ZQEKG3EF2C=GS1.1.1696335939.1.0.1696335941.58.0.0; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=56405112=1^9=p_ab_id=2=1^10=p_ab_id_2=6=1^11=lang=zh=1; _gcl_au=1.1.2068989696.1697797468; PHPSESSID=56405112_5F6NwBp0ibUH6FuPbdq8P8dKXRrJiakY; device_token=d9e66683eee3c683671ce6dd45961915; _ga_MZ1NL4PHH0=GS1.1.1698243034.3.1.1698243060.0.0.0; __utmz=235335808.1698489562.713.11.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.73441192.1699788507; _ga_ZPL8LPMDK3=GS1.1.1699930329.18.1.1699930357.0.0.0; __cf_bm=X67SFTFNe9KvEzK6AxS96ftfSVWEqcIgua.4.3EcMVc-1699935025-0-AfkUhf87pN2+siqG5r1YvGpphK/bajDCL09AvrYlnYhvxsux9sdfZQIN8W3Ha3ztxG0ErV0mnsKzNjCErKsxohNNrRGurEMD/KweXvYGAHlI; __utma=235335808.740189076.1647993924.1699930321.1699935028.744; __utmc=235335808; __utmt=1; cf_clearance=SJHsrjUq5DYhRK8AO2UWSsB.5pZbPWf68VmswfYjLVA-1699935773-0-1-631cd866.8b0b9526.341d8786-0.2.1699935773; _ga=GA1.2.740189076.1647993924; __utmb=235335808.16.10.1699935028; _ga_75BBYNYN9J=GS1.1.1699935028.495.1.1699936337.0.0.0"
        }
        for illust_id in id_group]

    for url, add_headers in zip(urls, additional_headers):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        }

        headers.update(add_headers)

        proxies = {
            "https": "127.0.0.1:7890"
        }

        response = requests.get(
                        url, headers=headers,
                        proxies=proxies,
                        timeout=4)

        # 获取 JSON 内容
        json_content = response.json()

        # 指定保存路径和文件名
        save_path = "E://vscode_clustter//code//github//Animate-Image-Bed//utils//crawler//test//jsons//re.json"

        # 将 JSON 内容保存到文件
        with open(save_path, "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, ensure_ascii=False, indent=4)

        if response.status_code == 200:
            print(f"url: {url} , resp_code==200, collected Over !" )
            # 因为一个作品可能有多个img ，所以要进行归一化
            collected_urls = set()
            for url in response.json()["body"]:
                collected_urls.add(url["urls"]["original"])
        
        if collected_urls is not None:
            downloader.add(collected_urls)
        pbar.update()

print("===== download start =====")
downloader.download()



