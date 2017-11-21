from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow,
            onupdate=datetime.utcnow)


# 用户表
class User(Base):
    __tablename__ = 'user'

    ROLE_USER = 10

    ROlE_COMPAMY = 20

    ROLE_ADMIN = 30
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger)
    sex = db.Column(db.String(16))
    age = db.Column(db.SmallInteger)
    # 简历url
    resume_url = db.Column(db.String(256))
    # 投递信息表ID
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', uselist=False)

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


# 投递信息表
class Delivery(Base):
    __tablename__ = 'delivery'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', uselist=False)
    company = db.Column(db.String(64), nullable=False)
    job = db.Column(db.String(32), unique=True, nullable=False)


# 企业表
class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(256))
    name = db.Column(db.String(64), nullable=False)
    # 企业网站
    website = db.Column(db.String(128), nullable=False)
    # 地址
    address = db.Column(db.String(128), nullable=False)
    # 一句话介绍
    brief_introduction = db.Column(db.String(128))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    # 招牌职位数量
    job_num = db.Column(db.Integer, nullable=False)
    # 企业详细介绍
    detailed_introduction = db.Column(db.Text)
    # 在招职位
    recruit_job = db.relationship('Job')

    def __repr__(self):
        return '<Company:{}>'.format(slef.name)


# 职位表
class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    # 职位描述
    describe = db.Column(db.String(256))
    # 职位要求
    requirement = db.Column(db.Text, nullable=False)
    # 薪水范围
    salary = db.Column(db.String(32), nullable=False)
    # 经验要求
    experience_requirement = db.Column(db.String(32), nullable=False)
    # 面试地点
    adress = db.Column(db.String(128), nullable=False)
    company = db.relationship('Company', uselist=False)
    # 公司信息
    company_info = db.Column(db.Text)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)
