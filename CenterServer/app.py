from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json

#定义数据库连接地址
SQLALCHEMY_DATABASE_URI='postgresql://postgres:0222@localhost:5432/test0'
DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['JSON_AS_ASCII'] = False #防止返回的json中文乱码
#数据库对象实例化
db = SQLAlchemy(app)

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
@app.route('/',methods=["POST"])
def hello_world():
    #将数据库模型配置到数据库中
    db.create_all()
    #返回json数据
    data=request.data
    jd=json.loads(data)
    return jsonify({'error_code':jd['userid']})




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
        data = request.data
        Json = json.loads(data)
        if Json['type']=='live':
            #code
            return jsonify({'a':1})
        elif Json['type']=='video':
            #code
            return jsonify({'a':2})


#向管理员返回设备和普通用户信息并提供权限编辑服务
@app.route('/index/equ_user',methods=['GET','POST'])
def equ_user():
    #返回设备及用户权限信息
    if request.method=="GET":
        t={
            'error_code': 0,
            'camera':[],
            'user':[]
        }
        for i in Camera.query.all():
            t['camera'].append({
                'cameraid':i.cameraid,
                'type':i.type,
                'longitude': i.longitude,
                'latitude': i.latitude
            })
        for i in User.query.all():
            if i.rank==2:
                j={
                    'userid':i.userid,
                    'username':i.username,
                    'rank':2,
                    'cameraids':[]
                }
                for k in Rank_info.query.filter_by(userid=i.userid):
                    j['cameraids'].append(k.cameraid)
                t['user'].append(j)
            else:
                t['user'].append({
                    'userid': i.userid,
                    'username': i.username,
                    'rank': 1
                })
        return jsonify(t)

    #根据管理员的请求更改普通用户的权限，
    if request.method=="POST":
        data=request.data
        Json=json.loads(data)
        userid=Json['userid']
        if User.query.get(userid).rank == 2:
            if Json['add']:
                add = Json['add']
                for i in add:
                    db.session.add(Rank_info(userid=userid,cameraid=i))
            if Json['reduce']:
                reduce = Json['reduce']
                for i in reduce:
                    db.session.delete(Rank_info.query.get((userid,i)))
            if Json['update']:
                update=Json['update']
                for i in update:
                    Rank_info.query.get((userid,i[0])).cameraid=i[1]
            db.session.commit()
            return jsonify({'error_code':0})

        else:
            return jsonify({'error_code':1})



if __name__ == '__main__':
    app.run(debug=True)
