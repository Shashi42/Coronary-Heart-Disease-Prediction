from django.db import models

# Create your models here.
class Patient(models.Model):

    # Labels Dictionary for Choice Fields
    CHOICE_LABEL_DICT = {
        'gender': [(0, 'Female'), (1, 'Male'), (2, 'Other')],
        'chest_pain_type': [(1, 'Typical Angina'), (2, 'Atypical Angina'), (3, 'Non-Anginal Pain'), (4, 'Asymptomatic')],
        'rest_ecg': [(0, 'Normal'), (1, 'Having ST-T Wave Abnormality'), (2, "Showing probable or definite left ventricular hypertrophy (Estes')")],
        'slope': [(1, "Upsloping"), (2, "Flat"), (3, "Downsloping")],
        'defect_type': [(3, "Normal"), (6, "Fixed Defect"), (7, "Reversable Defect")],
        'Yes/No': [(False, "No"), (True, "Yes")]
    }

    age = models.IntegerField()
    gender = models.CharField(max_length= 10, choices= CHOICE_LABEL_DICT['gender'])
    chest_pain_type = models.CharField(max_length= 20, choices= CHOICE_LABEL_DICT['chest_pain_type'])
    resting_blood_pressure = models.IntegerField()
    serum_cholestrol_level = models.IntegerField()
    # widget= forms.RadioSelect()
    fasting_blood_sugar_greater_than_120mgdl= models.BooleanField(choices= CHOICE_LABEL_DICT['Yes/No'])
    resting_ecg_results = models.CharField(max_length= 100, choices= CHOICE_LABEL_DICT['rest_ecg'])
    max_heart_rate_achieved = models.IntegerField()
    exercise_induced_angina = models.BooleanField(choices= CHOICE_LABEL_DICT['Yes/No'])
    st_depression_exercise_rest = models.FloatField()
    slope_peak_exercise_st_segment = models.CharField(max_length= 20, choices= CHOICE_LABEL_DICT['slope'])
    major_vessels_colored = models.IntegerField()
    defect_type = models.CharField(max_length= 20, choices= CHOICE_LABEL_DICT['defect_type'])