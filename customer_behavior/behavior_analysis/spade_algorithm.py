import pandas as pd
from collections import defaultdict

def preprocess_data(data):
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
    sequences = defaultdict(list)
    for _, row in data.iterrows():
        sequences[row['customer_id']].append((row['timestamp'], row['product']))
    for customer_id in sequences:
        sequences[customer_id] = sorted(sequences[customer_id], key=lambda x: x[0])
    sequence_data = []
    for customer_id, events in sequences.items():
        sequence_data.append([event[1] for event in events])
    print("Chuỗi tuần tự sau khi tiền xử lý:", sequence_data)
    return sequence_data

def generate_candidates(patterns, k):
    candidates = set()
    for i in range(len(patterns)):
        for j in range(i + 1, len(patterns)):
            p1, p2 = patterns[i], patterns[j]
            if p1[:-1] == p2[:-1]:
                candidates.add(tuple(p1) + (p2[-1],))
    return list(candidates)

def calculate_support(sequence_data, candidates):
    support_count = defaultdict(int)
    for sequence in sequence_data:
        for candidate in candidates:
            candidate_tuple = tuple(candidate)
            if is_subsequence(candidate_tuple, sequence):
                support_count[candidate_tuple] += 1
    print("Tần suất các ứng viên:", support_count)
    return support_count

def is_subsequence(subseq, seq):
    it = iter(seq)
    return all(item in it for item in subseq)

def filter_frequent_patterns(support_count, minsup):
    return {pattern: count for pattern, count in support_count.items() if count >= minsup}

def spade_algorithm(data, minsup):
    sequence_data = preprocess_data(data)
    items = set(item for sequence in sequence_data for item in sequence)
    patterns = [[item] for item in items]
    frequent_patterns = {}
    k = 1

    while patterns:
        support_count = calculate_support(sequence_data, patterns)
        filtered_patterns = filter_frequent_patterns(support_count, minsup)
        frequent_patterns.update(filtered_patterns)
        patterns = generate_candidates(list(filtered_patterns.keys()), k)
        k += 1

    return frequent_patterns