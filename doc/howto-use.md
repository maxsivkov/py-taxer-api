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

## Общее
* Все API вызовы поддерживают параметр `X-Fields`. С помощью этого параметра можно ограничивать количество выдаваемой информации.  
  Например, если в вызове */user/{userId}/operation* указать **X-Fields** значение `operations{id,type,contents{sumCurrency}}` получим только те поля, которые заказывали:
  ```json
    [
      {
        "id": 30,
        "type": "FlowOutgo",
        "contents": [
          {
            "sumCurrency": 12.12
          }
        ]
      },
      {
        "id": 29,
        "type": "FlowIncome",
        "contents": [
          {
            "sumCurrency": 12.12
          }
        ]
      },
      ...
    ]
  ``` 
* Некоторые вызовы, которые выдают множественные результаты (например */user/{userId}/operation*, */user/{userId}/accounts*, ...) поддерживают фильтрацию посредством необязательного параметра **q**.  
  Данный параметр определяет фильтр в [Lucene](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html) нотации.Например:
  ```sql
    filterDate:[2020-04-01 TO 2020-04-30] AND filterTotal:[* TO 200] AND filterCurrency:USD
  ```
   `filterDate:[2020-04-01 TO 2020-04-30]` - выбрать записи с *2020-04-01* по *2020-04-30*   
   `filterTotal:[* TO 200]` - сумма до 200  
   `filterCurrency:USD` - Валюта USD  
   
   **Важно**  
   В фильтре поддерживается только операция **AND**
     
   Критерии для фильтра будут приведены в каждой операции, которая поддерживает фильтрацию
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

<a href="#top">Наверх</a>

## Счета
Есть два способа получения информации: полный и постраничный.  
### Критерии фильтра:
* *filterTitle* - Название счета (Пример `filterTitle:Счет`)
* *filterNum* - Номер счета (Пример `filterNum:ES7921000813610123456789`)
* *filterBank* - Название Банка (Пример `filterBank:"Spain bank"`)
* *filterCurrency* - Валюта счета (Пример `filterCurrency:USD`)
* *filterBalance* - Баланс (Примеры: `filterBalance:[* TO 2000]` - до 2000, `filterBalance:[2000 TO *]` - более 2000, `filterBalance:[2000 TO 2000]` - ровно 2000)
 
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
