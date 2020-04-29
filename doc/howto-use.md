# Использование
## Содержание
   * [Использование](#использование)
      * [Содержание](#содержание)
      * [Учетная запись](#учетная-запись)
      * [Счета](#счета)
         * [Получение информации по всем счетам](#получение-информации-по-всем-счетам)
         * [Получение информации по счетам постранично](#получение-информации-по-счетам-постранично)
  
Все примеры приведены с использованием [curl](https://curl.haxx.se/) и [jq](https://stedolan.github.io/jq/download/).  
Всю документацию по назначению полей для каждой модели можно найти на http://127.0.0.1:7080/docs раздел Models

## Учетная запись
Запрос:
```bash
curl -sX GET "http://127.0.0.1:7080/account" -H "accept: application/json" | jq
```
Ответ
```json
{
  "accountId": 217106,
  "accountName": "Свирид",
  "users": [
    {
      "id": 200664,
      "idKey": null,
      "titleName": "ФОП Свиридов С. С.",
      "isCompany": false
    }
  ]
}
```
В данном примере в нашем аккаунте один зарегистрированный пользователь _ФОП Свиридов С. С._ с userId **200664**

## Счета
Есть два способа получения информации: полный и постраничный.
### Получение информации по всем счетам
В этом случае мы получаем в ответе информацию по _всем_ счетам, если счетов много, запрос может занять продолжительное время
Обращаем внимание что мы получаем информацию по *userId* = **200664**  
Запрос:
```bash
http://127.0.0.1:7080/user/200664/accounts
```
Ответ
```json
[
  {
    "id": 3,
    "balance": 1048.24,
    "title": "Счет USD",
    "currency": "USD",
    "num": "ES7921000813610123456789",
    "bank": "Spain bank",
    "mfo": null,
    "comment": null,
    "tfBankPlace": "Spain",
    "tfBankSwift": "SPA34",
    "tfBankCorr": "Bank Corr",
    "tfBankCorrPlace": "NY",
    "tfBankCorrSwift": "NY456",
    "tfBankCorrAccount": "123431"
  },
  {
    "id": 2,
    "balance": 14976.88,
    "title": "Счет UAH",
    "currency": "UAH",
    "num": "GR9608100010000001234567890",
    "bank": "УкрПостБудПромИнвТранс Банк",
    "mfo": null,
    "comment": null,
    "tfBankPlace": null,
    "tfBankSwift": null,
    "tfBankCorr": null,
    "tfBankCorrPlace": null,
    "tfBankCorrSwift": null,
    "tfBankCorrAccount": null
  },
  {
    "id": 1,
    "balance": 51,
    "title": "Готівковий",
    "currency": "UAH",
    "num": null,
    "bank": null,
    "mfo": null,
    "comment": null,
    "tfBankPlace": null,
    "tfBankSwift": null,
    "tfBankCorr": null,
    "tfBankCorrPlace": null,
    "tfBankCorrSwift": null,
    "tfBankCorrAccount": null
  }
]
```
У нас 3 зарегистрированных счета:  
* _Готівковий_  имеет **id** 1
* _Счет UAH_ имеет **id** 2
* _Счет USD_ имеет **id** 3

### Получение информации по счетам постранично
Страницы начинаются с **1**  
Запрос:
```bash
http://127.0.0.1:7080/user/200664/accounts/page/1
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
      "balance": 1048.24,
      "title": "Счет USD",
      "currency": "USD",
      "num": "ES7921000813610123456789",
      "bank": "Spain bank",
      "mfo": null,
      "comment": null,
      "tfBankPlace": "Spain",
      "tfBankSwift": "SPA34",
      "tfBankCorr": "Bank Corr",
      "tfBankCorrPlace": "NY",
      "tfBankCorrSwift": "NY456",
      "tfBankCorrAccount": "123431"
    },
    {
      "id": 2,
      "balance": 14976.88,
      "title": "Счет UAH",
      "currency": "UAH",
      "num": "GR9608100010000001234567890",
      "bank": "УкрПостБудПромИнвТранс Банк",
      "mfo": null,
      "comment": null,
      "tfBankPlace": null,
      "tfBankSwift": null,
      "tfBankCorr": null,
      "tfBankCorrPlace": null,
      "tfBankCorrSwift": null,
      "tfBankCorrAccount": null
    },
    {
      "id": 1,
      "balance": 51,
      "title": "Готівковий",
      "currency": "UAH",
      "num": null,
      "bank": null,
      "mfo": null,
      "comment": null,
      "tfBankPlace": null,
      "tfBankSwift": null,
      "tfBankCorr": null,
      "tfBankCorrPlace": null,
      "tfBankCorrSwift": null,
      "tfBankCorrAccount": null
    }
  ]
}
```
По значению **paginator** можно понять сколько страниц с данными у нас доступно. Т.е. если бы _paginator.totalPages_ было бы равно 2, то мы бы могли получить следующую страницу со счетами с помощью `http://127.0.0.1:7080/user/200664/accounts/page/2`

