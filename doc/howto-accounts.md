# Счета
#Содержание
- [Счета](#счета)
  - [Критерии фильтра](#критерии-фильтра)
  - [Получение информации по всем счетам](#получение-информации-по-всем-счетам)
  - [Получение информации по счетам постранично](#получение-информации-по-счетам-постранично)
  - [Добавление нового счета](#добавление-нового-счета)
    - [Валютного](#валютного)
    - [UAH](#uah)
  
Есть два способа получения информации: полный и постраничный.  
## Критерии фильтра
* *filterTitle* - Название счета (Пример `filterTitle:Счет`)
* *filterNum* - Номер счета (Пример `filterNum:ES7921000813610123456789`)
* *filterBank* - Название Банка (Пример `filterBank:"Spain bank"`)
* *filterCurrency* - Валюта счета (Пример `filterCurrency:USD`)
* *filterBalance* - Баланс (Примеры: `filterBalance:[* TO 2000]` - до 2000, `filterBalance:[2000 TO *]` - более 2000, `filterBalance:[2000 TO 2000]` - ровно 2000)
 
## Получение информации по всем счетам
В этом случае мы получаем в ответе информацию по _всем_ счетам, если счетов много, запрос может занять продолжительное время
Обращаем внимание что мы получаем информацию по *userId* = **200664**  
Запрос:
```bash
curl -sX GET "http://127.0.0.1:7080/user/200664/accounts" | jq

```
Ответ
```json
[
  {
    "id": 3,
    "balance": 1346.28,
    "title": "Счет USD",
    "currency": "USD",
    "num": "ES7921000813610123456789",
    "bank": "Spain bank",
    "tfBankPlace": "Spain",
    "tfBankSwift": "SPA34",
    "tfBankCorr": "Bank Corr",
    "tfBankCorrPlace": "NY",
    "tfBankCorrSwift": "NY456",
    "tfBankCorrAccount": "123431"
  },
  {
    "id": 2,
    "balance": 18188.64,
    "title": "Счет UAH",
    "currency": "UAH",
    "num": "GR9608100010000001234567890",
    "bank": "УкрПостБудПромИнвТранс Банк"
  },
  {
    "id": 1,
    "balance": 301,
    "title": "Готівковий",
    "currency": "UAH"
  }
]
```
У нас 3 зарегистрированных счета:  
* _Готівковий_  имеет **id** 1
* _Счет UAH_ имеет **id** 2
* _Счет USD_ имеет **id** 3  

## Получение информации по счетам постранично
Страницы начинаются с **1**  
Запрос:
```bash
curl -sX GET "http://127.0.0.1:7080/user/200664/accounts/page/1" | jq

```
Ответ
```json
{
  "paginator": {
    "currentPage": 1,
    "recordsOnPage": 15,
    "totalPages": 1
  },
  "accountsCurrencies": [
    "UAH",
    "USD"
  ],
  "accounts": [
    {
      "id": 3,
      "balance": 1346.28,
      "title": "Счет USD",
      "currency": "USD",
      "num": "ES7921000813610123456789",
      "bank": "Spain bank",
      "tfBankPlace": "Spain",
      "tfBankSwift": "SPA34",
      "tfBankCorr": "Bank Corr",
      "tfBankCorrPlace": "NY",
      "tfBankCorrSwift": "NY456",
      "tfBankCorrAccount": "123431"
    },
    {
      "id": 2,
      "balance": 18188.64,
      "title": "Счет UAH",
      "currency": "UAH",
      "num": "GR9608100010000001234567890",
      "bank": "УкрПостБудПромИнвТранс Банк"
    },
    {
      "id": 1,
      "balance": 301,
      "title": "Готівковий",
      "currency": "UAH"
    }
  ]
}
```
По значению **paginator** можно понять сколько страниц с данными у нас доступно. Т.е. если бы _paginator.totalPages_ было бы равно 2, то мы бы могли получить следующую страницу со счетами с помощью `http://127.0.0.1:7080/user/200664/accounts/page/2`

<a href="#top">Наверх</a>

## Добавление нового счета
### Валютного
Запрос:
```bash
curl -sX POST "http://127.0.0.1:7080/user/200664/accounts" -H  "Content-Type: application/json"  -d @add-account-data.json
```
Где `add-account-data.json` - файл в кодировке UTF-8 следующего содержания
```json
{
  "title": "Тестовый EUR",
  "currency": "EUR",
  "num": "SA4420000001234567891234",
  "bank": "Saudi Arabia bank",
  "comment": "Тестовый Saudi Arabia bank",
  "tfBankPlace": "Saudi Arabia",
  "tfBankSwift": "SA123",
  "tfBankCorr": "Norway bank",
  "tfBankCorrPlace": "Norway",
  "tfBankCorrSwift": "NW321",
  "tfBankCorrAccount": "657890"
}
```
Ответ
```json
{
    "id": 6
}
```
### UAH
Запрос:
```bash
curl -sX POST "http://127.0.0.1:7080/user/200664/accounts" -H  "Content-Type: application/json"  -d @add-account-data.json
```
Где `add-account-data.json` - файл в кодировке UTF-8 следующего содержания
```json
{
  "title": "Приватбанк-UAH",
  "currency": "UAH",
  "num": "UA513052990000000000000026000",
  "bank": "Приватбанк",
  "comment": "Тестовый Приватбанк"
}
```
Ответ
```json
{
    "id": 7
}
```
