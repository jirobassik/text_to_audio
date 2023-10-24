import vanna as vn
from operator import getitem
from typing import NoReturn


class VannaUse:
    def __init__(self):
        vn.set_api_key('bd170b4f8e3842cc93b4522ccadf43ce')
        vn.set_model('audio')
        vn.connect_to_postgres('localhost', 'text_to_audio', 'postgres', 'postgres', '5432')

    @staticmethod
    def train_vanna(sql_schema='''SELECT * FROM information_schema.columns''') -> NoReturn:
        df_information_schema = vn.run_sql(sql_schema)
        print(df_information_schema)
        plan = vn.get_training_plan_generic(df_information_schema)
        print(plan)
        vn.train(plan=plan)

    @staticmethod
    def text_to_sql(question: str):
        answer = vn.ask(question, auto_train=True, print_results=False)
        sql_answer = getitem(answer, 0)
        print(sql_answer)
        return sql_answer

# vanna_use = VannaUse()
# print(vanna_use.text_to_sql('Print use_vote and text in table history_historymodel'))
