import pandas as pd

# Load the CSV
df = pd.read_csv("Phishing_Email.csv", encoding='ISO-8859-1')

# Drop rows where 'Email Text' is NaN or empty
df = df.dropna(subset=['Email Text'])  # Remove rows with NaN
df = df[df['Email Text'].str.strip() != ""]  # Remove rows with empty strings

# Reset index
df = df.reset_index(drop=True)

# Save cleaned data
df.to_csv("Phishing_Email_Cleaned.csv", index=False)

print("✅ Cleaned data saved to 'Phishing_Email_Cleaned.csv'")
