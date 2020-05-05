# Операции
#Содержание
* [Общие](#общие)
* [Критерии фильтра](#критерии-фильтра)
* [Получение краткой информации по всем операциям](#получение-краткой-информации-по-всем-операциям)
* [Получение информации по счетам постранично](#получение-информации-по-счетам-постранично)
* [Операция <em>FlowIncome</em> - доход](#операция-flowincome---доход)
  * [Получение информации](#получение-информации)
  * [Добавление](#добавление)
## Общие
Существует несколько типов операций, их различают по названиям, далее будут часто встречаться
* *FlowIncome* - доход  
* *AutoExchange* - валютный доход  
* *FlowOutgo* - расход  
* *CurrencyExchange* - обмен валют  
* *Withdrawal* - перевод между счетами  

Есть два способа получения информации: полный и постраничный.  
## Критерии фильтра
* *filterType* - Тип операции. см. выше (Пример `filterType:Withdrawal`)
* *filterDate* - Дата проведения операции (Пример `filterDate:[2020-04-24 TO 2020-04-24]` - отобрать за 24.04, `filterDate:[* TO 2020-04-24]` - до 24.04, `filterDate:[2020-04-24 TO *]` - после 24.04)
* *filterTotal* - Сумма (Пример `filterTotal:[200 TO 200]`- отобрать за операции с суммой 200, `filterTotal:[* TO 200]` - до 200, `filterTotal:[200 TO *]` - свыше 200)
* *filterCurrency* - Валюта (Пример `filterCurrency:USD`)
* *filterAccount* - Фильтр по идентификатору счета (Примеры: `filterAccount:7`)
* *filterComment* - Фильтр по коментарию (Примеры: `filterComment:трололо`)
 
## Получение краткой информации по всем операциям
В этом случае мы получаем в ответе информацию по _всем_ счетам, если операций много, запрос может занять продолжительное время.  
Запрос:
```bash
curl -sX GET "http://127.0.0.1:7080/user/200664/operation" | jq

```
Ответ
```json
[
  {
    "id": 30,
    "type": "FlowOutgo",
    "path": "/user/200664/operation/flowoutgo/30",
    "comment": "Расход",
    "contents": [
      {
        "id": 46,
        "date": "2020-04-24T01:02:00",
        "sumCurrency": 12.12,
        "accountTitle": "Счет UAH",
        "accountCurrency": "UAH",
        "comment": ""
      }
    ]
  },
  {
    "id": 29,
    "type": "FlowIncome",
    "path": "/user/200664/operation/flowincome/29",
    "comment": "Доход",
    "contents": [
      {
        "id": 45,
        "date": "2020-04-24T01:02:00",
        "sumCurrency": 12.12,
        "accountTitle": "Счет USD",
        "accountCurrency": "USD",
        "comment": "Курс НБУ на 24.04.2020 27,0137"
      }
    ]
  },
  .....
]
```
выбрано 2 операции, первая *FlowOutgo* - расход, более детальную информацию можно получить по `/user/200664/operation/flowoutgo/30`; 
вторая FlowIncome (расход), детальная информация `/user/200664/operation/flowincome/29`

## Получение информации по счетам постранично
Страницы начинаются с **1**  
Запрос:
```bash
curl -sX GET "http://127.0.0.1:7080/user/200664/operation/page/1" | jq

```
Ответ
```json
{
  "paginator": {
    "currentPage": 1,
    "recordsOnPage": 15,
    "totalPages": 2
  },
  "currencies": [
    "UAH",
    "USD",
    "EUR"
  ],
  "operations": [
    {
      "id": 30,
      "type": "FlowOutgo",
      "path": "/user/200664/operation/flowoutgo/30",
      "comment": "Расход",
      "contents": [
        {
          "id": 46,
          "date": "2020-04-24T01:02:00",
          "sumCurrency": 12.12,
          "accountTitle": "Счет UAH",
          "accountCurrency": "UAH",
          "comment": ""
        }
      ]
    },
    {
      "id": 29,
      "type": "FlowIncome",
      "path": "/user/200664/operation/flowincome/29",
      "comment": "Доход",
      "contents": [
        {
          "id": 45,
          "date": "2020-04-24T01:02:00",
          "sumCurrency": 12.12,
          "accountTitle": "Счет USD",
          "accountCurrency": "USD",
          "comment": "Курс НБУ на 24.04.2020 27,0137"
        }
      ]
    },
    ....
]
```
По значению **paginator** можно понять сколько страниц с данными у нас доступно. Т.к. _paginator.totalPages_ у нас 2, то мы можем получить следующую страницу с операциями с помощью `http://127.0.0.1:7080/user/200664/operation/page/1`

<a href="#top">Наверх</a>

## Операция *FlowIncome* - доход  
### Получение информации
Запрос:
```bash
curl -sX GET "http://127.0.0.1:7080/user/200664/operation/flowincome/29" | jq
```
Ответ
```json
{
  "id": 29,
  "date": "2020-04-24T01:02:00",
  "comment": "Доход",
  "financeType": "custom",
  "total": 12.12,
  "payedSum": 12.11,
  "account": {
    "id": 3,
    "title": "Счет USD",
    "currency": "USD"
  },
  "contractor": {
    "id": 1,
    "title": "ABC Co."
  },
  "parent": {
    "id": 1,
    "number": "ABC Co Документ № 1",
    "title": "Договір №ABC Co Документ № 1 від 01.04.2020",
    "type": "contract"
  }
}
```
В принципе не вижу смысла все расписывать, и так вроде понятно
### Добавление
Запрос:
```bash
curl -sX POST "http://127.0.0.1:7080/user/200664/operation/flowincome" -H  "Content-Type: application/json"  -d @add-operation-data.json
```
Где `add-operation-data.json` - файл в кодировке UTF-8 следующего содержания
```json
{
  "date": "2020-04-24T01:02:00",
  "comment": "Доход",
  "total": 12.12,
  "payedSum": 12.11,
  "account": {
    "id": 3
  },
  "contractor": {
    "id": 1
  },
  "parent": {
    "id": 1,
    "type": "contract"
  }
}
```
* *account* - счет 
* *contractor* - контрагент
* *parent* - это документ, к которому привязывается доход. Его можно не указывать

Ответ
```json
{
    "id": 33
}
```
