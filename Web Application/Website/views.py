from flask import Blueprint, request, render_template, make_response
import ahpy
import itertools
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/introduction')
def introduction():
    return render_template("introduction.html")


@views.route('/pairwisecomparison')
def pairwisecomparison():
    return render_template('pairwisecomparison.html')


@views.route('/calculationandresult', methods=['POST'])
def calculationandresult():
    selected_options = request.form.getlist('comparison')
    criteria_comparisons = {
        ('accuracy', 'coveragearea'): selected_options[0],
        ('accuracy', 'powerconsumption'): selected_options[1],
        ('accuracy', 'cost'): selected_options[2],
        ('accuracy', 'scalability'): selected_options[3],
        ('accuracy', 'responsetime'): selected_options[4],
        ('accuracy', 'robustness'): selected_options[5],

        ('coveragearea', 'powerconsumption'): selected_options[6],
        ('coveragearea', 'cost'): selected_options[7],
        ('coveragearea', 'scalability'): selected_options[8],
        ('coveragearea', 'responsetime'): selected_options[9],
        ('coveragearea', 'robustness'): selected_options[10],

        ('powerconsumption', 'cost'): selected_options[11],
        ('powerconsumption', 'scalability'): selected_options[12],
        ('powerconsumption', 'responsetime'): selected_options[13],
        ('powerconsumption', 'robustness'): selected_options[14],

        ('cost', 'scalability'): selected_options[15],
        ('cost', 'responsetime'): selected_options[16],
        ('cost', 'robustness'): selected_options[17],

        ('scalability', 'responsetime'): selected_options[18],
        ('scalability', 'robustness'): selected_options[19],

        ('responsetime', 'robustness'): selected_options[20]
    }
    criteria = ahpy.Compare(name='criteria', comparisons=criteria_comparisons,
                            precision=3, random_index='saaty')


# technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1,
                       3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3, 9, 3, 9, 1 / 7)
    accuracy_comparisons = dict(zip(alternative_pairs, accuracy_values))

    coveragearea_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9,
                           1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9, 5)
    coveragearea_comparisons = dict(zip(alternative_pairs, coveragearea_values))

    powerconsumption_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5,
                               1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3, 5)
    powerconsumption_comparisons = dict(zip(alternative_pairs, powerconsumption_values))

    cost_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost_comparisons = dict(zip(alternative_pairs, cost_values))

    scalability_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability_comparisons = dict(zip(alternative_pairs, scalability_values))

    responsetime_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5,
                           1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5, 5)
    responsetime_comparisons = dict(zip(alternative_pairs, responsetime_values))

    robustness_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3,
                         1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    robustness_comparisons = dict(zip(alternative_pairs, robustness_values))

    accuracy = ahpy.Compare('accuracy', accuracy_comparisons, precision=3)
    coveragearea = ahpy.Compare('coveragearea', coveragearea_comparisons, precision=3)
    powerconsumption = ahpy.Compare('powerconsumption', powerconsumption_comparisons, precision=3)
    cost = ahpy.Compare('cost', cost_comparisons, precision=3)
    scalability = ahpy.Compare('scalability', scalability_comparisons, precision=3)
    responsetime = ahpy.Compare('responsetime', responsetime_comparisons, precision=3)
    robustness = ahpy.Compare('robustness', robustness_comparisons, precision=3)

    criteria.add_children([accuracy, coveragearea, powerconsumption, cost, scalability, responsetime,
                           robustness])


# Data for graph of criteria weights
    data = [
        ("Accuracy", accuracy.global_weight),
        ("Cost", cost.global_weight),
        ("Robustness", robustness.global_weight),
        ("Coverage Area", coveragearea.global_weight),
        ("Response Time", responsetime.global_weight),
        ("Power Consumption", powerconsumption.global_weight),
        ("Scalability", scalability.global_weight),
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    # Data for graph of technology recommendation

    data9 = [
        (alternative, weight) for alternative, weight in criteria.target_weights.items() if
        alternative in alternatives
    ]

    labelsrecommendation = [row[0] for row in data9]
    valuesrecommendation = [row[1] for row in data9]

    # ############################################### ACCURACY increase 20%

    sensitivity1_comparisons = {
        ('accuracy1', 'coveragearea1'): selected_options[0] + "2",
        ('accuracy1', 'powerconsumption1'): selected_options[1] + "2",
        ('accuracy1', 'cost1'): selected_options[2] + "2",
        ('accuracy1', 'scalability1'): selected_options[3] + "2",
        ('accuracy1', 'responsetime1'): selected_options[4] + "2",
        ('accuracy1', 'robustness1'): selected_options[5] + "2",

        ('coveragearea1', 'powerconsumption1'): selected_options[6],
        ('coveragearea1', 'cost1'): selected_options[7],
        ('coveragearea1', 'scalability1'): selected_options[8],
        ('coveragearea1', 'responsetime1'): selected_options[9],
        ('coveragearea1', 'robustness1'): selected_options[10],

        ('powerconsumption1', 'cost1'): selected_options[11],
        ('powerconsumption1', 'scalability1'): selected_options[12],
        ('powerconsumption1', 'responsetime1'): selected_options[13],
        ('powerconsumption1', 'robustness1'): selected_options[14],

        ('cost1', 'scalability1'): selected_options[15],
        ('cost1', 'responsetime1'): selected_options[16],
        ('cost1', 'robustness1'): selected_options[17],

        ('scalability1', 'responsetime1'): selected_options[18],
        ('scalability1', 'robustness1'): selected_options[19],

        ('responsetime1', 'robustness1'): selected_options[20]
    }
    sensitivity1 = ahpy.Compare(name='sensitivity1', comparisons=sensitivity1_comparisons, precision=3,
                                random_index='saaty')

    # technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy1_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1, 3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3,
                        9, 3, 9, 1 / 7)
    accuracy1_comparisons = dict(zip(alternative_pairs, accuracy1_values))

    coveragearea1_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9, 1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9,
                            5)
    coveragearea1_comparisons = dict(zip(alternative_pairs, coveragearea1_values))

    powerconsumption1_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5, 1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3,
                                5)
    powerconsumption1_comparisons = dict(zip(alternative_pairs, powerconsumption1_values))

    cost1_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost1_comparisons = dict(zip(alternative_pairs, cost1_values))

    scalability1_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability1_comparisons = dict(zip(alternative_pairs, scalability1_values))

    responsetime1_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5,
                            5)
    responsetime1_comparisons = dict(zip(alternative_pairs, responsetime1_values))

    robustness1_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1,
                          1, 1, 1)
    robustness1_comparisons = dict(zip(alternative_pairs, robustness1_values))

    accuracy1 = ahpy.Compare('accuracy1', accuracy1_comparisons, precision=3)
    coveragearea1 = ahpy.Compare('coveragearea1', coveragearea1_comparisons, precision=3)
    powerconsumption1 = ahpy.Compare('powerconsumption1', powerconsumption1_comparisons, precision=3)
    cost1 = ahpy.Compare('cost1', cost1_comparisons, precision=3)
    scalability1 = ahpy.Compare('scalability1', scalability1_comparisons, precision=3)
    responsetime1 = ahpy.Compare('responsetime1', responsetime1_comparisons, precision=3)
    robustness1 = ahpy.Compare('robustness1', robustness1_comparisons, precision=3)

    sensitivity1.add_children([accuracy1, coveragearea1, powerconsumption1, cost1, scalability1, responsetime1,
                               robustness1])

    # Data for accuracy sensitivity graph

    data2 = [
        (alternative, weight) for alternative, weight in sensitivity1.target_weights.items() if
        alternative in alternatives
    ]

    labels2 = [row[0] for row in data2]
    values2 = [row[1] for row in data2]

    # ################################################################### COVERAGE AREA increase 20%

    if selected_options[0] == "1":
        # Wenn selected_options[0] gleich 1 ist, soll es zu 1/3 werden
        accuracy_coveragearea_value = 0.333
    elif selected_options[0] > "1":
        # Wenn selected_options[0] größer als 1 ist, dann subtrahiere 2
        accuracy_coveragearea_value = float(selected_options[0]) - 2
    elif selected_options[0] == "0.333":
        # Wenn selected_options[0] gleich 1/3 ist, soll es zu 1/5 werden
        accuracy_coveragearea_value = 0.2
    elif selected_options[0] == "0.2":
        # Wenn selected_options[0] gleich 1/5 ist, soll es zu 1/7 werden
        accuracy_coveragearea_value = 0.1428
    elif selected_options[0] == "0.1428":
        # Wenn selected_options[0] gleich 1/7 ist, soll es zu 1/9 werden
        accuracy_coveragearea_value = 0.111
    else:
        # Wenn selected_options[0] gleich 1/9 ist, soll es so bleiben
        accuracy_coveragearea_value = selected_options[0]

    sensitivity2_comparisons = {
        ('accuracy2', 'coveragearea2'): accuracy_coveragearea_value,
        ('accuracy2', 'powerconsumption2'): selected_options[1],
        ('accuracy2', 'cost2'): selected_options[2],
        ('accuracy2', 'scalability2'): selected_options[3],
        ('accuracy2', 'responsetime2'): selected_options[4],
        ('accuracy2', 'robustness2'): selected_options[5],

        ('coveragearea2', 'powerconsumption2'): selected_options[6] + "2",
        ('coveragearea2', 'cost2'): selected_options[7] + "2",
        ('coveragearea2', 'scalability2'): selected_options[8] + "2",
        ('coveragearea2', 'responsetime2'): selected_options[9] + "2",
        ('coveragearea2', 'robustness2'): selected_options[10] + "2",

        ('powerconsumption2', 'cost2'): selected_options[11],
        ('powerconsumption2', 'scalability2'): selected_options[12],
        ('powerconsumption2', 'responsetime2'): selected_options[13],
        ('powerconsumption2', 'robustness2'): selected_options[14],

        ('cost2', 'scalability2'): selected_options[15],
        ('cost2', 'responsetime2'): selected_options[16],
        ('cost2', 'robustness2'): selected_options[17],

        ('scalability2', 'responsetime2'): selected_options[18],
        ('scalability2', 'robustness2'): selected_options[19],

        ('responsetime2', 'robustness2'): selected_options[20]
    }
    sensitivity2 = ahpy.Compare(name='sensitivity2', comparisons=sensitivity2_comparisons,
                                precision=3, random_index='saaty')

    # technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy2_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1,
                        3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3, 9, 3, 9, 1 / 7)
    accuracy2_comparisons = dict(zip(alternative_pairs, accuracy2_values))

    coveragearea2_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9,
                            1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9, 5)
    coveragearea2_comparisons = dict(zip(alternative_pairs, coveragearea2_values))

    powerconsumption2_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5,
                                1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3, 5)
    powerconsumption2_comparisons = dict(zip(alternative_pairs, powerconsumption2_values))

    cost2_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost2_comparisons = dict(zip(alternative_pairs, cost2_values))

    scalability2_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability2_comparisons = dict(zip(alternative_pairs, scalability2_values))

    responsetime2_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5,
                            1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5, 5)
    responsetime2_comparisons = dict(zip(alternative_pairs, responsetime2_values))

    robustness2_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3,
                          1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    robustness2_comparisons = dict(zip(alternative_pairs, robustness2_values))

    accuracy2 = ahpy.Compare('accuracy2', accuracy2_comparisons, precision=3)
    coveragearea2 = ahpy.Compare('coveragearea2', coveragearea2_comparisons, precision=3)
    powerconsumption2 = ahpy.Compare('powerconsumption2', powerconsumption2_comparisons, precision=3)
    cost2 = ahpy.Compare('cost2', cost2_comparisons, precision=3)
    scalability2 = ahpy.Compare('scalability2', scalability2_comparisons, precision=3)
    responsetime2 = ahpy.Compare('responsetime2', responsetime2_comparisons, precision=3)
    robustness2 = ahpy.Compare('robustness2', robustness2_comparisons, precision=3)

    sensitivity2.add_children([accuracy2, coveragearea2, powerconsumption2, cost2, scalability2, responsetime2,
                               robustness2])

    # Data for coverage area sensitivity graph

    data3 = [
        (alternative, weight) for alternative, weight in sensitivity2.target_weights.items() if
        alternative in alternatives
    ]

    labels3 = [row[0] for row in data3]
    values3 = [row[1] for row in data3]

    # ############################################################################### POWER CONSUMPTION increase 20%

    if selected_options[1] == "1":
        accuracy_powerconsumption_value = 0.333
    elif selected_options[1] > "1":
        accuracy_powerconsumption_value = float(selected_options[1]) - 2
    elif selected_options[1] == "0.333":
        accuracy_powerconsumption_value = 0.2
    elif selected_options[1] == "0.2":
        accuracy_powerconsumption_value = 0.1428
    elif selected_options[1] == "0.1428":
        accuracy_powerconsumption_value = 0.111
    else:
        accuracy_powerconsumption_value = selected_options[1]

    if selected_options[6] == "1":
        coveragearea_powerconsumption_value = 0.333
    elif selected_options[6] > "1":
        coveragearea_powerconsumption_value = float(selected_options[6]) - 2
    elif selected_options[6] == "0.333":
        coveragearea_powerconsumption_value = 0.2
    elif selected_options[6] == "0.2":
        coveragearea_powerconsumption_value = 0.1428
    elif selected_options[6] == "0.1428":
        coveragearea_powerconsumption_value = 0.111
    else:
        coveragearea_powerconsumption_value = selected_options[6]

    sensitivity3_comparisons = {
        ('accuracy3', 'coveragearea3'): selected_options[0],
        ('accuracy3', 'powerconsumption3'): accuracy_powerconsumption_value,
        ('accuracy3', 'cost3'): selected_options[2],
        ('accuracy3', 'scalability3'): selected_options[3],
        ('accuracy3', 'responsetime3'): selected_options[4],
        ('accuracy3', 'robustness3'): selected_options[5],

        ('coveragearea3', 'powerconsumption3'): coveragearea_powerconsumption_value,
        ('coveragearea3', 'cost3'): selected_options[7],
        ('coveragearea3', 'scalability3'): selected_options[8],
        ('coveragearea3', 'responsetime3'): selected_options[9],
        ('coveragearea3', 'robustness3'): selected_options[10],

        ('powerconsumption3', 'cost3'): selected_options[11] + "2",
        ('powerconsumption3', 'scalability3'): selected_options[12] + "2",
        ('powerconsumption3', 'responsetime3'): selected_options[13] + "2",
        ('powerconsumption3', 'robustness3'): selected_options[14] + "2",

        ('cost3', 'scalability3'): selected_options[15],
        ('cost3', 'responsetime3'): selected_options[16],
        ('cost3', 'robustness3'): selected_options[17],

        ('scalability3', 'responsetime3'): selected_options[18],
        ('scalability3', 'robustness3'): selected_options[19],

        ('responsetime3', 'robustness3'): selected_options[20]
    }
    sensitivity3 = ahpy.Compare(name='sensitivity3', comparisons=sensitivity3_comparisons,
                                precision=3, random_index='saaty')

    # technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy3_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1,
                        3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3, 9, 3, 9, 1 / 7)
    accuracy3_comparisons = dict(zip(alternative_pairs, accuracy3_values))

    coveragearea3_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9,
                            1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9, 5)
    coveragearea3_comparisons = dict(zip(alternative_pairs, coveragearea3_values))

    powerconsumption3_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5,
                                1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3, 5)
    powerconsumption3_comparisons = dict(zip(alternative_pairs, powerconsumption3_values))

    cost3_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost3_comparisons = dict(zip(alternative_pairs, cost3_values))

    scalability3_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability3_comparisons = dict(zip(alternative_pairs, scalability3_values))

    responsetime3_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5,
                            1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5, 5)
    responsetime3_comparisons = dict(zip(alternative_pairs, responsetime3_values))

    robustness3_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3,
                          1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    robustness3_comparisons = dict(zip(alternative_pairs, robustness3_values))

    accuracy3 = ahpy.Compare('accuracy3', accuracy3_comparisons, precision=3)
    coveragearea3 = ahpy.Compare('coveragearea3', coveragearea3_comparisons, precision=3)
    powerconsumption3 = ahpy.Compare('powerconsumption3', powerconsumption3_comparisons, precision=3)
    cost3 = ahpy.Compare('cost3', cost3_comparisons, precision=3)
    scalability3 = ahpy.Compare('scalability3', scalability3_comparisons, precision=3)
    responsetime3 = ahpy.Compare('responsetime3', responsetime3_comparisons, precision=3)
    robustness3 = ahpy.Compare('robustness3', robustness3_comparisons, precision=3)

    sensitivity3.add_children([accuracy3, coveragearea3, powerconsumption3, cost3, scalability3, responsetime3,
                               robustness3])

    # Data for power consumption sensitivity graph

    data4 = [
        (alternative, weight) for alternative, weight in sensitivity3.target_weights.items() if
        alternative in alternatives
    ]

    labels4 = [row[0] for row in data4]
    values4 = [row[1] for row in data4]

    # ################################################################################### COST increase 20%

    if selected_options[2] == "1":
        accuracy_cost_value = 0.333
    elif selected_options[2] > "1":
        accuracy_cost_value = float(selected_options[2]) - 2
    elif selected_options[2] == "0.333":
        accuracy_cost_value = 0.2
    elif selected_options[2] == "0.2":
        accuracy_cost_value = 0.1428
    elif selected_options[2] == "0.1428":
        accuracy_cost_value = 0.111
    else:
        accuracy_cost_value = selected_options[2]

    if selected_options[7] == "1":
        coveragearea_cost_value = 0.333
    elif selected_options[7] > "1":
        coveragearea_cost_value = float(selected_options[7]) - 2
    elif selected_options[7] == "0.333":
        coveragearea_cost_value = 0.2
    elif selected_options[7] == "0.2":
        coveragearea_cost_value = 0.1428
    elif selected_options[7] == "0.1428":
        coveragearea_cost_value = 0.111
    else:
        coveragearea_cost_value = selected_options[7]

    if selected_options[11] == "1":
        powerconsumption_cost_value = 0.333
    elif selected_options[11] > "1":
        powerconsumption_cost_value = float(selected_options[11]) - 2
    elif selected_options[11] == "0.333":
        powerconsumption_cost_value = 0.2
    elif selected_options[11] == "0.2":
        powerconsumption_cost_value = 0.1428
    elif selected_options[11] == "0.1428":
        powerconsumption_cost_value = 0.111
    else:
        powerconsumption_cost_value = selected_options[11]

    sensitivity4_comparisons = {
        ('accuracy4', 'coveragearea4'): selected_options[0],
        ('accuracy4', 'powerconsumption4'): selected_options[1],
        ('accuracy4', 'cost4'): accuracy_cost_value,
        ('accuracy4', 'scalability4'): selected_options[3],
        ('accuracy4', 'responsetime4'): selected_options[4],
        ('accuracy4', 'robustness4'): selected_options[5],

        ('coveragearea4', 'powerconsumption4'): selected_options[6],
        ('coveragearea4', 'cost4'): coveragearea_cost_value,
        ('coveragearea4', 'scalability4'): selected_options[8],
        ('coveragearea4', 'responsetime4'): selected_options[9],
        ('coveragearea4', 'robustness4'): selected_options[10],

        ('powerconsumption4', 'cost4'): powerconsumption_cost_value,
        ('powerconsumption4', 'scalability4'): selected_options[12],
        ('powerconsumption4', 'responsetime4'): selected_options[13],
        ('powerconsumption4', 'robustness4'): selected_options[14],

        ('cost4', 'scalability4'): selected_options[15] + "2",
        ('cost4', 'responsetime4'): selected_options[16] + "2",
        ('cost4', 'robustness4'): selected_options[17] + "2",

        ('scalability4', 'responsetime4'): selected_options[18],
        ('scalability4', 'robustness4'): selected_options[19],

        ('responsetime4', 'robustness4'): selected_options[20]
    }
    sensitivity4 = ahpy.Compare(name='sensitivity4', comparisons=sensitivity4_comparisons,
                                precision=3, random_index='saaty')

    # technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy4_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1,
                        3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3, 9, 3, 9, 1 / 7)
    accuracy4_comparisons = dict(zip(alternative_pairs, accuracy4_values))

    coveragearea4_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9,
                            1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9, 5)
    coveragearea4_comparisons = dict(zip(alternative_pairs, coveragearea4_values))

    powerconsumption4_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5,
                                1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3, 5)
    powerconsumption4_comparisons = dict(zip(alternative_pairs, powerconsumption4_values))

    cost4_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost4_comparisons = dict(zip(alternative_pairs, cost4_values))

    scalability4_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability4_comparisons = dict(zip(alternative_pairs, scalability4_values))

    responsetime4_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5,
                            1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5, 5)
    responsetime4_comparisons = dict(zip(alternative_pairs, responsetime4_values))

    robustness4_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3,
                          1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    robustness4_comparisons = dict(zip(alternative_pairs, robustness4_values))

    accuracy4 = ahpy.Compare('accuracy4', accuracy4_comparisons, precision=3)
    coveragearea4 = ahpy.Compare('coveragearea4', coveragearea4_comparisons, precision=3)
    powerconsumption4 = ahpy.Compare('powerconsumption4', powerconsumption4_comparisons, precision=3)
    cost4 = ahpy.Compare('cost4', cost4_comparisons, precision=3)
    scalability4 = ahpy.Compare('scalability4', scalability4_comparisons, precision=3)
    responsetime4 = ahpy.Compare('responsetime4', responsetime4_comparisons, precision=3)
    robustness4 = ahpy.Compare('robustness4', robustness4_comparisons, precision=3)

    sensitivity4.add_children([accuracy4, coveragearea4, powerconsumption4, cost4, scalability4, responsetime4,
                               robustness4])

    # Data for cost sensitivity graph

    data5 = [
        (alternative, weight) for alternative, weight in sensitivity4.target_weights.items() if
        alternative in alternatives
    ]

    labels5 = [row[0] for row in data5]
    values5 = [row[1] for row in data5]

    # ################################################################################### SCALABILITY increase 20%

    if selected_options[3] == "1":
        accuracy_scalability_value = 0.333
    elif selected_options[3] > "1":
        accuracy_scalability_value = float(selected_options[3]) - 2
    elif selected_options[3] == "0.333":
        accuracy_scalability_value = 0.2
    elif selected_options[3] == "0.2":
        accuracy_scalability_value = 0.1428
    elif selected_options[3] == "0.1428":
        accuracy_scalability_value = 0.111
    else:
        accuracy_scalability_value = selected_options[3]

    if selected_options[8] == "1":
        coveragearea_scalability_value = 0.333
    elif selected_options[8] > "1":
        coveragearea_scalability_value = float(selected_options[8]) - 2
    elif selected_options[8] == "0.333":
        coveragearea_scalability_value = 0.2
    elif selected_options[8] == "0.2":
        coveragearea_scalability_value = 0.1428
    elif selected_options[8] == "0.1428":
        coveragearea_scalability_value = 0.111
    else:
        coveragearea_scalability_value = selected_options[8]

    if selected_options[12] == "1":
        powerconsumption_scalability_value = 0.333
    elif selected_options[12] > "1":
        powerconsumption_scalability_value = float(selected_options[12]) - 2
    elif selected_options[12] == "0.333":
        powerconsumption_scalability_value = 0.2
    elif selected_options[12] == "0.2":
        powerconsumption_scalability_value = 0.1428
    elif selected_options[12] == "0.1428":
        powerconsumption_scalability_value = 0.111
    else:
        powerconsumption_scalability_value = selected_options[12]

    if selected_options[15] == "1":
        cost_scalability_value = 0.333
    elif selected_options[15] > "1":
        cost_scalability_value = float(selected_options[15]) - 2
    elif selected_options[15] == "0.333":
        cost_scalability_value = 0.2
    elif selected_options[15] == "0.2":
        cost_scalability_value = 0.1428
    elif selected_options[15] == "0.1428":
        cost_scalability_value = 0.111
    else:
        cost_scalability_value = selected_options[15]

    sensitivity5_comparisons = {
        ('accuracy5', 'coveragearea5'): selected_options[0],
        ('accuracy5', 'powerconsumption5'): selected_options[1],
        ('accuracy5', 'cost5'): selected_options[2],
        ('accuracy5', 'scalability5'): accuracy_scalability_value,
        ('accuracy5', 'responsetime5'): selected_options[4],
        ('accuracy5', 'robustness5'): selected_options[5],

        ('coveragearea5', 'powerconsumption5'): selected_options[6],
        ('coveragearea5', 'cost5'): selected_options[7],
        ('coveragearea5', 'scalability5'): coveragearea_scalability_value,
        ('coveragearea5', 'responsetime5'): selected_options[9],
        ('coveragearea5', 'robustness5'): selected_options[10],

        ('powerconsumption5', 'cost5'): selected_options[11],
        ('powerconsumption5', 'scalability5'): powerconsumption_scalability_value,
        ('powerconsumption5', 'responsetime5'): selected_options[13],
        ('powerconsumption5', 'robustness5'): selected_options[14],

        ('cost5', 'scalability5'): cost_scalability_value,
        ('cost5', 'responsetime5'): selected_options[16],
        ('cost5', 'robustness5'): selected_options[17],

        ('scalability5', 'responsetime5'): selected_options[18] + "2",
        ('scalability5', 'robustness5'): selected_options[19] + "2",

        ('responsetime5', 'robustness5'): selected_options[20]
    }
    sensitivity5 = ahpy.Compare(name='sensitivity5', comparisons=sensitivity5_comparisons,
                                precision=3, random_index='saaty')

    # technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy5_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1,
                        3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3, 9, 3, 9, 1 / 7)
    accuracy5_comparisons = dict(zip(alternative_pairs, accuracy5_values))

    coveragearea5_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9,
                            1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9, 5)
    coveragearea5_comparisons = dict(zip(alternative_pairs, coveragearea5_values))

    powerconsumption5_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5,
                                1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3, 5)
    powerconsumption5_comparisons = dict(zip(alternative_pairs, powerconsumption5_values))

    cost5_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost5_comparisons = dict(zip(alternative_pairs, cost5_values))

    scalability5_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability5_comparisons = dict(zip(alternative_pairs, scalability5_values))

    responsetime5_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5,
                            1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5, 5)
    responsetime5_comparisons = dict(zip(alternative_pairs, responsetime5_values))

    robustness5_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3,
                          1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    robustness5_comparisons = dict(zip(alternative_pairs, robustness5_values))

    accuracy5 = ahpy.Compare('accuracy5', accuracy5_comparisons, precision=3)
    coveragearea5 = ahpy.Compare('coveragearea5', coveragearea5_comparisons, precision=3)
    powerconsumption5 = ahpy.Compare('powerconsumption5', powerconsumption5_comparisons, precision=3)
    cost5 = ahpy.Compare('cost5', cost5_comparisons, precision=3)
    scalability5 = ahpy.Compare('scalability5', scalability5_comparisons, precision=3)
    responsetime5 = ahpy.Compare('responsetime5', responsetime5_comparisons, precision=3)
    robustness5 = ahpy.Compare('robustness5', robustness5_comparisons, precision=3)

    sensitivity5.add_children([accuracy5, coveragearea5, powerconsumption5, cost5, scalability5, responsetime5,
                               robustness5])

    # Data for scalability sensitivity graph

    data6 = [
        (alternative, weight) for alternative, weight in sensitivity5.target_weights.items() if
        alternative in alternatives
    ]

    labels6 = [row[0] for row in data6]
    values6 = [row[1] for row in data6]

    # ######################################################################## RESPONSE TIME increase 20%

    if selected_options[4] == "1":
        accuracy_responsetime_value = 0.333
    elif selected_options[4] > "1":
        accuracy_responsetime_value = float(selected_options[4]) - 2
    elif selected_options[4] == "0.333":
        accuracy_responsetime_value = 0.2
    elif selected_options[4] == "0.2":
        accuracy_responsetime_value = 0.1428
    elif selected_options[4] == "0.1428":
        accuracy_responsetime_value = 0.111
    else:
        accuracy_responsetime_value = selected_options[4]

    if selected_options[9] == "1":
        coveragearea_responsetime_value = 0.333
    elif selected_options[9] > "1":
        coveragearea_responsetime_value = float(selected_options[9]) - 2
    elif selected_options[9] == "0.333":
        coveragearea_responsetime_value = 0.2
    elif selected_options[9] == "0.2":
        coveragearea_responsetime_value = 0.1428
    elif selected_options[9] == "0.1428":
        coveragearea_responsetime_value = 0.111
    else:
        coveragearea_responsetime_value = selected_options[9]

    if selected_options[13] == "1":
        powerconsumption_responsetime_value = 0.333
    elif selected_options[13] > "1":
        powerconsumption_responsetime_value = float(selected_options[13]) - 2
    elif selected_options[13] == "0.333":
        powerconsumption_responsetime_value = 0.2
    elif selected_options[13] == "0.2":
        powerconsumption_responsetime_value = 0.1428
    elif selected_options[13] == "0.1428":
        powerconsumption_responsetime_value = 0.111
    else:
        powerconsumption_responsetime_value = selected_options[13]

    if selected_options[16] == "1":
        cost_responsetime_value = 0.333
    elif selected_options[16] > "1":
        cost_responsetime_value = float(selected_options[16]) - 2
    elif selected_options[16] == "0.333":
        cost_responsetime_value = 0.2
    elif selected_options[16] == "0.2":
        cost_responsetime_value = 0.1428
    elif selected_options[16] == "0.1428":
        cost_responsetime_value = 0.111
    else:
        cost_responsetime_value = selected_options[16]

    if selected_options[18] == "1":
        scalability_responsetime_value = 0.333
    elif selected_options[18] > "1":
        scalability_responsetime_value = float(selected_options[18]) - 2
    elif selected_options[18] == "0.333":
        scalability_responsetime_value = 0.2
    elif selected_options[18] == "0.2":
        scalability_responsetime_value = 0.1428
    elif selected_options[18] == "0.1428":
        scalability_responsetime_value = 0.111
    else:
        scalability_responsetime_value = selected_options[18]

    sensitivity6_comparisons = {
        ('accuracy6', 'coveragearea6'): selected_options[0],
        ('accuracy6', 'powerconsumption6'): selected_options[1],
        ('accuracy6', 'cost6'): selected_options[2],
        ('accuracy6', 'scalability6'): selected_options[3],
        ('accuracy6', 'responsetime6'): accuracy_responsetime_value,
        ('accuracy6', 'robustness6'): selected_options[5],

        ('coveragearea6', 'powerconsumption6'): selected_options[6],
        ('coveragearea6', 'cost6'): selected_options[7],
        ('coveragearea6', 'scalability6'): selected_options[8],
        ('coveragearea6', 'responsetime6'): coveragearea_responsetime_value,
        ('coveragearea6', 'robustness6'): selected_options[10],

        ('powerconsumption6', 'cost6'): selected_options[11],
        ('powerconsumption6', 'scalability6'): selected_options[12],
        ('powerconsumption6', 'responsetime6'): powerconsumption_responsetime_value,
        ('powerconsumption6', 'robustness6'): selected_options[14],

        ('cost6', 'scalability6'): selected_options[15],
        ('cost6', 'responsetime6'): cost_responsetime_value,
        ('cost6', 'robustness6'): selected_options[17],

        ('scalability6', 'responsetime6'): scalability_responsetime_value,
        ('scalability6', 'robustness6'): selected_options[19],

        ('responsetime6', 'robustness6'): selected_options[20] + "2"
    }
    sensitivity6 = ahpy.Compare(name='sensitivity6', comparisons=sensitivity6_comparisons,
                                precision=3, random_index='saaty')

    # technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy6_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1,
                        3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3, 9, 3, 9, 1 / 7)
    accuracy6_comparisons = dict(zip(alternative_pairs, accuracy6_values))

    coveragearea6_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9,
                            1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9, 5)
    coveragearea6_comparisons = dict(zip(alternative_pairs, coveragearea6_values))

    powerconsumption6_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5,
                                1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3, 5)
    powerconsumption6_comparisons = dict(zip(alternative_pairs, powerconsumption6_values))

    cost6_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost6_comparisons = dict(zip(alternative_pairs, cost6_values))

    scalability6_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability6_comparisons = dict(zip(alternative_pairs, scalability6_values))

    responsetime6_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5,
                            1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5, 5)
    responsetime6_comparisons = dict(zip(alternative_pairs, responsetime6_values))

    robustness6_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3,
                          1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    robustness6_comparisons = dict(zip(alternative_pairs, robustness6_values))

    accuracy6 = ahpy.Compare('accuracy6', accuracy6_comparisons, precision=3)
    coveragearea6 = ahpy.Compare('coveragearea6', coveragearea6_comparisons, precision=3)
    powerconsumption6 = ahpy.Compare('powerconsumption6', powerconsumption6_comparisons, precision=3)
    cost6 = ahpy.Compare('cost6', cost6_comparisons, precision=3)
    scalability6 = ahpy.Compare('scalability6', scalability6_comparisons, precision=3)
    responsetime6 = ahpy.Compare('responsetime6', responsetime6_comparisons, precision=3)
    robustness6 = ahpy.Compare('robustness6', robustness6_comparisons, precision=3)

    sensitivity6.add_children([accuracy6, coveragearea6, powerconsumption6, cost6, scalability6, responsetime6,
                               robustness6])

    # Data for response time sensitivity graph

    data7 = [
        (alternative, weight) for alternative, weight in sensitivity6.target_weights.items() if
        alternative in alternatives
    ]

    labels7 = [row[0] for row in data7]
    values7 = [row[1] for row in data7]

    # ######################################################################## ROBUSTNESS increase 20%

    if selected_options[5] == "1":
        accuracy_robustness_value = 0.333
    elif selected_options[5] > "1":
        accuracy_robustness_value = float(selected_options[5]) - 2
    elif selected_options[5] == "0.333":
        accuracy_robustness_value = 0.2
    elif selected_options[5] == "0.2":
        accuracy_robustness_value = 0.1428
    elif selected_options[5] == "0.1428":
        accuracy_robustness_value = 0.111
    else:
        accuracy_robustness_value = selected_options[5]

    if selected_options[10] == "1":
        coveragearea_robustness_value = 0.333
    elif selected_options[10] > "1":
        coveragearea_robustness_value = float(selected_options[10]) - 2
    elif selected_options[10] == "0.333":
        coveragearea_robustness_value = 0.2
    elif selected_options[10] == "0.2":
        coveragearea_robustness_value = 0.1428
    elif selected_options[10] == "0.1428":
        coveragearea_robustness_value = 0.111
    else:
        coveragearea_robustness_value = selected_options[10]

    if selected_options[14] == "1":
        powerconsumption_robustness_value = 0.333
    elif selected_options[14] > "1":
        powerconsumption_robustness_value = float(selected_options[14]) - 2
    elif selected_options[14] == "0.333":
        powerconsumption_robustness_value = 0.2
    elif selected_options[14] == "0.2":
        powerconsumption_robustness_value = 0.1428
    elif selected_options[14] == "0.1428":
        powerconsumption_robustness_value = 0.111
    else:
        powerconsumption_robustness_value = selected_options[14]

    if selected_options[17] == "1":
        cost_robustness_value = 0.333
    elif selected_options[17] > "1":
        cost_robustness_value = float(selected_options[17]) - 2
    elif selected_options[17] == "0.333":
        cost_robustness_value = 0.2
    elif selected_options[17] == "0.2":
        cost_robustness_value = 0.1428
    elif selected_options[17] == "0.1428":
        cost_robustness_value = 0.111
    else:
        cost_robustness_value = selected_options[17]

    if selected_options[19] == "1":
        scalability_robustness_value = 0.333
    elif selected_options[19] > "1":
        scalability_robustness_value = float(selected_options[19]) - 2
    elif selected_options[19] == "0.333":
        scalability_robustness_value = 0.2
    elif selected_options[19] == "0.2":
        scalability_robustness_value = 0.1428
    elif selected_options[19] == "0.1428":
        scalability_robustness_value = 0.111
    else:
        scalability_robustness_value = selected_options[19]

    if selected_options[20] == "1":
        responsetime_robustness_value = 0.333
    elif selected_options[20] > "1":
        responsetime_robustness_value = float(selected_options[20]) - 2
    elif selected_options[20] == "0.333":
        responsetime_robustness_value = 0.2
    elif selected_options[20] == "0.2":
        responsetime_robustness_value = 0.1428
    elif selected_options[20] == "0.1428":
        responsetime_robustness_value = 0.111
    else:
        responsetime_robustness_value = selected_options[20]

    sensitivity7_comparisons = {
        ('accuracy7', 'coveragearea7'): selected_options[0],
        ('accuracy7', 'powerconsumption7'): selected_options[1],
        ('accuracy7', 'cost7'): selected_options[2],
        ('accuracy7', 'scalability7'): selected_options[3],
        ('accuracy7', 'responsetime7'): selected_options[4],
        ('accuracy7', 'robustness7'): accuracy_robustness_value,

        ('coveragearea7', 'powerconsumption7'): selected_options[6],
        ('coveragearea7', 'cost7'): selected_options[7],
        ('coveragearea7', 'scalability7'): selected_options[8],
        ('coveragearea7', 'responsetime7'): selected_options[9],
        ('coveragearea7', 'robustness7'): coveragearea_robustness_value,

        ('powerconsumption7', 'cost7'): selected_options[11],
        ('powerconsumption7', 'scalability7'): selected_options[12],
        ('powerconsumption7', 'responsetime7'): selected_options[13],
        ('powerconsumption7', 'robustness7'): powerconsumption_robustness_value,

        ('cost7', 'scalability7'): selected_options[15],
        ('cost7', 'responsetime7'): selected_options[16],
        ('cost7', 'robustness7'): cost_robustness_value,

        ('scalability7', 'responsetime7'): selected_options[18],
        ('scalability7', 'robustness7'): scalability_robustness_value,

        ('responsetime7', 'robustness7'): responsetime_robustness_value
    }
    sensitivity7 = ahpy.Compare(name='sensitivity7', comparisons=sensitivity7_comparisons,
                                precision=3, random_index='saaty')

    # technological Knowledgebase for alternatives#

    alternatives = ('WIFI', 'RFID', 'Bluetooth', 'UWB', 'VLC', 'Zigbee', 'Ultrasound')
    alternative_pairs = list(itertools.combinations(alternatives, 2))

    accuracy7_values = (1 / 5, 1 / 3, 1 / 9, 1 / 9, 1 / 7, 1,
                        3, 1 / 3, 1 / 3, 1, 7, 1 / 7, 1 / 7, 1 / 5, 1 / 7, 1, 3, 9, 3, 9, 1 / 7)
    accuracy7_comparisons = dict(zip(alternative_pairs, accuracy7_values))

    coveragearea7_values = (5, 5, 3, 1 / 5, 3, 7, 3, 1 / 5, 1 / 9,
                            1 / 5, 5, 1 / 3, 1 / 9, 1 / 3, 3, 1 / 7, 1, 5, 7, 9, 5)
    coveragearea7_comparisons = dict(zip(alternative_pairs, coveragearea7_values))

    powerconsumption7_values = (1 / 5, 1 / 5, 1 / 3, 1 / 3, 1 / 5,
                                1, 1, 3, 3, 1, 5, 3, 3, 1, 5, 1, 1 / 3, 3, 1 / 3, 3, 5)
    powerconsumption7_comparisons = dict(zip(alternative_pairs, powerconsumption7_values))

    cost7_values = (1 / 5, 1 / 5, 5, 1 / 5, 1 / 3, 3, 1, 9, 1, 3, 7, 9, 1, 3, 7, 1 / 9, 1 / 7, 1 / 3, 3, 7, 5)
    cost7_comparisons = dict(zip(alternative_pairs, cost7_values))

    scalability7_values = (1 / 5, 1 / 5, 1 / 5, 5, 1 / 5, 1, 1, 1, 9, 1, 5, 1, 9, 1, 5, 9, 1, 5, 1 / 9, 1 / 5, 5)
    scalability7_comparisons = dict(zip(alternative_pairs, scalability7_values))

    responsetime7_values = (5, 5, 3, 1, 1, 5, 1, 1 / 3, 1 / 5,
                            1 / 5, 1, 1 / 3, 1 / 5, 1 / 5, 1, 1 / 3, 1 / 3, 3, 1, 5, 5)
    responsetime7_comparisons = dict(zip(alternative_pairs, responsetime7_values))

    robustness7_values = (1, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3,
                          1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    robustness7_comparisons = dict(zip(alternative_pairs, robustness7_values))

    accuracy7 = ahpy.Compare('accuracy7', accuracy7_comparisons, precision=3)
    coveragearea7 = ahpy.Compare('coveragearea7', coveragearea7_comparisons, precision=3)
    powerconsumption7 = ahpy.Compare('powerconsumption7', powerconsumption7_comparisons, precision=3)
    cost7 = ahpy.Compare('cost7', cost7_comparisons, precision=3)
    scalability7 = ahpy.Compare('scalability7', scalability7_comparisons, precision=3)
    responsetime7 = ahpy.Compare('responsetime7', responsetime7_comparisons, precision=3)
    robustness7 = ahpy.Compare('robustness7', robustness7_comparisons, precision=3)

    sensitivity7.add_children([accuracy7, coveragearea7, powerconsumption7, cost7, scalability7, responsetime7,
                               robustness7])

    # Data for robustness sensitivity graph

    data8 = [
        (alternative, weight) for alternative, weight in sensitivity7.target_weights.items() if
        alternative in alternatives
    ]

    labels8 = [row[0] for row in data8]
    values8 = [row[1] for row in data8]

    return render_template("calculationandresult.html", selected_options=selected_options, criteria_comparisons=criteria_comparisons,
                        criteria=criteria, alternatives=alternatives, alternative_pairs=alternative_pairs,
                        accuracy=accuracy, coveragearea=coveragearea,
                        powerconsumption=powerconsumption, cost=cost, scalability=scalability,
                        responsetime=responsetime, robustness=robustness, labels=labels, values=values,
                        labelsrecommendation=labelsrecommendation, valuesrecommendation=valuesrecommendation,
                        target_weights=criteria.target_weights, labels2=labels2, values2=values2, labels3=labels3,
                        values3=values3, labels4=labels4, values4=values4, labels5=labels5, values5=values5,
                        labels6=labels6, values6=values6, labels7=labels7, values7=values7, labels8=labels8,
                        values8=values8, sensitivity1=sensitivity1, sensitivity2=sensitivity2,
                        sensitivity3=sensitivity3, sensitivity4=sensitivity4, sensitivity5=sensitivity5,
                        sensitivity6=sensitivity6, sensitivity7=sensitivity7)


@views.route('/generate_pdf1', methods=['GET'])
def generate_pdf1():
    # create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()
    # create a canvas with a specified page size (e.g., letter)
    pdf = canvas.Canvas(buffer, pagesize=letter)
    # add content to the PDF
    pdf.drawString(100, 740, "Your Technology Recommendation Report (summarized)")
    pdf.drawString(100, 680, "Author: Havvanur")
    pdf.drawString(100, 660, "print(accuracy_comparisons)")
    pdf.drawString(100, 640, "print(coveragearea_comparisons)")
    pdf.drawString(100, 620, "print(powerconsumption_comparisons)")
    pdf.drawString(100, 600, "print(cost_comparisons)")
    pdf.drawString(100, 580, "print(scalability_comparisons)")
    pdf.drawString(100, 560, "print(responsetime_comparisons)")
    pdf.drawString(100, 540, "print(robustness_comparisons)")
    pdf.showPage()
    # save the PDF to the buffer
    pdf.save()

    # reset the buffer position to the beginning
    buffer.seek(0)

    # create a flask response with the PDF data
    response = make_response(buffer.read())
    response.mimetype = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Summarized_report.pdf'

    return response


@views.route('/generate_pdf2', methods=['GET'])
def generate_pdf2():
    # create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()
    # create a canvas with a specified page size (e.g., letter)
    pdf = canvas.Canvas(buffer, pagesize=letter)
    # add content to the PDF
    pdf.drawString(100, 740, "Your Technology Recommendation Report (detailed)")
    pdf.drawString(100, 680, "Author: Havvanur")
    pdf.drawString(100, 660, "Accuracy: {accuracy.global_weight}")
    pdf.drawString(100, 640, "Coverage Area: {coveragearea.global_weight}")
    pdf.drawString(100, 620, "Power Consumption: {powerconsumption.global_weight}")
    pdf.drawString(100, 600, "Cost: {cost.global_weight}")
    pdf.drawString(100, 580, "Scalability: {scalability.global_weight}")
    pdf.drawString(100, 560, "Response Time: {responsetime.global_weight}")
    pdf.drawString(100, 540, "Robustness: {robustness.global_weight}")
    pdf.drawString(100, 520, "Accuracy_Report: {accuracy.report(show=True)}")
    pdf.showPage()
    # save the PDF to the buffer
    pdf.save()

    # reset the buffer position to the beginning
    buffer.seek(0)

    # create a flask response with the PDF data
    response = make_response(buffer.read())
    response.mimetype = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Detailed_report.pdf'

    return response


@views.route('/help')
def help():
    return render_template("help.html")
