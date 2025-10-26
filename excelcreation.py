import pandas as pd

data = {
    "username": ["hari"],
    "password": ["demo"]
}

df = pd.DataFrame(data)
df.to_excel("config/test_data.xlsx", index=False)
print("✅ Excel file created successfully!")
