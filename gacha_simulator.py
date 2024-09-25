import openpyxl
import random

# ガチャデータの読み込み
# "https://bluearchive.wikiru.jp/?:config/plugin/gachasimulator/table/240925_黒君は遠き慮り有りて" のデータを利用
wb = openpyxl.load_workbook("gacha_simulator\gacha_simu_data.xlsx")

def gacha_process(rand_num, is_special):

    # 乱数からレア度決定

    # ピックアップ (0.7%)
    if rand_num <= 70:
        sheet = wb["70"]
        rank = 3
    
    # ☆3 (2.3%)
    elif rand_num <= 300:
        sheet = wb["230"]
        rank = 3

    # 10連用☆2確定 (97%)
    elif is_special == True:
        sheet = wb["9700"]
        rank = 2
    
    # ☆2 (18.5%)
    elif rand_num <= 2150:
        sheet = wb["1850"]
        rank = 2

    # ☆1 (78.5%)
    else:
        sheet = wb["7850"]
        rank = 1

    # シートの行数から同レア度のキャラ数を取得
    max_row = sheet.max_row

    # 同レア度のキャラ候補リストを作成
    gacha_candidate = list(map(lambda c: c.value, sheet["a"]))

    # キャラ候補からランダムに抽出
    rand_candidate = random.randint(0, max_row - 1)
    gacha_result = gacha_candidate[rand_candidate]
    
    return gacha_result, rank


# 1回ひく
def gacha_once():
    rand_gacha = random.randint(1, 10000)

    return gacha_process(rand_gacha, False)

# 10回ひく（☆2確定処理あり）
def gacha_ten_time():
    result_list = []

    for trial in range(10):
        rand_gacha = random.randint(1, 10000)

        if trial != 9:
            is_special = False
        else:
            is_special = True

        result = gacha_process(rand_gacha, is_special)
        result_list.append(result)

    return result_list

print(gacha_ten_time())