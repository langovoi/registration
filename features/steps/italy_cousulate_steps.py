from behave import step, use_step_matcher
from utils import telegram

use_step_matcher('re')


@step("gather italy consulate dates")
def gather_dates(context):
    # check context
    for date_slot in context.page.get_elements('dates section'):
        if date_slot.text:
            context.values['dates'].append(date_slot.text)
    # check Unfortunately message
    expected_message = 'Unfortunately, there are no appointments available at this time'
    if not context.page.is_element_displayed('unfortunately message') or expected_message not in context.page.get_text(
            'unfortunately message'):
        with open("page_source.html", "w") as f:
            f.write(context.driver.page_source)
        try:
            telegram.send_document(context, caption="Unfortunately message is not displayed or changed")
        except Exception:
            raise RuntimeError('gather dates step')


@step("send italy dates")
def send_dates(context):
    with open('page_source.html', 'w') as f:
        f.write(context.driver.page_source)
    telegram.send_document(context, caption=f'🇮🇹 Итальянские даты найдены 🇮🇹')
    raise RuntimeError('autoretry')
