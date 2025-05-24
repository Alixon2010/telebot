from bilimlar_marafoni.game_classes.savol.savol import Savol
import psycopg2
import json
from tabulate import tabulate
from bilimlar_marafoni.game_classes.user.user import User
class Database:
    conn = psycopg2.connect(
        dbname='bilimlar_marafoni',
        user='postgres',
        host='localhost',
        password='Alixon2010',
        port = 5432
    )
    # @staticmethod
    # def load_questions():
    #     try:
    #         with open('savollar.json') as file:
    #             savollar = json.load(file)
    #             res = [Savol(savol['matn'], savol['variantlar'], savol['togri_javob'], savol['kategoriya']) for savol in savollar]
    #             return res
    #     except FileNotFoundError:
    #         print("Fayl topilmadi")
    @classmethod
    def get_categories(cls):
        curr = cls.conn.cursor()
        with cls.conn:
            curr.execute("SELECT id, name FROM category")
        return curr.fetchall()

    @classmethod
    def get_subcategories(cls, cat_id = None):
        curr = cls.conn.cursor()
        with cls.conn:
            if cat_id:
                curr.execute(f"SELECT id, name FROM subcategory WHERE category_id = {cat_id}")
            else:
                curr.execute("SELECT id, name FROM subcategory")
        return curr.fetchall()

    @classmethod
    def get_questions(cls, subcategory_id = None):
        curr = cls.conn.cursor()
        with cls.conn:
            if subcategory_id:
                curr.execute(f"SELECT id, question FROM quiz WHERE subcategory_id = {subcategory_id}")
            else:
                curr.execute(f"SELECT id, question FROM quiz")
        return curr.fetchall()

    @classmethod
    def get_answers(cls, question_id):
        curr = cls.conn.cursor()
        with cls.conn:
            curr.execute(f"SELECT id, option_text, is_correct FROM option WHERE quiz_id = {question_id}")
        return curr.fetchall()

    @classmethod
    def load_questions(cls):
        res = []
        for cat_id, cat_name in cls.get_categories():
            for sub_id, sub_name in cls.get_subcategories(cat_id):
                for question_id, question in cls.get_questions(sub_id):
                    r = cls.get_answers(question_id)
                    togri_javob = ''
                    for answer in r:
                        if answer[-1]:
                            togri_javob = answer[0]
                    variant = dict([(k, v) for k, v in zip(map(lambda x: x[0], r), map(lambda x: x[1], r))])
                    res.append(Savol(id = question_id, kategorya=cat_name, subcategory=sub_name, matn=question, togri_javob=togri_javob, variant=variant))
        return res
        # res = {'quiz': quiz, 'subcategory': subcategory, 'category': category}
        # savollar = [Savol(kategorya=res["category"][1], subcategory = res["subcategory"][2], matn = res["quiz"][2])]

    @classmethod
    def load_questions_by_category_and_subcategory(cls, cat, sub, questions):
        res=[]
        for question in questions:
            if question.kategorya == cat.capitalize() and question.subcategory == sub:
                res.append(question)
        return res

    @classmethod
    def save_user(cls, chat_id, first_name):
        curr = cls.conn.cursor()
        with cls.conn:
            curr.execute(f"INSERT INTO users(chat_id, name) VALUES({chat_id}, '{first_name}')")

    @classmethod
    def save_results(cls, chat_id, quiz_id, option_id, answered_at):
        curr = cls.conn.cursor()
        with cls.conn:
            curr.execute(f"INSERT INTO users_answer(chat_id, quiz_id, option_id, answered_at) VALUES (%s, %s, %s, %s)", (chat_id, quiz_id, option_id, answered_at))

    @classmethod
    def load_users(cls):
        res = []
        curr = cls.conn.cursor()
        command = "SELECT * FROM users"
        with cls.conn:
            curr.execute(command)
        for user in curr.fetchall():
            res.append(User(*user[1:], user[0]))
        return res

    @classmethod
    def show_ranking(cls):
        curr = cls.conn.cursor()
        command = """SELECT ua.user_id, COUNT(*) * 10 AS score
                     FROM users_answer ua
                     JOIN option o ON ua.option_id = o.id
                     WHERE o.is_correct = 1
                     GROUP BY ua.user_id;"""
        with cls.conn:
            curr.execute(command)
        print(tabulate(curr.fetchall(), headers=['user_id', 'score'], tablefmt='psql'))

    @classmethod
    def search_user_by_chat_id(cls, chat_id):
        curr = cls.conn.cursor()
        command = """SELECT * FROM users WHERE chat_id = %s"""
        with cls.conn:
            curr.execute(command, (chat_id, ))
        return curr.fetchone()
    # @classmethod
    # def requiz(cls, dquizs):
    #     output = []
    #
    #     for i in range(0, len(dquizs), 4):
    #         group = dquizs[i:i + 4]  # берём 4 элемента
    #         id_ = group[0][0]
    #         question = group[0][1]
    #         third_values = tuple(item[2] for item in group)
    #         fourth_values = tuple(item[3] for item in group)
    #         th_f = tuple(zip(third_values, fourth_values))
    #         output.append((id_, question, th_f))
    #
    #     return output

if __name__ == '__main__':
    print()
    for index, x in enumerate(Database.load_questions(), 1):
        print(f"{index}. {x}\n\n")
        print("---------------------------------------------------------------------\n\n")