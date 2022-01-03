import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
import json

class fifteenthItem():

    def __init__(self, continentColumn, continentName, countryColumn, countryName, stateColumn, stateName, casesColumn, dayColumn, predictionDay, data):
        self.continentColumn = continentColumn
        self.continentName = continentName
        self.countryColumn = countryColumn
        self.countryName = countryName
        self.stateColumn = stateColumn
        self.stateName = stateName
        self.casesColumn = casesColumn
        self.dayColumn = dayColumn
        self.predictionDate = predictionDay
        self.data = data

    def dataFilter(self):
        if(self.continentColumn != ''):
            isContinent = self.data[self.continentColumn] == self.continentName
            self.data = self.data[isContinent]
        if(self.countryColumn != ''):
            isCountry = self.data[self.countryColumn] == self.countryName
            self.data = self.data[isCountry]
        if(self.stateColumn != ''):
            isState = self.data[self.stateColumn] == self.stateName
            self.data = self.data[isState]

    def analysis(self):
        transformedDate = []
        for date in self.data[self.dayColumn]:
            formatedDate = datetime.now()
            try:
                formatedDate = datetime.strptime(date, '%d/%m/%Y')
            except:
                formatedDate = datetime.strptime(date, '%Y/%m/%d')
            transformedDate.append(int(datetime.timestamp(formatedDate)))
        self.data[self.dayColumn] = transformedDate
        x = np.asarray(self.data[self.dayColumn]).reshape(-1, 1)
        y = self.data[self.casesColumn]
        formatedDate = datetime.now()
        try:
            formatedDate = datetime.strptime(self.predictionDate, '%d-%m-%Y')
        except:
            formatedDate = datetime.strptime(self.predictionDate, '%Y-%m-%d')
        xToPredict = int(datetime.timestamp(formatedDate))
        regr = linear_model.LinearRegression()
        regr.fit(x, y)
        pred = regr.predict(x)
        prediction = regr.predict([[xToPredict]])
        mse = mean_squared_error(y, pred)
        coef = regr.coef_
        r2 = r2_score(y, pred)
        labels = []
        for label in x:
            dt_obj = datetime.fromtimestamp(label[0]).strftime('%d-%m-%y')
            labels.append(dt_obj)
        setValues = []
        for value in y:
            setValues.append(value)
        predictedValues = []
        for value in pred:
            predictedValues.append(value)
        jsonString = self.generateJSON(labels, setValues, predictedValues, formatedDate, prediction, mse, r2, coef)
        return jsonString

    def generateJSON(self, labels, setValues, predictedValues, formatedDate, prediction, mse, r2, coef):
        labelsOutput = '"labels": ['
        contador = 0
        for label in labels:
            if contador == 0:
                labelsOutput += '"' + str(label) + '"'
            else:
                labelsOutput += ', "' + str(label) + '"'
            contador += 1
        labelsOutput += '], '
        setValuesOutput = '"setValues": ['
        contador = 0
        for value in setValues:
            if contador == 0:
                setValuesOutput += '"' + str(value) + '"'
            else:
                setValuesOutput += ', "' + str(value) + '"'
            contador += 1
        setValuesOutput += '], '
        predictedValuesOutput = '"predictedValues": ['
        contador = 0
        for value in predictedValues:
            if contador == 0:
                predictedValuesOutput += '"' + str(value) + '"'
            else:
                predictedValuesOutput += ', "' + str(value) + '"'
            contador += 1
        predictedValuesOutput += '], '
        graphName = '"graphName": "Tendencia de casos confirmados de Coronavirus en ' + self.stateName + ', ' + self.countryName + '", '
        conclutionOutput = self.generateConclution(formatedDate, prediction, mse, r2, coef)
        output = '{' + labelsOutput + setValuesOutput + predictedValuesOutput + graphName + conclutionOutput + '}'
        return json.loads(output)

    def generateConclution(self, formatedDate, prediction, mse, r2, coef):
        output = '"conclution": {'
        header = '"header": ["Eleazar Jared Lopez Osuna", "Facultad de Ingenieria", "Universidad de San Carlos de Guatemala", "Guatemala, Guatemala", "eleazarjlopezo@gmail.com"],'
        leftColumn = '"leftColumn": "'
        leftColumn += '   En base a la informacion proporcionada y aplicando metodos analiticos mediante el uso de software, se obtuvieron los '
        leftColumn += 'siguientes valores: \\nEl coeficiente de regresion lineal obtenido '
        leftColumn += 'fue de ' + str(coef) + '\\nEl error cuadratico medio (ECM) es de ' + str(mse)
        leftColumn += '\\nLa prediccion obtenida para la fecha ' + str(formatedDate) + ' es de ' + str(prediction) + ' casos confirmados.", '
        rightColumn = '"rightColumn": "   Mediante el uso de librerias tales como pandas, sklearn, scipy, numpy y flask '
        rightColumn += 'y los datos proporcionados, se creo un modelo de regresion lineal el cual es capaz de realizar predicciones '
        rightColumn += 'sobre el comportamiento de los casos confirmados en ' + str(self.countryName) + '. El modelo tiene un coeficiente de determinacion de '
        rightColumn += str(r2) + ' lo cual indica que '
        rightColumn += 'el modelo esta ajustado de manera correcta." ' if(r2 > 0.7) else 'el modelo no esta ajustado de la mejor manera."'
        output += header + leftColumn + rightColumn + '}'
        return output