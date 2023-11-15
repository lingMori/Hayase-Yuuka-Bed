import datetime


# NOTE: MODE_CONFIG only applies to ranking crawler
MODE_CONFIG = {
    # start date
    "START_DATE": datetime.date(2022, 8, 1),
    # date range: [start, start + range - 1]
    "RANGE": 1,

    # which ranking list
    "RANKING_MODES": [
        "daily", "weekly", "monthly",
        "male", "female", "daily_ai",
        "daily_r18", "weekly_r18",
        "male_r18", "female_r18", "daily_r18_ai"
    ],
    "MODE": "daily",  # choose from the above

    # illustration, manga, or both
    "CONTENT_MODES": [
        "all",  # download both illustrations & mangas
        "illust", "manga"
    ],
    "CONTENT_MODE": "all",  # choose from the above

    # download top x in each ranking
    #   suggested x be a multiple of 50
    "N_ARTWORK": 50
}

OUTPUT_CONFIG = {
    # verbose / simplified output
    "VERBOSE": False,
    "PRINT_ERROR": False
}

NETWORK_CONFIG = {
    # proxy setting
    #   you should customize your proxy setting accordingly
    #   default is for clash
    "PROXY": {"https": "127.0.0.1:7890"},

    # common request header
    "HEADER": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
}

USER_CONFIG = {
    # user id
    #   access your pixiv user profile to find this
    #   e.g. https://www.pixiv.net/users/xxxx
    "USER_ID": "100485309",

    "COOKIE": "first_visit_datetime_pc=2023-11-14%2021%3A14%3A16; p_ab_id=2; p_ab_id_2=5; p_ab_d_id=71834117; __utmz=235335808.1699964057.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _fbp=fb.1.1699964058282.1477207184; yuid_b=ExEzmCA; _gid=GA1.2.850018427.1699964127; _im_vid=01HF6W467E25MGXNXPJHEWPTDQ; device_token=dccafc93aaa8692c65f392c9a7ab00d2; privacy_policy_agreement=6; _ga_MZ1NL4PHH0=GS1.1.1699964577.1.0.1699964580.0.0.0; privacy_policy_notification=0; a_type=0; b_type=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; __cf_bm=EcdCq6u9Cawg5WGif5GMjKPfagY8Cn8LOorJQIztgy4-1699977997-0-ASiN6tdcrdSeVoHG+HLRzr4ie44p7eGBLLwf9926P50W+qVTe85kjNknXeTyrx0vQD5R1IFLtLWkOdggMgKe8eCw18QCPpazQ8PGIcyD5i1g; __utma=235335808.537133348.1699964057.1699964057.1699977999.2; __utmc=235335808; __utmt=1; cf_clearance=IS1KlIfrIWG0DyX6j9cU2VDiL2fgV5dfE7a4e3qhBwg-1699977998-0-1-91f80494.de9dec2c.c6f95b74-0.2.1699977998; PHPSESSID=100485309_FWeAxy5e9SMySeu4tvDPCSnMaDbMzocj; c_type=29; __utmv=235335808.|2=login%20ever=no=1^3=plan=premium=1^5=gender=male=1^6=user_id=100485309=1^9=p_ab_id=2=1^10=p_ab_id_2=5=1^11=lang=zh=1; __utmb=235335808.5.10.1699977999; _ga_75BBYNYN9J=GS1.1.1699977999.3.1.1699978046.0.0.0; _ga=GA1.2.362165901.1699964058"
}


DOWNLOAD_CONFIG = {
    # image save path
    #   NOTE: DO NOT miss "/"
    "STORE_PATH": "E://vscode_clustter//code//github//Animate-Image-Bed//images//2023-11-14//HayaseYuuka/",

    # abort request / download
    #   after 10 unsuccessful attempts
    "N_TIMES": 10,

    # need tag ?
    "WITH_TAG": True,

    # waiting time (s) after failure
    "FAIL_DELAY": 1,

    # max parallel thread number
    "N_THREAD": 12,
    # waiting time (s) after thread start
    "THREAD_DELAY": 1,
}
