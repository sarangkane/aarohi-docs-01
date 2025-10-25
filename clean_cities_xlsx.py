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
def clean_city_name(raw_city, volunteering_pref):
    raw_city_str = str(raw_city).strip()
    volunteering_pref_str = str(volunteering_pref).strip()
    # If more than one city is mentioned, use volunteering location preference
    if any(sep in raw_city_str for sep in [" and ", ",", "/", "-"]):
        if volunteering_pref_str:
            return volunteering_pref_str.title()
    # If only state name is present, keep as is
    state_names = ["Bihar", "Maharashtra", "Karnataka", "West Bengal", "Tamil Nadu", "Uttar Pradesh", "Punjab", "Gujarat", "Rajasthan", "Kerala", "Assam", "Odisha", "Jharkhand", "Chhattisgarh", "Haryana", "Telangana", "Andhra Pradesh", "Madhya Pradesh", "Goa", "Tripura", "Manipur", "Meghalaya", "Nagaland", "Arunachal Pradesh", "Sikkim", "Mizoram", "Puducherry", "Delhi"]
    if raw_city_str.title() in state_names:
        return raw_city_str.title()
    city = re.split(r",|-|/|\(|\[", raw_city_str)[0].strip().title()
    if city in MISSPELLINGS:
        city = MISSPELLINGS[city]
    # Map Allahabad and Prayagraj to Prayagraj
    if city.lower() in ["allahabad", "prayagraj"]:
        return "Prayagraj"
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
    volunteering_col = "Volunteering Location Preference"
    df.insert(
        df.columns.get_loc(city_col) + 1,
        "City (Updated)",
        [clean_city_name(city, vol) for city, vol in zip(df[city_col], df[volunteering_col])]
    )
    df["Changed/Unchanged"] = [
        "Changed" if str(orig).strip().title() != str(updated).strip().title() else "Unchanged"
        for orig, updated in zip(df[city_col], df["City (Updated)"])
    ]
    df.to_csv("Merged Excel - Cleaned.csv", index=False)
    df.to_excel("Merged Excel - Cleaned.xlsx", index=False)
if __name__ == "__main__":
    main()
