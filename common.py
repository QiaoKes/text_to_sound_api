from enum import Enum

class modelType(Enum):
    CHINESE_MODEL = 0
    JAPANESE_MODEL = 1

class jpModelId(Enum):
    '''
    ID      声线
    0       才羽桃井(元气、幼龄)
    1       枣伊吕波(正常)
    2       圣园未花(元气、少女)
    3       霞泽美游(羞答答幼龄)
    4       白洲梓(正常)
    5       天童爱丽丝(可爱)
    6       砂狼白子(沉闷、磁性)
    7       空崎日奈(沉闷)
    8       久田泉奈(超活力、幼龄)
    9       早濑优香(中性)
    10      神里绫华(温柔御姐)
    11      佩可莉姆(可爱少女)
    12      柏崎初音(可爱少女)
    13      镜华(萝莉)
    '''
    Caiyu_Taojing = 0        # 才羽桃井(元气、幼龄)
    Zaoi_Lübo = 1            # 枣伊吕波(正常)
    Shengyuan_Weihua = 2     # 圣园未花(元气、少女)
    Xiaze_Meiyou = 3         # 霞泽美游(羞答答幼龄)
    Baizhou_Azusa = 4        # 白洲梓(正常)
    Tiantong_Ailisi = 5      # 天童爱丽丝(可爱)
    Shalong_Baizi = 6        # 砂狼白子(沉闷、磁性)
    Kongqi_Rina = 7          # 空崎日奈(沉闷)
    Jiuta_Izumi = 8          # 久田泉奈(超活力、幼龄)
    Zaose_Youka = 9          # 早濑优香(中性)
    Shenli_Linghua = 10      # 神里绫华(温柔御姐)
    Peike_Limu = 11          # 佩可莉姆(可爱少女)
    Bojia_Chuoyin = 12       # 柏崎初音(可爱少女)
    Jinghua = 13             # 镜华(萝莉)

class cnModelId(Enum):
    '''
    ID      声线
    0       优菈(英气)
    1       刻晴(英气)
    2       理之律者(沉闷)
    3       德丽莎(少女)
    '''
    Youka = 0             # 优菈(英气)
    Keqing = 1            # 刻晴(英气)
    Lixue_Renzhe = 2      # 理之律者(沉闷)
    Delisa = 3            # 德丽莎(少女)
