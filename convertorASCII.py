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
    #supondo q todos os valores >=0

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
 
def valida(pixel):
    if is_valid_colour(pixel):
        return pixel
    else:
        soma = sum(pixel)
        media = sum(pixel)//len(pixel)
        #pixelaprox = closest_color(media)

        return tuple(3*[closest_color(media)])    

def parseImgB(img):

    points={tuple(3*[light]):[],
           tuple(3*[lightgrey]):[],
           tuple(3*[mediumgrey]):[],
           tuple(3*[darkgrey]):[],
           tuple(3*[dark]):[]}
    
    for x in range(img.width):
        for y in range(img.height):
            p = img.getpixel((x,y))
            pi = valida(p)
            points[pi].append((x,y))
            #d.point((x,y),(n,n,n))
            #img.putpixel((x,y),(n,n,n))

   
    d = ImageDraw.Draw(img)

    #drawing all light points:
    d.point(points[tuple(3*[light])],tuple(3*[light]))

    #drawing all lightgrey points:
    d.point(points[tuple(3*[lightgrey])],tuple(3*[lightgrey]))

    #drawing all mediumgrey points:
    d.point(points[tuple(3*[mediumgrey])],tuple(3*[mediumgrey]))

    #drawing all darkgrey points:
    d.point(points[tuple(3*[darkgrey])],tuple(3*[darkgrey]))

    #drawing all dark points:
    d.point(points[tuple(3*[dark])],tuple(3*[dark]))

  #  img.save("tomReduzido.jpg")


def runtime(func, *args):
    i = time.time()
    func(*args)
    end = time.time() - i

    print("Tempo da operação: "+str(end))


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
                    

def img_to_ascii_corzinha(img,filename):
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
                p = valida(pi)
               
                if w == img.width:
                    w = 1
                    f.write(linha+"\n")
                    linha = ""
                else:
                    w+=1
                    linha+=equivalencia[p[0]]

        f.write("\n</pre>\n</font>\n</body>\n</html>")

def print_l(l):
    for n in l:
        print(n)
        
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
            pi = valida(img.getpixel((x,y)))
            bsum += pi[0]
            bx += 1
            if bx % (block_length * block_height) == 0:
                avg = bsum//(block_length * block_height)
                bsum = 0
                imgstr += equivalencia[valida([avg]*3)[0]]
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

def escolha():
    while(True):
        escolha = input("Deseja realizar outra operacao? (S/N)")
        if escolha == 'N' or escolha == 'n':
            return False
        elif escolha == 'S' or escolha == 's':
            return True




rode = True
while(rode):
    cls()
    tudo = os.listdir()
    i = time.time()
    print("1- Converter nova imagem (multiplicador)")
    print("2- Converter nova imagem (bloco)")
    print("3- Listar diretório")
    print("4- Sair")
    print(30*"=")
    opcao = input("Escolha a opcao: ")
    if opcao == "1":
        path = input("Digite o caminho da imagem:\n")
        if (path in tudo):
            img = Image.open(path).convert("RGB")
            w = img.width
            h = img.height
            x = float(input("multiplicador:\n"))
            img = img.resize((int(w*x),int(h*x)))
            print("Convertendo imagem (MULTIPLICADOR)")
            runtime(img_to_ascii_corzinha,img,tira_extensao(path)+"mult.html")
            print(30*"=")
            rode = escolha()
    elif opcao == "2":
        path = input("Digite o caminho da imagem:\n")
        if (path in tudo):
            img = Image.open(path).convert("RGB")
            bh = int(input("altura do bloco(pixels):\n"))
            bl = int(input("largura do bloco(pixels):\n"))
            print("Convertendo imagem (BLOCO)")
            runtime(read_by_block,img,tira_extensao(path)+"block.html",bh,bl)
            print(30*"=")
            rode = escolha()
    elif opcao == "3":
        cls()
        print("Diretorio atual: "+os.getcwd() + "\\\n")
        for path in tudo:
            print(path)
        input("\nPressione ENTER para voltar")
    elif opcao == "4":
        rode = False
    else:
        print(30*"=")
