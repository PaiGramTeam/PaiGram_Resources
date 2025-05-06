import asyncio
import json
from pathlib import Path
from typing import Dict, List

save_path = Path("Resources")
avatar_data_path = save_path / "ExcelBinOutput" / "AvatarExcelConfigData.json"
avatar_promote_data_path = save_path / "ExcelBinOutput" / "AvatarPromoteExcelConfigData.json"
avatar_skill_depot_data_path = save_path / "ExcelBinOutput" / "AvatarSkillDepotExcelConfigData.json"
avatar_skill_data_path = save_path / "ExcelBinOutput" / "AvatarSkillExcelConfigData.json"
proud_skill_data_path = save_path / "ExcelBinOutput" / "ProudSkillExcelConfigData.json"
material_data_path = save_path / "ExcelBinOutput" / "MaterialExcelConfigData.json"
material_data: Dict[str, str] = {}
zh_lang_path = save_path / "TextMap" / "TextMapCHS.json"
with open(zh_lang_path, "r", encoding="utf-8") as _f:
    zh_lang = json.load(_f)
avatar_promote_data: Dict[str, str] = {}
skill_depot_map: Dict[str, int] = {}
"""
开发备忘：

avatar_promote_data_path 是角色升级数据，里面包含了角色升级所需的素材消耗信息
avatar_promote_data 是角色名称 -> avatarPromoteId 的 map

avatar_skill_depot_data_path 是一个角色 id -> 天赋 id 的 map，不包含天赋信息
skill_depot_map 是角色 id -> 主天赋 id 的 map
avatar_skill_data_path 是天赋基础信息，不包含天赋消耗信息，需要进一步通过 proudSkillGroupId 请求
proud_skill_data_path 是天赋详细信息，包含了素材消耗信息

material_data_path 是 item 信息
material_data 是 id -> name 的 map
zh_lang_path 是中文文本信息
"""
data = {"status": 0, "data": {}}


async def get_name_list():
    ignore_name_list = ["旅行者"]
    name_list = []
    with open(avatar_data_path, "r", encoding="utf-8") as f:
        avatar_data = json.load(f)
    for avatar in avatar_data:
        if avatar["featureTagGroupID"] == 10000001:
            # 未上线角色
            continue
        avatar_name = zh_lang[str(avatar["nameTextMapHash"])]
        if avatar_name not in ignore_name_list and avatar_name not in name_list:
            name_list.append(avatar_name)
            avatar_promote_data[avatar_name] = avatar["avatarPromoteId"]
            skill_depot_map[avatar_name] = avatar["skillDepotId"]
            data["data"][avatar_name] = {}
    return name_list


async def load_material_data():
    with open(material_data_path, "r", encoding="utf-8") as f:
        _material_data = json.load(f)
    for material in _material_data:
        try:
            material_data[material["id"]] = zh_lang[str(material["nameTextMapHash"])]
        except KeyError:
            pass


async def get_up_data():
    with open(avatar_promote_data_path, "r", encoding="utf-8") as f:
        _avatar_promote_data = json.load(f)
    data_map: Dict[str, Dict] = {}
    data_material_map: Dict[str, List[str]] = {}
    for avatar in _avatar_promote_data:
        pid = avatar["avatarPromoteId"]
        cos = avatar.get("costItems", [])
        if len(cos) != 4:
            continue
        for i in cos[2:]:
            if not i:
                continue
            t_list = data_material_map.get(pid, [])
            if i["id"] not in t_list:
                t_list.append(i["id"])
                data_material_map[pid] = t_list

        if avatar.get("promoteLevel") != 6:
            continue
        data_map[avatar["avatarPromoteId"]] = avatar
        data_material_map.get(pid, []).sort()
    for avatar in avatar_promote_data.keys():
        pid = avatar_promote_data[avatar]
        t = data_map[pid]
        data["data"][avatar]["ascension_materials"] = material_data[t["costItems"][0]["id"]]
        data["data"][avatar]["level_up_materials"] = material_data[t["costItems"][1]["id"]]
        data["data"][avatar]["materials"] = [material_data[i] for i in data_material_map[pid] if i]


async def load_avatar_skill_depot_data() -> Dict[int, int]:
    with open(avatar_skill_depot_data_path, "r", encoding="utf-8") as f:
        _avatar_skill_depot_data = json.load(f)
    energy_skill_map: Dict[int, int] = {}
    for _avatar in _avatar_skill_depot_data:
        if "energySkill" not in _avatar:
            continue
        energy_skill_map[_avatar["id"]] = _avatar["energySkill"]
    return energy_skill_map


async def load_avatar_skill_data() -> Dict[int, int]:
    with open(avatar_skill_data_path, "r", encoding="utf-8") as f:
        _avatar_skill_data = json.load(f)
    avatar_skill_map: Dict[int, int] = {}
    for _avatar in _avatar_skill_data:
        if "proudSkillGroupId" not in _avatar:
            continue
        avatar_skill_map[_avatar["id"]] = _avatar["proudSkillGroupId"]
    return avatar_skill_map


async def load_proud_skill_data() -> Dict[int, List[str]]:
    with open(proud_skill_data_path, "r", encoding="utf-8") as f:
        _proud_skill_data = json.load(f)
    proud_skill_map: Dict[int, List[str]] = {}
    for _avatar in _proud_skill_data:
        if _avatar["level"] != 10:
            continue
        key = _avatar["proudSkillGroupId"]
        cos = _avatar["costItems"]
        value = [material_data[cos[0]["id"]][1:3], material_data[cos[2]["id"]]]
        proud_skill_map[key] = value
    return proud_skill_map


async def get_skill_data():
    energy_skill_map = await load_avatar_skill_depot_data()
    avatar_skill_map = await load_avatar_skill_data()
    proud_skill_map = await load_proud_skill_data()
    for avatar in skill_depot_map.keys():
        depot_id = skill_depot_map[avatar]
        skill_id = energy_skill_map[depot_id]
        skill_group_id = avatar_skill_map[skill_id]
        data["data"][avatar]["talent"] = proud_skill_map[skill_group_id]


async def main():
    await get_name_list()
    await load_material_data()
    await get_up_data()
    await get_skill_data()
    save_roles_materials()


def save_roles_materials():
    save_path.mkdir(parents=True, exist_ok=True)
    with open(save_path / "roles_material.json", "w", encoding="utf-8") as m_j:
        json.dump(data, m_j, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
