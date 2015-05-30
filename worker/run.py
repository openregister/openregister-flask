import os
import redis

from application.registry import Register, registers

def get_config():
    from config import Config, DockerConfig
    if os.environ.get('SETTINGS') == 'config.Config':
        return Config
    else:
        return DockerConfig


def load_data(url):
    config = get_config()
    register = registers.get('address')
    if not register:
        register = Register('address',
                            config.MONGO_URI)
        registers['address'] = register

    print('loading', url)
    register.load_remote(url)


if __name__ == '__main__':
    config = get_config()
    redis_queue = redis.from_url(config.REDIS_URL)

    while True:
        load_url = redis_queue.blpop('load_url')
        load_data(load_url[1].decode('UTF-8'))
