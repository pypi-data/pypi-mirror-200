import random
import nonebot


try:
    bot_name = nonebot.get_driver().config.bot_name
except:
    bot_name = "寄"

chuo_CD_dir = {}

try:
    chuo_cd = nonebot.get_driver().config.chuo_cd
except:
    chuo_cd = 0
    
def chuo_send_msg():
    rand_num = random.randint(0, len(chuo_msg) - 1)
    return chuo_msg[rand_num]


chuo_msg = [
    f"别戳了，{bot_name}怕疼QwQ",
    f"呜呜，再戳{bot_name}脸都要肿了",
    f"戳坏了{bot_name}，你赔得起吗？",
    f"再戳{bot_name}，我要叫我主人了",
    f"别老戳{bot_name}了，您歇会吧~",
    f"再戳{bot_name}，咬你了嗷~",
    f"想好了再戳，(*-`ω´-)✄",
    f"喂，110吗，有人老戳我",
    f"嗷呜嗷呜...恶龙咆哮┗|｀O′|┛",
    f"有事恁叫我，别天天一个劲戳戳戳！",
    f"再戳我让你变成女人，嘿嘿",
    f"不要戳我了 >_<",
    f"不要这样子啦(*/ω＼*)",
    f"不要再戳了(害怕ing)",
    f"还戳，哼(つд⊂)（生气）",
    f"再戳，小心我顺着网线找你.",
    f"咱要型气了o(>﹏<)o",
    f"嘿嘿，好舒服呀(bushi)",
    f"乖，好了好了，别戳了~",
    f"我爪巴爪巴，球球别再戳了",
    f"别再戳我了，行🐎？！",
    f"啊呜，你有什么事吗？",
    f"lsp你再戳？",
    f"连个可爱美少女都要戳的肥宅真恶心啊。",
    f"你再戳！",
    f"？再戳试试？",
    f"别戳了别戳了再戳就坏了555",
    f"我爪巴爪巴，球球别再戳了",
    f"你戳你🐎呢？！",
    f"请不要戳{bot_name} >_<",
    f"放手啦，不给戳QAQ",
    f"喂(#`O′) 戳{bot_name}干嘛！",
    f"戳坏了，赔钱！",
    f"戳坏了",
    f"嗯……不可以……啦……不要乱戳",
    f"那...那里...那里不能戳...绝对...",
    f"(。´・ω・)ん?",
    f"有事恁叫我，别天天一个劲戳戳戳！",
    f"欸很烦欸！你戳🔨呢",
    f"再戳一下试试？",
    f"正在关闭对您的所有服务...关闭成功",
    f"啊呜，太舒服刚刚竟然睡着了。什么事？",
    f"正在定位您的真实地址...定位成功。轰炸机已起飞"
]



