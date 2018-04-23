import treePlotter
import trees

fr = open('lenses.txt')
lines = fr.readlines()
lenses = [ inst.strip().split('\t') for inst in lines]
lensesLabels = ['age', 'perscript', 'astigmatic', 'tearRate']
lensesTree = trees.createTree(lenses, lensesLabels)
treePlotter.createPlot(lensesTree)
