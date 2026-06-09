
from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MARATHI_TERMS = {
    'Employment': 'रोजगार',
    'Maternity': 'मातृत्व',
    'Birth & Education': 'जन्म आणि शिक्षण',
    'Child': 'बालक',
    'Adolescent': 'किशोरवयीन',
    'Family': 'कुटुंब',
    'Family/Distress': 'कुटुंब / संकट',
    'Senior Citizen': 'ज्येष्ठ नागरिक',
}

SCHEME_TRANSLATIONS = {
    'Mukhyamantri Majhi Ladki Bahin Yojana': 'मुख्यमंत्री माझी लाडकी बहीण योजना',
    'Beti Bachao Beti Padhao': 'बेटी बचाओ बेटी पढाओ',
    'Sukanya Samriddhi Yojana': 'सुकन्या समृद्धी योजना',
    'Majhi Kanya Bhagyashree Scheme': 'माझी कन्या भाग्यश्री योजना',
    'Balika Samridhi Yojana': 'बालिका समृद्धी योजना',
    'Scheme for Adolescent Girls SAG': 'किशोरवयीन मुलींसाठी योजना',
    'Poshan Abhiyaan': 'पोषण अभियान',
    'Anganwadi Services': 'अंगणवाडी सेवा',
    'ICDS Scheme': 'ICDS योजना',
    'Kishori Shakti Yojana': 'किशोरी शक्ती योजना',
    'SABLA Scheme': 'सबला योजना',
    'Savitribai Phule Scholarship': 'सावित्रीबाई फुले शिष्यवृत्ती',
    'Pre-Matric Scholarship for Girls': 'प्री-मॅट्रिक शिष्यवृत्ती मुलींसाठी',
    'Post-Matric Scholarship': 'पोस्ट-मॅट्रिक शिष्यवृत्ती',
    'Rajarshi Shahu Maharaj Scholarship': 'राजर्षी शाहू महाराज शिष्यवृत्ती',
    'EBC Scholarship Scheme': 'EBC शिष्यवृत्ती योजना',
    'Free Bicycle Scheme for Girls': 'मुलींसाठी मोफत सायकल योजना',
    'Kasturba Gandhi Balika Vidyalaya': 'कस्तुरबा गांधी बालिका विद्यालय',
    'Right to Education Support': 'शिक्षण हक्क सहाय्य',
    'Working Women Hostel Scheme': 'कामकाजी महिला वसतिगृह योजना',
    'Skill India Mission': 'कौशल्य भारत अभियान',
    'PM Kaushal Vikas Yojana': 'पंतप्रधान कौशल विकास योजना',
    'Mahila Samriddhi Loan Scheme': 'महिला समृद्धी कर्ज योजना',
    'Stand Up India Scheme': 'स्टँड अप इंडिया योजना',
    'Mudra Loan Scheme': 'मुद्रा कर्ज योजना',
    'Lakhpati Didi Scheme': 'लखपती दीदी योजना',
    'Maharashtra State Rural Livelihood Mission': 'महाराष्ट्र राज्य ग्रामीण उपजीविका अभियान',
    'Hub for Empowerment of Women': 'महिला सशक्तीकरण केंद्र',
    'STEP Scheme': 'STEP योजना',
    'Mahila E-Haat': 'महिला ई-हाट',
    'PM Matru Vandana Yojana': 'पंतप्रधान मातृ वंदना योजना',
    'Janani Suraksha Yojana': 'जननी सुरक्षा योजना',
    'Janani Shishu Suraksha Karyakram': 'जननी शिशु सुरक्षा कार्यक्रम',
    'Saksham Anganwadi and Poshan 2.0': 'सक्षम अंगणवाडी आणि पोषण 2.0',
    'Surakshit Matritva Aashwasan SUMAN': 'सुरक्षित मातृत्व आश्वासन सुमन',
    'National Creche Scheme': 'राष्ट्रीय पाळणाघर योजना',
    'One Stop Centre Scheme': 'वन स्टॉप सेंटर योजना',
    'Women Helpline 181': 'महिला हेल्पलाईन 181',
    'Ujjawala Scheme': 'उज्ज्वला योजना',
    'Swadhar Greh Scheme': 'स्वाधार गृह योजना',
    'Mahila Police Volunteer Scheme': 'महिला पोलीस स्वयंसेवक योजना',
    'Nari Adalat': 'नारी अदालत',
    'Widow Pension Scheme': 'विधवा निवृत्तीवेतन योजना',
    'Sanjay Gandhi Niradhar Yojana': 'संजय गांधी निराधार योजना',
    'Inter-Caste Marriage Incentive Scheme': 'आंतरजातीय विवाह प्रोत्साहन योजना',
    'Manodhairya Scheme': 'मनोधैर्य योजना',
    'Indira Gandhi National Widow Pension Scheme': 'इंदिरा गांधी राष्ट्रीय विधवा निवृत्तीवेतन योजना',
    'Indira Gandhi National Old Age Pension Scheme': 'इंदिरा गांधी राष्ट्रीय वृद्धापकाळ निवृत्तीवेतन योजना',
    'Shravanbal Seva State Pension Scheme': 'श्रावणबाळ सेवा राज्य निवृत्तीवेतन योजना',
    'Annapurna Scheme': 'अन्नपूर्णा योजना',
}

FOR_WHO_TRANSLATIONS = {
    'Economically weaker women': 'आर्थिकदृष्ट्या दुर्बल महिला',
    'Girls and families': 'मुली आणि कुटुंब',
    'Parents of girl child': 'मुलीचे पालक',
    'Girl children in poor families': 'गरीब कुटुंबातील मुली',
    'Girls from poor families': 'गरीब कुटुंबातील मुली',
    'Adolescent girls': 'किशोरवयीन मुली',
    'Girls and mothers': 'मुली आणि माता',
    'Children and mothers': 'मुले आणि माता',
    'Mothers and children': 'माता आणि मुले',
    'Girl students': 'मुली विद्यार्थिनी',
    'School girls': 'शाळकरी मुली',
    'College girls': 'महाविद्यालयीन मुली',
    'Students from weaker sections': 'दुर्बल घटकातील विद्यार्थी',
    'Economically backward students': 'आर्थिकदृष्ट्या मागास विद्यार्थी',
    'Rural school girls': 'ग्रामीण शाळकरी मुली',
    'Girls from disadvantaged groups': 'वंचित गटातील मुली',
    'Working women': 'कामकाजी महिला',
    'Women job seekers': 'नोकरी शोधणाऱ्या महिला',
    'Young women': 'तरुण महिला',
    'Women entrepreneurs': 'महिला उद्योजक',
    'Small business women': 'लहान व्यवसायातील महिला',
    'Self Help Group women': 'बचत गट महिला',
    'Rural women SHGs': 'ग्रामीण महिला बचत गट',
    'Women across sectors': 'सर्व क्षेत्रातील महिला',
    'Women needing training': 'प्रशिक्षण आवश्यक महिला',
    'Pregnant women': 'गर्भवती महिला',
    'Pregnant mothers': 'गर्भवती माता',
    'Mothers and infants': 'माता आणि बालके',
    'Pregnant and lactating mothers': 'गर्भवती आणि स्तनदा माता',
    'Eligible mothers': 'पात्र माता',
    'Working women with children': 'मुले असलेल्या कामकाजी महिला',
    'Mothers': 'माता',
    'Women facing violence': 'हिंसाचाराला बळी पडलेल्या महिला',
    'Women in distress': 'संकटग्रस्त महिला',
    'Women victims of trafficking': 'मानवी तस्करीच्या बळी महिला',
    'Destitute women': 'निराधार महिला',
    'Community women': 'समुदायातील महिला',
    'Women facing disputes': 'वाद असलेल्या महिला',
    'Widowed women': 'विधवा महिला',
    'Destitute women and families': 'निराधार महिला आणि कुटुंब',
    'Inter-caste couples': 'आंतरजातीय जोडपे',
    'Women victims of crimes': 'गुन्ह्यांच्या बळी महिला',
    'Widows below poverty line': 'दारिद्र्यरेषेखालील विधवा',
    'Elderly women': 'वृद्ध महिला',
    'Senior citizens': 'ज्येष्ठ नागरिक',
    'Elderly poor women': 'गरीब वृद्ध महिला',
    'Adult women': 'प्रौढ महिला',
    'All ages': 'सर्व वयोगट',
    'Women and girls': 'महिला आणि मुली',
    'Adult couples': 'प्रौढ जोडपे',
    'Eligible families': 'पात्र कुटुंब',
    'Youth and adults': 'युवक आणि प्रौढ',
}

AGE_TRANSLATIONS = {
    'Birth onwards': 'जन्मापासून',
    'Below 10 years': '१० वर्षांखाली',
    '14-18 years': '१४-१८ वर्षे',
    '11-18 years': '११-१८ वर्षे',
    'Various': 'विविध',
    '0-6 years': '०-६ वर्षे',
    'School and college': 'शाळा आणि महाविद्यालय',
    'Pre-10th standard': 'इयत्ता १० वी पूर्वी',
    'After 10th standard': 'इयत्ता १० वी नंतर',
    'College students': 'महाविद्यालयीन विद्यार्थी',
    'Eligible students': 'पात्र विद्यार्थी',
    'School-going girls': 'शाळेत जाणाऱ्या मुली',
    'School-age girls': 'शाळेच्या वयाच्या मुली',
    '6-14 years': '६-१४ वर्षे',
    'Adult women': 'प्रौढ महिला',
    'Youth and adults': 'युवक आणि प्रौढ',
    '18+ years': '१८+ वर्षे',
    'Pregnant mothers': 'गर्भवती माता',
    'Eligible mothers': 'पात्र माता',
    'Pregnant women': 'गर्भवती महिला',
    'Mothers': 'माता',
    'All ages': 'सर्व वयोगट',
    'Women and girls': 'महिला आणि मुली',
    '21-65 years': '२१-६५ वर्षे',
    '40-79 years': '४०-७९ वर्षे',
    '60+ years': '६०+ वर्षे',
    '65+ years': '६५+ वर्षे',
    'Senior citizens': 'ज्येष्ठ नागरिक',
    'Adult couples': 'प्रौढ जोडपे',
    'Eligible families': 'पात्र कुटुंब',
}

BENEFIT_TRANSLATIONS = {
    'Rs. 1500 monthly direct benefit transfer': 'दरमहा रु. १५०० थेट लाभ हस्तांतरण',
    'Girl child protection and education': 'मुलींचे संरक्षण आणि शिक्षण',
    'High interest savings account for education and marriage': 'शिक्षण आणि विवाहासाठी उच्च व्याज बचत खाते',
    'Financial support for girls': 'मुलींसाठी आर्थिक सहाय्य',
    'Scholarship and savings support': 'शिष्यवृत्ती आणि बचत सहाय्य',
    'Nutrition and health support': 'पोषण आणि आरोग्य सहाय्य',
    'Nutrition improvement program': 'पोषण सुधारणा कार्यक्रम',
    'Nutrition and preschool services': 'पोषण आणि पूर्वशाळा सेवा',
    'Child nutrition and health': 'बाल पोषण आणि आरोग्य',
    'Skill and health awareness': 'कौशल्य आणि आरोग्य जागरूकता',
    'Nutrition and vocational training': 'पोषण आणि व्यावसायिक प्रशिक्षण',
    'Scholarship support for education': 'शिक्षणासाठी शिष्यवृत्ती सहाय्य',
    'Financial assistance for school girls': 'शाळकरी मुलींसाठी आर्थिक सहाय्य',
    'Fee support for higher education': 'उच्च शिक्षणासाठी फी सहाय्य',
    'Free bicycle for transportation to school': 'शाळेसाठी मोफत सायकल',
    'Free and compulsory education': 'मोफत आणि सक्तीचे शिक्षण',
    'Safe and affordable accommodation': 'सुरक्षित आणि परवडणारी निवास व्यवस्था',
    'Skill development training': 'कौशल्य विकास प्रशिक्षण',
    'Free skill training and certification': 'मोफत कौशल्य प्रशिक्षण आणि प्रमाणपत्र',
    'Business loans at low interest': 'कमी व्याजावर व्यवसाय कर्ज',
    'Startup loans from Rs. 10 lakh to 1 crore': 'रु. १० लाख ते १ कोटी स्टार्टअप कर्ज',
    'Business funding up to Rs. 10 lakh': 'रु. १० लाखांपर्यंत व्यवसाय निधी',
    'Income generation support to earn Rs. 1 lakh per year': 'वार्षिक रु. १ लाख कमाईसाठी सहाय्य',
    'Cash assistance of Rs. 5000 in installments': 'रु. ५००० रोख सहाय्य हप्त्यांमध्ये',
    'Cash incentive for safe institutional delivery': 'सुरक्षित प्रसूतीसाठी रोख प्रोत्साहन',
    'Free maternity care drugs diagnostics and transport': 'मोफत प्रसूती सेवा औषधे निदान आणि वाहतूक',
    'Nutrition support during pregnancy': 'गर्भधारणेदरम्यान पोषण सहाय्य',
    'Free respectful healthcare during delivery': 'प्रसूतीदरम्यान मोफत आदरणीय आरोग्यसेवा',
    'Child daycare facilities for working mothers': 'कामकाजी मातांसाठी बालसंगोपन सुविधा',
    'Legal medical police and shelter support under one roof': 'एकाच छताखाली कायदेशीर वैद्यकीय पोलीस आणि निवारा',
    '24x7 emergency helpline for women': 'महिलांसाठी २४x७ आपत्कालीन हेल्पलाईन',
    'Rescue rehabilitation and reintegration support': 'बचाव पुनर्वसन आणि पुनर्एकीकरण सहाय्य',
    'Shelter food healthcare and vocational training': 'निवारा अन्न आरोग्यसेवा आणि व्यावसायिक प्रशिक्षण',
    'Women safety and community support': 'महिला सुरक्षा आणि समुदाय सहाय्य',
    'Community-based legal support for women': 'महिलांसाठी समुदाय-आधारित कायदेशीर सहाय्य',
    'Monthly pension support for widows': 'विधवांसाठी मासिक निवृत्तीवेतन',
    'Monthly financial assistance Rs. 1000-1200': 'मासिक आर्थिक सहाय्य रु. १०००-१२००',
    'Financial incentive for inter-caste marriage': 'आंतरजातीय विवाहासाठी आर्थिक प्रोत्साहन',
    'Compensation Rs. 1-10 lakhs plus rehabilitation': 'भरपाई रु. १-१० लाख आणि पुनर्वसन',
    'Monthly pension of Rs. 1500': 'रु. १५०० मासिक निवृत्तीवेतन',
    'Monthly pension support for senior citizens': 'ज्येष्ठ नागरिकांसाठी मासिक निवृत्तीवेतन',
    'Monthly financial assistance for elderly': 'वृद्धांसाठी मासिक आर्थिक सहाय्य',
    'Free food grains every month': 'दरमहा मोफत अन्नधान्य',
}

def translate_scheme(scheme, lang):
    if lang != 'mr':
        return scheme
    name = SCHEME_TRANSLATIONS.get(scheme[0], scheme[0])
    for_who = FOR_WHO_TRANSLATIONS.get(scheme[1], scheme[1])
    age = AGE_TRANSLATIONS.get(scheme[2], scheme[2])
    benefit = BENEFIT_TRANSLATIONS.get(scheme[3], scheme[3])
    life_stage = MARATHI_TERMS.get(scheme[4], scheme[4])
    apply_link = scheme[5] if len(scheme) > 5 else '#'
    return (name, for_who, age, benefit, life_stage, apply_link)

def search_schemes(query):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'sakhi.db'))
    c = conn.cursor()
    query = query.lower()

    keywords = {
        'child': 'Birth & Education',
        'girl': 'Birth & Education',
        'baby': 'Birth & Education',
        'birth': 'Birth & Education',
        'education': 'Birth & Education',
        'school': 'Birth & Education',
        'scholarship': 'Birth & Education',
        'adolescent': 'Adolescent',
        'teen': 'Adolescent',
        'maternity': 'Maternity',
        'pregnant': 'Maternity',
        'pregnancy': 'Maternity',
        'mother': 'Maternity',
        'delivery': 'Maternity',
        'employment': 'Employment',
        'job': 'Employment',
        'business': 'Employment',
        'startup': 'Employment',
        'work': 'Employment',
        'loan': 'Employment',
        'skill': 'Employment',
        'family': 'Family',
        'health': 'Family',
        'insurance': 'Family',
        'safety': 'Family/Distress',
        'violence': 'Family/Distress',
        'distress': 'Family/Distress',
        'widow': 'Senior Citizen',
        'senior': 'Senior Citizen',
        'old': 'Senior Citizen',
        'pension': 'Senior Citizen',
        'elderly': 'Senior Citizen',
        'मुलगी': 'Birth & Education',
        'शिक्षण': 'Birth & Education',
        'गर्भवती': 'Maternity',
        'बाळंतपण': 'Maternity',
        'रोजगार': 'Employment',
        'कर्ज': 'Employment',
        'कुटुंब': 'Family',
        'आरोग्य': 'Family',
        'विधवा': 'Senior Citizen',
        'वृद्ध': 'Senior Citizen',
        'सुरक्षा': 'Family/Distress',
    }

    matched_stage = None
    for keyword, stage in keywords.items():
        if keyword in query:
            matched_stage = stage
            break

    if matched_stage:
        c.execute('SELECT name, for_who, age, benefit, life_stage, apply_link FROM schemes WHERE life_stage=?', (matched_stage,))
        results = c.fetchall()
    else:
        words = query.split()
        results = []
        for word in words:
            if len(word) > 2:
                c.execute(
                    '''SELECT name, for_who, age, benefit, life_stage, apply_link FROM schemes
                       WHERE LOWER(name) LIKE ?
                       OR LOWER(life_stage) LIKE ?
                       OR LOWER(for_who) LIKE ?
                       OR LOWER(benefit) LIKE ?''',
                    ('%'+word+'%', '%'+word+'%', '%'+word+'%', '%'+word+'%')
                )
                results.extend(c.fetchall())
        results = list(set(results))

    conn.close()
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    age = int(data.get('age', 0))
    income = data.get('income', 'all')
    marital = data.get('marital', 'all')
    category = data.get('category', 'all')
    lang = data.get('lang', 'en')

    conn = sqlite3.connect(os.path.join(BASE_DIR, 'sakhi.db'))
    c = conn.cursor()
    c.execute('SELECT name, for_who, age, benefit, life_stage, income, marital_status, category, apply_link FROM schemes WHERE min_age <= ? AND max_age >= ?', (age, age))
    all_results = c.fetchall()
    conn.close()

    filtered = []
    for r in all_results:
        scheme_income = r[5]
        scheme_marital = r[6]
        scheme_category = r[7]
        apply_link = r[8]
        income_ok = scheme_income == 'all' or income == 'all' or scheme_income == income
        marital_ok = scheme_marital == 'all' or marital == 'all' or marital in scheme_marital
        category_ok = scheme_category == 'all' or category == 'all' or category in scheme_category
        if income_ok and marital_ok and category_ok:
            filtered.append((r[0], r[1], r[2], r[3], r[4], apply_link))

    if filtered:
        response = []
        for r in filtered:
            translated = translate_scheme(r, lang)
            response.append({
                'name': translated[0],
                'for_who': translated[1],
                'age': translated[2],
                'benefit': translated[3],
                'life_stage': translated[4],
                'apply_link': translated[5]
            })
        return jsonify({'found': True, 'schemes': response})
    else:
        msg = 'तुमच्यासाठी कोणतीही योजना सापडली नाही.' if lang == 'mr' else 'No schemes found for your profile.'
        return jsonify({'found': False, 'message': msg})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    lang = data.get('lang', 'en')
    results = search_schemes(question)
    if results:
        response = []
        for r in results:
            translated = translate_scheme(r, lang)
            response.append({
                'name': translated[0],
                'for_who': translated[1],
                'age': translated[2],
                'benefit': translated[3],
                'life_stage': translated[4],
                'apply_link': translated[5] if len(translated) > 5 else '#'
            })
        return jsonify({'found': True, 'schemes': response})
    else:
        if lang == 'mr':
            msg = 'कोणतीही योजना सापडली नाही. मातृत्व, शिक्षण, रोजगार, कुटुंब असे शब्द वापरा.'
        else:
            msg = 'No schemes found. Try keywords like maternity, education, employment, family, safety, pension.'
        return jsonify({'found': False, 'message': msg})
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    scheme_name = data.get('scheme', '')
    rating = data.get('rating', '')
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'sakhi.db'))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        scheme_name TEXT,
        rating TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('INSERT INTO feedback VALUES (NULL, ?, ?)', (scheme_name, rating))
    conn.commit()
    conn.close()
    return jsonify({'success': True})
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)