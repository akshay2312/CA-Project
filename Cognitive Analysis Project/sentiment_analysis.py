import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()


def sentiment(sentence):
    # Get the polarity scores using VADER
    scores = sid.polarity_scores(sentence)

    # Determine the sentiment based on the compound score
    if scores['compound'] > 0.05:
        sentiment = 'positive'
    elif scores['compound'] < -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment


if __name__ == "__main__":
    from review_extraction import scrape_imdb_reviews
    from temporal_analysis import temporal_sentiment_analysis
    from temporal_analysis import plot_temporal_sentiment
    movie = 'Archies'
    reviews = scrape_imdb_reviews(movie)

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    # Perform sentiment analysis for each review
    for review in reviews:
        review_sentiment = sentiment(review['content'])
        if review_sentiment == 'positive':
            positive_count += 1
        elif review_sentiment == 'negative':
            negative_count += 1
        else:
            neutral_count += 1

    # Print the counts of positive, negative, and neutral reviews
    print('Positive reviews:', positive_count)
    print('Negative reviews:', negative_count)
    print('Neutral reviews:', neutral_count)
    print((positive_count/(positive_count+negative_count+neutral_count))*100,'% like this movie ')
    sentiment_counts=temporal_sentiment_analysis(reviews)
    plot_temporal_sentiment(sentiment_counts)