from multiprocessing import cpu_count
from os import environ

def max_workers():
    return (2 * cpu_count()) + 1

bind = '0.0.0.0:%s' % environ.get('PORT', '8000')
workers = max_workers()
