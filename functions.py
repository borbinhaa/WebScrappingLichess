from selenium import webdriver
import pandas as pd
from math import floor


class ChromeDriver:

    def __init__(self):
        self.tournament_list = self.table = self.new_table = []
        self.driver_path = 'chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.chrome = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def get(self, site):
        self.chrome.get(site)

    def quit(self):
        self.chrome.quit()

    def num_players(self):
        all_num = self.chrome.find_element_by_xpath('//*[@id="main-wrap"]/main/div[2]/div/div[2]/div/span').text
        index = all_num.find('/')
        num_player = int(all_num[index + 2:])
        return self.correct_num(num_player)

    def next_page(self):
        self.chrome.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/div[2]/div/button[4]').click()

    @staticmethod
    def correct_num(num):
        if str(num)[-1] == '0':
            num = floor(num / 10)
        else:
            num = (floor(num / 10)) + 1
        return num

    def get_datas(self):
        style = 'swiss'
        tie_breaks = self.chrome.find_elements_by_class_name('tieBreak')
        if not tie_breaks:
            self.table = self.chrome.find_element_by_class_name('tour__standing')
        else:
            self.table = self.chrome.find_element_by_class_name('swiss__standing ')
        ranks = self.table.find_elements_by_class_name('rank')
        names = self.table.find_elements_by_class_name('name')
        ratings = self.table.find_elements_by_class_name('rating')

        if not tie_breaks:
            style = 'arena'
            points = self.table.find_elements_by_class_name('total')
            for index in range(len(names)):
                rank = ranks[index].text
                name = names[index].text
                rating = ratings[index].text
                point = points[index].text

                self.tournament_list.append([rank, name, rating, point])
            return self.tournament_list, style

        points = self.table.find_elements_by_class_name('points')

        for index in range(len(names)):
            rank = ranks[index].text
            name = names[index].text
            rating = ratings[index].text
            point = points[index].text
            tie_break = tie_breaks[index].text
            self.tournament_list.append([rank, name, rating, point, tie_break])
        return self.tournament_list, style

    def do_excel(self, tournament_list, style, file_name, caminho):
        if style == 'arena':
            self.new_table = pd.DataFrame(tournament_list, columns=['Colocação', 'Nome', 'Rating', 'Pontos'])
        else:
            self.new_table = pd.DataFrame(tournament_list, columns=['Colocação', 'Nome', 'Rating', 'Pontos', 'Desempate'])

        try:
            self.new_table.to_excel(caminho + r'\ ' + file_name + '.xlsx', index=False)
        except:
            self.new_table.to_excel(caminho + '/' + file_name + '.xlsx', index=False)
        return self.new_table
