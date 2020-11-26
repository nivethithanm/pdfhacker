# importing tkinter and tkinter.ttk 
# and all their functions and classes 
from tkinter import * 
from tkinter.ttk import *

# from class filedialog 
from tkinter.filedialog import askopenfile

# Data Extraction part imports
from PIL import Image
import pytesseract
import sys 
from pdf2image import convert_from_path 
# Highlightling
import fitz
import os 
# ML Part Imports
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
# PDF Reader Module
import webbrowser

nltk.download('words')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')

root = Tk() 
root.geometry('400x300')

dirpath = str(os.getcwd()) + '/'
filename = ''

directory = os.path.join(dirpath, 'pdfhacker')
if (os.path.isdir(directory) == False):
    os.mkdir(directory)
path = directory + '/'
outputfile = path + 'output.pdf'

tempdirectory = os.path.join(path, 'temp')
if (os.path.isdir(tempdirectory) == False):
    os.mkdir(tempdirectory)
temppath = tempdirectory + '/'

def PDFViewer(outputfilename):
    webbrowser.open(r'file:///'+outputfilename)


def open_file(): 
    file = askopenfile(mode ='r', filetypes =[('PDF files','*.pdf'),('Document files','*.doc'),('Python Files', '*.py')]) 
    global filename
    filename = str(file.name)

def getTextFromPDF(filename):
    pages = convert_from_path(filename, 500, fmt='jpeg') 
    output = ""
    image_counter = 1
    for page in pages:
        imagefile = temppath+ "page_"+str(image_counter)+".jpg"
        page.save(imagefile, 'JPEG')
        text = str(((pytesseract.image_to_string(Image.open(imagefile)))))
        text = text.replace('-\n', '') 
        output = output + '-' + text
        os.remove(imagefile)
        image_counter += 1
    return output

def highlightWords(list_of_words, filename,outputfile):
    doc = fitz.open(filename)
    doc.pageCount
    for i in range(doc.pageCount):
        page = doc[i]
        for item in list_of_words:
            text_instances = page.searchFor(item + ' ')
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
    doc.save(outputfile, garbage=4, deflate=True, clean=True)

def extract_entities(text):
	entities = []
	for sentence in nltk.sent_tokenize(text):
	    chunks = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
	    entities.extend([chunk for chunk in chunks if hasattr(chunk, 'label')])
	return entities

def convertToPDF(filename):
    
    return filename

def getTextFromDoc(filename):
    pdffilename = convertToPDF(filename)
    output = getTextFromPDF(pdffilename)
    return output

def getKeywordsDocument(filename):
    list_of_words = []
    if('.pdf' in filename):
        text = getTextFromPDF(filename)
    if('.doc' in filename):
        text = getTextFromDoc(filename)
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    stemmer = SnowballStemmer("english")
    stemmed_tokens = [stemmer.stem(t) for t in tokens]
    fdist = nltk.FreqDist(stemmed_tokens)
    sorted(nltk.corpus.stopwords.words('english'))[:50]
    stemmed_tokens_no_stop = [stemmer.stem(t) for t in stemmed_tokens if t not in nltk.corpus.stopwords.words('english')]
    stemmed_tokens_cured = [stemmer.stem(t) for t in stemmed_tokens_no_stop if t not in ['!','\'',',','.',';','/','\\','\"','\'','[',']','(',')','|','.',':','>','<','?','~','`','*','-','+','=','_','-','1','2','3','4','5','6','7','8','9','0']]
    fdist2 = nltk.FreqDist(stemmed_tokens_cured)
    
    vocab = list(fdist2.most_common(int(len(fdist2)/20)))
    for item in vocab:
        list_of_words.append(item[0])
    for entity in extract_entities(text):
        list_of_words.append(entity[0][0])
    return list_of_words

def getHighlighted(filename,outputfile):
    list_of_words = getKeywordsDocument(filename)
    print(list_of_words)
    highlightWords(list_of_words,filename,outputfile)

w = Canvas(root, width=40, height=60)
w.pack()

btn = Button(root, text ='Open', command = lambda:open_file()) 
btn.pack(side = LEFT, padx = 20) 
        
openbtn = Button(root, text ='Close', command = root.destroy) 
openbtn.pack(side = RIGHT, padx = 20)

btn = Button(root, text ='Highlight', command = lambda:getHighlighted(filename,outputfile)) 
btn.pack(side = BOTTOM, pady = 20)

viewbtn = Button(root, text ='View', command = lambda:PDFViewer(outputfile)) 
viewbtn.pack(side = TOP, pady = 20)

mainloop()
