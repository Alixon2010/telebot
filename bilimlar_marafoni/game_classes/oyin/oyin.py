import random
import time
import psycopg2
from bilimlar_marafoni.game_classes.database.database import Database
from datetime import datetime

class Oyin:
    def __init__(self, user):
        self.user = user
        self.ball = 0

    def start_game(self, savollar):
        savollar = random.sample(savollar, 5)
        for savol in savollar:
            start = time.time()
            print(savol)
            # a = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
            keys = list(savol.variant.keys())
            variant = {'a': keys[0], 'b': keys[1], 'c': keys[2], 'd': keys[3]}
            while True:
                javob = input('Javob: ')
                if javob in variant.keys():
                    end = time.time()
                    break
            if variant[javob] == savol.togri_javob:
                if end - start > 15:
                    print("Vaqt tugadi!")
                else:
                    print("Bu to'g'ri javob! sizga 10 ball qo'shildi")
                    self.ball += 10
            else:
                print("Bu javob xato(")
            answered_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            Database.save_results(self.user.id, savol.id, variant.get(javob), answered_at)
        else:
            print(f"O'yin tugadi umumiy ball: {self.ball}")
            self.ball = 0

    # def save_result(self):
    #     with open('natijalar.txt', 'a') as file:
    #         file.write(f"{self.ism}: {self.ball}\n")

    # @staticmethod
    # def show_ranking():
    #     with open('natijalar.txt') as file:
    #         datas = file.readlines()
    #         datas.sort(key=lambda x: int(x.split(':')[-1]), reverse=True)
    #         num = 1
    #         for data in datas:
    #             print(f"{num}. {data}", end="")
    #             num += 1

if __name__ == '__main__':
    datas = ['Ali: 50', "Abu: 35", "Umar: 60", "inrge: 4", "Afa: 2"]
    datas.sort(key=lambda x: int(x.split(': ')[1]), reverse=True)
    for data in datas:
        print(data)

