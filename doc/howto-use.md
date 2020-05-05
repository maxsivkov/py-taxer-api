# Использование
## Содержание
  * [Общее](#общее)
  * [Учетная запись](#учетная-запись)
  * [<a href="howto-accounts.md">Счета</a>](#счета)
  * [<a href="howto-operations.md">Операции</a>](#операции)  
  
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
  Данный параметр определяет фильтр в [Lucene](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html) нотации. Например:
  ```sql
    filterDate:[2020-04-01 TO 2020-04-30] AND filterTotal:[* TO 200] AND filterCurrency:USD
  ```
   `filterDate:[2020-04-01 TO 2020-04-30]` - выбрать записи с *2020-04-01* по *2020-04-30*   
   `filterTotal:[* TO 200]` - сумма до 200  
   `filterCurrency:USD` - Валюта USD  
   
   **Важно**  
   В фильтрах поддерживается только операция **AND**
     
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

## [Счета](howto-accounts.md)
## [Операции](howto-operations.md)
