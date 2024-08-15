import aiohttp
import asyncio
import json
import time
from faker import Faker

class LeakpeekController:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.isProcessing = False

        # Replace with your cookies when logged in
        self.cookie = (
            'PHPSESSID=; '
            'TawkConnectionTime=; '
            'twk_idm_key=;'
            'twk_uuid_5e0a72c07e39ea1242a266c8= '
        )
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": Faker().user_agent(),
            "Cookie": self.cookie,  # You can also use session cookies e.g session = requests.Session() / session.get(endpoint) / append session.cookies to dict
            "Referer": "https://leakpeek.com/",
            "Origin": "https://leakpeek.com/"
        }

        self.endpoints = {
            "username": [
                "https://leakpeek.com/inc/username2?t={}&input={}",
                "https://leakpeek.com/inc/iap14?id={}&query={}&t={}&input={}"
            ],
            "email": [
                "https://leakpeek.com/inc/iap6?id={}&t={}&input={}",
                "https://leakpeek.com/inc/iap14?id={}&query={}&t={}&input={}"
            ],
            "password": [
                "https://leakpeek.com/inc/passwordsearch11?id={}&t={}&input={}",
                "https://leakpeek.com/inc/passwordsearch3?t={}&input={}"
            ],
            "keyword": [
                "https://leakpeek.com/inc/keyword7?id=&query=&t=&input={}",
                "https://leakpeek.com/inc/keyword3?t={}&k={}"
            ],
            "domain": [
                "https://leakpeek.com/inc/domain5?id={}&query={}&t={}&input={}"
            ],
            "ip": [
                "https://leakpeek.com/inc/ip1?id={}&t={}&input={}"
            ],
            "name": [
                "https://leakpeek.com/inc/name1?id={}&t={}&input={}",
                "https://leakpeek.com/inc/name2?id={}&t={}&input={}"
            ],
            "hash": [
                "https://leakpeek.com/inc/hash1?id={}&t={}&input={}"
            ],
            "phone": [
                "https://leakpeek.com/inc/phone?id={}&t={}&input={}"
            ]
        }

    async def Fetch(self, content: str, timestamp: float):
        url = "https://leakpeek.com/inc/i?type={}&t={}".format(content, timestamp)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    content = await response.text()
                    data = json.loads(content)
                    return data.get('success1')
                else:
                    print(await response.text())
                    return None

    async def MakeRequests(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [session.get(url, headers=self.headers) for url in urls]
            results = await asyncio.gather(*tasks)
            joinresults = []

            for url, response in zip(urls, results):
                print("Requested URL: {}".format(url))
                if response.status == 200:
                    data = await response.text()
                    joinresults.append(json.loads(data))
                else:
                    print(await response.text())
                    joinresults.append(None)
            return joinresults

    async def GetRequest(self, option, query):
        future = asyncio.get_event_loop().create_future()
        await self.queue.put((option, query, future))
        if not self.isProcessing:
            self.isProcessing = True
            await asyncio.create_task(self.ProcessQueue())
        return await future

    async def ProcessQueue(self):
        while not self.queue.empty():
            option, query, future = await self.queue.get()
            timestamp = time.time()
            identifier = await self.Fetch(option, timestamp)
            if not identifier:
                future.set_result(None)
                self.queue.task_done()
                continue

            urls = self.construct(option, identifier, timestamp, query)
            results = await self.MakeRequests(urls)

            filtered_results = []
            for result in results:
                if result:
                    filtered_result = {k: v for k, v in result.items() if
                                       k not in ['output', 'membership', 'status', 'alert']}
                    filtered_results.append(filtered_result)
                else:
                    filtered_results.append(result)

            future.set_result(filtered_results)
            self.queue.task_done()
            await asyncio.sleep(2)

        self.isProcessing = False

    def construct(self, option, identifier, timestamp, query):
        urls = []

        if option in self.endpoints:
            for url in self.endpoints[option]:
                if 'id=' in url and 'query=' in url and 'input=' in url:
                    urls.append(url.format(identifier, query, timestamp, query))
                elif 'id=' in url and 'input=' in url:
                    urls.append(url.format(identifier, timestamp, query))
                elif 't=' in url and 'input=' in url:
                    urls.append(url.format(timestamp, query))
                elif 't=' in url and 'k=' in url:
                    urls.append(url.format(timestamp, query))
                else:
                    urls.append(url.format(identifier, timestamp, query))

        return urls


async def lookup():
    controller = LeakpeekController()
    result = await controller.GetRequest("email", "test@gmail.com")     ## Change first param to any of the endpoints, Change second param for endpoints
    print(result)


asyncio.run(lookup())
