from flask import Flask, render_template, request
import requests
import random
from datetime import datetime

app = Flask(__name__)

# APIs Configuration
API_CONFIG = {
    'english': {
        'url': "https://v2.jokeapi.dev/joke/",
        'fallback': [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "How do you organize a space party? You planet!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call fake spaghetti? An impasta!"
        ]
    },
    'hindi': {
        'url': "https://hindi-jokes-api.onrender.com/random/joke",
        'fallback': [
            "कंप्यूटर: मैं थक गया हूँ। यूजर: क्यों? कंप्यूटर: क्योंकि मेरा 'विंडोज़' बंद नहीं होता!",
            "टीचर: बताओ, 3 और 3 में क्या अंतर है? स्टूडेंट: जी मैडम, एक 'और' का निशान!",
            "पिता: बेटा, तुम्हारी नाक इतनी बड़ी क्यों है? बेटा: पापा, आपके मोबाइल में जैसे 'फुल स्क्रीन डिस्प्ले' होता है, वैसे ही!",
            "डॉक्टर: आपको हर रोज सुबह गर्म पानी पीना चाहिए। मरीज: डॉक्टर साहब, मैं तो गर्म पानी से नहाता हूँ!",
            "शिक्षक: तुम रोज स्कूल क्यों लेट आते हो? छात्र: सर, रास्ते में एक साइनबोर्ड लगा है - 'स्कूल जाने से पहले ध्यान से देखें'!"
        ]
    }
}

# Categories for English jokes
ENGLISH_CATEGORIES = {
    'Any': 'Any',
    'Programming': 'Programming',
    'Misc': 'Miscellaneous',
    'Dark': 'Dark',
    'Pun': 'Pun'
}

def get_joke(language, category="Any"):
    """Get a single joke with proper fallback handling"""
    try:
        if language == 'english':
            # English joke with category
            params = {'safe-mode': True}
            if category != "Any":
                params['category'] = category
            
            response = requests.get(
                API_CONFIG['english']['url'] + category,
                params=params,
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data.get('error', False):
                    if data['type'] == 'single':
                        return data['joke']
                    return f"{data['setup']}\n\n{data['delivery']}"
        
        else:
            # Hindi joke
            response = requests.get(
                API_CONFIG['hindi']['url'],
                timeout=3
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('jokeContent', data.get('joke', None))
    
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"API Error ({language}): {str(e)}")
    
    # Fallback to local jokes if API fails
    return random.choice(API_CONFIG[language]['fallback'])

@app.route('/', methods=['GET', 'POST'])
def index():
    joke = None
    jokes = None
    
    if request.method == 'POST':
        language = request.form.get('language', 'english')
        category = request.form.get('category', 'Any')
        
        if 'single_joke' in request.form:
            joke = get_joke(language, category)
        elif 'five_jokes' in request.form:
            jokes = [get_joke(language, category) for _ in range(5)]
    
    return render_template(
        'index.html',
        joke=joke,
        jokes=jokes,
        english_categories=ENGLISH_CATEGORIES,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == '__main__':
    app.run(debug=True)