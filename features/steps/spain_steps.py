from time import sleep
from behave import step
from utils import telegram


@step("check if spain error")
def gather_dates(context):
    while True:
        if 'все слоты для записи на подачу документов полностью забронированы' not in context.driver.page_source:
            telegram.send_document(context, 'Испания: Нет ошибки на странице')
        else:
            sleep(60)
            context.driver.refresh()
