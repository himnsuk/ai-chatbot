import pandas as pd
import glob
import numpy as np
from rake_nltk import Rake
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

all_stopwords_gensim = STOPWORDS.union(set(['likes', 'explain', 'like', 'it\'s', 'tell']))


def extract_keyword(sen):
    keyword_list = create_n_grams(sen, dictionary_list)
    return keyword_list

def dataframe_reading_multiple_file(files_path, file_type, column_list, header_type):
    path = files_path

    dir_files = glob.glob(path + f"/*.{file_type}")

    final_df = pd.DataFrame(columns = column_list)

    for file_name in dir_files:
      print(file_name)
      temp_df = pd.read_csv(file_name, header=header_type)
      final_df = pd.concat([final_df,temp_df])
    return final_df

def create_n_grams(question, dictionary_directory):
  text = question
  tokens = word_tokenize(text.lower())
  tokens_without_sw = [word for word in tokens if not word in all_stopwords_gensim]
  filtered_unigram = [item for item in tokens_without_sw if item in dictionary_list]
  excluded_unigram = [item for item in tokens_without_sw if item not in dictionary_list]
  bigrams = list(ngrams(tokens,2))
  trigrams = list(ngrams(tokens,3))
  fourgrams = list(ngrams(tokens,4))
  fivegrams = list(ngrams(tokens,5))

  filterd_bigram = [" ".join(item) for item in bigrams if " ".join(item) in dictionary_list]
  filterd_trigram = [" ".join(item) for item in trigrams if " ".join(item) in dictionary_list]
  filterd_fourgram = [" ".join(item) for item in fourgrams if " ".join(item) in dictionary_list]

  combined_list = list(set(filtered_unigram + filterd_bigram + filterd_trigram + filterd_fourgram))
  return combined_list


if __name__ == "__main__":
    dictionary_directory = "chatbot/dictionaries"
    complete_dictionary = dataframe_reading_multiple_file(dictionary_directory, "txt", [], None)
    complete_dictionary = complete_dictionary.drop(1, axis=1)
    dictionary_list = complete_dictionary[0].tolist()

    question_path = "./csv-files/Question"
    columns_list = ['line', 'question', 'question_type']
    cdf = dataframe_reading_multiple_file(question_path, "csv", columns_list, 'infer')
    cdf['keywords'] = cdf.apply(lambda item: extract_keyword(item['question']), axis=1)
    cdf.to_csv("extracted_keywords2.csv", index=False)
