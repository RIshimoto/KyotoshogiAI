# パッケージのインポート
import random
import math
from enum import IntEnum, auto

class Koma(IntEnum):
    EMP = 0
    KY = 1
    GI = 2
    KI = 3
    FU = 4
    OU = 5
    TO = 6
    KA = 7
    KE = 8
    HI = 9


BOARD_SIZE = 25
MAX = 500
# ゲームの状態
class State:
    # 初期化
    def __init__(self, pieces=None, enemy_pieces=None, depth=0):
        # 方向定数
        self.dxy = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1, -2), (-1, -2))

        # 駒の配置
        self.pieces = pieces if pieces != None else [0] * (25+9)
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * (25+9)
        self.depth = depth

        # 駒の初期配置
        if pieces == None or enemy_pieces == None:
            self.pieces = [
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.TO, Koma.GI, Koma.OU, Koma.KI, Koma.FU,
                0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.enemy_pieces = [
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP,
                Koma.TO, Koma.GI, Koma.OU, Koma.KI, Koma.FU, 
                0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 負けかどうか
    def is_lose(self):
        for i in range(BOARD_SIZE):
            if self.pieces[i] == Koma.OU: # 王の存在
                return False
        return True

    # 引き分けかどうか
    def is_draw(self):
        return self.depth >= MAX # 500手

    # ゲーム終了かどうか
    def is_done(self):
        return self.is_lose() or self.is_draw()

    # デュアルネットワークの入力の2次元配列の取得
    def pieces_array(self):
        # プレイヤー毎のデュアルネットワークの入力の2次元配列の取得
        def pieces_array_of(pieces):
            table_list = []
            for koma in Koma:
                if koma == Koma.EMP:
                    continue
                table = [0] * BOARD_SIZE
                table_list.append(table)
                for i in range(BOARD_SIZE):
                    if pieces[i] == koma:
                        table[i] = 1

            for koma in Koma:
                if koma == Koma.EMP:
                    continue
                flag = 1 if pieces[24+koma] > 0 else 0
                table = [flag] * BOARD_SIZE
                table_list.append(table)
            return table_list
        
        # デュアルネットワークの入力の2次元配列の取得
        return [pieces_array_of(self.pieces), pieces_array_of(self.enemy_pieces)]

    def promote(self, koma):
        if koma == Koma.OU:
            return koma
        return (koma + 5) % 10
        
    # 駒の移動先と移動元を行動に変換
    def position_to_action(self, position_src, position_dst):
        return position_dst * 34 + position_src

    # 行動を駒の移動先と移動元に変換
    def action_to_position(self, action):
        return (int(action / 34), action % 34)

    # 合法手のリストの取得
    def legal_actions(self):
        actions = []
        for p in range(BOARD_SIZE):
            # 駒の移動時
            if self.pieces[p] != Koma.EMP:
                actions.extend(self.legal_actions_pos(p))

            # 持ち駒の配置時
            if self.pieces[p] == Koma.EMP and self.enemy_pieces[24-p] == Koma.EMP:
                for capture in range(1, 10):
                    if self.pieces[24+capture] != Koma.EMP:
                        actions.append(self.position_to_action(24+capture, p))
        return actions

    # 駒の移動時の合法手のリストの取得
    def legal_actions_pos(self, position_src):
        canjamp = [0, 1, 0, 0, 0, 0, 0, 1, 0, 1]
        actions = []

        # 駒の移動可能な方向
        piece_type = self.pieces[position_src]
        if piece_type > 9: piece_type-9
        directions = []
        if piece_type == Koma.KY: # 香 
            directions = [0]
        elif piece_type == Koma.GI: # 銀
            directions = [0, 1, 3, 5, 7]
        elif piece_type == Koma.KI: # 金
            directions = [0, 1, 2, 4, 6, 7]
        elif piece_type == Koma.FU: # 歩
            directions = [0]
        elif piece_type == Koma.OU: # 王
            directions = [0, 1, 2, 3, 4, 5, 6, 7]
        elif piece_type == Koma.TO: # と
            directions = [0, 1, 2, 4, 6, 7]
        elif piece_type == Koma.KA: # 角
            directions = [1, 3, 5, 7]
        elif piece_type == Koma.KE: # 桂
            directions = [8, 9]
        elif piece_type == Koma.HI: # 飛車
            directions = [0, 2, 4, 6]

        # 合法手の取得
        for direction in directions:
            i = 1
            while True:
                # 駒の移動先
                x = position_src%5 + i * self.dxy[direction][0]
                y = int(position_src/5) + i * self.dxy[direction][1]
                p = x + y * 5

                # 移動可能時は合法手として追加
                if 0 <= x and x < 5 and 0 <= y and y < 5 and self.pieces[p] == Koma.EMP:
                    actions.append(self.position_to_action(position_src, p))
                    if self.enemy_pieces[24 - p] != Koma.EMP:
                        break
                else:
                    break
                if not canjamp[piece_type]:
                    break
                i+=1
        return actions

    # 次の状態の取得
    def next(self, action):
        # 次の状態の作成
        state = State(self.pieces.copy(), self.enemy_pieces.copy(), self.depth+1)
        if action != None:
            # 行動を(移動先, 移動元)に変換
            position_dst, position_src = self.action_to_position(action)

            # 駒の移動
            if position_src < 25:
                # 駒の移動
                state.pieces[position_dst] = self.promote(state.pieces[position_src])
                state.pieces[position_src] = Koma.EMP

                # 相手の駒が存在する時は取る
                piece_type = state.enemy_pieces[24-position_dst]
                if piece_type != Koma.EMP:
                    if piece_type != Koma.OU:
                        state.pieces[24+piece_type] += 1 # 持ち駒+1
                        state.pieces[24+self.promote(piece_type)] += 1 # 持ち駒+1
                    state.enemy_pieces[24-position_dst] = Koma.EMP

            # 持ち駒の配置
            else:
                capture = position_src - 25 + 1
                state.pieces[position_dst] = capture
                state.pieces[position_src] -= 1 # 持ち駒-1
                state.pieces[24+self.promote(capture)] -= 1 # 持ち駒-1

        """
        # 千日手かどうか
        sennitite = 1
        for history in self.history:
            if state == history:
                sennitite += 1
        if sennitite >= 4:
            print("千日手")
            state.depth = MAX # 500手

        # 盤面の記録
        state.history.append(state)
        """

        # 駒の交代
        w = state.pieces
        state.pieces = state.enemy_pieces
        state.enemy_pieces = w
        return state

    # 先手かどうか
    def is_first_player(self):
        return self.depth%2 == 0

    # 文字列表示
    def __str__(self):
        pieces0 = self.pieces  if self.is_first_player() else self.enemy_pieces
        pieces1 = self.enemy_pieces  if self.is_first_player() else self.pieces
        hzkr0 = ('', '$香', '$銀', '$金', '$歩', '$王', '$と', '$角', '$桂', '$飛')
        hzkr1 = ('', '\香', '\銀', '\金', '\歩', '\王', '\と', '\角', '\桂', '\飛')

        # 後手の持ち駒
        str = '['
        for i in range(25, 34):
            if pieces1[i] >= 2: str += hzkr1[i-24]
            if pieces1[i] >= 1: str += hzkr1[i-24]
        str += ']\n'

        # ボード
        for i in range(BOARD_SIZE):
            if pieces0[i] != 0:
                str += hzkr0[pieces0[i]]
            elif pieces1[24-i] != 0:
                str += hzkr1[pieces1[24-i]]
            else:
                str += ' ー'
            if i % 5 == 4:
                str += '\n'

        # 先手の持ち駒
        str += '['
        for i in range(25, 34):
            if pieces0[i] >= 2: str += hzkr0[i-24]
            if pieces0[i] >= 1: str += hzkr0[i-24]
        str += ']\n'
        return str

# ランダムで行動選択
def random_action(state):
    legal_actions = state.legal_actions()
    if len(legal_actions) == 0:
        return None
    return legal_actions[random.randint(0, len(legal_actions)-1)]

def playout(state):
  if state.is_lose():
    return -1
  if state.is_draw():
    return 0
  return -playout(state.next(random_action(state)))

def argmax(collection, key=None):
  return collection.index(max(collection))

def mcts_action(state):
  class Node:
    def __init__(self, state):
      self.state = state
      self.w = 0
      self.n = 0
      self.child_nodes = None

    def evaluate(self):
      if self.state.is_done():
        value = -1 if self.state.is_lose() else 0
      
        self.w += value
        self.n += 1
        return value
      
      if not self.child_nodes:
        value = playout(self.state)

        self.w += value
        self.n += 1

        if self.n == 10:
          self.expand()
        return value
      else:
        value = -self.next_child_node().evaluate()

        self.w += value
        self.n += 1
        return value
    
    def expand(self):
      legal_actions = self.state.legal_actions()
      self.child_nodes = []
      for action in legal_actions:
        self.child_nodes.append(Node(self.state.next(action)))

    def next_child_node(self):
      for child_node in self.child_nodes:
        if child_node.n == 0:
          return child_node
      # calc UCB1
      t = 0
      for c in self.child_nodes:
        t += c.n
      ucb1_values = []
      for child_node in self.child_nodes:
        ucb1_values.append(-child_node.w / child_node.n + (2 * math.log(t) / child_node.n) ** 0.5)
      
      return self.child_nodes[argmax(ucb1_values)]
      
  if state.depth <= 1:
    return random_action(state)

  root_node = Node(state)
  root_node.expand()

  for _ in range(100):
    root_node.evaluate()
  
  legal_actions = state.legal_actions()
  n_list = []
  for c in root_node.child_nodes:
    n_list.append(c.n)
  return legal_actions[argmax(n_list)]
         

def evaluate(state):
    komaValue = [0, 1, 1, 1, 1, 10000, 1, 2, 1, 2]
    eval = 0
    for i in range(25):
        eval += komaValue[state.pieces[i]]
        eval -= komaValue[state.enemy_pieces[i]]

    for i in range(25, 29):
        eval += komaValue[i - 24] * state.pieces[i]
        eval -= komaValue[i - 24] * state.enemy_pieces[i]
    return eval

def alpha_beta(state, alpha, beta, depth=0, depthMax=3):
    if depth >= depthMax:
        return evaluate(state)
  
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -beta, -alpha, depth+1)
        if score > alpha:
            alpha = score
        if alpha >= beta:
            return alpha
  
    return alpha

def alpha_beta_action(state):
    if state.depth <= 1:
        return random_action(state)
    best_action = 0
    alpha = -float('inf')
    str = ['', '']
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -float('inf'), -alpha)
        if score > alpha:
            best_action = action
            alpha = score

        """
        a, b = state.action_to_position(action)
        str[0] = '{}{:2d}{:2d},'.format(str[0], a, b)
        str[1] = '{}{:2d},'.format(str[1], score)
        print('action:', str[0], '\nscore:', str[1], '\n')
    """
    return best_action


# 動作確認
if __name__ == '__main__':
    state = State()
    while True:
        # ゲーム終了時
        if state.is_done():
            break
        # 次の状態の取得
        state = state.next(alpha_beta_action(state))

        # 文字列表示
        print(state)
        print()
