import pytesseract as tess
import cv2
import re

tess.pytesseract.tesseract_cmd = r'/Users/kihun/opt/anaconda3/envs/ANTI_TBML/bin/tesseract'

def str_distance(str1,str2):
    '''
    str1과 str2를 각각 행과 열에 글자 단위로 쭉 늘어놓고, 글자 하나하나를 비교하는 식

    input : str1, str2
    output : len(str1)-distance / len(str1)
    '''
    str1,str2  = str1.lower(),str2.lower()
    len1,len2 = len(str1),len(str2) # vertical / horizontal
    # create distance table
    table = [None]*(len2+1)
    for i in range(len2+1):
        table[i] = [0]*(len1+1)
    for i in range(1, len2+1):
        table[i][0] = i
    for i in range(1, len1+1):
        table[0][i] = i
    for i in range(1, len2+1):
        for j in range(1, len1+1):
            if str1[j-1] == str2[i-1]:
                d = 0
            else:
                d = 1
            table[i][j] = min(table[i-1][j-1] + d, table[i-1][j] + 1, table[i][j-1] + 1)

    # substitute or copy, delete, insert
    dist = (len(str1)-table[len2][len1])/len(str1)
    return dist


class mytess:  # 2020.10.12 written by 최기훈
    '''
    input : image
    functon
    1. save_text : save the text
    '''

    def __init__(self, image, save_text=False):
        self.name = image.split('.')[0]
        self.img = cv2.imread(image)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        self.text = tess.image_to_string(self.img)
        self.boxes = tess.image_to_data(self.img)

    def save_text(self, text_name):
        '''
        save the text.

        input : text name
        output : text_name.txt
        '''
        f = open(text_name, 'w')

        for line in self.text.splitlines():
            f.write(line)
        f.close()

    # def save_boxes(self,table_name)

    def make_dict(self):
        '''
        make the dictionary.
        length of word > 3

        output = mytess.word_dict
        (format : {(x,y,w,h) : text}
        :rtype: object

        '''
        # boxes : tess.image_to_data output

        self.word_dict = {}
        for x, b in enumerate(self.boxes.splitlines()):
            if x == 0:
                continue
            b = b.split()
            m = re.match('\w\w\w\w+', b[-1])
            if m:
                self.word_dict[int(b[6]), int(b[7]), int(b[8]), int(b[9])] = m.group()

        return self.word_dict

    def find_danger(self, sanction_list, thresh=0.7, sort=False):
        '''
        make the danger_dict

        input : sanction list,threshold(default = 0.7)
        output : danger_dict
        (format :
            {sanction_word : {similar_word:[distance,[word position]]}}
        )
        '''
        danger = {}
        word_dict = self.word_dict
        for s_word in sanction_list:
            cand = []
            for place in word_dict:
                word = word_dict[place]
                dist = str_distance(s_word, word)
                if dist > thresh:
                    if s_word not in danger:
                        danger[s_word] = {word: [dist, place]}
                    else:
                        if word in danger[s_word]:
                            danger[s_word][word].append([dist, place])
                        else:
                            danger[s_word][word] = ([dist, place])
        if sort:
            for danger_word in danger:
                newdict = {}
                for word_ in sorted(danger[danger_word]):
                    newdict[word_] = danger[danger_word][word_]
                danger[danger_word] = newdict

        self.danger_dict = danger
        return self.danger_dict

    def make_box(self,save=False):
        for dangers in self.danger_dict.values():
            for danger in dangers:
                print(danger, dangers[danger])
                sim = danger
                x, y, w, h = dangers[danger][1][:]
                cv2.rectangle(self.img, (x, y), (w + x, y + h), (0, 0, 255), 2)
                word = sim + ' : ' + str(dangers[danger][0] * 100) + '%'
                cv2.putText(self.img, word, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 255), 2)
        cv2.imshow('img', self.img)
        if save:
            cv2.imwrite(self.name+'_boxed.jpg',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
