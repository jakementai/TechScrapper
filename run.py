

import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# run this for normal crawl
try:
    execute(
        [
            'scrapy',
            'crawl',
            'TomHwSpiderHub',
        ]
    )

# run this for pause and resume
# scrapy crawl TomHwSpider -s JOBDIR='files/crawler data/crawl-2'
# try:
#     execute(
#         [
#             'scrapy',
#             'crawl',
#             'TomHwSpider',
#             '-s',
#             'JOBDIR=files/crawler data/crawl-1'
#         ]
#     )
except SystemExit:
    pass
