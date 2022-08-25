from libries.PagesTecConcursos import QuestionPage
from libries.utils import *
import csv
import time
import logging
import traceback
import platform

DIVISOR = '/' if platform.system()=='Linux' else '\\'

class Main:
    def __init__(self) -> None:
        self.site = QuestionPage(profiles=True)
        self.log = logging.getLogger(__name__)
        self.log.debug("MainOperation started")

    
    def start(self):
        self.site.start()
    
    def loginManual(self):
        self.site.start()
            
    def scrap_quest(self):
        self.site.caderno_de_questoes(self.link)
        for n in range(0, self.pages):
            try:
                infos = self.site.infos()
                question_row = self.formatInfos(infos)
                self.rows_infos.append(question_row)
                self.site.next_page()
                time.sleep(2)
            except Exception as e:
                self.log.info(f"Erro na extração da questão N: {n}: {traceback.format_exc()}")
                print(f'Erro na extração da questão N: {n}\n {e}') 

    def formatInfos(self, infos):
        question = self.formatString(infos['question'])
        response = self.formatString(infos['response'] + '<hr>' + infos['comment'])
        return f'{question};{response}'


    def formatString(self, string):
        return string.replace(';', ',').replace('\n', '<br>')


    def salveCsv(self):
        with open(self.path_scraps, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([c.strip() for c in r.split(',')] for r in self.rows_infos)
            f.close()


    def close(self):
        self.site.driver.close()
    
    def set_enviroment(self):
        self.path = f'Questoes'
        self.path_scraps = f'{self.path}{DIVISOR}{time_now("%H_%M %D").replace("/", "_")}.csv'
        set_folder(self.path)
        set_folder('logs')

        
    def run(self, link, pages):
        self.link = link
        self.pages = pages
        print(f'\n{time_now("%H:%M:%S")} Iniciando buscas!')
        self.rows_infos = []
        self.start()
        self.set_enviroment()
        self.scrap_quest()
        self.salveCsv()
        self.close()
        print(f'{time_now("%H:%M:%S")} Busca finalizada!')
        print(f'\nArquivo de saída: \n{self.path_scraps}')



if __name__ == '__main__':
    bot = Main()
    bot.run()
    print(f'{time_now("%H:%M:%S")} Busca finalizada!')

