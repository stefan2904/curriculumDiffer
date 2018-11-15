import pprint
import collections
import requests
from bs4 import BeautifulSoup


# <config>


# Doctoral School Informatik
# https://www.tugraz.at/studium/studienangebot/doktoratsstudien/doctoral-school-informatik/

# 791 Dr.-Studium der Naturwissenschaften: csr_nr=572&pStpStpNr=600
# https://online.tugraz.at/tug_online/semesterplaene.uebersicht?corg_nr=37&csr_nr=572&pStpStpNr=600&csj_nr=1039&csprache_nr=
label_1 = 'Naturwissenschaften'

# 786 Dr.-Studium der Technischen Wissenschaften: csr_nr=571&pStpStpNr=601
# https://online.tugraz.at/tug_online/semesterplaene.uebersicht?corg_nr=37&csr_nr=571&pStpStpNr=601&csj_nr=1039&csprache_nr=
label_0 = 'Technische Wissenschaften'

# Winter:
study0_w = 'https://online.tugraz.at/tug_online/semesterplaene.semesterplan?csr_nr=571&csj_nr=1039&csum_flag=J&cbackto=T&corg=37&csprache_nr=1&cstp_nr=601&cwfk_nr=21616&cwfk_sem=W'
study1_w = 'https://online.tugraz.at/tug_online/semesterplaene.semesterplan?csr_nr=572&csj_nr=1039&csum_flag=J&cbackto=T&corg=37&csprache_nr=1&cstp_nr=600&cwfk_nr=21601&cwfk_sem=W'

# Summer:
study0_s = 'https://online.tugraz.at/tug_online/semesterplaene.semesterplan?csr_nr=571&csj_nr=1039&csum_flag=J&cbackto=T&corg=37&csprache_nr=1&cstp_nr=601&cwfk_nr=21616&cwfk_sem=S'
study1_s = 'https://online.tugraz.at/tug_online/semesterplaene.semesterplan?csr_nr=572&csj_nr=1039&csum_flag=J&cbackto=T&corg=37&csprache_nr=1&cstp_nr=600&cwfk_nr=21601&cwfk_sem=S'


# </config>


summer = (study0_s, study1_s)
winter = (study0_w, study1_w)


def fetch(url):
    return requests.get(url).text


def val(array, index):
    return array[index].get_text().replace(u'\xa0', u'')


def get_lvs(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find_all('table')[4]

    lvs = {}
    for tr in table.find_all('tr'):
        lv = {}
        lvd = tr.find_all('td')

        if len(lvd) < 5:
            continue

        lv['nr'] = val(lvd, 0)
        lv['title'] = val(lvd, 1)
        lv['teacher'] = val(lvd, 2)
        lv['semester'] = val(lvd, 5)
        lv['kind'] = val(lvd, 4)

        lvs[lv['nr']] = lv

    return lvs


def get_diff(urls):
    semester = []
    for url in urls:
        data = fetch(url)
        lvs = get_lvs(data)
        semester.append(lvs)

    only_tech = {k: semester[0][k]
                 for k in set(semester[0]) - set(semester[1])}
    only_nat = {k: semester[1][k] for k in set(semester[1]) - set(semester[0])}

    return only_tech, only_nat


def print_diff(diff):
    print('## Only in {}: '.format(label_0))
    pprint.pprint(diff[0])
    print('## Only in {}: '.format(label_1))
    pprint.pprint(diff[1])
    print('')


def do_diff(urls):
    diffs = get_diff(urls)
    print_diff(diffs)


print('# Winter:')
do_diff(winter)

print('# Summer:')
do_diff(summer)
