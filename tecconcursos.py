from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
import web
import time

       
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
    PERGUNTA = (By.XPATH,'//*[contains(@class,"questao-enunciado-texto")]')
    ALTERNATIVAS = (By.XPATH,'(//*[@class="questao-enunciado-alternativas"]//li)[1]')
    RESULTADO = (By.XPATH,'//*[@class="questao-enunciado-resolucao-mensagem ng-binding ng-scope"]')
    RESOLVER_QUESTÃO = (By.XPATH,'//*[@title="Resolver questão (tecla Enter)"]')

    VER_RESOLUCAO = (By.XPATH,'//span[contains(text(), "Ver resolução")]')

    GABARITO = (By.XPATH,'//*[@class="ng-scope correcao"]')
    COMENTARIO = (By.XPATH,'//*[contains(@class,"questao-complementos-comentario-conteudo-texto")]')
    IMG = (By.XPATH,'//*[contains(@class,"questao-complementos-comentario-conteudo-texto")]//img')


    def __init__(self, profiles=False, headless=False):
        self.driver = web.Webdriver(profiles, headless)
    
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

    def click_ver_solucao(self):
        self.driver.click(self.VER_RESOLUCAO)

    def select_alternativa(self):
        self.driver.click(self.VER_RESOLUCAO)

    def next_page(self):
        if self.driver.exist(self.PROXIMA_QUESTAO, wait=5):
            self.driver.click(self.PROXIMA_QUESTAO)
            return True
        return False

    def close(self):
        self.driver.close()


class QuestionPage(TecConcurso):

    def infos(self, img_path):
        dic = dict()
        time.sleep(2)#ajustar
        dic['Matéria'] = self.driver.find_element(self.MATERIA).text.split(': ')[1]
        dic['Assunto'] = self.driver.find_element(self.ASSUNTO).text.split(': ')[1]
        dic['Questão'] = self.driver.find_element(self.QUESTÃO).text
        dic['Pergunta'] = self.driver.find_element(self.PERGUNTA).text
        dic['Link'] =  self.driver.find_element(self.LINK).get_attribute("href")

        self.comentario_prof()
        
        if self.driver.exist(self.GABARITO, wait=3): 
            dic['Gabarito'] = self.driver.find_element(self.GABARITO).text
        else:
            dic['Gabarito'] = 'Certo' if 'acertou' in self.driver.find_element(self.RESULTADO).text else 'Errado'

        time.sleep(2)
        if self.driver.exist(self.COMENTARIO, wait=3): 
            dic['Comentario do professor'] = self.driver.find_element(self.COMENTARIO).text
        else:
            dic['Comentario do professor'] = 'Sem comentário'
            
        dic['Img'] = self.get_img(img_path)

        return dic

    
    def comentario_prof(self):
        self.driver.click(self.ALTERNATIVAS)
        if self.driver.exist(self.RESOLVER_QUESTÃO, wait=3):
            self.driver.click(self.RESOLVER_QUESTÃO, hover_to=False)
        if self.driver.exist(self.VER_RESOLUCAO, wait=3):
            self.driver.click(self.VER_RESOLUCAO)
    
    def get_img(self, img_path):
        if self.driver.exist(self.IMG, wait=2):
            with open(img_path, 'wb') as file:
                file.write(self.driver.find_element(self.IMG).screenshot_as_png)
            return img_path
        return 'Sem Imagem'
    
    def last_quest(self):
        quest = self.driver.find_element(self.INDEX_QUESTÃO).text

        
