import pandas as pd
from pandas.core.indexes.base import Index

class ToExcel:
    ORDER = [
        'Id','Matéria', 'Assunto', 'Questão', 'Pergunta',
        'Gabarito', 'Comentario do professor', 'Img', 'Link'
        ]

    def create(self):
        self.data = pd.DataFrame()

    def add_in_df(self, data):
        self.data=self.data.append(data)   

    def to_excel(self, path):
        if len(self.data)!=0:
            data = self.data[self.ORDER]
            data.to_excel(path, index = False, encoding='utf8')

