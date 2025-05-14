from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .spade_algorithm import spade_algorithm

def index(request):
    return render(request, 'behavior_analysis/index.html')

def process(request):
    if request.method == 'POST':
        file = request.FILES['file']
        minsup = int(request.POST['minsup'])
        data = pd.read_csv(file)

        request.session['uploaded_data'] = data.to_dict(orient='records')
        request.session['minsup'] = minsup

        patterns, most_popular_item = spade_algorithm(data, minsup)

        return render(request, 'behavior_analysis/result.html', {
            'patterns': patterns,
            'most_popular_item': most_popular_item,
        })
    return HttpResponse("Invalid request")

def analyze_trends(data):
    data['timestamp'] = pd.to_datetime(data['timestamp'], dayfirst=True, errors='coerce')

    trends = data.groupby(data['timestamp'].dt.to_period('M'))['product'].value_counts()

    trends_df = trends.reset_index(name='count')
    trends_df.rename(columns={'timestamp': 'month', 'product': 'product'}, inplace=True)

    return trends_df


def generate_recommendations(data, customer_history):
    patterns = spade_algorithm(data, minsup=5)

    recommendations = []
    for pattern in patterns:
        if len(pattern) > 1 and pattern[:-1] == customer_history[-len(pattern[:-1]):]:
            recommendations.append(pattern[-1])

    return recommendations
