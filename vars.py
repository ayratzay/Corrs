

#siblings are indies which are very similar to each other
#name is a way to represent column in chartio. Always as unicode

data_types = {
        u'stress': {'dt': 'dis', 'siblings': [], 'name': u'stress'},
        u'vegetative': {'dt': 'dis', 'siblings': [], 'name': u'vegetative'},
        u'pnn50': {'dt': 'dis', 'siblings': [u'vegetative', u' stress_level', u'stress', u'rmssd', u'sd1', u'sd2', u'tinn', u'sdnn', u'hrvi'], 'name': u'pNN50'},
        u'bpm': {'dt': 'dis', 'siblings': [], 'name': u'BPM'},
        u'fracdim': {'dt': 'dis', 'siblings': [], 'name': u'FracDim'},
        u'power': {'dt': 'dis', 'siblings': [], 'name': u'Power'},
        u'hf': {'dt': 'dis', 'siblings': [], 'name': u'hf'},
        u'lf': {'dt': 'dis', 'siblings': [], 'name': u'lf'},
        u'lfhf': {'dt': 'dis', 'siblings': [], 'name': u'lfhf'},
        u'vlf': {'dt': 'dis', 'siblings': [], 'name': u'vlf'},
        u'ulf': {'dt': 'dis', 'siblings': [], 'name': u'ulf'},
        u'sdann': {'dt': 'dis', 'siblings': [], 'name': u'SDANN'},
        u'hrvi': {'dt': 'dis', 'siblings': [], 'name': u'HRVI'},
        u'sd1': {'dt': 'dis', 'siblings': [], 'name': u'SD1'},
        u'sd2': {'dt': 'dis', 'siblings': [], 'name': u'SD2'},
        u'rmssd': {'dt': 'dis', 'siblings': [], 'name': u'rMSSD'},
        u'apen': {'dt': 'dis', 'siblings': [], 'name': u'ApEn'},
        u'sdnnind': {'dt': 'dis', 'siblings': [], 'name': u'SDNNIND'},
        u'tinn': {'dt': 'dis', 'siblings': [], 'name': u'TINN'},
        u'stdrr': {'dt': 'dis', 'siblings': [], 'name': u'STDRR'},
        u'mean hr': {'dt': 'dis', 'siblings': [], 'name': u'Mean HR'},
        u'hr std': {'dt': 'dis', 'siblings': [], 'name': u'HR STD'},
        u'beats': {'dt': 'dis', 'siblings': [], 'name': u'beats'},
        u'madrr': {'dt': 'dis', 'siblings': [], 'name': u'madrr'},
        u'stdhr': {'dt': 'dis', 'siblings': [], 'name': u'stdhr'},
        u'meanhr': {'dt': 'dis', 'siblings': [], 'name': u'meanhr'},
        u'irrr': {'dt': 'dis', 'siblings': [], 'name': u'irrr'},
        u'maxhr': {'dt': 'dis', 'siblings': [], 'name': u'maxhr'},
        u'sdnnidx': {'dt': 'dis', 'siblings': [], 'name': u'sdnnidx'},
        u'minhr': {'dt': 'dis', 'siblings': [], 'name': u'minhr'},
        u'meanrr': {'dt': 'dis', 'siblings': [], 'name': u'meanrr'},
        u'stress_out': {'dt': 'dis', 'siblings': [], 'name': u'stress_out'},
        u'diff': {'dt': 'dis', 'siblings': [], 'name': u'diff'},
        u'humidity': {'dt': 'dis', 'siblings': [], 'name': u'humidity'},
        u'pressure': {'dt': 'dis', 'siblings': [], 'name': u'pressure'},
        u'temp': {'dt': 'dis', 'siblings': [], 'name': u'temp'},
        u'temp_max': {'dt': 'dis', 'siblings': [], 'name': u'temp_max'},
        u'deg': {'dt': 'dis', 'siblings': [], 'name': u'deg'},
        u'speed': {'dt': 'dis', 'siblings': [], 'name': u'speed'},
        u'all': {'dt': 'dis', 'siblings': [], 'name': u'all'},
        u'temp_min': {'dt': 'dis', 'siblings': [], 'name': u'temp_min'},
        u'grnd_level': {'dt': 'dis', 'siblings': [], 'name': u'grnd_level'},
        u'sea_level': {'dt': 'dis', 'siblings': [], 'name': u'BPM'},
        u'weight': {'dt': 'dis', 'siblings': [], 'name': u'weight'},
        u'height': {'dt': 'dis', 'siblings': [], 'name': u'height'},
        u'heart_rate': {'dt': 'dis', 'siblings': [], 'name': u'heart_rate'},
        u'body_fat': {'dt': 'dis', 'siblings': [], 'name': u'body_fat'},
        u'systolic': {'dt': 'dis', 'siblings': [], 'name': u'systolic'},
        u'diastolic': {'dt': 'dis', 'siblings': [], 'name': u'diastolic'},
        u'blood_glucose': {'dt': 'dis', 'siblings': [], 'name': u'blood_glucose'},
        u'blood_oxygen': {'dt': 'dis', 'siblings': [], 'name': u'blood_oxygen'},
        u'air_oxygen': {'dt': 'dis', 'siblings': [], 'name': u'air_oxygen'},
        u'duration': {'dt': 'dis', 'siblings': [], 'name': u'duration'},
        u'distance': {'dt': 'dis', 'siblings': [], 'name': u'distance'},
        u'steps': {'dt': 'dis', 'siblings': [], 'name': u'steps'},
        u'calories': {'dt': 'dis', 'siblings': [], 'name': u'calories'},
        u'calories_ate': {'dt': 'dis', 'siblings': [], 'name': u'calories_ate'},
        u'carbohydrate': {'dt': 'dis', 'siblings': [], 'name': u'carbohydrate'},
        u'fat': {'dt': 'dis', 'siblings': [], 'name': u'fat'},
        u'protein': {'dt': 'dis', 'siblings': [], 'name': u'protein'},
        u'sodium': {'dt': 'dis', 'siblings': [], 'name': u'sodium'},
        u'sugar': {'dt': 'dis', 'siblings': [], 'name': u'sugar'},
        u'fiber': {'dt': 'dis', 'siblings': [], 'name': u'fiber'},
        u'saturatedfat': {'dt': 'dis', 'siblings': [], 'name': u'saturatedFat'},
        u'monounsaturatedfat': {'dt': 'dis', 'siblings': [], 'name': u'monounsaturatedFat'},
        u'polyunsaturatedfat': {'dt': 'dis', 'siblings': [], 'name': u'polyunsaturatedFat'},
        u'cholesterol': {'dt': 'dis', 'siblings': [], 'name': u'cholesterol'},
        u'vitamina': {'dt': 'dis', 'siblings': [], 'name': u'vitaminA'},
        u'vitaminc': {'dt': 'dis', 'siblings': [], 'name': u'vitaminC'},
        u'calcium': {'dt': 'dis', 'siblings': [], 'name': u'calcium'},
        u'iron': {'dt': 'dis', 'siblings': [], 'name': u'iron'},
        u'potassium': {'dt': 'dis', 'siblings': [], 'name': u'potassium'},
        u'timeAsleep': {'dt': 'dis', 'siblings': [], 'name': u'timeAsleep'},
        u'timeAwake': {'dt': 'dis', 'siblings': [], 'name': u'timeAwake'},
        u'efficiency': {'dt': 'dis', 'siblings': [], 'name': u'efficiency'},
        u'timeToFallAsleep': {'dt': 'dis', 'siblings': [], 'name': u'timeToFallAsleep'},
        u'timeAfterWakeup': {'dt': 'dis', 'siblings': [], 'name': u'timeAfterWakeup'},
        u'timeInBed': {'dt': 'dis', 'siblings': [], 'name': u'timeInBed'},
        u'business_percentage': {'dt': 'dis', 'siblings': [], 'name': u'business_percentage'},
        u'communication_and_scheduling_percentage': {'dt': 'dis', 'siblings': [], 'name': u'communication_and_scheduling_percentage'},
        u'social_networking_percentage': {'dt': 'dis', 'siblings': [], 'name': u'social_networking_percentage'},
        u'design_and_composition_percentage': {'dt': 'dis', 'siblings': [], 'name': u'design_and_composition_percentage'},
        u'entertainment_percentage': {'dt': 'dis', 'siblings': [], 'name': u'entertainment_percentage'},
        u'news_percentage': {'dt': 'dis', 'siblings': [], 'name': u'news_percentage'},
        u'software_development_percentage': {'dt': 'dis', 'siblings': [], 'name': u'software_development_percentage'},
        u'reference_and_learning_percentage': {'dt': 'dis', 'siblings': [], 'name': u'reference_and_learning_percentage'},
        u'shopping_percentage': {'dt': 'dis', 'siblings': [], 'name': u'shopping_percentage'},
        u'utilities_percentage': {'dt': 'dis', 'siblings': [], 'name': u'utilities_percentage'},
        u'total_hours': {'dt': 'dis', 'siblings': [], 'name': u'total_hours'}}