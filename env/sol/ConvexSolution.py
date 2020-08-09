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

    def trajectory(self, type, portion, bandwidth, frequency):
        """
        trajectory 根据给定的其他变量求解UAV轨迹
        """
        return

    def resource(self, trajectory, type, portion):
        """
        求解资源分配子问题
        """
        pass

    def offloading(self, trajectory, bandwidth, frequency):
        """
        求解卸载比例子问题
        """
        pass
