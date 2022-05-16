import libries.WebBase as WebBase
from selenium.webdriver.common.by import By
import time

import logging
import traceback


WAIT = 10
       
class TecConcurso:
    URL = r"https://www.tecconcursos.com.br/login"

    EMAIL = (By.ID, 'email')
    SENHA = (By.ID, 'senha')
    ENTRAR = (By.ID, 'entrar-site')

    INDEX_QUESTÃO = (By.XPATH,'//*[@class="questao-cabecalho-informacoes-numero espacamento-1"]')

    PROXIMA_QUESTAO = (By.XPATH, '//*[@class="questao-navegacao-botao questao-navegacao-botao-proxima-cinza ng-isolate-scope"]')

    MATERIA = (By.XPATH,"//*[@class='questao-cabecalho-informacoes-materia espacamento-1']")
    ASSUNTO = (By.XPATH,'//*[contains(@class,"uestao-cabecalho-informacoes-assunto")]')
    QUESTÃO = (By.XPATH,'//*[@class="questao-rg-area-titulo"]')
    LINK = (By.XPATH,'//*[@class="id-questao ng-binding"]')
    QUESTÃO_COMPLETA = (By.XPATH,"//article")
    PERGUNTA = (By.XPATH,'//*[contains(@class,"questao-enunciado-texto")]')
    ALTERNATIVAS = (By.XPATH, "//ul[@class='questao-enunciado-alternativas']")
    ALTERNATIVA_A = (By.XPATH, "(//ul[@class='questao-enunciado-alternativas']//li)[1]")
    RESULTADO = (By.XPATH,'//*[@class="questao-enunciado-resolucao-mensagem ng-binding ng-scope"]')

    RESOLVER_QUESTAO = (By.XPATH,'//button[contains(@class, "botao-resolver")]')
    VER_RESOLUCAO = (By.XPATH,'//span[contains(text(), "Ver resolução")]')

    RIGHT_RESPONSE_C = (By.XPATH,'//li[contains(@class, "correcao")]')
    RIGHT_RESPONSE_A = (By.XPATH,'//li[contains(@class, "acerto")]')


    COMENTARIO = (By.XPATH,'//*[contains(@class,"questao-complementos-comentario-conteudo-texto")]')
    IMG = (By.XPATH,'//*[contains(@class,"questao-complementos-comentario-conteudo-texto")]//img')



    def __init__(self, profiles=False, headless=False):
        self.driver = WebBase.Webdriver(profiles, headless)
        self.log = logging.getLogger(__name__)

    
    def start(self):
        self.driver.start()
        self.driver.open_page(self.URL)

    def login(self, login, senha):
        self.driver.fill(self.EMAIL, login)
        self.driver.fill(self.SENHA, senha)
        self.driver.click(self.ENTRAR)
    
    def caderno_de_questoes(self, url_caderno ):
        self.driver.open_page(url_caderno)
    
    def click_proxima_questao(self):
        self.driver.click(self.PROXIMA_QUESTAO)

    def clickVerSolucao(self):
        self.driver.click(self.VER_RESOLUCAO)

    def clickResolverQuestao(self):
        self.driver.click(self.RESOLVER_QUESTAO, True)

    def select_alternativa(self):
        self.driver.click(self.ALTERNATIVA_A)

    def next_page(self):
        if self.driver.exist(self.PROXIMA_QUESTAO, wait=WAIT):
            self.driver.click(self.PROXIMA_QUESTAO)
            return True
        return False

    def close(self):
        self.driver.close()





class QuestionPage(TecConcurso):

    def infos(self):
        try:
            question = self.getQuestion()
            if not question:
                question_number = self.driver.find_element(self.INDEX_QUESTÃO)
                self.log.info(f"Corpo de questão não encontrada! - {question_number}")
                alert = f'Questão {question_number}\n não extraida!'
                return {'question': alert, 'response':'Questão não extraida', 'comment':'Sem comentário'}

            response = self.getResponse()

            if self.openSolution() and self.driver.exist(self.COMENTARIO, wait=WAIT):
                comment = self.driver.find_element(self.COMENTARIO).text
            else:
                comment = 'Sem comentário'
            return {'question':question, 'response':response, 'comment':comment}

        except Exception as e:
            question_number = self.driver.find_element(self.INDEX_QUESTÃO)
            self.log.info(f"Erro {question_number}\n    {traceback.format_exc()}")
            alert = f'Questão {question_number}- Não extraida!'
            return {'question': alert, 'response':'Questão não extraida', 'comment':'Sem comentário'}
    
    def getQuestion(self):
        if self.driver.exist(self.QUESTÃO_COMPLETA, wait=WAIT):
            text = self.driver.find_element(self.PERGUNTA).text
            text +='<br>' + self.driver.find_element(self.ALTERNATIVAS).text
            return text
        return False

    def getResponse(self):
        if self.driver.exist(self.RESOLVER_QUESTAO, wait=WAIT):
            self.select_alternativa()
            time.sleep(1)
            self.clickResolverQuestao()
            time.sleep(3)
            try:
                if self.driver.exist(self.RESOLVER_QUESTAO, wait=2):
                    self.clickResolverQuestao()
            except: 
                pass
        if self.driver.exist(self.RIGHT_RESPONSE_C, wait=4):
            return self.driver.find_element(self.RIGHT_RESPONSE_C).text
        else:
            return self.driver.find_element(self.RIGHT_RESPONSE_A).text

    
    def openSolution(self):
        if self.driver.exist(self.VER_RESOLUCAO, wait=WAIT):
            self.clickVerSolucao()
            return True
        return False
    

        
if __name__ == '__main__':
        import configparser
        import pprint

        CONFIGS = configparser.ConfigParser()
        CONFIGS.read('configs.ini')
        site = QuestionPage(profiles=True)
        site.start()
        site.caderno_de_questoes(CONFIGS['login']['URL'])
        for item in range(1, 10):
            infos = site.infos()
            pprint.pprint(infos)
            site.next_page()
            time.sleep(2)