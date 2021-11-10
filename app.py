import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import lxml
from colorama import Fore, init
init()
GRAY = Fore.LIGHTBLACK_EX
GREEN = Fore.GREEN
CYAN = Fore.CYAN
WHITE = Fore.WHITE

fua = lambda : UserAgent().random
print(f'{GREEN}Разведчик (by German){WHITE}\n')
addr = input(f'Адрес веб-сайта: ')

url = f'https://www.reg.ru/misc/ip_host_lookup?ip_address_or_host={addr}'
headers={'User-Agent':fua()}
ip = str(requests.get(url,headers=headers).json()['ipv4'][0])
print(f'IPV4: {ip}')
del url
print('\nПодождите, сканирование портов...')
ports = (20,21,22,23,25,53,69,80,110,123,143,156,443,465,993,3389,5432,5900,7071,9090)
open_ports = []
url = 'https://portchecker.co/'
for port in ports:
	data = {
		'target_ip': ip,
		'port': port,
		'selectPort': '21',
		'_csrf': '8M8TrC2tPDqq5Jxo-W9ti6QRzHJTQLntLTMyafb8Syc'
	}
	headers = {
	'authority': 'portchecker.co',
	'method': 'POST',
	'path': '/',
	'scheme': 'https',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'ru,en;q=0.9',
	'cache-control': 'max-age=0',
	'content-length': '94',
	'content-type': 'application/x-www-form-urlencoded',
	'cookie': 'rack.session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Np%0Ab25JZAY6D0BwdWJsaWNfaWRJIkVjYTUxMDEyMWQyMmY0MTJhMDVkNmE4OWY5%0AODc0MmNiNjQwZjYxNGUwMjQ0OGVmNGU2ODk5YWE0YzEwZjU2ZjBiBjsARkki%0AD2NzcmYudG9rZW4GOwBUSSIwOE04VHJDMnRQRHFxNUp4by1XOXRpNlFSekhK%0AVFFMbnRMVE15YWZiOFN5YwY7AEY%3D%0A--88847d641a9c04429d92dd025328fde5eedbf270; _ga=GA1.2.1506639089.1636556348; _gid=GA1.2.119159653.1636556348',
	'origin': 'https://portchecker.co',
	'referer': 'https://portchecker.co/',
	'sec-ch-ua': '"Yandex";v="21", " Not;A Brand";v="99", "Chromium";v="93"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1',
	'user-agent': fua()
	}
	response = requests.post(url, headers=headers, data=data)
	if 'open' in BeautifulSoup(response.content,'lxml').find('div',{'id':'results-wrapper'}).text:
		open_ports.append(port)
print(f"{GRAY}Просканированные порты: {str(ports).replace('(','').replace(')','')}")
print(f"{GREEN}Открытые порты: {str(open_ports).replace('[','').replace(']','')}")
del url

url = 'https://www.whatweb.net/whatweb.php'
data = {
	'target':addr
}
headers = {'User-Agent':fua()}
response = requests.post(url, headers=headers, data=data)
info = response.text.replace('&#171;','«').replace('&#187;','»').replace('],','],\n')
print(f'{CYAN}\nИнформация WatchWeb:\n\n{info}')

print(f'{WHITE}[Y] - сохранить результат разведки в файл "Info.txt"\n[Другая буква] - завершить работу')
vybor = input('Ваш выбор: ')
if vybor.lower() == 'y':
	with open('Info.txt','w') as file:
		file.write(f"""Домен: {addr}
IPV4: {ip}

Открытые порты: {str(open_ports).replace('[','').replace(']','')}
*Просканированные порты: {str(ports).replace('(','').replace(')','')}

Информация WatchWeb:

{info}
		""")