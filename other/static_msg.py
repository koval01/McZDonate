repeat = "Повторите попытку (/start)"

start_answer = "Привет! Я Донат-Бот Залупы. Чтобы продолжить пришли мне пожалуйста свой никнейм."
nick_error = "Невалидный никнейм. %s" % repeat
service_error = "Невалидный выбор. %s" % repeat
canceled = "Отменено!"
receipt_get_error = "Этот чек не твой или он не существует."
thr_receipt = "<i>Для проверки платежа стоит ограничение в 30 секунд. " \
              "После каждого запроса ставится ограничение, при запросе " \
              "до завершения таймера он сбрасывается опять.</i>"
qiwi_check = "Проверяем платёж..."
qiwi_ok = "Платёж найден."
qiwi_err = "Платёж не найден."
service_done = "Команды отправлены в консоль."
old_receipt_notify = "<i>Неоплаченный чек живёт 30 минут, после чего он будет удалён.</i>"
check_receipt_notify = "<i>Используйте эту команду после того как QIWI сообщил об успешном завершении транзакции.</i>"
qiwi_disclaimer = "<i>После перехода по ссылке для оплаты ничего не меняйте. В противном случае " \
                  "оплата может пройти неуспешно.</i>"
throttled_check_pay = "Троттлинг сообщения. Вызывать проверку оплаты можно раз в 30 секунд. " \
                      "Если отправить запрос раньше, чем через 30 секунд, то таймер сбросится. " \
                      "Извините за неудобства.\n\n" \
                      "<i>Сделано это по той причине, что Киви даёт возможность за одну минуту " \
                      "отправлять не больше 100 запросов. После исчерпания лимита запросы " \
                      "блокируются на 5 минут.</i>"
