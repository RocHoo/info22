from . import passport_blue

from flask import request,jsonify,current_app,make_response

from info.utils.response_code import RET

from info.utils.captcha.captcha import captcha

from info import redis_store,constants

import re,random

from info.libs.yuntongxun import sms

@passport_blue.route('/image_code')
def generate_image_code():
    image_code_id=request.args.get('image_code_id')
    if not image_code_id:
        return jsonify(errno=RET.PARAMERR,errmsg='参数缺失')
    name,text,image=captcha.generate_captcha()
    try:
        redis_store.setex('ImageCode_'+image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存数据失败')
    response=make_response(image)
    response.headers['Content-Type']='image/jpg'
    return response
@passport_blue.route('/sms_code',methods=['POST'])
def send_sms_code():
    mobile=request.json.get('mobile')
    image_code=request.json.get('image_code')
    image_code_id=request.json.get('image_code_id')
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数错误')
    if not re.match(r'1[3456789]\d{9}$',mobile):
        return jsonify(errno=RET.PARAMERR,errmsg='手机号格式错误')
    try:
        real_image_code=redis_store.get('ImageCode_'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='获取数据失败')
    if not real_image_code:
        return jsonify(errno=RET.NODATA,errmsg='数据已过期')
    try:
        redis_store.delete('ImageCode_'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    if real_image_code != image_code:
        return jsonify(errno=RET.DATAERR,errmsg='图片验证码错误')
    sms_code='%06d'%random.randint(0,999999)
    try:
        redis_store.setex('SMSCode_'+mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存短信验证码失败')
    try:
        ccp=CCP()
        result=ccp.send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg='发送短信异常')
    if result==0:
        return jsonify(errno=RET.OK,errmsg='发送成功')
    else:
        return jsonify(errno=RET.THIRDERR,errmsg='发送失败')
