from env import Env
from env.Solution import Solution
import cvxpy as cp


class ConvexSolution(Solution):
    """
    使用CVX求解目标问题
    """

    def __init__(self, env: Env) -> None:
        super().__init__('cvx_solution')
        self.__env = env

    def solve(self):
        super().solve()
