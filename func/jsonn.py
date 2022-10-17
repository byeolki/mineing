from nextcord import Member
import json, math

class Jsonn():
    def __init__(self, user : Member):
        self.user = user
        self.Json = []
        self.path = r'Team Timeless\yubin\func\json\user.json'

    def name_check(self, name:str):
        try:
            with open(self.path , "r" , encoding = "UTF-8") as f:
                data = json.load(f)
            for i in data:
                if name == data[i][0]['name']:
                    return "돌아가"
            return "통과"
        except:
            return "통과"
    def user_read(self):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            return json.load(f)[str(self.user.id)]

    def all_read(self):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            return json.load(f)

    def signup(self, name: str):
        print("[!] 새 유저가 가입함")
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data= json.load(f)
        data[str(self.user.id)] = []
        data[str(self.user.id)].append({"name":name, "level":1, "exp":0, "money":100000})
        data[str(self.user.id)].append({"돌":0, "구리":0, "철":0, "금":0, "다이아몬드":0, "에메랄드":0})
        data[str(self.user.id)].append({"lv.1":[300]})
        # data[str(self.user.id)].append({"보석가공인":[1000], "석재가공인":[5000], "철강업자":[2000]})
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')
    
    def plus_money(self, money:int):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)[str(self.user.id)]
        data[0]['money'] = data[0]['money']+money
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')

    def plus_exp(self, exp:int):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        data[str(self.user.id)][0]['exp'] = data[str(self.user.id)][0]['exp']+exp
        while data[str(self.user.id)][0]['level']*150 <= data[str(self.user.id)][0]['exp']+exp:
            data[str(self.user.id)][0]['exp'] = data[str(self.user.id)][0]['exp']+exp - data[str(self.user.id)][0]['level']*150
            data[str(self.user.id)][0]['level'] = data[str(self.user.id)][0]['level'] + 1
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')
        return data[str(self.user.id)][0]

    def plus_pickaxe(self, lv:int):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        try: data[str(self.user.id)][2][f'lv.{lv}'].append(((lv+lv)**2)*300)
        except: data[str(self.user.id)][2][f'lv.{lv}'] = [(((lv+lv)**2)*300)]
        if data[str(self.user.id)][0][f'money'] - 50000*lv < 0:
            return "놉"
        data[str(self.user.id)][0][f'money']=data[str(self.user.id)][0][f'money'] - 50000*lv
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')
        return ((lv+lv)**2)*300

    def choose_pickaxe(self):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        pickaxe_data = data
        lst = []; 
        for i in pickaxe_data[str(self.user.id)][2]:
            lst.append(int(i.split('.')[-1]))
        lst.sort(reverse=True)
        if len(lst) == 0:
            return "곡괭이 없음"
        self.pickaxe = lst
        return f'lv.{lst[0]}'
    
    def mining(self, block_count, block:dict):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        block_data = data
        block_data[str(self.user.id)][1]["돌"] = block_data[str(self.user.id)][1]["돌"]+block["돌"]; block_data[str(self.user.id)][1]["구리"] = block_data[str(self.user.id)][1]["구리"]+block["구리"]; block_data[str(self.user.id)][1]["철"] = block_data[str(self.user.id)][1]["철"]+block["철"]
        block_data[str(self.user.id)][1]["금"] = block_data[str(self.user.id)][1]["금"]+block["금"]; block_data[str(self.user.id)][1]["다이아몬드"] = block_data[str(self.user.id)][1]["다이아몬드"]+block["다이아몬드"]; block_data[str(self.user.id)][1]["에메랄드"] = block_data[str(self.user.id)][1]["에메랄드"]+block["에메랄드"]
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(block_data, f, ensure_ascii=False, indent='\t')
        pickaxe_data = data
        if pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"][0]-block_count < 0:
            del pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"][0]
            try: pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"][0] = pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"[1]][0]-block_count
            except: 
                try : pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"][0] = pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"][1]-block_count    
                except:
                    if len(pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"]) == 0:
                        del pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"]
                    with open(self.path, "w", encoding='utf-8') as f:
                        json.dump(pickaxe_data, f, ensure_ascii=False, indent='\t')
                    return '곡괭이 깨짐'
        pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"][0] = pickaxe_data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"][0]-block_count        
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(pickaxe_data, f, ensure_ascii=False, indent='\t')
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        return data[str(self.user.id)][2][f"lv.{self.pickaxe[0]}"]
    
    def get_axe(self):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data=  json.load(f)
        read = []
        for i in data[str(self.user.id)][2]:
            for h in data[str(self.user.id)][2][i]:
                if ((int(i.split(".")[-1]))**2)*300 == h: pass
                else: read.append(f'{i} 곡괭이 : 내구도 : {h}')
        return read

    def fix_pickaxe(self, lv, nagoo):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        user_data = data[str(self.user.id)]; z = 0
        for i in user_data[2][lv]:
            if i == nagoo:
                pickaxe = z
            z += 1
        level = int(lv.split(".")[-1]); nagooo = ((level+level)**2)*300
        before = user_data[2][lv][pickaxe]; fix = math.ceil((nagooo - before)/100)
        if level == 1: gub = "돌"
        elif level == 2: gub = "구리"
        elif level == 3: gub = "철"
        elif level >= 4: gub="다이아몬드"
        if user_data[1][gub] < fix: return 'nope'
        else:
            user_data[1][gub] = user_data[1][gub]-fix
            user_data[2][lv][pickaxe] = nagooo
            data[str(self.user.id)] = user_data
            with open(self.path, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent='\t')
            with open(self.path , "r" , encoding = "UTF-8") as f:
                data = json.load(f)
            return data[str(self.user.id)][2][lv][pickaxe]
            
    def get_block(self):
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        user_data = data[str(self.user.id)]
        read = ["전체"]
        for i in user_data[1]:
            if user_data[1][i] != 0:
                read.append(f"{i} : {user_data[1][i]}개")
        return read
    
    def sell_block(self, category):
        sise = {"돌":1000, "구리":3500,"철":5000, "금":7000, "다이아몬드":10000, "에메랄드":12000}
        with open(self.path , "r" , encoding = "UTF-8") as f:
            data = json.load(f)
        user_data = data[str(self.user.id)]; y= 0
        if category == "전체":
            block_count = 0
            for i in user_data[1]:
                user_data[0]['money'] = user_data[0]['money']+(sise[i]*user_data[1][i]);y+=sise[i]*user_data[1][i]; block_count+=user_data[1][i]
                user_data[1][i] = 0
            data[str(self.user.id)] = user_data
            with open(self.path, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent='\t')
            return [y, user_data[0]['money'], block_count]
        else:
            user_data[0]['money'] = user_data[0]['money']+(sise[category]*user_data[1][category]);y=sise[category]*user_data[1][category]
            user_data[1][category] = 0
            data[str(self.user.id)] = user_data
            with open(self.path, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent='\t')
            return [y,user_data[0]['money']]
            