# coding:utf-8
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import jieba as jb
import re
import pymongo

mongo_client = pymongo.MongoClient(
    host='localhost',
    port=27017,
)
mongo_db = mongo_client["test"]


# 定义删除除字母,数字，汉字以外的所有符号的函数
def remove_punctuation(line):
    line = str(line)
    if line.strip() == '':
        return ''
    rule = re.compile(u"[^a-zA-Z0-9\u4E00-\u9FA5]")
    line = rule.sub('', line)
    return line


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords


df = pd.read_csv('counter_type.csv',encoding='utf-8')
df = df[['cat', 'review']]
# print("数据总量: %d ." % len(df))
# print(df.sample(10))
# print("在 cat 列中总共有 %d 个空值." % df['cat'].isnull().sum())
# print("在 review 列中总共有 %d 个空值." % df['review'].isnull().sum())

df = df[pd.notnull(df['review'])]
d = {'cat':df['cat'].value_counts().index, 'count': df['cat'].value_counts()}
df_cat = pd.DataFrame(data=d).reset_index(drop=True)
df['cat_id'] = df['cat'].factorize()[0]
cat_id_df = df[['cat', 'cat_id']].drop_duplicates().sort_values('cat_id').reset_index(drop=True)
cat_to_id = dict(cat_id_df.values)
id_to_cat = dict(cat_id_df[['cat_id', 'cat']].values)

# 加载停用词
stopwords = stopwordslist("chineseStopWords.txt")

# 删除除字母,数字，汉字以外的所有符号
df['clean_review'] = df['review'].apply(remove_punctuation)

# 分词，并过滤停用词
df['cut_review'] = df['clean_review'].apply(lambda x: " ".join([w for w in list(jb.cut(x)) if w not in stopwords]))


def chi2_check():
    tfidf = TfidfVectorizer(norm='l2', ngram_range=(1, 2))
    features = tfidf.fit_transform(df.cut_review)
    labels = df.cat_id
    N = 2
    for cat, cat_id in sorted(cat_to_id.items()):
        features_chi2 = chi2(features, labels == cat_id)
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(tfidf.get_feature_names())[indices]
        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        # mongo_db.chat.insert({'leibie':feature_names,'unigrams':unigrams[-N:],'bigrams':bigrams[-N:]})
        print("# '{}':".format(cat))
        print("  . Most correlated unigrams:\n       . {}".format('\n       . '.join(unigrams[-N:])))
        print("  . Most correlated bigrams:\n       . {}".format('\n       . '.join(bigrams[-N:])))
        # break
chi2_check()


# 朴素贝叶斯分类器，首先将Review转换成词频向量，然后将词频向量再转换成TF-IDF向量
# 两个步骤：1、生成词频向量，2、生成TF-IDF向量。最后开始训练MultinomialNB的分类器
# X_train, X_test, y_train, y_test = train_test_split(df['cut_review'], df['cat_id'], random_state=0)
# count_vect = CountVectorizer()
# X_train_counts = count_vect.fit_transform(X_train)
#
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#
# clf = MultinomialNB().fit(X_train_tfidf, y_train)
#
#
#
# def myPredict(sec):
#     format_sec=" ".join([w for w in list(jb.cut(remove_punctuation(sec))) if w not in stopwords])
#     pred_cat_id=clf.predict(count_vect.transform([format_sec]))
#     print(id_to_cat[pred_cat_id[0]])
#
#
# myPredict('感谢京东自营产地直采。你们把我质量关。第三次购买')