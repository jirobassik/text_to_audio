import vanna as vn
from operator import getitem
vn.set_api_key('bd170b4f8e3842cc93b4522ccadf43ce')
vn.set_model('audio')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'text_to_audio',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
vn.connect_to_postgres('localhost', 'text_to_audio', 'postgres', 'postgres', '5432')
# sql_schema = '''SELECT * FROM information_schema.columns'''
#
# df_information_schema = vn.run_sql(sql_schema)
# print(df_information_schema)
# plan = vn.get_training_plan_generic(df_information_schema)
# print(plan)
# vn.train(plan=plan)

d = vn.ask("sort by time in table history_historymodel", auto_train=True, print_results=False)
print(getitem(d, 0))
# vn.set_model('chinook')
# vn.ask('Print date in table history_historymodel')
# print(vn.get_training_data())