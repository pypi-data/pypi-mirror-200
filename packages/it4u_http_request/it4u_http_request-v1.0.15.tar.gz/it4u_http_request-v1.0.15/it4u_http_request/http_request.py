import requests
import logging
import os
import pickle
import reactivex as rx
from reactivex import Observable
from reactivex import operators as ops
from typing import Dict, Any, Callable, List, Tuple

class Url:
    def __init__(self, url: str, method: str = "GET", params: Dict[str, Any] = None, json: Dict[str, Any] = None) -> None:
        self.url: str = url
        self.method: str = method
        self.params: Dict[str, Any] = params
        self.json: Dict[str, Any] = json

class HttpRequest:
    def __init__(self, 
                 cache_key_calculator: Callable[[str, str, Dict[str, Any], Dict[str, Any], Dict[str, str]], str], 
                 session_builder: Callable[[], requests.Session] = lambda: requests.Session(),
                 headers: Dict[str, str] = None):
        self.session_builder: Callable[[], requests.Session] = session_builder
        self.cache_key_calculator = cache_key_calculator
        self.cache: Dict[Any, str] = {}
        self.headers: Dict[str, str] = headers

    def get_response_stream(self, 
                            url: Url, 
                            pipes: List[Observable] = [], 
                            headers: Dict[str, str] = None, 
                            allow_redirects: bool = True, 
                            timeout: int = 5, 
                            verify: bool = False, 
                            max_retries: int = 3, 
                            proxy_builder: Callable[[], Dict[str, str]]=None
                            ) -> Tuple[Url, Any]:
        headers = headers or self.headers
        cache_key = self.cache_key_calculator(url.url, url.method, url.params, url.json, headers)
        if cache_key in self.cache:
            logging.info(f"Getting response from cache for URL: {url}")
            return url, rx.of(self.cache[cache_key]) \
                    .pipe(*pipes) \
                    .run()

        logging.info(f"Making a request to URL: {url.url}")
        retries = 0
        while retries < max_retries:
            try:
                response = self.session_builder().request(
                    url.method, 
                    url.url, 
                    headers=headers, 
                    json=url.json, 
                    params=url.params, 
                    allow_redirects=allow_redirects, 
                    timeout=timeout, 
                    verify=verify, 
                    proxies=proxy_builder() if proxy_builder is not None else None, 
                    stream=False
                )

                self.cache[cache_key] = response.text

                return url, rx.of(self.cache[cache_key]) \
                    .pipe(*pipes) \
                    .run()
            except Exception as e:
                logging.warning(f"Request to URL {url.url} failed: {e}. Retrying...")
                retries += 1

        raise Exception(f"Failed to get response from URL {url.url} after {max_retries} retries")
    
    def get_responses_stream(self, 
                             urls: List[Url], 
                             pipes: List[Observable] = [], 
                             headers: Dict[str, str] = None, 
                             allow_redirects: bool = True, 
                             timeout: int = 5, 
                             verify: bool = False, 
                             max_retries: int = 3, 
                             proxy_builder: Callable[[], Dict[str, str]]=None
                             ) -> List[Tuple[Url, Any]]:
        responses = []
        for url in urls:
            try:
                response = self.get_response_stream(url=url, 
                                        pipes=[],
                                        headers=headers,
                                        allow_redirects=allow_redirects,
                                        timeout=timeout,
                                        verify=verify,
                                        max_retries=max_retries,
                                        proxy_builder=proxy_builder)
                
                logging.info("Crawled data from: %s", url.url)
                responses.append(response)
            except Exception as e:
                logging.error("Error crawling data from: %s, %s", url.url, e)
        return rx.of(responses) \
                    .pipe(*pipes) \
                    .run()

    def store_cache(self, file_path: str):
        with open(file_path, "wb") as cache_file:
            pickle.dump(self.cache, cache_file)

    def load_cache(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "rb") as cache_file:
                self.cache = pickle.load(cache_file)

    def clear_cache_by_key(self, cache_key: str):
        if cache_key in self.cache:
            del self.cache[cache_key]

    def clear_cache_by_url(self, url: str):
        cache_keys = [k for k, v in self.cache.items() if v.url == url]
        for key in cache_keys:
            del self.cache[key]

    def clear_all_cache(self):
        self.cache.clear()



def default_cache_key_calculator(url: str, method: str, params: Dict[str, Any], json: Dict[str, Any], headers: Dict[str, str]) -> str:
    return (url, method, str(params), str(json), str(headers))


default_headers: Dict[str, str] = {}
default_headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
default_headers["Accept-Language"] = "en-US,en;q=0.8"
default_headers["Connection"] = "keep-alive"



proxies = [
    { "http": "27.64.192.178:4001" },
    { "http": "116.96.74.167:4002" },
    { "http": "202.151.163.10:1080" },
    { "http": "61.28.224.211:3128" },
    { "http": "221.132.18.26:8090" },
    { "http": "27.74.243.242:5678" },
    { "http": "27.79.167.117:4001" },
    { "http": "117.4.242.216:5678" },
    { "http": "203.210.235.91:5678" },
    { "http": "113.162.84.219:1080" },
    { "http": "116.98.224.19:10003" },
    { "http": "113.161.131.43:80" },
    { "http": "113.161.254.4:1080" },
    { "http": "221.121.12.238:47012" },
    { "http": "116.118.98.5:5678" },
    { "http": "116.118.98.25:5678" },
    { "http": "14.187.141.43:19132" },
    { "http": "171.241.42.190:5203" },
    { "http": "14.241.39.165:19132" },
    { "http": "14.232.163.52:10801" },
    { "http": "27.76.232.171:4001" },
    { "http": "14.177.236.212:55443" },
    { "http": "113.176.195.145:4153" },
    { "http": "27.72.104.89:8080" },
    { "http": "171.247.151.99:4003" },
    { "http": "171.244.68.28:5678" },
    { "http": "27.73.175.178:4001" },
    { "http": "115.72.172.155:8080" },
    { "http": "113.162.84.218:1080" },
    { "http": "113.160.159.160:19132" },
    { "http": "113.160.227.32:1080" },
    { "http": "116.111.117.53:3333" },
    { "http": "116.107.251.134:3333" },
    { "http": "113.160.247.27:19132" },
    { "http": "14.241.111.38:8080" }
]

