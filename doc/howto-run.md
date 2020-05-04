# Запуск
В зависимости от режима работы приложение требует различных входных параметров (они задаются с помощью переменных среды)
Запуск с помощью указания cookies более предпочтителен, так как в приложение не передаются данные пользователя (username/password), однако потребует неких дополнительных действий (см ниже)

Если запуск идет с помощью указания cookies, нужно установить переменные среды:
* **TAXER_COOKIES** - строка с куками (токен там уже закодирован, его отдельно передавать ненужно).Как получить cookies описано ниже   

Если запускаем с помощью указания user/password:
* **TAXER_USER** - имя пользователя для входа в taxer.ua 
* **TAXER_PWD** - пароль

## Как получить cookies
* Открываем браузер, [логинимся](https://taxer.ua/login)
* Открываем браузерный отладчик (обычно F12)
* Переходим во вкладку Console
* В консоли выполняем `document.cookie`
* Копируем эти данные (без кавычек). Это будет наша переменная **TAXER_COOKIES**
* Taxer выдает куки где-то на 1 неделю, т.е. через неделю они заекспайрятся и нужно будет проделать всю процедуру заново
 
## Запуск с помощью cookies

### Используя [docker](https://www.docker.com/)
- требуется установленный сам [docker](https://www.docker.com/) и [docker-compose](https://docs.docker.com/compose/install/)
- скачать файл docker-compose.yml
- создать файл `.user.env` и поместить туда переменную **TAXER_COOKIES** с содержимым. Должно получиться примерно так:
```env
TAXER_COOKIES=_ga=GA1.2.147289...b28852cb2da6033936efb; XSRF-TOKEN=02da4f9ff62e0f7...4e1217a; _gat=1
```
- открыть новую консоль (cmd) и запустить `docker-сompose up pytaxerapi`
В результате в консоли должна появиться строка типа такой
```log
2020-04-20 16:55:59 INFO     werkzeug              * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
```
- проверить работу: открыть в браузере http://localhost:7080/docs и попробовать прочитать учетную запись (раздел *account*)
- для завершения работы в консоли нужно нажать Ctrl-C
- В случае возникновения ошибок в консоли будут писаться сообщения. По ним в принципе можно понять что происходит

### Вручную
* Требуется установленный [Python](https://www.python.org/downloads/) 3.7 или выше вместе с установленным [virtualenv](https://virtualenv.pypa.io/en/latest/) (`pip install virtualenv`)
* Требуется установленная [Visual Studio 2019](https://visualstudio.microsoft.com/downloads/) с пакетом _MSVC v142 - VS 2019 C++ x64/x86 build tools (v14.25)_ 
* Cклонировать проект. Репозиторий можэно склонировать с помощью [Git](https://git-scm.com/download) а можно скачать в виде [zip архива](https://github.com/maxsivkov/py-taxer-api/archive/master.zip) 
    ```
    git clone https://github.com/maxsivkov/py-taxer-api.git
    ```
* Pапустить коммандную строку _x64 Native Tools Command Prompt for VS 2019_ либо _x86 Native Tools Command Prompt for VS 2019_ в зависимости от битности установленного python из `Start Menu -> Programs -> Visual Studio 2019 -> Visual Studio Tools -> VC` 
* Перейти в корень проекта
    ```bash
    cd py-taxer-api
    ```
* Устанавливаем virtualenv для проекта 
    ```bash
    virtualenv venv
    ```
* активируем 
    ```bash
    venv\Scripts\activate
    ```
* инсталируем
    ```bash
    pip install .
    ```
* устанавливаем переменную среды **TAXER_COOKIES**
    ```bash
    set TAXER_COOKIES=ga=GA1.2.147289...b28852cb2da6033936efb; XSRF-TOKEN=02da4f9ff62e0f7...4e1217a; _gat=1
    ```
* запускаем
    ```bash
    flask run --port 7080 --host=0.0.0.0 --no-reload
    ```

## Запуск с помощью username/password
В этом режиме никакие махинации с cookies не требуются, т.к. приложение с помощью [Selenium](https://www.selenium.dev/) само выполнит логин и получит cookies.
С другой стороны вы передаете в приложение свои username/password  
Решать вам.  
Итак:
- требуется установленный сам [docker](https://www.docker.com/) и [docker-compose](https://docs.docker.com/compose/install/)
- скачать файл docker-compose.yml
- создать файл `.user.env` и поместить туда переменные **TAXER_USER** и **TAXER_PWD** с содержимым. Должно получиться примерно так:
```env
TAXER_USER=username@domain.com
TAXER_PWD=mypassword
```
- открыть новую консоль (cmd) и запустить `docker-сompose up`
В результате в консоли должна появиться строка типа такой
```log
2020-04-20 16:55:59 INFO     werkzeug              * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
```
- проверить работу: открыть в браузере http://localhost:7080/docs и попробовать прочитать учетную запись (раздел *account*)
- для завершения работы в консоли нужно нажать Ctrl-C
- В случае возникновения ошибок в консоли будут писаться сообщения. По ним в принципе можно понять что происходит

### Вручную
* Требуется установленный [Python](https://www.python.org/downloads/) 3.7 или выше вместе с установленным [virtualenv](https://virtualenv.pypa.io/en/latest/) (`pip install virtualenv`)
* Требуется установленная [Visual Studio 2019](https://visualstudio.microsoft.com/downloads/) с пакетом _MSVC v142 - VS 2019 C++ x64/x86 build tools (v14.25)_ 
* Требуется установленный [Firefox Browser](https://www.mozilla.org/en-US/firefox/new/) и [gecodriver WebDriver](https://github.com/mozilla/geckodriver/releases)
* Cклонировать проект. Репозиторий можэно склонировать с помощью [Git](https://git-scm.com/download) а можно скачать в виде [zip архива](https://github.com/maxsivkov/py-taxer-api/archive/master.zip) 
    ```
    git clone https://github.com/maxsivkov/py-taxer-api.git
    ```
* Pапустить коммандную строку _x64 Native Tools Command Prompt for VS 2019_ либо _x86 Native Tools Command Prompt for VS 2019_ в зависимости от битности установленного python из `Start Menu -> Programs -> Visual Studio 2019 -> Visual Studio Tools -> VC` 
* Перейти в корень проекта
    ```bash
    cd py-taxer-api
    ```
* Устанавливаем virtualenv для проекта 
    ```bash
    virtualenv venv
    ```
* активируем 
    ```bash
    venv\Scripts\activate
    ```
* инсталируем
    ```bash
    pip install .
    ```
* устанавливаем переменные среды **TAXER_USER** и **TAXER_PWD**
    ```bash
    set TAXER_USER=username@domain.com
    set TAXER_PWD=mypassword
    ```
* запускаем
    ```bash
    flask run --port 7080 --host=0.0.0.0 --no-reload
    ```
