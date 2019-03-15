from flask import json
import requests
from modules.sentiment import SentimentAnalysis


class Wikipedia:

    def __init__(self):

        self.proxy = self._get_proxy()
        self.neg_count = 0
        self.neu_count = 0
        self.pos_count = 0
        self.obj = SentimentAnalysis()
        self.api_base = 'https://en.wikipedia.org/w/api.php?'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

    def _get_proxy(self):
        url = "http://credsnproxy/api/v1/proxy"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            return {"proxy_host": '103.59.95.71',
                    "proxy_port": '23344'}

    def search(self, query, limit):

        # https://en.wikipedia.org/w/api.php?action=opensearch&search=apple&limit=200
        api_url = self.api_base+'action=opensearch&format=json&search='+query+'&limit='+str(limit)

        response = requests.get(api_url, headers=self.headers, proxies={"http": "socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']})
        data = json.loads(response.content.decode('utf-8'))
        # print(data)

        if response.status_code == 200:
            k = []
            l = len(data[1])
            if l != 0:
                a, b, c = data[1], data[2], data[3]
                for i in range(l):
                    new_dict = dict()
                    new_dict['title'] = a[i]
                    new_dict['content'] = b[i]
                    if not new_dict['content']:
                        new_dict['content'] = None

                    new_dict['url'] = c[i]
                    new_dict['type'] = 'link'

                    pol = self.obj.analize_sentiment(b[i])
                    new_dict['polarity'] = pol
                    # k.append({'post_title': a[i], 'post_content': b[i], 'post_url': c[i]})
                    k.append(new_dict)

                    if pol == 1:
                        new_dict['polarity'] = 'positive'
                        self.pos_count += 1
                    elif pol == -1:
                        new_dict['polarity'] = 'negative'
                        self.neg_count += 1
                    else:
                        new_dict['polarity'] = 'neutral'
                        self.neu_count += 1

            else:
                k = None

            ps = self.pos_count
            ng = self.neg_count
            nu = self.neu_count

            sentiments = dict()
            sentiments["positive"] = ps
            sentiments["negative"] = ng
            sentiments["neutral"] = nu

            # return {
            #     'data': {
            #             'results': k,
            #             'total': len(k),
            #             'sentiments': Sentiments
            #         }
            #     }
            return {'data': k}
        else:
            return None


if __name__ == "__main__":
    obj = Wikipedia()
    print(obj.search("donald trump", 60))

# donald trump