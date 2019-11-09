import bs4 as bs
import urllib.request
import random
import os
import re
import pandas as pd
import csv
from time import sleep
from random import randint
import fake_useragent

enable_proxy = False

# Proxy List generation --------------------------------------------------------------

ua = fake_useragent.UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

# Retrieve latest proxies
proxies_req = urllib.request.Request('https://www.sslproxies.org/')
proxies_req.add_header('User-Agent', ua.random)
proxies_doc = urllib.request.urlopen(proxies_req).read().decode('utf8')

soup = bs.BeautifulSoup(proxies_doc, 'html.parser')
proxies_table = soup.find(id='proxylisttable')

def random_proxy():
  return random.randint(0, len(proxies) - 1)

# Save proxies in the array
for row in proxies_table.tbody.find_all('tr'):
  proxies.append({
    'ip':   row.find_all('td')[0].string,
    'port': row.find_all('td')[1].string
  })

proxy_index = random_proxy()
proxy = proxies[proxy_index]

# Random user agents ----------------------------------------------------------------------
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

total_requests_made = 0
def process_url(url):
    global total_requests_made
    global proxy_index
    global proxy
    global enable_proxy
    total_requests_made += 1

    if enable_proxy:
        # Every 10 requests, generate a new proxy
        if total_requests_made % 10 == 0:
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

        for _ in range(0,4):
            try:
                user_agent = random.choice(user_agent_list)
                request = urllib.request.Request(url,headers={'User-Agent': user_agent})
                request.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
                print(proxy)
                response = urllib.request.urlopen(request)
                break
            except:
                del proxies[proxy_index]
                proxy_index = random_proxy()
                proxy = proxies[proxy_index]
    else:
        user_agent = random.choice(user_agent_list)
        request = urllib.request.Request(url,headers={'User-Agent': user_agent})
        response = urllib.request.urlopen(request)

    
    
    html = response.read()

    soup = bs.BeautifulSoup(html, 'lxml')
 
    campaign_title = soup.find('h1', {'class': ['a-campaign-title']}).text.strip()
    raised_vs_goal = soup.find('h2', {'class': ['m-progress-meter-heading']}).text.strip()
    campaign_story = soup.find('div', {'class': ['o-campaign-story']}).text.strip().replace("\n", " ")
    
    
    cover_image = soup.find('div', {'class':['a-image']}).attrs['style']
    cover_image_url = cover_image[cover_image.find("(")+1:cover_image.find(")")]

    story_images = soup.find_all('img', {'class':['not-resizable']})

    story_image_urls = [story_image.attrs['src'].strip() for story_image in story_images]
    num_story_images = len(story_image_urls)

    creation_date = soup.find('span', {'class': ['m-campaign-byline-created']}).text.strip()
    
    byline = soup.find('div', {'class': ['m-campaign-byline-description']}).text.strip()

    campaign_type = soup.find('a', {'class':['m-campaign-byline-type']}).text.strip()
    
    return (url.strip(), campaign_title.strip(), campaign_story.strip(), cover_image_url.strip(), story_image_urls, num_story_images, creation_date.strip(), byline.strip(), campaign_type.strip(), raised_vs_goal.strip())

output_file = 'out.csv'
already_scraped_urls = set()

# Populate set of already scraped urls
if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
    df = pd.read_csv(output_file)
    matrix2 = df[df.columns[0]].as_matrix()
    list2 = matrix2.tolist()
    for url in list2:
        already_scraped_urls.add(url)

print(already_scraped_urls)

urls = tuple(open('urls/9.txt', 'r'))
with open(output_file,'a', newline='') as csvfile:
        wr = csv.writer(csvfile,delimiter=',')
        for url in urls:
            if url.strip() in already_scraped_urls:
                print("URL {} was already scraped, skipping".format(url))
                continue
            else:
                print("Processing {}".format(url))

            try:
                result = process_url(url)
                wr.writerow(list(result))
            except Exception as e:
                print("Failed to process {} due to error {}".format(url, e))
            
            sleep(randint(1,3))
            # exit(0)


    
