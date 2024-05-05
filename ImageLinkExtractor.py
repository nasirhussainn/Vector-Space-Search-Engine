import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class WebCrawler:
    def __init__(self, seed_url, max_pages=1000, output_file='image_urls.txt'):
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.output_file = output_file
        self.visited_urls = set()
        self.pages_crawled = 0

    def crawl(self, url):
        if self.pages_crawled >= self.max_pages:
            return

        if url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.visited_urls.add(url)
                self.pages_crawled += 1

                # Parse HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract image URLs
                image_tags = soup.find_all('img')
                image_urls = [img['src'] for img in image_tags]

                # Save image URLs to file
                with open(self.output_file, 'a') as f:
                    f.write(','.join(image_urls) + '\n')

                print(f"Crawled: {url}")

                # Find links on the page and crawl them
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    self.crawl(next_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def start_crawl(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        self.crawl(self.seed_url)

# Example usage
if __name__ == "__main__":
    seed_url = "https://developers.google.com"
    crawler = WebCrawler(seed_url)
    crawler.start_crawl()
