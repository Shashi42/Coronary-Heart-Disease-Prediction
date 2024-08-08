from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
import numpy as np
import pandas as pd
from django.core.files.storage import FileSystemStorage
#Base learners
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
#Stacked learner
from sklearn.neural_network import MLPClassifier
#For loading saved models
import joblib
# Create your views here.
def Home(request):
    if 'predict' in request.POST:
        return redirect('Form')
    if 'dpredict' in request.POST:
        return redirect('Fileupload')
    return render(request, 'home.html', {})

def Form(request):
    if request.method=="POST":
        age = int(request.POST.get("Age"))
        sex = int(request.POST.get("Sex"))
        cp = int(request.POST.get("cp"))
        trestbps = int(request.POST.get("trestbps"))
        chol = int(request.POST.get("chol"))
        fbs = int(request.POST.get("fbs"))
        restecg = int(request.POST.get("restecg"))
        thalach = int(request.POST.get("thalach"))
        exang = int(request.POST.get("exang"))
        oldpeak = float(request.POST.get("oldpeak"))
        slope = int(request.POST.get("slope"))
        ca = int(request.POST.get("ca"))
        thal = int(request.POST.get("thal"))
        row = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        print(row)
        #row will have [0:age,1:sex,2:cp,3:trestbps,4:chol,5:fbs,6:restecg,7:thalach,8:exang,9:oldpeak,10:slope,11:ca,12:thal]
        request.session['row']=row
        return redirect("Result")
    return render(request, 'form.html', {})

def Fileupload(request):
    if request.method=="POST":
        fs = FileSystemStorage("../HDPS_site/user_files/")
        patientdata = request.FILES['patientdata']
        fs.save("patientdata.csv",patientdata)
        print("Success")
        return redirect("DResult")
    return render(request, 'fileupload.html', {})

def Result(request):
    if 'predict' in request.POST:
        return render(request, 'form.html', {},  RequestContext(request))
    cparr = [0,0,0,0]
    thalarr = [0,0,0,0]
    slopearr = [0,0,0]
    row = request.session['row']
    #Dictionary
    keys=['Age','Sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
    rowd = {}
    for i in range(len(keys)):
        rowd[keys[i]] = row[i]
    print("Dictionary row")
    print(rowd)
    #data for dummy columns
    cparr[row[2]] = 1
    thalarr[row[12]] = 1
    slopearr[row[10]] = 1
    #row for testing ,replace  2:cp, 10:slope ,12:thal
    #    age,sex -> trestbps to oldpeak -> ca -> cp ,thal, slope
    trow = row[:2]+row[3:10] + [row[11]] + cparr + thalarr + slopearr
    print(trow)
    print(len(trow))
    #making dataframe with the trow
    new_df = pd.DataFrame(columns=['age', 'sex', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang','oldpeak', 'ca', 'cp_0', 'cp_1', 'cp_2', 'cp_3', 'thal_0','thal_1', 'thal_2', 'thal_3', 'slope_0', 'slope_1', 'slope_2'], data=[trow])
    #importing pre normalized data
    x_data = pd.read_csv("../HDPS_project/xfornorm.csv")
    print(x_data)
    #Normalizing new instance
    new_df = (new_df.head() - np.min(x_data)) / (np.max(x_data) - np.min(x_data)).values
    print("Normalized row :")
    print(type(new_df))

    #Loading base and stacked models
    svm = joblib.load("../HDPS_project/SVM.sav")
    rf = joblib.load("../HDPS_project/RF.sav")
    ld_snn = joblib.load("../HDPS_project/StackedNN.sav")

    print("SVM Results")
    print(svm.predict(new_df))
    print("RF Results")
    print(rf.predict(new_df))

    #Making new dataframe from base predictions
    base=[]
    base.append(svm.predict(new_df))
    base.append(rf.predict(new_df))
    print(type(base))
    new_df = pd.DataFrame(columns=['SVM','RF'], data=[base])
    print(new_df)
    #Stacked Neural Networks
    res = ld_snn.predict(new_df)
    print("Neural Network Results")
    print(res[0])
    print("Probability")
    print(ld_snn.predict_proba(new_df))
    strres = "No risk" if(res[0]==0) else "At risk"
    return render(request, 'Results.html', {'riskresult': strres , 'formdata' : rowd})

#Doctors results view
def DResult(request):
    print("co,ing to dresults")
    cparr = [0,0,0,0]
    thalarr = [0,0,0,0]
    slopearr = [0,0,0]
    #patient data as csv
    pdata = pd.read_csv("../HDPS_site/user_files/patientdata.csv")
    pdata1 = pdata.loc[:, ~pdata.columns.str.contains('^PatientID')]
    # -------------------------------Check if data format is correct.---------------------------------------------
    # if check() == -1:
    #   return render_to_response('Invalid.html', {})     #_____________________________make html file.
    # else:
    #   continue below code here.
    # preprocessing the data.
    rows_list = []
    for row in pdata1.itertuples():
            cparr = [0,0,0,0]
            thalarr = [0,0,0,0]
            slopearr = [0,0,0]
            cparr[row[3]] = 1
            thalarr[row[13]] = 1
            slopearr[row[11]] = 1
            # get input row in dictionary format
            # key = col_name
            dict1 = {'age': row[1] , 'sex':row[2] , 'trestbps':row[4] , 'chol':row[5] , 'fbs':row[6] , 'restecg':row[7] , 'thalach':row[8] , 'exang':row[9] ,'oldpeak':row[10] , 'ca':row[12] , 'cp_0':cparr[0] , 'cp_1':cparr[1] , 'cp_2':cparr[2] , 'cp_3':cparr[3] , 'thal_0':thalarr[0] ,'thal_1':thalarr[1] , 'thal_2':thalarr[2] , 'thal_3':thalarr[3] , 'slope_0':slopearr[0] , 'slope_1':slopearr[1] , 'slope_2':slopearr[2]}
            rows_list.append(dict1)
    df2 = pd.DataFrame(rows_list,columns=['age', 'sex', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang','oldpeak', 'ca', 'cp_0', 'cp_1', 'cp_2', 'cp_3', 'thal_0','thal_1', 'thal_2', 'thal_3', 'slope_0', 'slope_1', 'slope_2'])

    #Importing normalized data
    x_data = pd.read_csv("../HDPS_project/xfornorm.csv")
    #Normalizing data
    new_df = (df2 - np.min(x_data)) / (np.max(x_data) - np.min(x_data)).values


    #Loading base and stacked models
    svm = joblib.load("../HDPS_project/SVM.sav")
    rf = joblib.load("../HDPS_project/RF.sav")
    ld_snn = joblib.load("../HDPS_project/StackedNN.sav")

    print("SVM Results")
    svmpred = svm.predict(new_df)
    print(svm.predict(new_df))
    print("RF Results")
    rfpred = rf.predict(new_df)
    print(rf.predict(new_df))

    #Making new dataframe from base predictions
    base=[]
    tmp=[]
    for i in range(0,len(svmpred)):
        dict1 = {'SVM' : svmpred[i], 'RF' : rfpred[i]}
        base.append(dict1)
        # tmp = [ svmpred[i] , rfpred[i] ]
        # base[i] =
    #
    # base.append(svm.predict(new_df))
    # base.append(rf.predict(new_df))
    print(base)
    print(type(base))
    new_df = pd.DataFrame(base,columns=['SVM','RF'])
    print(new_df)

    #Stacked layer predictions
    res = ld_snn.predict(new_df)
    print("Neural Network results")
    print(res)
    print("Probability")
    print(ld_snn.predict_proba(new_df))
    #sending Results
    patientresults = {}
    ids = list(pdata['PatientID'])
    ris = list(res)
    for i in range(0,len(ids)):
        patientresults[ids[i]] = "No risk" if(ris[i]==0) else "At risk"
    print(patientresults)
    print(type(patientresults))
    return render(request, 'DResults.html', {'patientsrisk': patientresults})
