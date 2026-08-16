import pandas as pd

df = pd.DataFrame({
    "Sales": [100, 200, 300],
    "Profit": [10, 20, 30]
})

print(type(df))
print(type(df["Sales"]))
print(type(df.columns))
print(type(df.index))

cols = list(df.columns)
print(type(cols))