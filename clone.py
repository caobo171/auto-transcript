import argparse
import speech_recognition as sr
import pydub
import itertools
from pydub import AudioSegment

import editdistance


def checkHidden(text):
    for i in range(0, len(text)):
        if(text[i] != '-'):
            return False
    return True

r = sr.Recognizer()

parser = argparse.ArgumentParser()
parser.add_argument("--path")
args = parser.parse_args()
path = args.path

song = AudioSegment.from_mp3(path)
song.export('test.wav', format='wav')

file_duration = song.__len__()/1000
CHUNK_DURATION = 5
chunks = round(file_duration/CHUNK_DURATION)



# f = open("text2.txt", "r")

f = open("text2.txt", "r" , encoding="utf8")
origin_script_text = f.read()
script_text = origin_script_text.replace('.','',1000).replace('"','',10000).replace(':','',1000).replace(',','',1000).replace('“','',1000).replace('”','',1000)
script_text = script_text.split()

print(script_text)

text_array = []
for i in range(0, chunks):
    with sr.AudioFile('test.wav') as source:
        try:
            audio = r.record(source, 
                duration= min(CHUNK_DURATION, file_duration- CHUNK_DURATION * i),
                offset= CHUNK_DURATION * i
            )
            text = r.recognize_google(audio)
            r_text = ' '.join(text.split(' '))
      
                
            # print('----------')
            # print(r_text)
            text_array.append(r_text)
            # print('---end----')
        except:
            text_array.append(-1)



index_array = []
for text in text_array:    

    if(text == -1):
        index_array.append(-1)
    else:
        r_text = text.split()
        len_r_text = len(r_text)
        min_diff = 99999
        minIndex = -1
        for i in range( 0, len(script_text) - len_r_text + 1):
            compare_script = script_text[i : i + len_r_text  ]
            diff = 0 
            for j in range(0, len_r_text):
                if(checkHidden(compare_script[j])):
                    print('vo day roi')
                    if(len(compare_script[j]) != len(r_text[j])):
                        diff = diff + 1
                    else :
                        diff = diff -1
                else:
                    if(compare_script[j] != r_text[j]):
                        diff = diff + 2
                    else:
                        diff = diff - 2
            if( diff <= min_diff ):
                min_diff = diff
                minIndex = i
        index_array.append(minIndex)
        print(script_text[minIndex: minIndex + len_r_text] + ' vs ' + r_text)

last_result = []
increasing_before = 0
increasing_after = 0
for i in range(0, len(index_array)):
    if( i == 0 and index_array[i+1] < index_array[i] ):
        last_result.append(-1)
    elif (i == len(index_array) - 1 and index_array[i-1] > index_array[i]):
        last_result.append(-1)
    elif (index_array[i-1] > index_array[i] and index_array[i+1] < index_array[i]):
        last_result.append(-1)
    else:
        last_result.append(index_array[i])


print(last_result)
result = ''
current_index = 0
for  i in range(0, len(script_text)) :


    # if(current_index >= len(index_array)): 
    #     break
    
    for j, index in enumerate(index_array):
        if(i == index):
            result += '[{}]'.format(j * CHUNK_DURATION)
    result = result +  script_text[i] + ' '
    

            
    
# print('done !!')
