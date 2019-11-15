try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

directory = os.path.join("D:\\_test")
path = os.path.join(directory, "results")
Top = 'Наименование лесничества\tНаименование участкового лесничества\tНаименование урочища\t№ лесного квартала\t№ лесотаксационного выдела\t№карточки дешифрирования\tНаименование лесопользователя\tплощадь,га\tобъем, м3\tдата архивной космической съемки\tдата текущей космической съемки\tдата дешифрирования\n'
cnfg = ""
txt = ""

lesn = (2480,128,3400,170)
uch_lesn = (2480,180,3400,220)
uroch = (2365,220,3400,265)
kvart = (2480,530,3400,575)
videl = (2480,575,3400,620)
id_kart = (1060,90,1420,130)
lesopolz = (2485,310,3400,350)
squre = (2480,1105,2700,1145)
zapas = (2480,1150,2700,1190)
arch_date = (2085, 2035,2255,2075)
curr_date = (1610,1990,1780,2030)
create_date = (425,2345,595,2385)

parts = [lesn, uch_lesn, uroch, kvart, videl, id_kart, lesopolz, squre, zapas, arch_date, curr_date, create_date]

#Распознавалка
def ocr(file,cnfg):
    text = pytesseract.image_to_string(file, lang='rus', config=cnfg)
    if len(text) <= 1:
        return '-'
    else:
        return text

#Распознавалка с опредением границ слов
def ocr_canvas(file):    
    text = pytesseract.image_to_data(img, lang='rus')
    return text

#Пробежка по массиву мест распознавания
def parts_walk(file, text, pre_fix):
    cnfg = "--psm 7"
    j = 0
    for i in parts:        
        image = file.crop(i)
        image.save(path +"\\"+ pre_fix + str(j) + ".jpg")
        text = text + ocr(image, cnfg) + '\t'
        j = j + 1
    text = text + '\n'
    return text
    
#Пробежка по каталогу с карточками
for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith(".jpg"):
          pre_fix=file[:-4]
          img = Image.open(file) #.convert('L')
          txt = txt + parts_walk(img,cnfg,pre_fix)
    with open(path + "\\result.txt",'w') as f: f.write(str(Top + '\n' + txt))
