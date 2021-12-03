from os import write
import os
import requests
from bs4 import BeautifulSoup
import getpass

login = input("Введите логин: ").strip()
password = getpass.getpass("Введите пароль: ")
print('Ожидайте...')
url_login = 'https://signin.intra.42.fr/users/sign_in/'
url_main = 'https://profile.intra.42.fr/users/'+login+'/locations_stats'

client = requests.session()
html = client.get(url_login)
soup = BeautifulSoup(html.text, 'lxml')
token = soup.find('input', dict(name='authenticity_token'))['value']

data = {
	'utf8': '✓',
	'authenticity_token': token,
	'user[login]': login,
	'user[password]': password,
	'commit': 'Sign+in',
}

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36',
	'Referer': url_main,
	'Connection': 'keep-alive',
}
r = client.post(url_login, data=data, headers=headers)
content = client.get(url_main).json()

# блок проверяет на наличие файла со статистикой снятой ранее, если существует записывает данные о последней записи
if os.path.exists('stats.txt'):
	f = open('stats.txt', 'r')
	count_str = 0
	for line in f.readlines():
		break
	split_line = line.split(' ')
	split_line = split_line[1].split('.')
	split_line[2] = split_line[2].rstrip(',')
	f.close
else:
	split_line = [0, 0, 0]

# блок записи распаршенных данных во временный файл
tmp = open('tmp.txt', 'w')	
sum_days = 0
for i in content:
	sum_days = sum_days + 1
	date = i.split('-')
	time = (content[i].split('.'))
	if int(date[0]) < int(split_line[2]):
		break
	if int(date[1]) < int(split_line[1]) and int(date[0]) == int(split_line[2]):
		break
	if int(date[2]) < int(split_line[0]) and int(date[1]) == int(split_line[1]) and int(date[0]) == int(split_line[2]):
		break
	tmp.write('Дата: '+date[2]+'.'+date[1]+'.'+date[0]+', количество времени: '+time[0]+'\n')
tmp.close()

# блок дозаписывает старые данные в конец временного файла с новыми данными
if os.path.exists('stats.txt'):
	f = open('stats.txt', 'r')
	tmp = open('tmp.txt', "a+")
	count = 0
	for line in f.readlines():
		if count != 0:
			tmp.write(line)
		count = count + 1
	f.close()
	tmp.close()

# блок записывает полную базу со старыми данными и новыми в основной файл и удаляет временный файл	
f = open ('stats.txt', 'w')
tmp = open('tmp.txt', "r")
sum_days = 0
for line in tmp.readlines():
	sum_days = sum_days + 1
	f.write (line)
f.close()
tmp.close()
os.remove("tmp.txt")
print("Файл stats.txt обновлен")
print(sum_days)