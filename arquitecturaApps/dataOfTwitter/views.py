from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import ProcessUrl
from .keys import get_oauth2_token as getAuth
import json, os, csv
from arquitecturaApps import settings as stt
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
import pycountry
from googletrans import Translator
# Create your views here.


# variables globales INICIO
dicInfo={"hashtags":'',"numberTweets":'',"uniqueTweets":'',"firstTweet":'',"lastTweet":'',}
# variables globales FIN
# carpeta ficheros INICIO
baseDirDatafile=stt.BASE_DIR+"/datafile"
if not os.path.exists(baseDirDatafile):
    os.mkdir(baseDirDatafile)
# carpeta ficheros FIN


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProcessUrl(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            #'/baseDataTwitter.tsv' '/'+stt.BASEDATOS_FILE+'.tsv'
            url_file=form.data['url_tags']
            gc = getAuth.authenticate_google_docs()
            sh = gc.open_by_url(url_file)
            worksheet = sh.get_worksheet(0)
            colum1 = worksheet.col_values(1)
            colum2 = worksheet.col_values(2)

            #obtener key del archivo
            guk=getKeyUrl(url_file)
            #generar una ruta con la key del archivo
            pathFileKey=baseDirDatafile+"/"+guk
            if existKeyDir(guk):
                print("Fichero Existente..............")
                if getInfoInit(colum1, colum2)== readAndLoad(guk, stt.ARCHIVO_INICIAL)['lastTweet']:
                    print("Fichero exisitente y actualizado, no se descargara...")
                else:
                    #os.mkdir(pathFileKey)
                    os.remove(pathFileKey+'/'+stt.BASEDATOS_FILE+'.tsv')
                    worksheetData = sh.get_worksheet(1)
                    export_file = worksheetData.export(format='tsv')
                    f = open(pathFileKey+'/'+stt.BASEDATOS_FILE+'.tsv', 'wb')
                    f.write(export_file)
                    f.close()
                    print("Actualizando fichero....")
                    getInfoInit(colum1, colum2)
                    writeToJSONFile(guk, stt.ARCHIVO_INICIAL, dicInfo)
                    #actualizarFicheros(guk)
            else:
                os.mkdir(pathFileKey)
                worksheetData = sh.get_worksheet(1)
                export_file = worksheetData.export(format='tsv')
                f = open(pathFileKey + '/'+stt.BASEDATOS_FILE+'.tsv', 'wb')
                f.write(export_file)
                f.close()
                print("Fichero descargado y guardado...")
                getInfoInit(colum1, colum2)
                writeToJSONFile(guk, stt.ARCHIVO_INICIAL, dicInfo)
                #actualizarFicheros(guk)
            #return HttpResponseRedirect("/datos/")
            #return redirect(datosTwitter(request=request, info=dicInfo, key="urls"))
            #analizarDatos(guk)
            actualizarFicheros(guk, comprobate=True)
            return HttpResponseRedirect("/datos/"+guk)
        else:
            if "key_tags" in request.POST:
                dicPost = request.POST.dict()
                claveIn=dicPost['key_tags']
                if existKeyDir(claveIn):
                    #getWordsTwitte(claveIn)
                    actualizarFicheros(claveIn, comprobate=True)
                    return HttpResponseRedirect("/datos/" + claveIn)
                else:
                    raise "Error: Key no existe!"
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProcessUrl()
    return render(request, 'index.html', {'formUrl': form})

'''
def datosTwitter(request, key=None):
    if (key is None) or (not key in os.listdir(baseDirDatafile)):
        print("if dentro....")
        return redirect(index)
    else:
        dicInfo=readAndLoad(key, stt.ARCHIVO_INICIAL)
        data=dicInfo['hashtags']
        data_number=dicInfo['numberTweets']
        data_number=data_number.replace(",", "")
        data=data.replace(" OR", ",")
        dicInfo.update({"hashtags": data})
        dicInfo.update({"numberTweets": data_number})
        dicInfo.update({"uniqueTweetsPor": (100*int(str(dicInfo['uniqueTweets']).replace(",","")))/int(data_number)})
        numero_paises=readAndLoad(key, stt.COUNTRYS_TWITTER)
        return render(request, 'infoData.html', {'infoBasic':dicInfo, 'country':len(numero_paises.keys())})
'''
def datosTwitter(request, key=None):
    if (key is None) or (not key in os.listdir(baseDirDatafile)):
        print("if dentro....")
        return redirect(index)
    else:
        dicInfo=readAndLoad(key, stt.ARCHIVO_INICIAL)
        data=dicInfo['hashtags']
        data_number=dicInfo['numberTweets']
        data_number=data_number.replace(",", "")
        data=data.replace(" OR", ",")
        data_ini=dicInfo['firstTweet']
        data_ini=data_ini.replace(" (", ",")
        data_fin=dicInfo['lastTweet']

        dicInfo.update({"hashtags": data})
        dicInfo.update({"numberTweets": data_number})
        dicInfo.update({"firstTweet": data_ini})
        dicInfo.update({"lastTweet": data_fin})
        dicInfo.update({"uniqueTweetsPor": (100*int(str(dicInfo['uniqueTweets']).replace(",","")))/int(data_number)})
        numero_paises=readAndLoad(key, stt.COUNTRYS_TWITTER )
        imagesJson=readAndLoad(key, stt.IMAGES_TWITTER )
        return render(request, 'infoData.html', {'infoBasic':dicInfo,
                                                 'country':len(numero_paises),
                                                 'countryCounter':numero_paises,
                                                 'keyUrl':key,
                                                 'images':imagesJson})

def viewRealTime(request):
    return render(request, 'realTime.html')

def viewAnalisis(request, key2=None):
    if (key2 is None) or (not existKeyDir(key2)):
        return redirect(index)
    data=readAndLoad(key2, stt.DATEFORTWITTE)
    users=getCsv(key2, stt.TOPUSERS)
    words=readAndLoad(key2, stt.TOPWORDS)
    return render(request, 'analisisDatos.html', {"keyUrl":key2,
                                                  "datatime":data,
                                                  "topUsers":users,
                                                  "topWords":words})

def viewEstadisticas(request, key=None):
    if (key is None) or (not existKeyDir(key)):
        return redirect(index)
    return render(request, 'infoData.html', {'keyUrl':"as"})

def viewImagenes(request):
    return render(request, 'images.html')


# class DataSheet(models):
#
#     hasgTag	= models.CharField('hasgTag')
#     period	= models.CharField(max_length=200, blank=True, null=True)
#     numberTweet = models.CharField(max_length=200, blank=True, null=True)
#     primerTweet = models.CharField(max_length=200, blank=True, null=True)
#     ultimoTweet = models.CharField(max_length=200, blank=True, null=True)
#     in_reply_to_user_id_str	= models.CharField(max_length=200, blank=True, null=True)
#
#
#     models.CharField(max_length=200, blank=True, null=True)
#     def __init__(self, arg):
#         super(DataSheet, self).__init__()
#         self.arg = arg

def actualizarFicheros(key, update=False, comprobate=False):
    if update:
        analizarDatos(key)
        analizarImg(key)
        getDateTweet(key)
        getTopUsers(key)
        getWordsTwitte(key)
    elif comprobate:
        listaDir=[]
        for a in os.listdir(baseDirDatafile+"/"+key):
            dir=os.path.splitext(a)[0]
            listaDir.append(dir)
        if not stt.COUNTRYS_TWITTER in listaDir:
            analizarDatos(key)
        if not stt.IMAGES_TWITTER in listaDir:
            analizarImg(key)
        if not stt.DATEFORTWITTE in listaDir:
            getDateTweet(key)
        if not stt.TOPUSERS in listaDir:
            getTopUsers(key)
        if not stt.TOPWORDS in listaDir:
            getWordsTwitte(key)
    else:
        pass


def writeToJSONFile(clave, fileName, data):
    print("####")
    print(clave)
    print("####")
    filePathNameWExt = baseDirDatafile +"/"+clave +"/"+fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)
        return True
    return False

def getKeyUrl(url):
    list=str(url).split("/d/")
    key=list[1].split("/")
    return key[0]

def getInfoInit(col1, col2):
    dateLastTweet=""
    for index, item in enumerate(col1):
        if (item == "2. Enter term" or "Enter" in item):
            dicInfo.update({"hashtags": col2[index]})
        elif (item == "Number of Tweets"):
            dicInfo.update({"numberTweets": col2[index]})
        elif (item == "Unique tweets"):
            dicInfo.update({"uniqueTweets": col2[index]})
        elif (item == "First Tweet"):
            dicInfo.update({"firstTweet": col2[index]})
        elif (item == "Last Tweet"):
            dicInfo.update({"lastTweet": col2[index]})
            dateLastTweet=col2[index]
    return dateLastTweet

def readAndLoad(key, namefile):
    filePathNameWExt = baseDirDatafile + "/"+ key+"/"+ namefile+ '.json'
    with open(filePathNameWExt) as json_file:
        data = json.load(json_file)
    return data

def getCsv(key, namefile):
    filePathNameWExt = baseDirDatafile + "/"+ key+"/"+ namefile+ '.csv'
    render=[]
    with open(filePathNameWExt, 'rb') as f:
        reader = csv.reader(f)
    return reader

def existKeyDir(calveDir):
    return calveDir in os.listdir(baseDirDatafile)

def analizarDatos(key):
    datas=pd.read_csv(baseDirDatafile+"/"+key+"/"+stt.BASEDATOS_FILE+".tsv", sep="\t", index_col="id_str")
    datafilecsv=datas.copy()
    filter1 = ~datafilecsv['user_location'].isnull()
    paises = datafilecsv[filter1]
    valor=paises['user_location'][0:]
    valor=valor.values
    paisesTwi={}
    for pais in valor:
        try:
            res = detectCountry(pais)
            paisesTwi[res]+=1
        except:
            paisesTwi.update({res:1})
    dicToPisesCode=[]
    for k, valueP in paisesTwi.items():
        if k!=None:
            nombre=str(k).split("-")
            dicToPisesCode.append({"code":nombre[1], "name":nombre[0]+" ("+str(valueP)+")", "value":valueP, "color":"#eea638"})
    writeToJSONFile(key, stt.COUNTRYS_TWITTER, dicToPisesCode)
    pass


def analizarImg(key):
    datas=pd.read_csv(baseDirDatafile+"/"+key+"/"+stt.BASEDATOS_FILE+".tsv", sep="\t", index_col="id_str")
    datafilecsv=datas.copy()
    filter1 = ~datafilecsv['entities_str'].isnull()
    img = datafilecsv[filter1]
    valor=img['entities_str'][0:]
    valor=valor.values
    lisToIma=[]
    #lis.append({"thumbnail":"root","value":5})
    count=1
    for valordict in valor:
        lista=json.loads(valordict)
        if 'media' in lista:
            for media in lista['media']:
                typeUrl=media['type']
                if(typeUrl=="photo"):
                    lisToIma.append({"thumbnail":media['media_url'],
                                "enlarged":media['media_url'],
                                "title":media['url'],
                                "categories":[{"id":1, "title":str(typeUrl).title()}],
                                "tWidth":media['sizes']['thumb']['w'],
                                "tHeight":media['sizes']['thumb']['h'],
                                "eWidth":media['sizes']['large']['w'],
                                "eHeight":media['sizes']['large']['h']})
                else:
                    lisToIma.append({"thumbnail": media['media_url'],
                                "enlarged": media['media_url'],
                                "title": media['url'],
                                "categories": [{"id": 2, "title": "Other"}],
                                "tWidth": media['sizes']['thumb']['w'],
                                "tHeight": media['sizes']['thumb']['h'],
                                "eWidth": media['sizes']['large']['w'],
                                "eHeight": media['sizes']['large']['h']})
                count=count+1
    writeToJSONFile(key,stt.IMAGES_TWITTER, lisToIma)


def getStopWords(text, join=True):
    #user_lang
    stop_words = set(stopwords.words('english'))
    stop_words.update(set(stopwords.words('spanish')))
    stop_words.update(set(stopwords.words('italian')))
    stop_words.update(set(stopwords.words('russian')))
    stop_words.update(set(stopwords.words('french')))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', '≠', '\'\'', '🇺🇸','🌌', '✡', '|', ')', '[', ']', '{', '}', '#', '❤', '&', '@', '-', '/', '🌍', '``'])
    words = tokenizar(text, sentences=False)
    new_sentence = []
    for word in words:
        if word not in stop_words:
            new_sentence.append(word)
    if join:
        return " ".join(new_sentence)
    else:
        return new_sentence

def tokenizar(text, sentences=True):
    text=str(text)
    if sentences:
        return [word_tokenize(sentence) for sentence in sent_tokenize(text)]
    else:
        return word_tokenize(text)

def detectCountry(country):
    paisStr=str(country)
    mapping = {'.':'', '"':'', "'":'', '?':'', '!':'',':':'', ';':'', '(':'', '≠':'', '\'\'':'', '🇺🇸':'','🌌':'',
               '✡':'', '|':'', ')':'', '[':'', ']':'', '{':'', '}':'', '#':'', '❤':'', '&':'', '@':'', '/':'',
               '🌍':'', '``':''}
    for k, v in mapping.items() :
        paisStr = paisStr.replace(k, v)
    lista = paisStr.split(",")
    for pais in lista:
        if pais.isupper():
            if len(pais)==2:
                try:
                    p = pycountry.countries.get(alpha_2=pais)
                    return p.name+"-"+p.alpha_2
                except:
                    pass
            elif len(pais)==3:
                try:
                    p = pycountry.countries.get(alpha_3=pais)
                    return p.name+"-"+p.alpha_2
                except:
                    pass
            elif len(pais)>3:
                if (pais[0] == ' '):
                    data1=pais[1:]
                    if len(data1) == 2:
                        try:
                            p = pycountry.countries.get(alpha_2=pais)
                            return p.name+"-"+p.alpha_2
                        except:
                            pass
                    elif len(data1) == 3:
                        try:
                            p = pycountry.countries.get(alpha_3=pais)
                            return p.name+"-"+p.alpha_2
                        except:
                            pass
                    pass
                else:
                    try:
                        for caracter in pais.split(" "):
                            p = pycountry.countries.get(name=caracter.title())
                            return p.name+"-"+p.alpha_2
                    except:
                        pass

        elif(pais):
            try:
                if(pais[0]==' ' or pais[-1]==' '):
                    data=pais.replace(' ', '')
                    #data=traductor(data)
                    p = pycountry.countries.get(name=data.title())
                    return p.name+"-"+p.alpha_2
                else:
                    p = pycountry.countries.get(name=pais.title())
                    return p.name+"-"+p.alpha_2
            except:
                pass

def calculate_languages_ratios(text):

    languages_ratios = {}

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)

    return languages_ratios


#----------------------------------------------------------------------
def detect_language(text):

    ratios = calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language

def getDateTweet(key):
    #created_at Tue Dec 26 19:09:51 + 4000 2017
    #time 26/12/2017 19:09:51
    datas = pd.read_csv(baseDirDatafile + "/" + key + "/" + stt.BASEDATOS_FILE + ".tsv", sep="\t", index_col="id_str")
    fechas = pd.DataFrame()
    fechas['date']=datas['time']
    fechas['entities_str']=datas['entities_str']
    fechas=fechas.dropna(how='any')
    fechas['date'] = pd.to_datetime(fechas['date'])
    fechas.index = fechas['date']
    del fechas['date']
    save=pd.DataFrame()
    save=fechas.resample('H').count()
    save.to_json(baseDirDatafile + "/" + key + "/" + stt.DATEFORTWITTE + ".json", orient='table')

def getTopUsers(key):
    #created_at Tue Dec 26 19:09:51 + 4000 2017
    #time 26/12/2017 19:09:51
    datas = pd.read_csv(baseDirDatafile + "/" + key + "/" + stt.BASEDATOS_FILE + ".tsv", sep="\t", index_col="id_str")
    users = pd.DataFrame()
    users['users']=datas['from_user']
    users=users.dropna(how='any')
    save=users.groupby(['users']).size().reset_index(name='counts').sort_values(['counts'], ascending=False).head(20)
    save.rename(columns={'users': 'id', 'counts': 'value'}, inplace=True)
    save.to_csv(baseDirDatafile + "/" + key + "/" + stt.TOPUSERS + ".csv")
    save.to_csv(stt.BASE_DIR+ "/dataOfTwitter/static/" + stt.TOPUSERS + ".csv")

def countIdiomas(key):
    datas = pd.read_csv(baseDirDatafile + "/" + key + "/" + stt.BASEDATOS_FILE + ".tsv", sep="\t", index_col="id_str")
    save = datas.groupby(['user_lang']).size().reset_index(name='counts').sort_values(['counts'], ascending=False).head(20)
    save.to_json(baseDirDatafile + "/" + key + "/" + stt.DATEFORTWITTE + ".json", orient='table')

def getWordsTwitte(key):
    datas = pd.read_csv(baseDirDatafile + "/" + key + "/" + stt.BASEDATOS_FILE + ".tsv", sep="\t", index_col="id_str")
    textoTwitte = pd.DataFrame()
    filter1 = ~datas['text'].isnull()
    textoTwitte=datas[filter1][0:1000]
    resultStopWords=pd.DataFrame()
    if "textStopWords.csv" in os.listdir(baseDirDatafile+"/"+key):
        resultStopWords = pd.read_csv(baseDirDatafile + "/" + key + "/textStopWords"+".csv", index_col="id_str")
    else:
        resultStopWords["text"] = textoTwitte['text'].apply(getStopWords)
        resultStopWords.to_csv(baseDirDatafile + "/" + key + "/textStopWords" + ".csv")
    result=pd.DataFrame()
    result["res"]=resultStopWords.text.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0)
    saveText=result.sort_values(['res'], ascending=False).head(205)

    saveText.rename(columns={'res': 'size'}, inplace=True)
    #saveText.reset_index(inplace=True)  # Resets the index, makes factor a column
    saveText.drop(["RT", "https", "El","2015"], inplace=True)
    print(saveText)
    saveText.to_json(baseDirDatafile + "/" + key + "/"+stt.TOPWORDS+".json", orient='table')
    #.sort_values(['counts'], ascending=False).head(20)


def traductor(text, idioma="us"):
    tran = Translator()
    es = tran.translate(text)
    print(es.text)
    return es.text
