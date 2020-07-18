from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource

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
    status=db.Column(db.Boolean)
    ip=db.Column(db.VARCHAR(15),nullable=False)
    longitude=db.Column(db.Float)
    latitude = db.Column(db.Float)

class Rank_info(db.Model):
    __tablename__ = 'rank_info'
    userid=db.Column(db.Integer,db.ForeignKey('user.userid'),primary_key=True)
    cameraid=db.Column(db.Integer,db.ForeignKey('camera.cameraid'),primary_key=True)

#测试函数
class hello_world(Resource):
    #从服务端get数据（有四个方法接口get，put，post，delete
    def get(self):
        #将数据库模型配置到数据库中
        db.create_all()
        #返回json数据
        return User.query.get(2).username
#将类函数放到相应url中
api.add_resource(hello_world,'/')


#向普通用户返回摄像头信息
class camera_map(Resource):
    #从服务端get数据（有四个接口get，put，post，delete
    def get(self,userid):
        if Rank_info.query.filter_by(userid=userid).first()!=None:

            t={
                "error_code": 0,
                "data":[

                ]
            }
            j=0
            for i in Rank_info.query.all():
                if i.userid == userid:
                    t.data["cameraid"]=userid
                    k=Camera.query.filter_by(cameraid=i.cameraid)
                    t.data["longitude"]=k.longitude
                    t.data["latitude"]=k.latitude
                    t.data["permission"]=1
                    j+=1

                return jsonify(t)

        else:
            return {"error_code": 1}

#将类函数放到相应url中
api.add_resource(camera_map,'/index/camera_map_<userid>')

if __name__ == '__main__':
    app.run(debug=True)
