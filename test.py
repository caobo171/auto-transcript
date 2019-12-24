import speech_recognition as sr
import pydub
import itertools
from pydub import AudioSegment
from pydub.silence import split_on_silence , detect_silence

sound_file = AudioSegment.from_wav("test.wav")
not_silence_ranges = detect_silence(sound_file, 
    # must be silent for at least half a second
    min_silence_len= 100,

    # consider it silent if quieter than -16 dBFS
    silence_thresh= -20
)


def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

start_min = 0
sound_chunks = []
keep_silence = 100
for (start_i, end_i), (start_ii, end_ii) in pairwise(not_silence_ranges):
    end_max = end_i + (start_ii - end_i + 1)//2  # +1 for rounding with integer division
    start_i = max(start_min, start_i - keep_silence)
    end_i = min(end_max, end_i + keep_silence)

    sound_chunks.append({ 'start': start_i, 'duration': end_i - start_i})
    start_min = end_max


r = sr.Recognizer()


# sound = AudioSegment.from_mp3('test3.mp3')

# sound.export('test.wav', format='wav')



# CHUNK_DURATION = 60
# chunks = round(file_duration/CHUNK_DURATION)


# for i in range(0, chunks):
#     with sr.AudioFile('test.wav') as source:
#         audio = r.record(source, duration= min(CHUNK_DURATION, file_duration - CHUNK_DURATION*i ) , offset= i * CHUNK_DURATION ) 
#         text = r.recognize_google(audio,None, language='vi-VN')
#         print( i , len(text.split(' ') ))
#         print(text)

for i in range(0, len(sound_chunks)):
    with sr.AudioFile('test.wav') as source:
        print(sound_chunks[i]['duration'], sound_chunks[i]['start'])
        try:
                
            audio = r.record(source, duration= sound_chunks[i]['duration'], offset= sound_chunks[i]['start']) 
            text = r.recognize_google(audio,None, language='vi-VN')
            print(text)
        except:
            a = 0