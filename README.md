# SKUD Avto

## Видеопрезентация работы системы
![Image alt](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/static/readme/img_6.png)

https://youtu.be/_NTpVR3EmIg


## Installation
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
6. If you want to change user login, password or telegram bot token, edit [config.py](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/config.py)

#### Optionally

7. If you want to run telegram bot you need in another terminal window run [bot.py](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/bot.py) (don't forget insert bot token from BotFather in [config.py](https://github.com/pavelorlovyeah/SKUD_Avto/blob/master/config.py))
```bash
python3 bot.py
```
