from gevent import monkey
monkey.patch_all()

import json
import codecs
import logging
from gevent.pool import Pool
from master import Master
from server import Server

MASTER_SERVER = ('hl2master.steampowered.com', 27011)

APPIDS = [
    20, # tfc
    30, # dod
    40, # dmc
    50, # gearbox
    60, # ricochet
    70, # halflife
    130, # bshift
    225840, # svencoop
    223710, # cryoffear
]

def fetch_server(addr):
    info = {}
    server = Server(addr)
    try:
        info = server.get_info()
    except:
        pass
    if info and info['hostname']:
        info['address'] = '%s:%d' % addr
        if info['numplayers']:
            try:
                info['players'] = server.get_players()
            except:
                info['players'] = []
        logging.info(info['address'])
        return info
    return None

def main():
    pool = Pool(size=100)
    greenlets = []
    master = Master(MASTER_SERVER)
    for appid in APPIDS:
        for addr in master.get_servers(appid=appid):
            greenlets.append(pool.spawn(fetch_server, addr))
    greenlets = [greenlet.get() for greenlet in greenlets]
    servers = sorted(filter(None, greenlets), key=lambda x: (x['gamedir'], x['hostname'].lower()))
    with codecs.open('servers.json', 'w', 'utf8') as f:
        f.write(json.dumps(servers))
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()