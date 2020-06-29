# -*- coding: utf-8 -*-
from PIL import Image, ImageFilter
from PIL import ImageFont 
from PIL import ImageDraw 
import numpy as np
import os
import glob
import random
import cv2
import textwrap
import json
from collections import OrderedDict

data_group = OrderedDict()
char_C =[]
L = []
# word = open('use_word.txt', 'r', encoding='UTF8')
# while(1):
#     line = word.readline()
#     try:escape=line.index('\n')
#     except:escape=len(line)
#     if line:
#         L.append(line[0:escape])
#     else:
#         break
# word.close()
num = 0
folderSave = 0

filename = 'val.txt' #kor_data.txt #chin_chosen.txt
with open(filename, 'r', encoding='utf-8') as file_object:
    contents = file_object.read()

for j in range(len(contents)):
    char_C.append(contents[j])

cnt =0
def create_an_image(bground_path, width, height):
    bground_list = os.listdir(bground_path)
    bground_choice = random.choice(bground_list)
    bground = Image.open(bground_path+bground_choice)
    x, y = random.randint(0,bground.size[0]-width), random.randint(0, bground.size[1]-height)
    bground = bground.crop((x, y, x+width, y+height))
    return bground


def random_font(font_path):
    font_list = os.listdir(font_path)
    random_font = random.choice(font_list)
    return font_path + random_font

def chose_font(font_path, count, i):
    font_list = os.listdir(font_path)
    if (count % 9731) == 0 :
        i = i+1
    return font_path + font_list[i]

def random_word_color():
    font_color_choice = [[0,0,0]] #,[0,255,255],[255,255,0],[255,0,255]
    font_color = random.choice(font_color_choice)

    noise = np.array([random.randint(0,10),random.randint(0,10),random.randint(0,10)])
    font_color = (np.array(font_color) + noise).tolist()
    return tuple(font_color)

def darken_func(image):
    filter_ = random.choice(
                            [ImageFilter.SMOOTH,
                            ImageFilter.SMOOTH_MORE,
                            ImageFilter.GaussianBlur(radius=1.3)]
                            )
    image = image.filter(filter_)
    return image

def draw_rotated_text(image, angle, xy, text, fill, *args, **kwargs):

    # get the size of our image
    width, height = image.size
    max_dim = max(width, height)

    # build a transparency mask large enough to hold the text
    mask_size = (max_dim * 2, max_dim * 2)
    mask = Image.new('L', mask_size, 0)

    # add text to mask
    draw = ImageDraw.Draw(mask)
    draw.text((max_dim, max_dim), text, 255, *args, **kwargs)

    if angle % 90 == 0:
        # rotate by multiple of 90 deg is easier
        rotated_mask = mask.rotate(angle)
    else:
        # rotate an an enlarged mask to minimize jaggies
        bigger_mask = mask.resize((max_dim*8, max_dim*8),
                                  resample=Image.BICUBIC)
        rotated_mask = bigger_mask.rotate(angle).resize(
            mask_size, resample=Image.LANCZOS)

    # crop the mask to match image
    mask_xy = (max_dim - xy[0], max_dim - xy[1])
    b_box = mask_xy + (mask_xy[0] + width, mask_xy[1] + height)
    mask = rotated_mask.crop(b_box)

    # paste the appropriate color, with the text transparency mask
    color_image = Image.new('RGBA', image.size, fill)
    image.paste(color_image, mask)

#텍스트 저장
save = open('./gt3.txt', 'w', encoding='utf-8')

font_i =0
k =0
for i in range(len(char_C)):#29139

    HVCheck = 0#random.randint(0, 1) #가로, 세로 체크 1이면 가로 0이면 세로
    
    #이미지 생성
    target_image = create_an_image('./background/',128 , 128)
    #폰트 선택
    font_name = random_font('./font/') # chose_font(font_path, count, i):
    #font_name = chose_font('./font/', i, font_i)
    #폰트 색
    font_color = random_word_color()

    #폰트 지정
    font = ImageFont.truetype(font_name, 100)

    if i % 50000 ==0:
        folderSave = folderSave + 1
        dir_path = 'data/d' + str(folderSave)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path + '/')
            
    #이미지 그리기
    draw = ImageDraw.Draw(target_image)
    #이미지에 텍스트 넣기
    # 단어 길이를 받아오고 그 길이만큼 for문을 돌려서 아래로 써준다!r
    # convert to pillow image
    if (i % len(char_C)) == 0 :
        k =0
    x = (64-int(100/2))
    y = (64-int(100/2))
    draw.text((x, y-5),char_C[k], fill = font_color, font = font)# 세로쓰기


    target_image = np.array(target_image)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    target_image=Image.fromarray(target_image)
    target_image.save(dir_path +'/'+str(char_C[k])+'.jpg')#save image
    #target_image.save(dir_path +'/'+str(i)+'.jpg')#save image

    save.write('train/'+ str(num) + '.jpg')
    save.write(' '+str(char_C[k]))

    if i != len(char_C):
        save.write('\n')
    k = k+1

    num = num + 1
    