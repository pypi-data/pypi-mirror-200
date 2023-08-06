import requests
import openai
from nltk import sent_tokenize
from .contexts import *
from .models import Models
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import configparser



class SmartyGPT:

    def __init__(self, model=Models.GPT3, prompt="Rapper", path=''):
        self.model = model
        config = configparser.ConfigParser()
        config.read(path+'config.txt')
        self.api_key = config['auth']['api_key'] 
        if prompt in list(ManualContexts.__dict__.keys()):
            self.prompt = ManualContexts.__dict__[prompt]   
        elif prompt in AwesomePrompts.dataset['act']:
            context = AwesomePrompts.dataset.filter(lambda x: x['act']==prompt)['prompt'][0]
            context = ' '.join(sent_tokenize(context)[:-1])
            self.prompt = context
        else:
            self.prompt = CustomPrompt(path, prompt).prompt
            print(self.prompt)

    def change_context(self,prompt):
        self.prompt = prompt
    
    def get_context(self):
        return self.prompt

    '''
    This function wraps user's petition question with the adequate context 
    to better orient the response of the language model
    '''
    def wrapper(self, query:str) -> str:

        ### Models
        if self.model==Models.FlanT5:
            model = AutoModelForSeq2SeqLM.from_pretrained(Models.FlanT5)
            tokenizer = AutoTokenizer.from_pretrained(Models.FlanT5)
            inputs = tokenizer(self.prompt + " \"" + query+ "\"", return_tensors="pt")
            outputs = model.generate(**inputs)
            response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            response = response[0].lower()       
            return response

        elif self.model==Models.GPT3:
            openai.api_key= self.api_key
            response = openai.Completion.create(
                engine=self.model,
                prompt=self.prompt +'\n'+ query,
                temperature=0,
                max_tokens=256,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            response = response['choices'][0]['text']+'\n'
            response = response.lower()
            return response            
            
        elif self.model==Models.ChatGPT or self.model==Models.GPT4:
            openai.api_key=self.api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a chatbot"},
                    {"role": "user", "content": self.prompt+'\n'+query},
                ]
            )
            reply = response["choices"][0]["message"]["content"]
            return reply
