import json
import looter as lt
from concurrent import futures
from operator import itemgetter

domain = 'https://github.com/tuna/blogroll/blob/master/README.md'
total_rank = []

def get_tasklist(url):
    src = lt.get_source(url)
    links = src.cssselect('table tbody tr td:nth-child(3) a')
    return [link.get('href') for link in links]


def crawl(url):
    rank = lt.get_alexa_rank(url)
    if rank:
        data = {}
        data['site'] = rank[0]
        data['reach'] = int(rank[1])
        data['popularity'] = int(rank[2])
        total_rank.append(data)


if __name__ == '__main__':
    tasklist = get_tasklist(domain)
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    r = sorted(total_rank, key=itemgetter('popularity'))
    with open('blogRank.json', 'w') as f:
        f.write(json.dumps(r))