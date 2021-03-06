# -*- coding: utf-8 -*-
"""train_cycle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1idLFL3EgD7GOF6gQMq9iDuHDq9zLoN96
"""

from dual_network import dual_network
from self_play import self_play
from train_network import train_network
from evaluate_network import evaluate_network
from evaluate_best_player import evaluate_best_player

dual_network()

for _ in range(10):
    for i in range(10):
        print('Train', i, '======================')
        self_play()
        train_network()
        evaluate_network()
    evaluate_best_player()
