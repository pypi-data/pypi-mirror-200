from __future__ import annotations
import numpy as np
from pandas import DataFrame, Series
from scipy.optimize import linprog
from scipy.linalg import null_space
from itertools import product
from .utils import stable_type
from IPython.display import display, Markdown

class GameFrame(DataFrame):
    @classmethod
    def create(cls, payoff_table, row_player_strategies, col_player_strategies):
        return cls(payoff_table, index=row_player_strategies, columns=col_player_strategies)

    @stable_type
    def copy(self, *args, **kwargs) -> GameFrame:
        return super().copy(*args, **kwargs)

    def player2axis(self, player, axis=None) -> int:
        if axis is not None:
            return axis
        if player == "row":
            return 0
        elif player == "col":
            return 1
        raise ValueError("player can be only 'row' or 'col'!")

    @stable_type
    def player_table(self, player=None, axis=None) -> GameFrame:
        axis = self.player2axis(player, axis)
        return self.applymap(lambda x: x[axis])

    def player_matrix(self, **kwargs) -> np.matrix:
        return self.player_table(**kwargs).to_numpy()

    def find_elimination_idx(self, axis) -> int:
        player_table = self
        if axis == 0:
            player_table = player_table.T
        for j1, j2 in product(player_table.columns, repeat=2):
            if j1 == j2:
                continue
            if (player_table[j1] <= player_table[j2]).all():
                return j1
        return None

    def eliminate(self, display_progress=True, inplace=False) -> GameFrame:
        if not inplace:
            self = self.copy()
        step = 0
        while self.size > 1:
            for axis in (0, 1):
                step += 1
                player_table = self.player_table(axis=axis)
                minidx = player_table.find_elimination_idx(axis)
                if minidx is None:
                    return self
                self.drop(minidx, axis=axis, inplace=True)
                if display_progress:
                    display(Markdown(
                        f"### Step {step}: Eliminate {'row' if axis == 0 else 'column'}[{minidx}]"))
                    display(self)
        return self
    
    def player_best_responses(self,player='row') -> Series:
        axis = self.player2axis(player)
        return self.player_table(axis=axis).idxmax(axis=axis)
    
    @property
    def pure_nash_equilibriums(self):
        r2c = self.player_best_responses(player='col')
        c2r = self.player_best_responses(player='row')
        for r,c in r2c.items():
            if c2r.loc[c] == r:
                yield (r,c)
        
    def player_nash_equilibrium_mixed_strategies(self, player='row') -> DataFrame:
        M = self.player_matrix(player=player)
        axis = self.player2axis(player)
        if axis == 0:
            M = M.T
        w = null_space(np.concatenate([M, np.ones((len(M), 1))], axis=1))[:len(M)]
        w /= w.sum(axis=0)
        index = self.index if axis == 0 else self.columns
        return DataFrame(w, index=index)

    @property
    def row_player_nash_equilibrium_mixed_strategies(self) -> DataFrame:
        return self.player_nash_equilibrium_mixed_strategies(player='row')

    @property
    def col_player_nash_equilibrium_mixed_strategies(self) -> DataFrame:
        return self.player_nash_equilibrium_mixed_strategies(player='col')

    def game_value(self, row_player_strategy, col_player_strategy) -> DataFrame:
        return row_player_strategy.T@self@col_player_strategy


class ZeroSumGameFrame(GameFrame):
    @stable_type
    def player_table(self, player=None, axis=None) -> ZeroSumGameFrame:
        axis = self.player2axis(player, axis)
        sign = 1 if axis == 0 else -1
        return self.applymap(lambda x: sign*x)

    def player_matrix(self, **kwargs) -> np.matrix:
        return self.to_numpy()

    @property
    def row_player_mixed_strategy(self) -> Series:
        payoff_matrix = self.player_matrix()
        N = payoff_matrix.shape[0]
        result = linprog(np.ones(N), A_ub=-payoff_matrix.T, b_ub=-np.ones(N))
        w_x = result.x/np.sum(result.x)
        return Series(w_x, index=self.index)

    @property
    def col_player_mixed_strategy(self) -> Series:
        payoff_matrix = self.player_matrix()
        N = payoff_matrix.shape[1]
        result = linprog(-np.ones(N), A_ub=payoff_matrix, b_ub=np.ones(N))
        w_y = result.x/np.sum(result.x)
        return Series(w_y, index=self.columns)

    def row_player_payoff(self, strategy: Series) -> float:
        return np.min(strategy.T@self)

    def col_player_payoff(self, strategy: Series) -> float:
        return np.max(self@strategy)