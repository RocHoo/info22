from redis import StrictRedis


class Config:
    DEBUG=None
    SECRET_KEY = 'pr2fPX72RfUAMJEMA+u7pUILxC9CYcjFUY9JiPjA3111hKkETyZiYw=='
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost/info22'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'
    REDIS_HOST='127.0.0.1'
    REDIS_PORT=6379
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SINGER = True
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

config_dict={
    'development':DevelopmentConfig,
    'production':ProductionConfig
}