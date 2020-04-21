# IMPORTAR AS LIBS
import time
import os


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from chatterbot import ChatBot 
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

import wikipedia
wikipedia.set_lang('pt')

import requests
import json

from PIL import Image #pip install Pillow

from imgurpython import ImgurClient # PIP INSTALL IMGURPYTHON

# INSTANCIAR CHATBOT
chatbot = ChatBot('Ananda')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.portuguese')
trainerer = ListTrainer(chatbot)

# ARMAZENAR DIRETORIO PRINCIPAL EM VARIAVEL
dir_path = os.getcwd()

# INICIAR APLICAÇÃO 
driver = webdriver.Chrome(dir_path+'chromedriver.exe')
driver.get('https://web.whatsapp.com/')
driver.implicity_wait(15)

# FUNÇÕES BASICAS DE COMUNICAÇÃO 
def pegaConversa():
	try:
		post = driver.find_elements_by_class_name('_12pGw')
		ultimo = len(post) - 1
		texto = post[utimo].find_elements_by_css_selector('span.selectable-text').text
		return texto
	except:
		pass

def enviaMensagem(mensagem):
	caixa_de_texto = driver.find_elements_by_class_name('_3u328')
	valor = "Ananda:* "+str(mensagem)
	for part in valor.split('\n'):
		caixa_de_texto.send_keys(part)
		ActionChains(driver).key_down(keys.SHIFT).key_down(keys.ENTER).key_up(keys.SHIFT).perform()
	time.sleep(0.5)
	botao_enviar = driver.find_elements_by_class_name('_3M-N-')
	botao_enviar.click()


def treinar(mensagem):
	resposta = 'Como respondo isso? me ensina, por favor...? utilize ;"'+str(mensagem)+'"'
	enviaMensagem(resposta)
	novo = []
	try:
		while True:
			ultima = pegaConversa()
			if ultima == "!":
				enviaMensagem("Você desativou meu aprendizado.")
				break
			elif ultima.replace(';', '') != '' and ultima != mensagem and ultima[0] == ';':
				auxiliar = ultima
				print(mensagem.lower().strip())
				print(ultima.replace(';','').lower().strip())
				novo.append(mensagem.lower().strip())
				novo.append(ultima.replace(';','').lower().strip())
				trainerer.train(novo)
				enviaMensagem("Pronto, aprendi! Obrigada <3")
				break
	except:
		pass

# WIKIPEDIA
def wiki():
	try:
		busca = str(pegaConversa().lower().trip()[2:])
		mensagem = '{}'.format(wikipedia.summary(busca))
		enviaMensagem(mensagem)

	except:
		enviaMensagem("Nada encontrado para {} na wikipedia Brasil. ".format(busca))

# NOTICIAS
def noticias():
	try:
		req = requests.get('https://newsapi.org/v2/top-headlines?country=br&category=technology&apiKey=a2c3a13397e14b23949109d598378f35')
		noticias = json.loads(req.text)
		for news in noticias['articles']:
			titulo = news['title']
			link = news['title']
			desc = news['description']
			mensagem = "{}\n{}\n{}".format(titulo, desc, link)
			enviaMensagem(mensagem)
			time.sleep(1)			
	except:
		enviaMensagem('agora não...')
		pass

# VISAO COMPUTACIONAL
def visa():
	# CAPTAR A FOTO
	foto = driver.find_elements_by_class_name("_3mdDl")
	last = len(foto) - 1
	for img in foto[last].find_elements_by_tag_name("img"):
		try:
			#salvar img
			img.screenshot("path/name.png")
			# converter img
			im = Image.open("path/nome.png")
			rgb.im.convert("RGB")
			rgb.save("path/nome.jpg")
			break
		except:
			enviaMensagem('agora não...')
			break
	# PUBLICAR FOTO NA WEB
	client_id = 'YOUR CLIENT ID'
	client_secret = 'YOUR CLIENT SECRET'
	client = ImgurClient(client_id, client_secret)
	image = client.upload_from_path("path/nome.jpg", anon=False)
	# API AZURE FACE
	subscription_key = '161c7c262f804fce9b9b343b759e36c7'
	assert subscription_key
	face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
	image_url = image['link']
	headers = {'Ocp-Apim-Subscription-Key': subscription_key}
	params = {'returnFaceId': 'true', 'returnFaceLandmarks': 'false', 'returnFaceAttributes': 'age,gender',}
	respo = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
	print(json.dumps(response.json()))
	# ENVIAR RESULTADOS DA API
	try:
		genero = None
		if (respo.json()[0]["faceAttributes"]["gender"] == "male"):
			genero = "Homem"
		else:
			genero = "Mulher"
		enviaMensagem("{}, {} anos.".format(genero,int(respo.json()[0]["faceAttributes"]["age"])))
	except:
		enviaMensagem("Rosto não reconhecido.")

# BLOCO PRINCIPAL DE EXECUÇÃO
salva = pegaConversa()
while True:
	try:
		if pegaConversa() != "" and pegaConversa()[:8] != "Ananda: " and pegaConversa() != salva and pegaConversa().strip() != "!" and pegaConversa().strip() != ";" and pegaConversa().strip().lower()[:2] != "W:" and pegaConversa().lower() != "noticias" and pegaConversa().strip().lower() != "notícias" and pegaConversa().strip().lower() != "visão computacional":
			texto = str(pegaConversa().strip().lower())
			response = chatbot.get_response(texto)
			if float(response.confidence) < 0.2:
				treinar(pegaConversa())
			else:
				enviaMensagem(response)
		elif pegaConversa().strip().lower()[:2] == "w:":
			wiki()
		elif pegaConversa().strip().lower() == "noticias" or pegaConversa().strip().lower() == "notícias":
			noticias()
		elif pegaConversa().strip().lower() == "visão computacional":
			enviaMensagem("Aguardando envio da imagem...")
			time.sleep(15)
			visa()
			pass
		else:
			pass

	except:
		pass
