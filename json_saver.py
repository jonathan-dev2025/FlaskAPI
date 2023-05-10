from http.client import HTTPException
import json
import logging
import os


class JsonSaver:
    def __init__(self,file):
        self.file = file
        self.elements = []
        self.create_if_not_exist()
        self.load()


    def load(self):
        try:
            with open (self.file,'r') as f:
                self.elements = json.load(f)
            logging.info(self.elements)
        except FileNotFoundError:
            self.elements = []
        
    def find_all(self):
        logging.info("json_saver: récupération de la liste")
        return self.elements
    
    def save(self, index):
        try:
            with open (self.file, 'r') as f:
                content = json.load(f)
            if not content:
                content.append(self.elements[index])
            content = self.elements
            with open (self.file, 'w') as f:
                json.dump(content,f)
            return{"status_code":"204", "detail":"opération effectuée"}
        except FileNotFoundError:
            return{"status_code":"404", "detail":"pas de fichier de donnée."}
    
    def delete(self, id):
        index = index = self.index_by_id(id)
        del self.elements[index]
        self.save(index)

    def update(self, id, element):
        index = self.index_by_id(id)
        self.elements[index] = element
        self.save(index)

    def find(self, id):
        index = index = self.index_by_id(id)
        return self.elements[index]

    def create_if_not_exist(self):
        if not os.path.exists(self.file):
            with open (self.file, 'w') as f:
                json.dump([],f)

    
    def add(self,id, element):
        self.elements.append(element)
        index = self.index_by_id(id)
        return self.save(index)


    def index_by_id(self, id):
        if not self.elements:
            return{"status_code":404, "detail":"La liste est vide."}
            
        id_dict = {item['id']: index for index, item in enumerate(self.elements)}
        if id not in id_dict:
            return{"status_code":"404", "detail":"ID non trouvé."}
            
        return id_dict.get(id)