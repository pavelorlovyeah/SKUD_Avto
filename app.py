from pickle import GET
from flask import Flask, redirect, render_template, session, request, redirect, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cv2
import os
from PIL import Image
from model_car_type.yolo_detector import detect_car_type, show_result
from detect_model import detect_number
from functions.translitter import translitter
from config import login_admin, password_admin
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poskudavto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    plates = db.Column(db.String(10), nullable=False)
    fio = db.Column(db.String(40), nullable=False)
    room = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Car> %r' % self.id

class Log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    plates = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime(30), default=datetime.now)
    
    def __repr__(self):
        return '<Log> %r' % self.id

db.create_all()

camera = cv2.VideoCapture(2)
if camera.isOpened() == False:
    camera = cv2.VideoCapture(0)

'''
for creating db - type in terminal:
    >>> python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
'''

images_dir = './Images/'

def gen_frames():
    file_count = 0
    try:
        last_log = Log.query.order_by(Log.date).all()[-1].date
    except:
        last_log = datetime.now()
    log_time_wait = 10
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            file_count += 1
            if file_count % 90 == 0:
                frame_rgb = frame[:,:,::-1]
                pil_img = Image.fromarray(frame_rgb)
                log_time = str(datetime.now())[:-7]
                pil_img.save(f'./Images/{log_time}.jpg')

                car_type = detect_car_type(f'./Images/{log_time}.jpg')

                if car_type in ['Полиция', 'Скорая помощь', 'Пожарная']:
                    print(f'{car_type} подьехала!')

                    delta_1 = (datetime.now() - last_log).total_seconds()
                    if delta_1 > log_time_wait:
                        log = Log(plates=car_type)
                        try:
                            db.session.add(log)
                            db.session.commit()
                            last_log = datetime.now()
                        except:
                            return 'Произошла ошибка при добавлении в базу данных'
                    else:
                        print(f'Такой лог уже есть, подождите: {log_time_wait - delta_1}')

                elif car_type == 'Обычная':
                    print('Обычная машина подьехала!')
                    number = detect_number(f'Images/{log_time}.jpg')
                    if number:
                        number = translitter(number[0])
                        print('Считанный номер: ', number)
                        delta_2 = (datetime.now() - last_log).total_seconds()
                        if delta_2 > log_time_wait:
                            check_plates(number)
                            last_log = datetime.now()
                        else:
                            print(f'Такой лог уже есть, подождите: {log_time_wait - delta_2}')
                    else:
                        print('Нет номера')

                else:
                    print('Нет машины')

                # очищаем базу хранилище фоток
                if len(os.listdir(images_dir)) >= 20:
                    for file in os.listdir(images_dir):
                        os.remove(images_dir + file)
                print('-'*15)

            # real time type detection block
            # frame_rgb = frame[:,:,::-1]
            # pil_img = Image.fromarray(frame_rgb)
            # new_frame = show_result(pil_img)[:,:,::-1]

            _, buffer = cv2.imencode('.jpg', frame)
            
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def check_plates(input_plates):
    all_plates = Car.query.order_by(Car.plates).all()
    for el in all_plates:
        if el.plates == input_plates:
            print('Номер в базе данных')
            plates = el.plates
            log = Log(plates=plates)
            try:
                db.session.add(log)
                db.session.commit()
            except:
                return 'Произошла ошибка при добавлении в базу данных'

@app.route('/')
def index():
    return render_template("index.html", query = False)

@app.route('/monitoring')
def monitoring():
    return render_template("monitoring.html")

@app.route('/signin', methods=['POST'])
def sing_in():
    if request.method == 'POST':
        login_input = request.form['login']
        password_input = request.form['password']
        if login_input == login_admin and password_input == password_admin:
            return render_template('monitoring.html')
        else:
            return render_template("index.html", query = True)

@app.route('/_stuff', methods = ['GET'])
def stuff():
    query = '○○○ Шлагбаум Закрыт ○○○'
    try:
        last_date = Log.query.order_by(Log.date).all()[-1].date
        last_plate = f'Автомобиль: {str(Log.query.order_by(Log.date).all()[-1].plates)}'
        last_date_txt = f'Дата: {str(last_date)[:-7]}'
        # last_log = f'Автомобиль: {last_plate} Дата: {str(last_date)[:-7]}'
        delta_3 = (datetime.now() - last_date).total_seconds()
        if delta_3 < 10:
            query = '●●● Шлагбаум Открыт ●●●'
    except:
        last_plate = 'Еще никто не вьезжал'
        last_date_txt = 'Давно'
        # last_log = 'Еще никто не вьезжал'
    return jsonify(last_plate=last_plate, last_date=last_date_txt, query=query) 

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cars')
def cars():
    all_cars = Car.query.order_by(Car.plates).all()
    return render_template("cars.html", all_cars=all_cars)

@app.route('/cars/<int:id>/delete')
def car_delete(id):
    car = Car.query.get_or_404(id)
    
    try:
        db.session.delete(car)
        db.session.commit()
        return redirect('/cars')
    except:
        return 'Произошла ошибка при удалении из базы данных'

@app.route('/cars/<int:id>/edit', methods=['POST', 'GET'])
def car_edit(id):
    if request.method == 'POST':
        car_old = Car.query.get_or_404(id)
        plates = request.form['plates'].upper()
        fio = request.form['fio']
        room = request.form['room']
        phone = request.form['phone']

        car = Car(plates=plates, fio=fio, room=room, phone=phone)

        try:
            db.session.delete(car_old)
            db.session.add(car)
            db.session.commit()
            return redirect('/cars')
        except:
            return 'Произошла ошибка при сохранении изменений в базу данных'
    else:
        car = Car.query.get_or_404(id)
        return render_template('edit.html', car=car)
    
@app.route('/logs')
def logs():
    all_logs = Log.query.order_by(Log.date.desc()).all()
    all_logs = [(x.plates, str(x.date)[:-7]) for x in all_logs]
    return render_template("logs.html", all_logs=all_logs)

@app.route('/requests')
def requests():
    with open('request_list.json') as json_file:
        data = json.load(json_file)
    all_requests = data
    return render_template("requests.html", all_requests=all_requests)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        plates = request.form['plates'].upper()
        fio = request.form['fio']
        room = request.form['room']
        phone = request.form['phone']

        car = Car(plates=plates, fio=fio, room=room, phone=phone)

        try:
            db.session.add(car)
            db.session.commit()
            return redirect('/cars')
        except:
            return 'Произошла ошибка при добавлении в базу данных'
    else:
        return render_template('add.html')
