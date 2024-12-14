from Lab3.crossroad.data import GlobalData
from Lab3.crossroad.simulation import Game
from Lab3.crossroad.data import GlobalData
from Lab3.crossroad.data_analysis import DataAnalyzer
import os

game = Game()
game.run()

GlobalData.export_to_csv()

analyzer = DataAnalyzer(GlobalData)
analyzer.process()