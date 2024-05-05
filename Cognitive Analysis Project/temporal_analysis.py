from sentiment_analysis import sentiment

def temporal_sentiment_analysis(reviews):

    sentiment_counts = {}

    for review in reviews:
        review_date = review['date'].date()
        review_content = review['content']
        review_sentiment = sentiment(review_content)

        # If the date is already in the dictionary, update sentiment count
        if review_date in sentiment_counts:
            sentiment_counts[review_date][review_sentiment] += 1
        # Otherwise, initialize sentiment count for the date
        else:
            sentiment_counts[review_date] = {'positive': 0, 'negative': 0, 'neutral': 0}
            sentiment_counts[review_date][review_sentiment] = 1

    return sentiment_counts


def plot_temporal_sentiment(sentiment_counts):

    import matplotlib.pyplot as plt

    dates = sorted(sentiment_counts.keys())
    positive_counts = [sentiment_counts[date]['positive'] for date in dates]
    negative_counts = [sentiment_counts[date]['negative'] for date in dates]
    neutral_counts = [sentiment_counts[date]['neutral'] for date in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, positive_counts, label='Positive', marker='o')
    plt.plot(dates, negative_counts, label='Negative', marker='o')
    plt.plot(dates, neutral_counts, label='Neutral', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Review Count')
    plt.title('Temporal Sentiment Analysis')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
