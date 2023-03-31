import asyncio
import json
from pathlib import Path

from bs4 import BeautifulSoup
from httpx import AsyncClient

"""
角色升级素材与天赋素材
90级升级材料的数量：
碎屑x1，断片x9，块x9，本体x6，
摩拉x2092530，紫书x419，
特产x168，
初级怪物素材x18，中级怪物素材x30，高级怪物素材x36，
世界boss素材x46

天赋10-10-10升级材料数量：
初级天赋书x9，中级天赋书x63，高级天赋书x114，皇冠x3，
摩拉x4957500，
初级怪物素材x18，中级怪物素材x66，高级怪物素材x93，
周本boss素材x18
"""

save_path = Path("Resources")
name_list = [
    "神里绫华",
    "琴",
    "丽莎",
    "芭芭拉",
    "凯亚",
    "迪卢克",
    "雷泽",
    "安柏",
    "温迪",
    "香菱",
    "北斗",
    "行秋",
    "魈",
    "凝光",
    "可莉",
    "钟离",
    "菲谢尔",
    "班尼特",
    "达达利亚",
    "诺艾尔",
    "七七",
    "重云",
    "甘雨",
    "阿贝多",
    "迪奥娜",
    "莫娜",
    "刻晴",
    "砂糖",
    "辛焱",
    "罗莎莉亚",
    "胡桃",
    "枫原万叶",
    "烟绯",
    "宵宫",
    "托马",
    "优菈",
    "雷电将军",
    "早柚",
    "珊瑚宫心海",
    "五郎",
    "九条裟罗",
    "荒泷一斗",
    "八重神子",
    "鹿野院平藏",
    "夜兰",
    "埃洛伊",
    "申鹤",
    "云堇",
    "久岐忍",
    "神里绫人",
    "柯莱",
    "多莉",
    "提纳里",
    "妮露",
    "赛诺",
    "坎蒂丝",
    "纳西妲",
    "莱依拉",
    "流浪者",
    "珐露珊",
    "瑶瑶",
    "艾尔海森",
    "迪希雅",
    "米卡",
]


async def get_material_data():
    client = AsyncClient()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0"
    }
    data = {"status": 0, "data": {}}
    # names = ["钟离", "纳西妲"]
    for name in name_list:
        try:
            re = await client.get(
                f"https://wiki.biligame.com/ys/{name}", headers=headers
            )
            soup = BeautifulSoup(re.text, "html.parser")
            ascension_materials = soup.select(
                ".tuPo > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(2) >"
                "div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next[0:4]
            level_up_materials = soup.select(
                ".tuPo > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > div:nth-child(1) > div:nth-child(3) >"
                "div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next
            materials_1 = soup.select(
                ".tuPo > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > div:nth-child(1) > div:nth-child(4) >"
                "div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next
            materials_2 = soup.select(
                ".tuPo > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > div:nth-child(1) > div:nth-child(5) >"
                "div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next
            materials_3 = soup.select(
                ".tuPo > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2) > div:nth-child(1) > div:nth-child(5) >"
                "div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next
            materials_4 = soup.select(
                ".tuPo > tbody:nth-child(1) > tr:nth-child(14) > td:nth-child(2) > div:nth-child(1) > div:nth-child("
                "5) >"
                "div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next
            talent_upgrade_1 = soup.select(
                ".visible-md > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > "
                "td:nth-child(2) > div:nth-child(2) > div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next
            talent_upgrade_2 = soup.select(
                ".visible-md > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > "
                "td:nth-child(4) > div:nth-child(4) > div:nth-child(3) > a:nth-child(1) > font:nth-child(1)"
            )[0].next
            data["data"][name] = {
                "ascension_materials": ascension_materials,
                "level_up_materials": level_up_materials,
                "materials": [materials_1, materials_2, materials_3, materials_4],
                "talent": [talent_upgrade_1[1:3], talent_upgrade_2],
            }
            # print(f"{name} 的培养素材爬取成功。")
        except (IndexError, ValueError):
            continue
    return data


def save_roles_materials(data: dict):
    save_path.mkdir(parents=True, exist_ok=True)
    with open(save_path / "roles_material.json", "w") as m_j:
        json.dump(data, m_j, ensure_ascii=False)


if __name__ == "__main__":
    roles_data = asyncio.run(get_material_data())
    save_roles_materials(roles_data)
