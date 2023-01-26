from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import numpy as np
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '76e6737ea96e4ee9defc29aa2d75830f'

CORS(app)
api = Api(app)

def rootValue(element,player,data):
	for item in data[player]:
		if element == item[0]:
			return item[1]

def spitItem(a, b):
	item1 = []
	for data in a:
		item1.append(data[0])
	
	item2 = []
	for data in b:
		item2.append(data[0])

	return item1, item2

def combination_cheker(a,b):
	passedValues = [0,1,2]

	for data in passedValues:

		itemValue1 = 0
		for item in a:
			itemValue1 += item[1]

		itemValue2 = 0
		for item in b:
			itemValue2 += item[1]

		if abs(itemValue1-itemValue2) == data:
			return 1
	
	return -1

def fair_process(a,b,data):
	temp1 = 0
	temp2 = 0

	size = range((len(a)-1)+1)[::-1]
	for i in size:
		temp1 = a[i]
		temp2 = b[i]

		value1 = temp1[1]
		value2 = temp2[1]
		
		a[i] = temp2
		b[i] = temp1

		a[i][1] = rootValue(a[i][0],'player1',data)
		b[i][1] = rootValue(b[i][0],'player2',data)

		if combination_cheker(a, b) != -1:
			return a, b
		else:
			a[i] = temp1
			b[i] = temp2

			a[i][1] = value1
			b[i][1] = value2

	return a, b

			
def alProcedure(data):
	favorPlayer = None
	output1, output2 = [], []

	itemSet1 = []
	for item in data['player1']:
		itemSet1.append(item[0])

	itemSet2 = []
	for item in data['player2']:
		itemSet2.append(item[0])

	i = 0
	while 1:
		if  len(itemSet1) == 0 or len(itemSet2) == 0:
			break

		if itemSet1[i] != itemSet2[i]:
			if itemSet1[i] not in output2:
				if itemSet2[i] not in output1:
					output1.append(itemSet1[i])
					output2.append(itemSet2[i])
					itemSet1.remove(itemSet1[i])
					itemSet2.remove(itemSet2[i])
				else:
					itemSet2.remove(itemSet2[i])
					favorPlayer = 'player2'
			else:
				itemSet1.remove(itemSet1[i])
				favorPlayer = 'player1'

		else:
			if favorPlayer == 'player1':
				output1.append(itemSet2[i])
				favorPlayer = 'player2'
			else:
				output2.append(itemSet1[i])
				favorPlayer = 'player1'
			
			itemSet1.remove(itemSet1[i])
			itemSet2.remove(itemSet2[i])


	while len(output1)!=len(output2):
		if favorPlayer == 'player1':
			output1.append(output2[-1])
			output2.remove(output2[-1])
		else:
			output2.append(output1[-1])
			output1.remove(output1[-1])
		
	initItems1 = []
	for item in data['player1']:
		if item[0] in output1:
			initItems1.append(item)

	initItems2 = []
	for item in data['player2']:
		if item[0] in output2:
			initItems2.append(item)

	result1, result2 = fair_process(initItems1, initItems2, data)

	return [result1,result2]

def Al_procedure_identical(data):
	favorPlayer = random.choice(['player1','plyer2'])
	playerTurn = [2,2]

	set1 = data['player1']
	set2 = data['player2']
	output1, output2 = [] ,[]

	if favorPlayer == 'player1':
		output1.append(set1[0])
		favorPlayer = 'player2'
	else:
		output2.append(set2[0])
		favorPlayer = 'player1'

	for i in range(1, len(set1)):
		if favorPlayer == 'player1':
			if playerTurn[0] != 0:
				output1.append(set1[i])
				playerTurn[0] -= 1
				
				if playerTurn[0] == 0:
					favorPlayer = 'player2'
					playerTurn[0] = 2
		else:
			if playerTurn[1] != 0:
				output2.append(set2[i])
				playerTurn[1] -= 1

				if playerTurn[1] == 0:
					favorPlayer = 'player1'
					playerTurn[1] = 2

	return [output1,output2]


class ProcessItems(Resource):
	def indenticalSet(self,data):

		set1 = np.array(data['player1']) 
		set2 = np.array(data['player2'])

		equal_arrays = (set1 == set2).all()
		return equal_arrays

	def post(self):
		data = request.get_json()
		print(data)
		if self.indenticalSet(data):
			return Al_procedure_identical(data)
		else:
			return alProcedure(data)	

api.add_resource(ProcessItems, "/alProcedure")

@app.route('/')
def index():
    return 'AL PROCEDURE API'


if __name__ == '__main__':
    app.run(debug=True, port=3000)