import pandas as pd

def load_and_process_data(filepath="European_Bank.csv"):
    df = pd.read_csv(filepath)
    if 'Surname' in df.columns:
        df = df.drop(columns=['Surname'])
        
    # Apply your verified Colab segmentation rules
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 29, 45, 60, 120], labels=['<30', '30–45', '46–60', '60+'])
    df['CreditScoreBand'] = pd.cut(df['CreditScore'], bins=[0, 599, 699, 850], labels=['Low', 'Medium', 'High'])
    df['TenureGroup'] = pd.cut(df['Tenure'], bins=[-1, 2, 6, 20], labels=['New', 'Mid-term', 'Long-term'])
    
    median_nonzero = df[df['Balance'] > 0]['Balance'].median()
    df['BalanceSegment'] = df['Balance'].apply(lambda x: 'Zero-balance' if x == 0 else ('Low-balance' if x <= median_nonzero else 'High-balance'))
    
    return df
