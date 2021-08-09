# импортируем нативных библиотек Python
import json
from urllib import parse, request

# Импорт установленных библиотек
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Импорт токена и chat id
from credentials import TOKEN, CHAT_ID

# Предоставленный банком адрес
URL = "https://api.monobank.ua/bank/currency"

# Достанем, расшифруем и выведем в консоль всю полученную информацию
content = request.urlopen(url=URL).read()
content_decoded = json.loads(content.decode("utf-8"))
print(content_decoded[0])

# Приведем нашу строку с курсом к дружелюбному виду
target_note = content_decoded[0]
message = f"Currency {target_note['currencyCodeA']} to {target_note['currencyCodeB']} rate: \n " \
          f"rate buy: {target_note['rateBuy']} \n rate sell: {target_note['rateSell']}"

# Сформируем запрос и отправим сообщение себе в чат
bot_url = f"https://api.telegram.org/{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={parse.quote(message)}&parse_mode=html"
request.urlopen(bot_url)

# Обьявим с какими Google сервисами будем работать
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']

# Авторизируемся со своим Service Account Key
client = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope))

# Обозначим к какому документу мы обращаемся
doc_name = 'test sheet'
sheet = client.open(doc_name)
worksheet = sheet.worksheet('Sheet1')

# И запишем данные в саму google таблицу
worksheet.append_row(['currency ISO', 'currency ISO', 'Buy rate', 'Sell rate'])
worksheet.append_row([target_note['currencyCodeA'], target_note['currencyCodeB'],
                      target_note['rateBuy'], target_note['rateSell']])
