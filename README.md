# KyotoshogiAI
## 概要
卒業論文の際に制作したAlphaZero[^1]アルゴリズムを用いた京都将棋[^2]のゲームAIです。</br>
[^1]:https://ja.wikipedia.org/wiki/AlphaZero
[^2]:https://ja.wikipedia.org/wiki/%E4%BA%AC%E9%83%BD%E5%B0%86%E6%A3%8B

## プレゼンスライド

https://github.com/RIshimoto/KyotoshogiAI/blob/main/%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89.pdf

## デモ

https://user-images.githubusercontent.com/57135683/210591241-84f426a5-ecc7-4506-a2ca-3945aacdc262.mp4


## インストール
```
$ git clone https://github.com/RIshimoto/KyotoshogiAI
$ cd KyotoshogiAI
$ conda create -n kyotoshogi python=3.9
$ conda activate kyotoshogi
(kyotoshogi)$ pip install .
```
### プレイ
```
(kyotoshogi)$ play
```

### 学習
```
(kyotoshogi)$ train
```

# 参考文献 
布留川 英一, 2019.『AlphaZero 深層学習・強化学習・探索 人工知能プログラミング実践入門』 ボーンデジタル
