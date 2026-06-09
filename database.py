
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'sakhi.db'))
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS schemes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    for_who TEXT,
    age TEXT,
    benefit TEXT,
    life_stage TEXT
)''')

schemes = [
    ("Mukhyamantri Majhi Ladki Bahin Yojana", "Economically weaker women", "21-65 years", "Rs. 1500 monthly direct benefit transfer", "Employment"),
    ("Beti Bachao Beti Padhao", "Girls and families", "Birth onwards", "Girl child protection and education", "Birth & Education"),
    ("Sukanya Samriddhi Yojana", "Parents of girl child", "Below 10 years", "High interest savings account for education and marriage", "Child"),
    ("Majhi Kanya Bhagyashree Scheme", "Girl children in poor families", "Birth onwards", "Financial support for girls", "Birth & Education"),
    ("Balika Samridhi Yojana", "Girls from poor families", "Birth onwards", "Scholarship and savings support", "Birth & Education"),
    ("Scheme for Adolescent Girls SAG", "Adolescent girls", "14-18 years", "Nutrition and health support", "Adolescent"),
    ("Poshan Abhiyaan", "Girls and mothers", "Various", "Nutrition improvement program", "Maternity"),
    ("Anganwadi Services", "Children and mothers", "0-6 years", "Nutrition and preschool services", "Child"),
    ("ICDS Scheme", "Mothers and children", "Various", "Child nutrition and health", "Child"),
    ("Kishori Shakti Yojana", "Adolescent girls", "11-18 years", "Skill and health awareness", "Adolescent"),
    ("SABLA Scheme", "Adolescent girls", "11-18 years", "Nutrition and vocational training", "Adolescent"),
    ("Savitribai Phule Scholarship", "Girl students", "School and college", "Scholarship support for education", "Birth & Education"),
    ("Pre-Matric Scholarship for Girls", "School girls", "Pre-10th standard", "Financial assistance for school girls", "Birth & Education"),
    ("Post-Matric Scholarship", "College girls", "After 10th standard", "Fee support for higher education", "Birth & Education"),
    ("Rajarshi Shahu Maharaj Scholarship", "Students from weaker sections", "College students", "Scholarship support", "Birth & Education"),
    ("EBC Scholarship Scheme", "Economically backward students", "Eligible students", "Tuition fee support", "Birth & Education"),
    ("Free Bicycle Scheme for Girls", "Rural school girls", "School-going girls", "Free bicycle for transportation to school", "Birth & Education"),
    ("Kasturba Gandhi Balika Vidyalaya", "Girls from disadvantaged groups", "School-age girls", "Free residential schooling", "Birth & Education"),
    ("Right to Education Support", "Girl students", "6-14 years", "Free and compulsory education", "Birth & Education"),
    ("Working Women Hostel Scheme", "Working women", "Adult women", "Safe and affordable accommodation", "Employment"),
    ("Skill India Mission", "Women job seekers", "Youth and adults", "Skill development training", "Employment"),
    ("PM Kaushal Vikas Yojana", "Young women", "18+ years", "Free skill training and certification", "Employment"),
    ("Mahila Samriddhi Loan Scheme", "Women entrepreneurs", "Adult women", "Business loans at low interest", "Employment"),
    ("Stand Up India Scheme", "Women entrepreneurs", "18+ years", "Startup loans from Rs. 10 lakh to 1 crore", "Employment"),
    ("Mudra Loan Scheme", "Small business women", "Adult women", "Business funding up to Rs. 10 lakh", "Employment"),
    ("Lakhpati Didi Scheme", "Self Help Group women", "Adult women", "Income generation support to earn Rs. 1 lakh per year", "Employment"),
    ("Maharashtra State Rural Livelihood Mission", "Rural women SHGs", "Adult women", "Self-employment and livelihood support", "Employment"),
    ("Hub for Empowerment of Women", "Women across sectors", "Adult women", "Awareness and empowerment support", "Employment"),
    ("STEP Scheme", "Women needing training", "Adult women", "Employment-oriented skill training", "Employment"),
    ("Mahila E-Haat", "Women entrepreneurs", "Adult women", "Online marketing platform for women businesses", "Employment"),
    ("PM Matru Vandana Yojana", "Pregnant women", "Pregnant mothers", "Cash assistance of Rs. 5000 in installments", "Maternity"),
    ("Janani Suraksha Yojana", "Pregnant women", "Eligible mothers", "Cash incentive for safe institutional delivery", "Maternity"),
    ("Janani Shishu Suraksha Karyakram", "Mothers and infants", "Pregnant women", "Free maternity care drugs diagnostics and transport", "Maternity"),
    ("Saksham Anganwadi and Poshan 2.0", "Pregnant and lactating mothers", "Adult women", "Nutrition support during pregnancy", "Maternity"),
    ("Surakshit Matritva Aashwasan SUMAN", "Pregnant women", "Eligible mothers", "Free respectful healthcare during delivery", "Maternity"),
    ("National Creche Scheme", "Working women with children", "Mothers", "Child daycare facilities for working mothers", "Employment"),
    ("One Stop Centre Scheme", "Women facing violence", "All ages", "Legal medical police and shelter support under one roof", "Family/Distress"),
    ("Women Helpline 181", "Women in distress", "All ages", "24x7 emergency helpline for women", "Family/Distress"),
    ("Ujjawala Scheme", "Women victims of trafficking", "Women and girls", "Rescue rehabilitation and reintegration support", "Family/Distress"),
    ("Swadhar Greh Scheme", "Destitute women", "Adult women", "Shelter food healthcare and vocational training", "Family/Distress"),
    ("Mahila Police Volunteer Scheme", "Community women", "Adult women", "Women safety and community support", "Family/Distress"),
    ("Nari Adalat", "Women facing disputes", "Adult women", "Community-based legal support for women", "Family/Distress"),
    ("Widow Pension Scheme", "Widowed women", "Adult women", "Monthly pension support for widows", "Senior Citizen"),
    ("Sanjay Gandhi Niradhar Yojana", "Destitute women and families", "Eligible families", "Monthly financial assistance Rs. 1000-1200", "Senior Citizen"),
    ("Inter-Caste Marriage Incentive Scheme", "Inter-caste couples", "Adult couples", "Financial incentive for inter-caste marriage", "Family"),
    ("Manodhairya Scheme", "Women victims of crimes", "Women and girls", "Compensation Rs. 1-10 lakhs plus rehabilitation", "Family/Distress"),
    ("Indira Gandhi National Widow Pension Scheme", "Widows below poverty line", "40-79 years", "Monthly pension of Rs. 1500", "Senior Citizen"),
    ("Indira Gandhi National Old Age Pension Scheme", "Elderly women", "60+ years", "Monthly pension support for senior citizens", "Senior Citizen"),
    ("Shravanbal Seva State Pension Scheme", "Senior citizens", "65+ years", "Monthly financial assistance for elderly", "Senior Citizen"),
    ("Annapurna Scheme", "Elderly poor women", "Senior citizens", "Free food grains every month", "Senior Citizen"),
]

c.executemany("INSERT INTO schemes VALUES (NULL,?,?,?,?,?)", schemes)
conn.commit()
conn.close()
print("Database created with", len(schemes), "schemes!")