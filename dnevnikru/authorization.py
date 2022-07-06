from time import sleep
from typing import Optional

import requests
from playwright.sync_api import sync_playwright
from pydantic import ValidationError

from dnevnikru import consts
from dnevnikru.exceptions import DnevnikError
from dnevnikru.models import LoginData, UserData


# Создание сессии по логину и паролю от dnevnik.ru
def create_session(user_data: dict):
    session = requests.Session()
    session.headers.update(consts.USER_AGENT)
    session.post('https://login.dnevnik.ru/login',
                 data=user_data)
    if session.cookies.get("t0"):
        school = session.cookies.get("t0")
        return session, UserData(**user_data, school=school)
    raise DnevnikError(message="Error", errors="Error")


# Создание сессии по логину и паролю от Госуслуг
def create_session_gosuslugi(login_data: LoginData, region: str):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(region)
        sleep(0.3)
        page.click("a.login__pubservices-link:nth-child(1)")
        page.fill("#login", login_data.login)
        page.fill("#password", login_data.password)
        sleep(0.3)
        page.click("#loginByPwdButton")
        # здесь должна быть дополнительная проверка на 2FA ответ, нужна помощь в получении нужных полей,
        # так как нет аккаунта!
        cookies = page.context.cookies()
        if "DnevnikAuth_a" in [c["name"] for c in cookies]:
            school = [c["value"] for c in cookies if c["name"] == "t0"][0]
            browser.close()
            session = requests.Session()
            session.headers.update(consts.USER_AGENT)
            session.cookies.update(cookies)
            return session, UserData(school=school, **login_data.dict())
        browser.close()
        raise DnevnikError("Auth error", "error")


# Валидация данных и создание сессии
def auth(login: str, password: str, region: Optional[str]):
    try:
        login_data = LoginData(login=login, password=password, region=region).dict()
    except ValidationError as e:
        raise DnevnikError(e.errors(), 'Error')
    else:
        if not region:
            return create_session(login_data)
        if region:
            return create_session_gosuslugi(LoginData(**login_data), region)
