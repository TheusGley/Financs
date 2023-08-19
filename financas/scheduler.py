from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from financas.views import scheduler_vencimento

# from datetime import datetime, timedelta


def start():
    print('Verificando datas de Vencimento')

scheduler = BackgroundScheduler()
scheduler.add_job(scheduler_vencimento, 'interval', days=1)

# scheduler.start()





 