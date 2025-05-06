KEYS_MAP = {
    "id": "ELKKIAIGOBK",
    "nameTextMapHash": "DNINKKHEILA",
    "descTextMapHash": "PGEPICIANFN",
    # AvatarSkillExcelConfigData
    "skillIcon": "BGIHPNEDFOL",
    "forceCanDoSkill": "CFAICKLGPDP",
    "costElemType": "PNIDLNBBJIC",
    "proudSkillGroupId": "DGIJCGLPDPI",
    # AvatarTalentExcelConfigData
    "talentId": "JFALAEEKFMI",
    "icon": "CNPCNIGHGJJ",
    # ReliquaryExcelConfigData
    "itemType": "CEBMMGCMIJM",
    "equipType": "HNCDIADOINL",
    "rankLevel": "IMNCLIODOBL",
    "mainPropDepotId": "AIPPMEGLAKJ",
    "appendPropDepotId": "GIFPAPLPMGO",
    # EquipAffixExcelConfigData
    "affixId": "NEMBIFHOIKM",
    "openConfig": "JIPJEMFCKAI",
    # ReliquaryMainPropExcelConfigData
    # ReliquaryAffixExcelConfigData
    "propType": "JJNPGPFNJHP",
    "propValue": "AGDCHCBAGFO",
    # WeaponExcelConfigData
    "awakenIcon": "KMOCENBGOEM",
    # MaterialExcelConfigData
    "materialType": "HBBILKOGMIP",
    "picPath": "PPCKMKGIIMP",
    # ManualTextMapConfigData
    "textMapId": "EHLGDOCBKBO",
    "textMapContentTextMapHash": "ECIGIIKPLGD",
    # ProfilePictureExcelConfigData
    "iconPath": "FPPENJGNALC",
    # AvatarSkillDepotExcelConfigData
    "skills": "CBJGLADMBHG",
    "energySkill": "GIEFGHHKGDD",
    "talents": "IAGMADCJGIA",
    # AvatarExcelConfigData
    "iconName": "OCNPJGGMLLO",
    "sideIconName": "IPNPPIGGOPB",
    "qualityType": "ADLDGBEKECJ",
    "skillDepotId": "HCBILEOPKHD",
    "candSkillDepotIds": "FOCOLMLMEFN",
    "featureTagGroupID": "EOCNJBDLDMK",
    "avatarPromoteId": "ECMKJJIDKAE",
    # AvatarPromoteExcelConfigData
    "costItems": "FPIJIIENLBP",
    "promoteLevel": "AKPHFJACMIB",
    # ProudSkillExcelConfigData
    "level": "BHFAPOEDIDB",
}


def fix_map(data: str) -> str:
    for k, v in KEYS_MAP.items():
        data = data.replace(f'"{v}":', f'"{k}":')
    return data
