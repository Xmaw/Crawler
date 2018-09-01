from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib

word = input("What word do you want to find?")
print(len(word))
print(str(word))
start_url = 'https://en.wikipedia.org'
client = urlopen(start_url)
page = client.read()
client.close()
soup = BeautifulSoup(page, "html.parser")
a = soup.findAll("a", {"": ""})

print("----------Getting Initial Seeds------------")
seed = []
for element in a:
    if element.has_attr('href'):
        if element.has_attr('href'):
            if 'media' in element['href']:
                pass
            elif element['href'].startswith('//'):
                pass
            elif 'Wikipedia:' in element['href']:
                pass
            elif 'mobileaction=' in element['href']:
                pass
            elif str(element['href']) in seed:
                pass
            elif ('.org' or '.com' or '.se' or '.net') in element['href']:
                seed.append(element['href'])
            else:
                seed.append(start_url + element['href'])

print("----------Looking for word in paragraphs------------")
crawl_max = 50
index = 0
crawl_layer = 0
while len(seed) > 0:
    flag_break = False
    print(crawl_layer, len(seed))
    try:
        l = len(seed)
        seed_url = seed[len(seed)-1]
        print(seed_url)
        crawl_layer += 1
        client = urlopen(seed_url)
        page1 = client.read()
        client.close()
        soup1 = BeautifulSoup(page1, "html.parser")
        paragraph = soup1.findAll("p", {"": ""})
        for para in paragraph:
            words = para.text.split(" ")
            for text in words:
                if word == text:
                    print("SUCCESS, word found in ", seed_url)
                    print(word, "found in", crawl_layer, " steps")
                    flag_break = True
                    break
        if flag_break:
            break

        a = soup1.findAll("a", {"": ""})
        for element in a:
            if element.has_attr('href'):
                if 'media' in element['href']:
                    pass
                elif element['href'].startswith('//'):
                    pass
                elif 'Wikipedia:' in element['href']:
                    pass
                elif 'mobileaction=' in element['href']:
                    pass
                elif str(element['href']) in seed:
                    pass
                elif ('.org' or '.com' or '.se' or '.net') in element['href']:
                    seed.append(element['href'])
                else:
                    seed.append(start_url + element['href'])
        print("Length of seed: ", len(seed))
    except urllib.error.HTTPError:
        print("Wops something went wrong!")
        seed.remove(seed[len(seed) - 1])
    except ValueError:
        print("Faw")
        seed.remove(seed[len(seed) - 1])
        pass
