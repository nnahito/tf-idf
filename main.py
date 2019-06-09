# -*- coding: utf-8 -*-
import csv
import numpy as np
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfTransformer

# ========================================
# TF-IDFのベクトル空間の作成
# ========================================

# 同名のラベルは文章をつなぎ合わせながら、CSVファイル読み込む
studies = {}
with open('studies.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # 余計な改行やスペースを省いて取得
        label = row[0].replace('\n', '').replace('\r', '').replace('\s', '').replace(' ', '').replace('　', '')
        text = row[1].replace('\n', '').replace('\r', '').replace('\s', '').replace(' ', '').replace('　', '')

        if not (label in studies):
            # まだ変数に追加されていないラベルデータの場合
            studies[label] = text
        else:
            # すでに変数にデータが有れば、本文テキストを末尾に追加する
            studies[label] += text

# 全データに対して形態素解析を行う
tokenizer = Tokenizer()
corpus = []
for key in studies:
    # 分かち書き
    wakachi = tokenizer.tokenize(studies[key], wakati=True)
    # list -> ホワイトスペース区切りの文字列
    corpus.append(' '.join(wakachi))

# TF-IDFの計算
vectorizer = CountVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
transformer = TfidfTransformer()
tf = vectorizer.fit_transform(corpus)
tfidf = transformer.fit_transform(tf)

# コサイン類似度算出時のリスト用に、labelをlistに紐付ける
label_list = [label for label in studies]

# ========================================
# テスト
# ========================================
sample = """
八年まえの事でありました。当時、私は極めて懶惰な帝国大学生でありました。一夏を、東海道三島の宿で過したことがあります。五十円を故郷の姉から、これが最後だと言って、やっと送って戴き、私は学生鞄に着更の浴衣やらシャツやらを詰め込み、それを持ってふらと、下宿を立ち出で、そのまま汽車に乗りこめばよかったものを、方角を間違え、馴染みのおでんやにとびこみました。其処には友達が三人来合わせて居ました。やあ、やあ、めかして何処へ行くのだと、既に酔っぱらっている友人達は、私をからかいました。私は気弱く狼狽して、いや何処ということもないんだけど、君たちも、行かないかね、と心にも無い勧誘がふいと口から辷り出て、それからは騎虎の勢で、僕にね、五十円あるんだ、故郷の姉から貰ったのさ、これから、みんなで旅行に出ようよ、なに、仕度なんか要らない、そのままでいいじゃないか、行こう、行こう、とやけくそになり、しぶる友人達を引張るようにして連れ出してしまいました。あとは、どうなることか、私自身にさえわかりませんでした。あの頃は私も、随分、呑気なところのある子供でした。世の中も亦、私達を呑気に甘えさせてくれていました。私は、三島に行って小説を書こうと思って居たのでした。三島には高部佐吉さんという、私より二つ年下の青年が酒屋を開いて居たのです。佐吉さんの兄さんは沼津で大きい造酒屋を営み、佐吉さんは其の家の末っ子で、私とふとした事から知合いになり、私も同様に末弟であるし、また同様に早くから父に死なれている身の上なので
"""
# 分かち書きしたものをリストに入れて渡す
wakachi = tokenizer.tokenize(sample.strip(), wakati=True)
sample_tf = vectorizer.transform([' '.join(wakachi)])
# TF-IDFを計算する
sample_tfidf = transformer.transform(sample_tf)
# コサイン類似度の計算
similarity = cosine_similarity(sample_tfidf, tfidf)[0]
# 類似度の高い順にlistのkeyを取得
similarity_key = np.argsort(similarity)

for key in similarity_key:
    print(label_list[key])