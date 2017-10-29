import crawler
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simple web crawler.')
    parser.add_argument('url', help='URL to crawl')
    parser.add_argument('depth', type=int, help='Depth to crawl')

    args = parser.parse_args()

    crawler = crawler.Crawler(args.url, args.depth)
    crawler.crawl()
