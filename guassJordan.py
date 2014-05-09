import csv
import sys
from fractions import Fraction

#OPERACIONES BASICAS
def changeRow(matrix, rowA, rowB):
	tmp = matrix[rowA]
	matrix[rowA] = matrix[rowB]
	matrix[rowB] = tmp
	printMatrix(matrix, "R{} <--> R{}".format(rowA, rowB))

def sumRow(matrix, rowA, rowB, multiplier=1):
	if multiplier == 0:
		#sys.exit("Error: Invalid operation, can't multiply by 0...")
		return
	for x in range(len(matrix[rowA])):
		matrix[rowA][x] += multiplier*matrix[rowB][x]
	printMatrix(matrix, "R{0} <-- R{0} + ({2})R{1}".format(rowA, rowB, multiplier))

def multiplyRow(matrix, row, val):
	if val == 0:
		#sys.exit("Error: Invalid operation, can't multiply by 0...")
		return
	for x in range(len(matrix[row])):
		matrix[row][x] *= val
	printMatrix(matrix, "R{0} <-- ({1})R{0}".format(row, val))

#TERMINAN OPERACIONES BASICAS

def gaussJordan(matrix, fila):#No es necesario saber el tamaño de la columna
	selectPivot(matrix)
	for i in range(fila):
		createPivot(matrix, i)
		for row in range(fila):
			if row != i:
				sumRow(matrix, row, i, -1*Fraction(matrix[row][i]))
				'''
				if matrix[row][i] >= 0:
					sumRow(matrix, row, i, -1*Fraction(matrix[row][i]))
				else:
					sumRow(matrix, row, i, Fraction(matrix[row][i]))
				'''

def selectPivot(matrix):
	rowNum = 0
	for row in matrix:
		if row[0] != 0:
			if rowNum != 0:
				changeRow(matrix, 0,rowNum)
			return
		rowNum += 1
	sys.exit("Error: There's no pivot...")

def createPivot(matrix, i):
	multiplyRow(matrix, i, Fraction(matrix[i][i].denominator/matrix[i][i].numerator))

def printMatrix(matrix, msg="Matrix:"):
	print("\n" + msg + "\n")
	rowLen = len(matrix[0])
	for row in matrix:
		for x in range(rowLen):
			print("{:6}".format(row[x]), end=" ")
		print()
	print("\n" + "======="*rowLen)

def createMatrixFromFile(filename):
	with open(filename,'r') as file:
		try:
		    reader = csv.reader(file)
		    dimension = next(reader)
		    fila = int(dimension[0])
		    #columna = dimension[1]
		    #print dimension[0] #Filas
		    #print dimension[1] #Columnas
		    if int(dimension[1]) - int(dimension[0]) != 1:
		    	sys.exit("Error")#Si las dimensiones 
		    matrix = [[0 for x in range(int(dimension[1]))] for x in range(int(dimension[0]))]
		    x = y = 0
		    for row in reader:
		    	for val in row:
		    		matrix[x][y] = Fraction(float(val))
		    		y += 1
		    	x += 1
		    	y = 0
		except csv.Error as e:
			sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
	gaussJordan(matrix, fila)

###################################
#File format:
#2,3
#8,3,4
#4,1,6
####################################

#filename = input("Write the file name:")
matrix = createMatrixFromFile("matrix.txt")

