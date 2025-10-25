import pandas as pd
import re

VALID_CITIES = [
    "Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Patna", "Ludhiana", "Agra", "Nashik", "Vadodara", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad", "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubli", "Mysore", "Tiruchirappalli", "Bareilly", "Aligarh", "Tiruppur", "Moradabad", "Jalandhar", "Bhubaneswar", "Salem", "Warangal", "Guntur", "Bhiwandi", "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", "Cuttack", "Firozabad", "Kochi", "Nellore", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Rourkela", "Nanded", "Kolhapur", "Ajmer", "Akola", "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Nellore", "Jammu", "Sangli", "Mangalore", "Erode", "Belgaum", "Kurnool", "Ambattur", "Tirupati", "Malegaon", "Gaya", "Jalgaon", "Udaipur", "Maheshtala", "Davanagere", "Kozhikode", "Kurnool", "Rajpur Sonarpur", "Bokaro", "South Dumdum", "Bellary", "Patiala", "Gopalpur", "Agartala", "Bhagalpur", "Muzaffarnagar", "Bhatpara", "Panipat", "Darbhanga", "Bardhaman", "Kharagpur", "Sikar", "Kollam", "Bilaspur", "Shahjahanpur", "Satara", "Bijapur", "Rampur", "Shivamogga", "Chandrapur", "Junagadh", "Thrissur", "Alwar", "Bihar Sharif", "Bhiwani", "Bettiah", "Shimla", "Ratlam", "Handwara", "Dibrugarh", "Aizawl", "Purnia", "Hapur", "Chhindwara", "Bongaigaon", "Bhimavaram", "Kumbakonam", "Dewas", "Kishanganj", "Budaun", "Kishangarh", "Bongaigaon", "Bhimavaram", "Kumbakonam", "Dewas", "Kishanganj", "Budaun", "Kishangarh"
]
MISSPELLINGS = {
    "Banglore": "Bangalore",
    "Bombay": "Mumbai",
    "Calcutta": "Kolkata",
    "Madras": "Chennai",
    "Hydrabad": "Hyderabad",
    "Punee": "Pune",
    "Ahemdabad": "Ahmedabad",
    "Kolkatta": "Kolkata",
    "Channai": "Chennai",
    "Bengluru": "Bangalore",
    "Bangaluru": "Bangalore",
    "Bengaluru": "Bangalore"
}
def proper_case(city):
    return city.title()
def clean_city_name(raw_city):
    city = re.split(r",|-|/|\(|\[", str(raw_city))[0].strip()
    city = city.title()
    if city in MISSPELLINGS:
        city = MISSPELLINGS[city]
    for valid in VALID_CITIES:
        if city.lower() == valid.lower():
            return valid
    for valid in VALID_CITIES:
        if city.lower() in valid.lower() or valid.lower() in city.lower():
            return valid
    return city
def main():
    df = pd.read_csv("Merged Excel.csv")
    city_col = df.columns[3]
    df.insert(df.columns.get_loc(city_col) + 1, "City (Updated)", df[city_col].apply(clean_city_name))
    df["Changed/Unchanged"] = [
        "Changed" if str(orig).strip().title() != str(updated).strip().title() else "Unchanged"
        for orig, updated in zip(df[city_col], df["City (Updated)"])
    ]
    df.to_csv("Merged Excel - Cleaned.csv", index=False)
    df.to_excel("Merged Excel - Cleaned.xlsx", index=False)
if __name__ == "__main__":
    main()
