from to_excel import ToExcel
from tecconcursos import QuestionPage
from utils import *
import traceback
from time import sleep

CONFIGS = consult_csv()
CONFIGS['QTD_ITENS'] = int(CONFIGS['QTD_ITENS'][0]) if CONFIGS['QTD_ITENS'][0]!='' else 999

class Main:
    PATH = 'Questões'

    def __init__(self) -> None:
        self.site = QuestionPage()
        self.to_excel = ToExcel()
    
    def start(self):
        self.site.start()
        self.site.login(CONFIGS['LOGIN'][0], CONFIGS['SENHA'][0])
        self.site.caderno_de_questoes(CONFIGS['URL'][0])
            
    def scrap_quest(self):
        self.to_excel.create()
        for item in range(1, CONFIGS['QTD_ITENS']+1):
            try:
                img_path = f'{self.path_screans}\\{item}.png'
                questao = self.site.infos(img_path)
                questao['Id'] = item
                self.site.next_page()
                self.to_excel.add_in_df([questao])
                self.to_excel.to_excel(self.path_scraps)

            except Exception: 
                pass
                #print(f'{item}')
                # traceback.print_exc()

    def close(self):
        self.site.driver.driver.close()
    
    def set_enviroment(self, categoria):
        path_cats="\\".join(categoria)
        self.path = f'{self.PATH}\\{path_cats}\\{time_now("%H_%M %D").replace("/", "_")}'
        self.path_scraps = f'{self.path}\\questões.xlsx'
        self.path_screans = f'{self.path}\\Imagens'
        set_folder(self.path)
        set_folder(self.path_screans)
        
    def run(self):
        self.start()
        self.set_enviroment(['Questões'])
        self.scrap_quest()
        self.close()
        return True


bot = Main()

try: 
    print(f'\n{time_now("%H:%M:%S")} Iniciando buscas!')
    bot.run()
    print(f'{time_now("%H:%M:%S")} Busca finalizada!')

except Exception:
    print('\nError! Mostre para o desenvolvedor.\n')
    traceback.print_exc()    
    
input()
