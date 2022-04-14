from pprint import pprint
from turtle import color
import matplotlib.pyplot as plt
from prometheus_client import Histogram
from dynamodb import *

# USER_SCORES = {
#     "mikepompeo": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "BarackObama": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "JoeBiden": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "SpeakerPelosi": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "KDTrey5": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "KingJames": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "billieeilish": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "willsmith": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "KimKardashian": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#     "AnneeJHathaway": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# }

# if __name__ == '__main__':
#     for person in USER_SCORES:
#         items = get_score(person)
#         for item in items:
#             score_labels = item["SCORES"][0]  # [Decimal(), ..., Decimal()]
#             for index, score in enumerate(score_labels):
#                 score = float(score)
#                 USER_SCORES[person][index] += score
#         num_replies = len(items)
#         USER_SCORES[person][:] = [score / num_replies for score in USER_SCORES[person]]
#     pprint(USER_SCORES)


USER_SCORES = {
    'Joe Biden': [0.17446818440645165, 0.028187267774193538, 0.062081947729032215, 0.029172068477419363, 0.07526187505806449, 0.04305714570000001],
    'Mike Pompeo': [0.22807587110880828, 0.03492595116839377, 0.08322995440932639, 0.03312240132901552, 0.09664371105699478, 0.06000321290155445],
    'Barack Obama': [0.11549559835046726, 0.029722526105140198, 0.04684719733411211, 0.02860837178504674, 0.05440339675700934, 0.04423467372663552],
    'SpeakerPelosi': [0.20711407092631584, 0.030165331781578958, 0.0741866274526316, 0.028631471457894752, 0.09997104778421055, 0.041751869192105245],
    'Kevin Durant': [0.17266614284347825, 0.033123266797826095, 0.08829272155434788, 0.030126198991304348, 0.08203828251304347, 0.03352137463043479],
    'LeBron James': [0.16505749739181286, 0.028427459833333345, 0.07332289408771928, 0.02615077251461987, 0.08677472714619883, 0.03259694291812863],
    'Anne Hathaway': [0.10765590633333333, 0.03375006083333334, 0.04268905583333334, 0.025504859333333327, 0.039992724333333333, 0.03280062383333334],
    'Kim Kardashian': [0.17985811279881658, 0.03586271000591715, 0.07104734757988165, 0.03792017273964496, 0.0857754561893491, 0.03773901010355028],
    'Will Smith': [0.10816130532000001, 0.027262271345, 0.05665584062999999, 0.02374509128000001, 0.053863283209999994, 0.02494882035],
    'Billie Eilish': [0.14299157308139532, 0.02841546633720931, 0.0901063873023256,0.02219780438953488, 0.0606141470348837, 0.02810385895930232]
}

if __name__ == '__main__':
    Label_Scores = {
        'Toxic': {}, 'Severe Toxic': {}, 'Obscene': {}, 'Threat': {}, 'Insult': {}, 'Identity Hate': {}
    }
    for user, scores in USER_SCORES.items():
        Label_Scores['Toxic'][user] = scores[0]
        Label_Scores['Severe Toxic'][user] = scores[1]
        Label_Scores['Obscene'][user] = scores[2]
        Label_Scores['Threat'][user] = scores[3]
        Label_Scores['Insult'][user] = scores[4]
        Label_Scores['Identity Hate'][user] = scores[5]
    # pprint(Label_Scores)
    # names = list(Label_Scores['Toxic'].keys())
    # values = list(Label_Scores['Toxic'].values())
    # plt.bar(range(len(Label_Scores['Toxic'])), values, tick_label=names, color='r')
    # plt.title("Histogram of Toxic Label")
    # plt.show()
    colors = list("mbkygr")
    for data_dict in Label_Scores.values():
        x = data_dict.keys()
        y = data_dict.values()
        plt.scatter(x, y, color=colors.pop(), s=80)
    plt.legend(Label_Scores.keys(), fontsize=13)
    plt.xticks(fontsize=13.5)
    plt.yticks(fontsize=15)
    plt.title("Plot of Label Scores Distribution of Targeted Twitter Users", fontsize=19)
    plt.show()
