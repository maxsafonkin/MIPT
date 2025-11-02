import os
import typing as t
from http import HTTPMethod, HTTPStatus
from functools import wraps

import httpx

P = t.ParamSpec("P")
T = t.TypeVar("T")


class ModuleError(Exception):
    pass


class NetworkError(ModuleError):
    pass


class WrongStatusCodeError(ModuleError):
    def __init__(self, code: int):
        self.code = code
        super().__init__(f"Wrong status code: {code}")


def handle_httpx_errors(function: t.Callable[P, T]) -> t.Callable[P, T]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return function(*args, **kwargs)
        except httpx.HTTPError as exc:
            raise NetworkError(str(exc)) from exc

    return wrapper


@handle_httpx_errors
def send_request(
    method: HTTPMethod,
    url: str,
    params: dict | None = None,
    headers: dict | None = None,
    payload: dict | None = None,
    content: bytes | None = None,
) -> httpx.Response:
    response = httpx.request(
        method=str(method),
        url=url,
        params=params,
        headers=headers,
        json=payload,
        content=content,
    )

    if (code := response.status_code) not in (
        HTTPStatus.OK,
        HTTPStatus.CREATED,
        HTTPStatus.ACCEPTED,
    ):
        raise WrongStatusCodeError(code=code)

    return response


def task_1():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = send_request(method=HTTPMethod.GET, url=url)

    posts = response.json()

    for post in posts[:5]:
        print(f"Title: `{post['title']}`, body: `{post['body']}`")


def _get_weather(city: str, api_key: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key}
    response = send_request(HTTPMethod.GET, url=url, params=params)
    payload = response.json()

    temp_K = payload["main"]["temp"]
    temp_C = round(temp_K - 273.15, 2)

    description = payload["weather"][0]["description"]

    return {"temp": temp_C, "description": description}


def task_2():
    api_key = os.environ["OPENWEATHER_API_KEY"]
    city = input("Type the city: ")

    weather = _get_weather(city=city, api_key=api_key)
    print(weather)


def task_3():
    url = "https://jsonplaceholder.typicode.com/posts"

    payload = {"title": "Post title", "body": "Post body", "userId": 777}
    response = send_request(method=HTTPMethod.POST, url=url, payload=payload)
    created_post = response.json()

    print(created_post)


def _handle_wrong_status_code(code: int) -> None:
    match code:
        case HTTPStatus.BAD_REQUEST:
            print("Invalid city name")
        case HTTPStatus.UNAUTHORIZED:
            print("Invalid API key")
        case HTTPStatus.NOT_FOUND:
            print("Couldn't find any weather data for city")
        case _:
            print(f"Unexpected status code: {code}")


def task_4():
    try:
        task_2()
    except WrongStatusCodeError as exc:
        _handle_wrong_status_code(code=exc.code)


def main():
    task_1()
    task_2()
    task_3()
    task_4()


if __name__ == "__main__":
    main()
