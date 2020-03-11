from PIL import Image, ImageDraw
import sys
import time
import os

light      = 255
lightgrey  = 192
mediumgrey = 129
darkgrey   = 66
dark       = 0



def closest_color(value):
    a = abs(light - value)
    b = abs(lightgrey - value)
    c = abs(mediumgrey - value)
    d = abs(darkgrey - value)
    e = abs(value)

    tones = {a:light,
             b:lightgrey,
             c:mediumgrey,
             d:darkgrey,
             e:dark}

    minimo = min(a,b,c,d,e)
    
    return tones[minimo]

def is_valid_colour(pixel):
    
    valid={tuple(3*[light]):True,
           tuple(3*[lightgrey]):True,
           tuple(3*[mediumgrey]):True,
           tuple(3*[darkgrey]):True,
           tuple(3*[dark]):True}

    try:
        return valid[pixel]
    except:
        return False
 
def validate(pixel):
    if is_valid_colour(pixel):
        return pixel
    else:
        soma = sum(pixel)
        media = sum(pixel)//len(pixel)

        return tuple(3*[closest_color(media)])    


def runtime(func, *args):
    i = time.time()
    func(*args)
    end = time.time() - i

    print("runtime: "+str(end))


def pixel_to_char(p):
    i = 9617
    light      = 255
    lightgrey  = 192
    mediumgrey = 129
    darkgrey   = 66
    dark       = 0
    
    light_chr      = 2*(" ")
    lightgrey_chr  = 2*(chr(i))
    mediumgrey_chr = 2*(chr(i+1))
    darkgrey_chr   = 2*(chr(i+2))
    dark_chr       = 2*(chr(9608))

    equivalencia = {light:light_chr,
                    lightgrey:lightgrey_chr,
                    mediumgrey:mediumgrey_chr,
                    darkgrey:darkgrey_chr,
                    dark:dark_chr}

    return equivalencia[p[0]]
                    

def img_to_ascii(img,filename):
    with open (filename, 'w', encoding="utf-8") as f:
        w = 1
        i = 9617
        
        light_chr      = 2*(" ")
        lightgrey_chr  = 2*(chr(i))
        mediumgrey_chr = 2*(chr(i+1))
        darkgrey_chr   = 2*(chr(i+2))
        dark_chr       = 2*(chr(9608))

        equivalencia = {light:light_chr,
                        lightgrey:lightgrey_chr,
                        mediumgrey:mediumgrey_chr,
                        darkgrey:darkgrey_chr,
                        dark:dark_chr}

        linha = ""
        
        f.write("<!DOCTYPE html>\n<html style=\"overflow: \">\n<body><font size=\"1\">\n")
        f.write("<head>\n<meta charset=\"UTF-8\">\n</head>\n<pre>")
        for y in range(img.height):
            for x in range(img.width):
                pi = img.getpixel((x,y))
                p = validate(pi)
               
                if w == img.width:
                    w = 1
                    f.write(linha+"\n")
                    linha = ""
                else:
                    w+=1
                    linha+=equivalencia[p[0]]

        f.write("\n</pre>\n</font>\n</body>\n</html>")

def read_by_block(img, filename, block_height, block_length):
    with open (filename, 'w', encoding="utf-8") as f:
        w = 1
        i = 9617

        light_chr      = 2*(" ")
        lightgrey_chr  = 2*(chr(i))
        mediumgrey_chr = 2*(chr(i+1))
        darkgrey_chr   = 2*(chr(i+2))
        dark_chr       = 2*(chr(9608))

        equivalencia = {light:light_chr,
                        lightgrey:lightgrey_chr,
                        mediumgrey:mediumgrey_chr,
			darkgrey:darkgrey_chr,
                        dark:dark_chr}
        
        f.write("<!DOCTYPE html>\n<html style=\"overflow: \">\n<body><font size=\"1\">\n")
        f.write("<head>\n<meta charset=\"UTF-8\">\n</head>\n<pre>")
        bx = 0
        incx = 0
        incy = 0
        imgh = img.height
        imgw = img.width
        t_imgh = imgh - (imgh % block_height)
        t_imgw = imgw - (imgw % block_length)
        max_bx = t_imgh * t_imgw
        bsum = 0
        auxy = 0
        imgstr = ""
        
        while bx < max_bx:
            x = bx % block_length + (incx * block_length)
            y = ((bx-auxy)//block_length) + (incy * block_height)
            pi = validate(img.getpixel((x,y)))
            bsum += pi[0]
            bx += 1
            if bx % (block_length * block_height) == 0:
                avg = bsum//(block_length * block_height)
                bsum = 0
                imgstr += equivalencia[validate([avg]*3)[0]]
                auxy += (block_length * block_height)
                incx = incx+1 if bx % ((block_length * block_height) * (t_imgw//block_length)) else 0
                if  bx % (t_imgw * block_height) == 0:
                    incy += 1
                    imgstr+="\n"
        f.write(imgstr)
        f.write("\n</pre>\n</font>\n</body>\n</html>")
    
            
    
def tira_extensao(path):
    ret = ""
    for c in path:
        if c == '.':
            break
        else:
            ret += c
    return ret
        
def cls():
    if sys.platform == 'linux':
        os.system('clear')
    else:
        os.system('cls')

def retry():
    while(True):
        c = input("Would you like to perform another operation? (Y/N)")
        if c == 'N' or c == 'n':
            return False
        elif c == 'Y' or c == 'y':
            return True




rode = True
while(rode):
    cls()
    tudo = os.listdir()
    i = time.time()
    print("1- Convert new image by rescaling")
    print("2- Convert new image by reading in blocks")
    print("3- Show this directory")
    print("4- Exit")
    print(30*"=")
    opcao = input("Choose option: ")
    if opcao == "1":
        path = input("Enter relative image path:\n")
        if (path in tudo):
            img = Image.open(path).convert("RGB")
            w = img.width
            h = img.height
            x = float(input("rescale factor(the dimensions of the img will be multiplied by this value):\n"))
            img = img.resize((int(w*x),int(h*x)))
            print("Converting image")
            runtime(img_to_ascii,img,tira_extensao(path)+"mult.html")
            print(30*"=")
            rode = retry()
    elif opcao == "2":
        path = input("Enter relative image path:\n")
        if (path in tudo):
            img = Image.open(path).convert("RGB")
            bh = int(input("block height(pixels):\n"))
            bl = int(input("block width(pixels):\n"))
            print("Converting image")
            runtime(read_by_block,img,tira_extensao(path)+"block.html",bh,bl)
            print(30*"=")
            rode = retry()
    elif opcao == "3":
        cls()
        print("Current dir: "+os.getcwd() + "\\\n")
        for path in tudo:
            print(path)
        input("\nPress ENTER to return")
    elif opcao == "4":
        rode = False
    else:
        print(30*"=")
