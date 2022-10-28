# SKUD Avto
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_7.png)

Система контроля и управления доступом для автомобилей, с определением номеров и классификацией машин.

# Описание проекта
Система предназначена для детекции и распознавания номеров обычных автомобилей, а также детекции автомобилей специального назначения (скорая, пожарная, полиция).
Если к шлагбауму подъезжает обычный автомобиль, то система сверяет номер машины с его наличием в базе данных и предоставляет доступ при нахождении номера.
При детекции спецавтотранспорта доступ предоставляется минуя базу данных с номерами.

### Видеопрезентация работы системы
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_6.png)

https://youtu.be/_NTpVR3EmIg

# Стек
- Разпознавание автомобилей и номеров - нейросети YOLO (детекция и классификация) и ResNet18 (распознавание номера). Работает достаточно точно и быстро.
- База данных - SQLite, SQLAlchemy.
- Управление системы - сервер  на Flask:
  * Вход по логину и паролю.
  * Просмотр видеопотока с камеры в режиме real-time.
  * Просмотр текущих номеров в базе данных, а также редактирование и удаление.
  * Просмотр логов со всеми вьездами.
  * Активные заявки на добавление новых номеров, получаемые из телеграм бота.
- В качестве источника сигнала можно использовать любое устройство видеозахвата (ip-камера, веб-камера, видеозапись)
- Telegram Bot для приема заявок

# Слайды с работой проекта
![Иллюстрация к проекту](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_2.png)

## Архитектура
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_3.png)

## Нейросети
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_4.png)

## Интерфейс
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_5.png)

## Telegram Bot
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_8.png)

# Installation
1. Clone Project
```bash
git clone git@github.com:pavelorlovyeah/SKUD_Avto.git
cd SKUD_Avto
```
2. Create env via conda with Python 3.7
```bash
conda create -n SKUD_Avto_Env python=3.7
```
3. Install requirements_pavel.txt
```bash
pip install -r requirements_pavel.txt
```
4. Models checkpoints
[model.zip](https://drive.google.com/drive/folders/1oWJkOWIZlKSHBMND4An9UUTg4jEGXund?usp=sharing) 
must be downloaded and unzipped in [data](https://github.com/pavelorlovyeah/SKUD_Avto/tree/master/data) folder on local machine
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_1.png)

5. Start project with run.py
```bash
python3 run.py
```

#### Optionally

6. If you want to change user login, password or telegram bot token, edit [config.py](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/config.py)

7. If you want to run telegram bot you need in another terminal window run [bot.py](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/bot.py) (don't forget insert bot token from BotFather in [config.py](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/config.py))
```bash
python3 bot.py
```
 ### Dataset
 [dataset.zip](https://drive.google.com/drive/folders/1oWJkOWIZlKSHBMND4An9UUTg4jEGXund?usp=sharing) 
 
 ### The project was developed by:
- Pavel Orlov https://github.com/pavelorlovyeah
- Igor Polubarev https://github.com/polubarev
- Leonid Shturmin
- Sergei Zhitar https://github.com/Sjitar
