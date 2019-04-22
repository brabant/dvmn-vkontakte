# Обрезка ссылок с помощью Битли

Скрипт публикует случайный комикс с сайта  [xkcd.com](https://xkcd.com/) на стене группы вКонтакте

### Как установить

После клонирования проекта создайте в корень файл .env с таким содержимым:

```
VK_GROUP_ID=Идентификатор группы VK
VK_ACCESS_TOKEN=Ключ доступа к api.vk.com```

### Как получить Access Token VK
https://oauth.vk.com/authorize?client_id=6953420&display=page&scope=photos,groups,wall&response_type=token&v=5.95&state=123456
* Создайте группу Вконтакте - [Управление группами](https://vk.com/groups?tab=admin)
* Получите group_id - (в адресной строке цифры после слова public) и вставьте его в .env
* Создайте standalone-приложение Вконтакте - [Мои приложения](https://vk.com/dev)
* Получите client_id созданного приложения (если нажать на кнопку "Редактировать" для нового приложения, в адресной строке вы увидите его client_id)
* Получите личный ключ [Процендура Implicit Flow](https://vk.com/dev/implicit_flow_user), сформируйте ссылку для получения ключа в браузере (вам понадобятся права photos,groups,wall) или просто поправьте эту https://oauth.vk.com/authorize?client_id=_______&display=page&scope=photos,groups,wall&response_type=token&v=5.95&state=123456
* Перейдите по ссылке выше, VK перенаправит вас на другую страницу, это нормально 
* Скопируйте access_token из адресной строки браузера и вставьте в .env 

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример запуска
```
python main.py
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).