import openai
from time import sleep
import json
import pkg_resources
from .helper import get_secret

class OpenAI:
    def __init__(self):
        # load the connection string from a config file
        config = json.loads(pkg_resources.resource_string(__name__, "config.json"))
        
        self.instance = openai;
        self.instance.api_key = get_secret("openai-api-key")

        self.prompt_limit = config["openai"]["prompt_limit"]
        # What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
        self.temperature = config["openai"]["temperature"]
        # An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or temperature but not both.
        self.top_p = config["openai"]["top_p"]
        self.max_tokens = config["openai"]["max_tokens"]
        self.frequency_penalty = config["openai"]["frequency_penalty"]
        self.presence_penalty = config["openai"]["presence_penalty"]
        self.embed_model = config["openai"]["embed_model"]
        self.llmodel = config["openai"]["llmodel"]
        self.chat_model = config["openai"]["chat_model"]
        self.chat_instructions = config["openai"]["chat_instructions"]
    
    def create_embeddings(self, texts):
        responses = self.instance.Embedding.create(input=texts, engine=self.embed_model)
        embeds = [record['embedding'] for record in responses['data']]
        return embeds
    
    def create_completion(self, prompt):        
        response = self.instance.Completion.create(
            prompt=prompt,
            engine=self.llmodel,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=1,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty
        )
        return response['choices'][0]['text'].strip()
    
    def get_chat_answer(self, messages, prompt):
        messages.append({"role": "system", "content": self.chat_instructions})
        messages.append({"role": "user", "content": prompt})
       
        response = self.instance.ChatCompletion.create(
            messages=messages,
            model=self.chat_model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            n=1,
            top_p=1,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty
        )
        return response['choices'][0].message