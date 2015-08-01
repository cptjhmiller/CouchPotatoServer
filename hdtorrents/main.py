import traceback

from datetime import datetime
from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import toUnicode
from couchpotato.core.helpers.variable import tryInt, getIdentifier
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
import re

log = CPLog(__name__)


class HDtorrents(TorrentProvider, MovieProvider):
#class Base(TorrentProvider):

    urls = {
        'login' : 'https://www.hdts.ru/login.php',
        'detail' : 'https://www.hdts.ru/details.php?id=%s',
        'search' : 'https://www.hdts.ru/torrents.php?search=%s&active=1',
        'home' : 'https://www.hdts.ru/%s',
    }

    http_time_between_calls = 1 #seconds

    def _search(self, movie, quality, results):

        url = self.urls['search'] % (getIdentifier(movie))#, cats[0])
        data = self.getHTMLData(url)
        
        if data:
          
          # Remove HDTorrents NEW list
          split_data = data.partition('<!-- Show New Torrents After Last Visit -->\n\n\n\n')
          data = split_data[2]

          html = BeautifulSoup(data)
          try:
              #Get first entry in table
              entries = html.find_all('td', attrs={'align' : 'center'})

              if len(entries) < 21:
                  return

              base = 21
              extend = 0

              try:
                  torrent_id = entries[base].find('div')['id']
              except:
                  extend = 2
                  torrent_id = entries[base + extend].find('div')['id']

              torrent_age = datetime.now() - datetime.strptime(entries[15 + extend].get_text()[:8] + ' ' + entries[15 + extend].get_text()[-10::], '%H:%M:%S %d/%m/%Y')
              
              results.append({
                              'id': torrent_id,
                              'name': entries[20 + extend].find('a')['title'].strip('History - ').replace('Blu-ray', 'bd50'),
                              'url': self.urls['home'] % entries[13 + extend].find('a')['href'],
                              'detail_url': self.urls['detail'] % torrent_id,
                              'size': self.parseSize(entries[16 + extend].get_text()),
                              'age': torrent_age.days,
                              'seeders': tryInt(entries[18 + extend].get_text()),
                              'leechers': tryInt(entries[19 + extend].get_text()),
                              'get_more_info': self.getMoreInfo,
              })

              #Now attempt to get any others
              result_table = html.find('table', attrs = {'class' : 'mainblockcontenttt'})

              if not result_table:
                  return

              entries = result_table.find_all('td', attrs={'align' : 'center', 'class' : 'listas'})

              if not entries:
                  return

              for result in entries:
                  block2 = result.find_parent('tr').find_next_sibling('tr')
                  if not block2:
                      continue
                  cells = block2.find_all('td')
                  try:
                      extend = 0
                      detail = cells[1 + extend].find('a')['href']
                  except:
                      extend = 1
                      detail = cells[1 + extend].find('a')['href']
                  torrent_id = detail.replace('details.php?id=', '')
                  torrent_age = datetime.now() - datetime.strptime(cells[5 + extend].get_text(), '%H:%M:%S %d/%m/%Y')

                  results.append({
                                  'id': torrent_id,
                                  'name': cells[1 + extend].find('b').get_text().strip('\t ').replace('Blu-ray', 'bd50'),
                                  'url': self.urls['home'] % cells[3 + extend].find('a')['href'],
                                  'detail_url': self.urls['home'] % cells[1 + extend].find('a')['href'],
                                  'size': self.parseSize(cells[6 + extend].get_text()),
                                  'age': torrent_age.days,
                                  'seeders': tryInt(cells[8 + extend].get_text()),
                                  'leechers': tryInt(cells[9 + extend].get_text()),
                                  'get_more_info': self.getMoreInfo,
                  })

          except:
              log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

    def getMoreInfo(self, item):
        full_description = self.getCache('hdtorrents.%s' % item['id'], item['detail_url'], cache_timeout = 25920000)
        html = BeautifulSoup(full_description)
        nfo_pre = html.find('div', attrs = {'id':'details_table'})
        description = toUnicode(nfo_pre.text) if nfo_pre else ''

        item['description'] = description
        return item

    def getLoginParams(self):
        return {
            'uid': self.conf('username'),
            'pwd': self.conf('password'),
            'Login': 'submit',
        }

    def loginSuccess(self, output):
        return "if your browser doesn\'t have javascript enabled" or 'logout.php' in output.lower()

    loginCheckSuccess = loginSuccess
