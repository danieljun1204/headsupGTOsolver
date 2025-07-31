import random
from collections import defaultdict
from .game_kuhn import deal, is_terminal, payoff, get_legal_actions

class InfoSet:
    #represents a decision point for a player
    def __init__(self, key, actions):
        self.key = key
        self.actions = actions
        self.regret_sum = {a: 0.0 for a in actions}
        #cumulative regret for not having played each other in the past
        self.strategy_sum = {a: 0.0 for a in actions}
        #cumulative weight of how often each action was played

    def get_strategy(self, realization_weight):
        #realization weight is how likely a player gets there
        pos_regrets = {a: max(r, 0) for a, r in self.regret_sum.items()}
        total_pos = sum(pos_regrets.values())
        if total_pos > 0:
            strat = {a: pos_regrets[a] / total_pos for a in self.actions}
        else:
            n = len(self.actions)
            strat = {a: 1.0/n for a in self.actions}
        for a in self.actions:
            self.strategy_sum[a] += realization_weight * strat[a]
        return strat

    def get_average_strategy(self):
        total = sum(self.strategy_sum.values())
        if total > 0:
            return {a: self.strategy_sum[a]/total for a in self.actions}
        else:
            n = len(self.actions)
            return {a: 1.0/n for a in self.actions}


class CFRTrainer:
    def __init__(self):
        self.node_map = {}

    def cfr(self, hist, p0, p1, cards):
        player = len(hist.split('-')) % 2
        if is_terminal(hist):
            return payoff(hist, cards)

        key = cards[player] + hist
        if key not in self.node_map:
            actions = get_legal_actions(hist)
            self.node_map[key] = InfoSet(key, actions)
        node = self.node_map[key]

        strat = node.get_strategy(p0 if player==0 else p1)
        util = {}
        node_util = 0.0
        for a in node.actions:
            next_h = hist + a if hist == '' else hist + '-' + a
            if player == 0:
                util[a] = -self.cfr(next_h, p0*strat[a], p1, cards)
            else:
                util[a] = -self.cfr(next_h, p0, p1*strat[a], cards)
            node_util += strat[a] * util[a]

        for a in node.actions:
            regret = util[a] - node_util
            if player == 0:
                node.regret_sum[a] += p1 * regret
            else:
                node.regret_sum[a] += p0 * regret

        return node_util

    def train(self, iterations=10_000, log_every=1_000):
        iters, infosets = [], []
        for i in range(1, iterations+1):
            cards = deal()
            self.cfr('', 1, 1, cards)
            #start fresh both player probability =1
            if i % log_every == 0:
                print(f"[{i}] infosets: {len(self.node_map)}")
                iters.append(i)
                infosets.append(len(self.node_map))
        return iters, infosets

    def get_strategy_profile(self):
        return {key: node.get_average_strategy() for key, node in self.node_map.items()}


if __name__ == '__main__':
    trainer = CFRTrainer()
    trainer.train(5_000, 500)

    print("\nFinal Strategy Profile:")
    profile = trainer.get_strategy_profile()
    for key, strat in sorted(profile.items()):
        print(f"{key}: {strat}")
