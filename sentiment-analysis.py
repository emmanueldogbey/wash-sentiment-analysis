from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

def read_file(filepath):
    df = pd.read_csv(filepath)
    df.drop(columns=['Unnamed: 0', 'Link'], inplace=True)

    return df

df = read_file('data/myjoyonline_data.csv')
# print(df.head())
print(df.shape)
# analyzer = SentimentIntensityAnalyzer()
# scores = analyzer.polarity_scores(text)
# print(scores)
