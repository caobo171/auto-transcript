import argparse
import speech_recognition as sr
import pydub
import itertools
from pydub import AudioSegment
import wave

import editdistance
import uuid
from longest_subsequence import LIS
import os 




def checkHidden(text):
    for i in range(0, len(text)):
        if(text[i] != '-'):
            return False
    return True

## Chunk là dùng xem mình làm bao nhiều một lượt 
## CHunk_duration là thời gian gửi lên google cloud

def googleAutoTranscript(mp3_file , origin_script_text , offset= 0, chunks = 5 , chunk_duration = 5):
    script_text = origin_script_text.replace('.','',1000).replace('"','',10000).replace(':','',1000).replace(',','',1000).replace('“','',1000).replace('”','',1000).replace("&#39;","'",1000)
    script_text = script_text.split()
    r = sr.Recognizer()
    song = AudioSegment.from_mp3(mp3_file)
    temp_file_path = './temp/{}.wav'.format(str(uuid.uuid1()))
    test= song.export(temp_file_path, format='wav')

    file_duration = song.__len__()/1000

    max_chunks = round(file_duration/chunk_duration)


    # using Google speech api to generate script
    text_array = []
    for i in range( offset , min( offset + chunks, max_chunks)):
        with sr.AudioFile(temp_file_path) as source:
            try:
                audio = r.record(source, 
                        duration= min(chunk_duration, file_duration - chunk_duration * i),
                        offset= chunk_duration * i
                    )
                    
                text = r.recognize_google(audio)
                print(text)
                r_text = ' '.join(text.split(' '))
                text_array.append(r_text)
            except:
                text_array.append(-1)
            source.audio_reader.close()


    # compare origin script with auto speech script
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

    last_result = LIS(index_array)
    print(temp_file_path)
    os.remove(temp_file_path)

    ## concatenate string array to result
    result = ''
    for  i in range(0, len(script_text)) :

        for j, index in enumerate(last_result):
            if(i == index):
                result = result + '[{}]'.format( (j + offset) * chunk_duration )
                break
            
        result = result +  script_text[i] + ' '
    if(offset + chunks >= max_chunks):
        return result, True
    else:
        return result, False

def googleAutoTranscriptV2(mp3_file , origin_script_text , offset= 0, chunks = 5 , chunk_duration = 5):
    script_text = origin_script_text.replace('.','',1000).replace('"','',10000).replace(':','',1000).replace(',','',1000).replace('“','',1000).replace('”','',1000).replace("&#39;","'",1000)
    script_text = script_text.split()
    r = sr.Recognizer()
    song = AudioSegment.from_mp3(mp3_file)
    temp_file_path = './temp/{}.wav'.format(str(uuid.uuid1()))
    test= song.export(temp_file_path, format='wav')

    file_duration = song.__len__()/1000

    max_chunks = round(file_duration/chunk_duration)


    # using Google speech api to generate script
    text_array = []
    for i in range( 0 , max_chunks):
        with sr.AudioFile(temp_file_path) as source:
            try:
                audio = r.record(source, 
                        duration= min(chunk_duration, file_duration - chunk_duration * i),
                        offset= chunk_duration * i
                    )
                    
                text = r.recognize_google(audio)
                print(text)
                r_text = ' '.join(text.split(' '))
                text_array.append(r_text)
            except:
                text_array.append(-1)
            source.audio_reader.close()


    # compare origin script with auto speech script
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

    last_result = LIS(index_array)
    os.remove(temp_file_path)

    ## concatenate string array to result
    result = ''
    for  i in range(0, len(script_text)) :

        for j, index in enumerate(last_result):
            if(i == index):
                result = result + '[{}]'.format( (j + offset) * chunk_duration )
                break
            
        result = result +  script_text[i] + ' '
    if(offset + chunks >= max_chunks):
        return result, True
    else:
        return result, True



