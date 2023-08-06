import pandas as pd

def hello_pandas(df):
    print("hello pandas!")
    return df.head()

if __name__ == '__main__':
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    print(hello_pandas(df))
