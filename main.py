# Calculate quartiles for RFM metrics
quartiles = rfm.quantile(q=[0.25, 0.5, 0.75])
quartiles = quartiles.to_dict()

# Functions to assign scores to Recency, Frequency, and Monetary
def r_score(x, p, d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1

def fm_score(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4

# Assigning scores
rfm['r_score'] = rfm['recency'].apply(r_score, args=('recency', quartiles))
rfm['f_score'] = rfm['frequency'].apply(fm_score, args=('frequency', quartiles))
rfm['m_score'] = rfm['monetary'].apply(fm_score, args=('monetary', quartiles))

# Combining scores to create RFM Segment
rfm['rfm_segment'] = rfm['r_score'].map(str) + rfm['f_score'].map(str) + rfm['m_score'].map(str)


# Calculating average values for RFM metrics in each segment
segment_analysis = rfm.groupby('rfm_segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': ['mean', 'count']
}).reset_index()

segment_analysis.columns = ['rfm_segment',
                            'average_recency',
                            'average_frequency',
                            'average_monetary',
                            'count']

# Analyzing the size of each segment
segment_size = rfm['rfm_segment'].value_counts().reset_index()
segment_size.columns = ['rfm_segment', 'size']