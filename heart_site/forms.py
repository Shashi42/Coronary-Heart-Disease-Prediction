from django import forms
from datetime import datetime

from django.urls import reverse_lazy
from .models import Patient

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PatientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'patient-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('heart_site:index'),
            'hx-target': '#patient-form',
            'hx-swap': 'outerHTML'
        }
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Patient
        fields = ['age', 'gender', 'chest_pain_type', 'resting_blood_pressure', 'serum_cholestrol_level', 'fasting_blood_sugar_greater_than_120mgdl', 'resting_ecg_results', 'max_heart_rate_achieved', 'exercise_induced_angina', 'st_depression_exercise_rest', 'slope_peak_exercise_st_segment', 'major_vessels_colored', 'defect_type']
        labels = {
            'age': "Age",
            'gender': "Gender",
            'chest_pain_type': "Type of Chest Pain", 
            'resting_blood_pressure': "Resting Blood Pressure reading (in mm Hg)", 
            'serum_cholestrol_level': "Serum Cholestrol Level (in mg/dl)", 
            'fasting_blood_sugar_greater_than_120mgdl': "Is the Fasting Blood Sugar Level greater than 120 mg/dl? ", 
            'resting_ecg_results': "Resting Electrocardiographic Results", 
            'max_heart_rate_achieved': "Maximum Heart Rate Achieved", 
            'exercise_induced_angina': "Is there any Exercise Induced Angina?", 
            'st_depression_exercise_rest': "Value of ST Depression induces by exercise relative to rest", 
            'slope_peak_exercise_st_segment': "The Slope of the peak exercise ST segment", 
            'major_vessels_colored': "Number of Major Vessels (0-3) colored by Flourosopy", 
            'defect_type': "Type of Defect"
        }

