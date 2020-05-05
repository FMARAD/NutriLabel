import PIL
from PIL import Image, ImageDraw, ImageFont
global r , g, y,w, fatRange, satsRange, carbRange, saltRange
import arabic_reshaper
from bidi.algorithm import get_display
from copy import copy, deepcopy


terms = [('Energy',u"الطاقة             "),('Fat',u'الدهون'),(u'Saturates',u'الدهون المشبعة                               '),
		('Sugars',u'سكر'),('Salt',u'الملح     ')]
Units = [('g',u"جرام"),('g',u"جرام"),('kj',u" ك جول"),('kcal',u'ك سعر')]


font_size = 35
font = ImageFont.truetype('font.ttf', font_size)
maxlimit = 1000

fatRange  = ((-1,3),(3,17.5),(17.5,maxlimit))
satsRange = ((-1,1.5),(1.5,5),(5,maxlimit)) # check with mom range
carbRange = ((-1,5),(5,22.5),(22.5,maxlimit))
saltRange = ((-1,0.3),(0.3,1.5),(1.5,maxlimit))
RIs = [8400,70,20,90,6]

def csvlabel(csv):
	ls = []
	offset=200
	with open(csv) as f:
		for row in f:
			ls.append(row)
		f.close()
	for i, row in enumerate(ls[1::]):
		row = row.split(',')
		energy = int(row[0])
		Fat = float(row[1])
		sat = float(row[2])
		sugar = float(row[3])
		try:
			salt = float(row[4].strip('\n'))
		except:
			salt = row[4]
		picAr, picEn = sequencer(energy,Fat,sat,sugar,salt)


		Arpiccanvas = Image.new("RGBA",(picAr.width,picAr.height+offset),color=(255,255,255,255))
		Enpiccanvas = Image.new("RGBA",(picEn.width,picEn.height+offset),color=(255,255,255,255))
		Arpiccanvas.paste(picAr,(0,offset))
		Enpiccanvas.paste(picEn,(0,offset))

		picAr = Arpiccanvas
		picEn = Enpiccanvas


		text = row[5].strip('\n')
		Entext = "out/"+text+'.png'
		Artext = "out/Ar"+text+'.png'
		picAr.save(Artext)
		picEn.save(Entext)

def setTitle(canvas,title,level):
	draw = ImageDraw.Draw(canvas)
	draw.text(((canvas.width/2)-((len(title)*6)*1.5) , canvas.height*level ), title ,font=font, fill='black')


def resize(img,bd):
	basewidth = bd
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	return img

y = Image.open("y.jpg")
r = Image.open("r.jpg")
g = Image.open("g.jpg")
w = Image.open("w.jpg")

ylw= resize(y,250)
red= resize(r,250)
grn= resize(g,250)
wht= resize(w,250)

canvas = Image.new("RGBA",(ylw.width*5,ylw.height),color=0)

def checkranges(ing,ranges):

	for i, rng in enumerate(ranges):
		if inrange(ing,rng):
			if i == 0:
				return deepcopy(grn)
			elif i == 1:
				return deepcopy(ylw)
			elif i == 2:
				return deepcopy(red)


def sequencer(e,fat,sats,carb,salt):
	seq = [wht]
	seq.append(checkranges(fat,fatRange))
	seq.append(checkranges(sats,satsRange))
	seq.append(checkranges(carb,carbRange))
	seq.append(checkranges(salt,saltRange))
	ing = [e,fat,sats,carb,salt]




	picAr = printlabelAr(seq,ing)
	picEn = printlabel(seq,ing)

	return picAr, picEn



def centerText(newimg, text, level):
	draw = ImageDraw.Draw(newimg)
	draw.text(((newimg.width/2)-((len(text)*6)*1.5) , newimg.height*level ), text ,font=font, fill='black')
	return newimg

def printlabel(seq,ing):
	canvas = Image.new("RGBA",(ylw.width*5,ylw.height),color=0)
	for i, img in enumerate(seq):
		newimg = deepcopy(img)
		centerText(newimg,terms[i][0],0.2)
		if i == 0:
			centerText(newimg,str(ing[i])+Units[2][0],0.35)
			centerText(newimg,str(round(ing[i]*0.239006))+Units[3][0],0.45)
		elif 0 < i <= 3:
			centerText(newimg,str(ing[i])+Units[0][0],0.4)
		else:
			centerText(newimg,str(ing[i])+Units[1][0],0.4)


		if type(ing[i]) is str:
			centerText(newimg,f'0%',0.7)
		else:
			centerText(newimg,f'{round((ing[i]/RIs[i])*100)}%',0.7)

		canvas.paste(newimg,(0+(i*(newimg.width)),0))
	return canvas

def printlabelAr(seq,ing):
	canvas = Image.new("RGBA",(ylw.width*5,ylw.height),color=0)
	termsAr = terms[::-1]
	ing = ing[::-1]
	RIsAr = RIs[::-1]
	for i, img in enumerate(seq[::-1]):
		newimg = deepcopy(img)
		centerText(newimg,arab(termsAr[i][1]),0.2)
		if i == 0:
			centerText(newimg,arab(Units[1][1])+str(ing[i]),0.4)
		elif 0 < i <= 3:
			centerText(newimg,arab(Units[0][1])+str(ing[i]),0.4)
		else:
			centerText(newimg,arab(Units[2][1])+str(ing[i]),0.35)
			centerText(newimg,arab(Units[3][1])+str(round(ing[i]*0.239006)),0.45)


		if type(ing[i]) is str:
			centerText(newimg,f'0%',0.7)
		else:
			centerText(newimg,f'{round((ing[i]/RIsAr[i])*100)}%',0.7)




		canvas.paste(newimg,(0+(i*(newimg.width)),0))
	return canvas



def arab(text):
	reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
	text =  get_display(reshaped_text)           # correct its direction
	return text

def inrange(z,r):
	if type(z) is str:
		return True
	return r[0] < z <= r[1]
		


csvlabel('list.csv')

# print(inrange(0.2,(0.3,1.5)))


# sequencer(500,3.5,1.5,8,2)
# text = arab(terms[0][1])

# canvas.save('out.png')

