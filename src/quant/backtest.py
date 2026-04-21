"""
回测模块
"""


class Backtester:
    """回测引擎"""

    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data

    def run(self):
        """运行回测"""
        pass
