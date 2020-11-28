import string
import random
from datetime import datetime
import moviepy.editor as mp
import os
import time
import azure.cognitiveservices.speech as speechsdk
import wave
from scipy.io import wavfile
import numpy as np
from moviepy.audio.AudioClip import AudioArrayClip
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from chatbot.schemas.model import *


def clipVideo(video_file_path, wav_file_path):
  clip = mp.VideoFileClip(video_file_path).subclip(0,900)
  clip.audio.write_audiofile(wav_file_path)

def speech_recognize_continuous_from_file(text_file_path, wav_file_path, subscription_key, region):
  """performs continuous speech recognition with input from an audio file"""
  f=open(text_file_path,"w+")
  speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
  audio_config = speechsdk.audio.AudioConfig(filename=wav_file_path)

  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

  done = False

  def stop_cb(evt):
    """callback that signals to stop continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    nonlocal done
    done = True

  all_results = []
  def handle_final_result(evt):
    all_results.append(evt.result.text)
      
  print("All Results", all_results)
  speech_recognizer.recognized.connect(handle_final_result)
  # Connect callbacks to the events fired by the speech recognizer
  speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
  speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
  speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
  speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
  speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
  # stop continuous recognition on either session stopped or canceled events
  speech_recognizer.session_stopped.connect(stop_cb)
  speech_recognizer.canceled.connect(stop_cb)

  # Start continuous speech recognition
  speech_recognizer.start_continuous_recognition()
  while not done:
    time.sleep(.5)

  speech_recognizer.stop_continuous_recognition()
  
  f.write('\n'.join(all_results))
  f.close()

def create_n_grams(text_file_path, stats_dictionary_path):
  fObj = open(text_file_path, encoding = "utf8")
  text = fObj.read()

  dict = open(stats_dictionary_path, encoding = "utf8")
  stat_dict = dict.read()
  stat_dict_list = stat_dict.split(",\n")
  tokens = word_tokenize(text.lower())
  tokens_without_sw = [word for word in tokens if not word in stop_words]
  filtered_unigram = [item for item in tokens_without_sw if item in stat_dict_list]
  excluded_unigram = [item for item in tokens_without_sw if item not in stat_dict_list]
  bigrams = list(ngrams(tokens,2))
  trigrams = list(ngrams(tokens,3))
  fourgrams = list(ngrams(tokens,4))
  fivegrams = list(ngrams(tokens,5))

  filterd_bigram = [" ".join(item) for item in bigrams if " ".join(item) in stat_dict_list]
  excluded_bigram = [" ".join(item) for item in bigrams if " ".join(item) not in stat_dict_list]

  filterd_trigram = [" ".join(item) for item in trigrams if " ".join(item) in stat_dict_list]
  excluded_trigram = [" ".join(item) for item in trigrams if " ".join(item) not in stat_dict_list]

  filterd_fourgram = [" ".join(item) for item in fourgrams if " ".join(item) in stat_dict_list]

  combined_list = list(set(filtered_unigram + filterd_bigram + filterd_trigram + filterd_fourgram))
  excluded_list = list(set(excluded_unigram + excluded_bigram + excluded_trigram))
  return (combined_list, excluded_list)


def create_db_entries(keywords):
  random_email_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8)) + "@example.com"
  f_name = ''.join(random.choices(string.ascii_uppercase, k=8))
  l_name = ''.join(random.choices(string.ascii_uppercase, k=8))
  m_number = ''.join(random.choices(string.digits, k=10))
  (combined_list, excluded_list) = keywords
  stu = Student(email = random_email_name, \
                first_name = f_name,\
                last_name = l_name,\
                mobile_number = m_number,\
                created_time = datetime.datetime.now())
  db.session.add(stu)
  db.session.commit()

  course = Course(course_name = "Introduction to statistics",\
                course_link = "https://aispry.com/",\
                course_landing_page = "https://aispry.com/",\
                created_time = datetime.datetime.now())
  db.session.add(course)
  db.session.commit()

  stu.subscription.append(course)
  db.session.commit()

  course_module = CourseModule(course_id = course.course_id,\
                module_name = "Module 1",\
                module_link = "https://aispry.com/module-17",\
                tags = [],\
                excluded_tags = excluded_list,\
                generated_tags = combined_list,\
                admin_approved = False,\
                created_time = datetime.datetime.now())
  db.session.add(course_module)
  db.session.commit()

def deleteTempFiles(path):
  if os.path.exists(path):
    os.remove(path)
  else:
    print("The file does not exist")

# Run script with parameters provide
def main():
  video_file_path = "chatbot/static/videos/Session2_26th_Jan2020.mp4"
  wav_file_path = "chatbot/ml_models/temp/15_minute_clip.wav"
  text_file_path = "chatbot/ml_models/temp/15_minute_text.txt"
  stats_dictionary_path = "chatbot/dictionaries/statistics.txt"
  subscription_key = "212843fb99f64ebfbd53855bab4e7bcc"
  region = "centralindia"
  clipVideo(video_file_path, wav_file_path)
  speech_recognize_continuous_from_file(text_file_path, wav_file_path, subscription_key, region)
  keywords = create_n_grams(text_file_path, stats_dictionary_path)
  print(keywords)
  create_db_entries(keywords)
  deleteTempFiles(wav_file_path)
  deleteTempFiles(text_file_path)

if __name__ == "__main__":
  main()
