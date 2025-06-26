import pandas as pd

def preprocess(df, region_df):
    # filtering for summer olympics only
    df = df[df['Season']=='Summer']
    # merge step
    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    # one-hot encoding for categorical data
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    return df

