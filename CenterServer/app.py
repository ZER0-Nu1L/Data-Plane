from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask import request
import json

#定义数据库连接地址
SQLALCHEMY_DATABASE_URI='postgresql://postgres:0222@localhost:5432/test0'
DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
#数据库对象实例化
db = SQLAlchemy(app)
#restful-api
api=Api(app)

#数据库模型
class User(db.Model):
    __tablename__ = 'user'
    userid=db.Column(db.Integer,primary_key=True)
    rank=db.Column(db.Integer,nullable=False)
    username=db.Column(db.VARCHAR(20))
    pwd=db.Column(db.VARCHAR(20),nullable=False)

class Camera(db.Model):
    __tablename__ = 'camera'
    cameraid=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.VARCHAR(10))
    ip=db.Column(db.VARCHAR(15),nullable=False)
    longitude=db.Column(db.Float)
    latitude = db.Column(db.Float)

class Rank_info(db.Model):
    __tablename__ = 'rank_info'
    userid=db.Column(db.Integer,db.ForeignKey('user.userid'),primary_key=True)
    cameraid=db.Column(db.Integer,db.ForeignKey('camera.cameraid'),primary_key=True)

#测试函数
@app.route('/')
def hello_world(Resource):
    #将数据库模型配置到数据库中
    db.create_all()
    #返回json数据
    t={
        'data':User.query.get(2).username
    }

    return jsonify(t)




#监控摄像头地图页面
@app.route('/index/camera_map_<int:userid>',methods=['GET','POST'])
def camera_map(userid):
    #向用户返回摄像头信息
    if request.method=="GET":
        #如果用户为管理员，则拥有所有监控权限
        if User.query.get(userid).rank == 1:
            t = {
                'error_code': 0,
                'data': []
            }

            for i in Camera.query.all():
                t['data'].append({
                    'cameraid':i.cameraid,
                    'longitude':i.longitude,
                    'latitude':i.latitude,
                    'permission':1
                    })
            return jsonify(t)

        #如果为普通用户则先查看有没有一个及以上摄像头权限
        if Rank_info.query.filter_by(userid=userid).first()!=None:
            t={
                'error_code': 0,
                'data':[]
            }

            for i in Camera.query.all():
                #如果在rank_info表里有该用户的行数据，则有相应权限
                if Rank_info.query.get((userid,i.cameraid))!=None :
                    t['data'].append({
                        'cameraid':i.cameraid,
                        'longitude':i.longitude,
                        'latitude':i.latitude,
                        'permission':1
                    })
                else:
                    t['data'].append({
                        'cameraid': i.cameraid,
                        'longitude': i.longitude,
                        'latitude': i.latitude,
                        'permission': 0
                    })
            return jsonify(t)

        else:
            return {"error_code": 1}

    #用户向server请求直播或录像视频
    if request.method=="POST":
        if request.form.get('type')=='live':


            #code
            return 'a'
        elif request.form.get('type')=='video':
            #code
            return {'a':'b'}


if __name__ == '__main__':
    app.run(debug=True)
