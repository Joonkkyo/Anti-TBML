from enum import Enum
import io
import json
from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
from sanction.models import SanctionList
import os
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/jkseo/PycharmProjects/Anti_TBML/document_inspection/key.json'
# sanc_list = np.load('sancdict.npy',allow_pickle='TRUE').item()

manual = np.load('C:/Users/jkseo/PycharmProjects/Anti_TBML/document_inspection/manual.npy', allow_pickle=True).item()
stopdict = np.load('C:/Users/jkseo/PycharmProjects/Anti_TBML/document_inspection/stopdict.npy', allow_pickle=True).item()

stopdict.update(manual)

data = SanctionList.objects.all()
sanc_list = [x.name for x in data]
print(sanc_list)
# sanc_list = ['corrections', 'Issuing', 'Guarantee']


def stopwords(words):
    word_new = ""
    for word in words.split(' '):
        word = word.lower()
        if word not in stopdict:
            word_new += word + ' '
    return word_new.strip()


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


# 좌표 정보가 들어오면 이미지에 박스 쳐줌
# ouput : boxed image
font = ImageFont.truetype("arial.ttf", 20)


def draw_boxes(image, output, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)
    word = output['word']
    bounds = output['place']
    danger = max(output['danger'])
    idx = output['danger'].index(danger)
    sim = output['similar_word'][idx]
    result = sim + ', ' + "similarity :" + str(danger)
    # result = ''.join(sim + ' ' + str(danger))

    # result = ' '.join([word, ' ::: ', result_])

    for bound in bounds:
        draw.polygon([
            bounds[0][0], bounds[0][1],
            bounds[1][0], bounds[1][1],
            bounds[2][0], bounds[2][1],
            bounds[3][0], bounds[3][1]], None, color)
        draw.text((bounds[0][0], bounds[0][1] - 20), result, (0, 0, 255), font)


# google api를 이용하여 이미지에 대한 response를 받아옴
# output : response,document
def get_document(image_file):
    with io.open(image_file, 'rb') as image_file_:
        content = image_file_.read()

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    return response, document


# get_document의 결과를 이용하여 바운드 정보를 저장
def get_document_bounds(document, feature):
    # Collect specified feature bounds by enumerating all document features
    bounds = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    # for symbol in word.symbols:
                    #     if feature == FeatureType.SYMBOL:
                    #         bounds.append(symbol.bounding_box)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def boxed_image(image, output, fileout):
    image_ = Image.open(image)
    for idx in output:
        # word = output[idx]['word']
        # bounds = output[idx]['place']
        # sim = output[idx]['similar_word']
        # danger = float(output[idx]['danger'])
        draw_boxes(image_, output[idx], 'blue')

    image_ = image_.convert('RGB')
    image_.save(fileout)
    print('boxed_image saved!')


# response를 json으로 저장해줌
def res_to_json(image, response, save=True, senlen=15, thresh=0.6):
    # API response to json file
    output = {}
    idx = 0
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                place = []
                for v in paragraph.bounding_box.vertices:
                    place.append((v.x, v.y))

                if len(paragraph.words) < senlen:
                    word_whole = ""
                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        word_whole = word_whole + word_text + ' '
                    word_whole = stopwords(word_whole)

                    similar_word, similarity = find_similar_word(word_whole, sanc_list, thresh)
                    if len(similarity) > 0:
                        output[idx] = {'word': word_whole, 'place': place,
                                       'danger': similarity, 'similar_word': similar_word}
                        idx += 1
                else:
                    for word in paragraph.words:
                        place = []
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])

                        for v in word.bounding_box.vertices:
                            place.append((v.x, v.y))
                        similar_word, similarity = find_similar_word(word_text, sanc_list, thresh)
                        if (len(similar_word)>0) and (word_text.lower() not in stopdict):
                            output[idx] = {'word': word_text, 'place': place,
                                           'danger': similarity, 'similar_word': similar_word}
                            idx += 1
    # dir, file = os.path.split(image)
    # file = file.split('.jpg')[0]
    # output_name = './boxed_images/'+file
    output_name = image[::-1].strip('gpj.').strip('/')[::-1]
    if save is True:
        if not os.path.isdir('./boxed_images/'):
            os.makedirs('./boxed_images/')
        with open(output_name+'.json', 'w') as file:
            json.dump(output, file, indent=1)
        print('json file saved!')
    return output, output_name


# edit distance 구함
def str_distance(str1_, str2_):
    '''
    str1과 str2를 각각 행과 열에 글자 단위로 쭉 늘어놓고, 글자 하나하나를 비교하는 식

    input : str1, str2
    output : len(str1)-distance / len(str1)
    '''
    # str1 > str2
    if str1_[0] != str2_[0]:
        return 0
    if len(str1_) < 3:
        return 0
    if len(str1_) > len(str2_):
        str1, str2 = str1_, str2_
    else:
        str1, str2 = str2_, str1_
    str1, str2 = str1.lower(), str2.lower()
    len1, len2 = len(str1), len(str2)  # vertical / horizontal

    # create distance table

    table = [None] * (len2 + 1)
    for i in range(len2 + 1):
        table[i] = [0] * (len1 + 1)
    for i in range(1, len2 + 1):
        table[i][0] = i
    for i in range(1, len1 + 1):
        table[0][i] = i
    for i in range(1, len2 + 1):
        for j in range(1, len1 + 1):
            if str1[j - 1] == str2[i - 1]:
                d = 0
            else:
                d = 1
            table[i][j] = min(table[i - 1][j - 1] + d, table[i - 1][j] + 1, table[i][j - 1] + 1)

        # substitute or copy, delete, insert
        #    dist = table[len2][len1]
    dist = (len(str1) - table[len2][len1]) / len(str1)
    dist = round(dist, 2)
    return dist


def dist_sen(str1, str2, thresh):
    dist_list = []
    for word1 in str1.split():
        for word2 in str2.split():
            dist_list.append(str_distance(word1, word2))
    if len(dist_list) > 0 and max(dist_list) > thresh:
        return round(sum(dist_list)/len(dist_list), 2)
    else: return 0


def api_main(image_path):
    image = image_path
    response, document = get_document(image)
    output, output_name = res_to_json(image, response)
    output_image = output_name + '_boxed.jpg'
    print(output_image)
    boxed_image(image, output, str(output_image))
    return output_image


# edit distance를 이용하여 thresh(0.8)이상인 애들을 list로 뽑아줌
def find_similar_word(word, sanc_list, thresh):
    similar_word = {}
    for sanc in sanc_list:
        similarity = dist_sen(word, sanc, thresh)
        # similarity = str_distance(word, sanc)

        if similarity > thresh:
            similar_word[sanc] = similarity

    return list(similar_word.keys()), list(similar_word.values())

