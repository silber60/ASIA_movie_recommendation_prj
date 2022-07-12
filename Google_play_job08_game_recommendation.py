import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieIdx, 0]
    return recMovieList


df_reviews = pd.read_csv('Google_play_data/google_play_cleaned_review_one_2.csv')
Tfidf_matrix = mmread('./Google_play_models/Tfidf_game_review.mtx').tocsr()
with open('google_play_models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 영화 제목 / index를 이용
game_idx = df_reviews[df_reviews['games']=='배틀그라운드'].index[0]
# gameidx = 1003
cosine_sim = linear_kernel(Tfidf_matrix[game_idx], Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation[1:11])

# keyword 이용
# embedding_model = Word2Vec.load('./Google_play_models/word2vec_google_play_reviews_2.model')
# keyword = '자동차'
# sim_word = embedding_model.wv.most_similar(keyword, topn=10)
# words = [keyword]
# for word, _ in sim_word:
#     words.append(word)
# sentence = []
# count = 10
# for word in words:
#     sentence = sentence + [word] * count
#     count -= 1
# sentence = ' '.join(sentence)
# sentence_vec = Tfidf.transform([sentence])
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# 문장 이용
# okt = Okt()
# sentence = '화려한 액션과 소름 돋는 반전이 있는 영화'
# review = re.sub('[^가-힣 ]', ' ', sentence)
# #
# token = okt.pos(review, stem=True)
# #
# df_token = pd.DataFrame(token, columns=['word', 'class'])
# df_token = df_token[(df_token['class'] == 'Noun') |
#                     (df_token['class'] == 'Verb') |
#                     (df_token['class'] == 'Adjective')]
# words = []
# for word in df_token.word:
#     if 1 < len(word):
#         words.append(word)
# cleaned_sentence = ' '.join(words)
# print(cleaned_sentence)
# sentence_vec = Tfidf.transform([cleaned_sentence])
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)