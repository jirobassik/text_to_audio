import vanna as vn
from operator import getitem
from typing import NoReturn


class VannaUse:
    def __init__(self):
        vn.set_api_key('bd170b4f8e3842cc93b4522ccadf43ce')
        vn.set_model('audio_3')
        vn.connect_to_postgres('localhost', 'text_to_audio', 'postgres', 'postgres', '5432')

    @staticmethod
    def train_vanna(sql_schema='''SELECT * FROM information_schema.columns''') -> NoReturn:
        df_information_schema = vn.run_sql(sql_schema)
        plan = vn.get_training_plan_generic(df_information_schema)
        vn.train(plan=plan)

    @staticmethod
    def text_to_sql(question: str):
        answer = vn.ask(question, auto_train=True, print_results=False)
        sql_answer = getitem(answer, 0)
        return sql_answer

# vanna_use = VannaUse()
# sql_ = '''SELECT * FROM INFORMATION_SCHEMA.COLUMNS
# WHERE table_name NOT IN ('auth_group', 'auth_group_permissions', 'auth_permission', 'auth_user', 'auth_user_groups',
# 'auth_user_user_permissions', 'django_admin_log', 'django_content_type', 'django_migrations', 'django_session',
# 'taggit_tag', 'taggit_taggeditem', 'user_vote_uservotemodel', 'vote_votemodel', 'user_vote_useraudiofile',
# 'vote_audiofilemodel') AND table_schema = 'public'
# AND column_name IN ('id', 'text', 'audio_file', 'content_type_id', 'time_add'); '''
# vanna_use.train_vanna(sql_)
# print(vanna_use.text_to_sql('Print text, audio_file and sort by time_add'))
