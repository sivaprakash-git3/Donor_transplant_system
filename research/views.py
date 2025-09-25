from django.shortcuts import render,redirect
from .models import *
from patient.models import *
from donor.models import *
from django.contrib import messages
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
import catboost as cb

def home(request):
    return render(request,'home/home.html')

def research_home(request):
    return render(request,'research/re_home.html')

def research_signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        research_de(name=name,email=email,password=password,phone=phone,address=address).save()
        messages.success(request, 'Sucessfully Signed Up.')
    else:
        messages.success(request, 'Something Went Wrong.')
    return render(request,'research/research_login.html')

def research_login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp = research_de.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['research'] = emp.email
            return render(request,'research/re_home.html')

        except:
            messages.success(request, 'Invalid Email And Password')
            return redirect('/re_login/')

    return render(request,'research/research_login.html')

def research_logout(request):
    if 'research' in request.session:
        request.session.pop('research',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/')

def research_patient_pre(request):
    eye = patient_eye_registration.objects.all()
    heart = patient_heart_re.objects.all()
    liv = patient_liver_re.objects.all()
    lun = patient_lungs_re.objects.all()
    kid = patient_kidney_re.objects.all()
    pa = {'patient_eye_registration': eye,
         'patient_heart_re': heart,
         'patient_liver_re': liv,
         'patient_lungs_re': lun,
         'patient_kidney_re': kid}
    return render(request,'research/re_pat_pre.html',{'pa':pa})

def research_donor_pre(request):
    eye = eye_details.objects.all()
    heart = heart_details.objects.all()
    liv = liv_reg.objects.all()
    lun = lun_reg.objects.all()
    kid = kid_reg.objects.all()
    do = {'eye_details': eye,
          'heart_details': heart,
          'liv_reg': liv,
          'lun_reg': lun,
          'kid_reg': kid}
    return render(request,'research/re_don_pre.html',{'do':do})


def algo(datas,r,o):
    print(o)
    if o =="eye":
        data = pd.read_csv('a.csv')
    if o =="donor_eye":
        data = pd.read_csv('de.csv')
    elif o == "heart":
        data = pd.read_csv('aa.csv')
    elif o == "liver":
        data = pd.read_csv('liver.csv')
    elif o == "lungs":
        data = pd.read_csv('lungs.csv')
    elif o == 'kidney':
        data = pd.read_csv('kidney.csv')
    data_x = data.iloc[:, :-1]
    data_y = data.iloc[:, -1]
    string_datas = [i for i in data_x.columns if data_x.dtypes[i] == np.object_]
    LabelEncoders = []
    for i in string_datas:
        newLabelEncoder = LabelEncoder()
        data_x[i] = newLabelEncoder.fit_transform(data_x[i])
        LabelEncoders.append(newLabelEncoder)
    ylabel_encoder = None
    if type(data_y.iloc[1]) == str:
        ylabel_encoder = LabelEncoder()
        data_y = ylabel_encoder.fit_transform(data_y)

    model = GradientBoostingClassifier()
    model.fit(data_x, data_y)

    value = {data_x.columns[i]: datas[i] for i in range(len(datas))}
    l = 0
    for i in string_datas:
        z = LabelEncoders[l]
        value[i] = z.transform([value[i]])[0]
        l += 1
    value = [i for i in value.values()]
    predicted = model.predict([value])
    if ylabel_encoder:
        predicted = ylabel_encoder.inverse_transform(predicted)
    return predicted[0]


def get_input(request, id, table_name):
    # if 'user' in request.session:
    eye = patient_eye_registration.objects.all()
    heart = patient_heart_re.objects.all()
    liv = patient_liver_re.objects.all()
    lun = patient_lungs_re.objects.all()
    kid = patient_kidney_re.objects.all()
    pa = {'patient_eye_registration': eye,
          'patient_heart_re': heart,
          'patient_liver_re': liv,
          'patient_lungs_re': lun,
          'patient_kidney_re': kid}


    if table_name == 'patient_eye_registration' :
        get = patient_eye_registration.objects.get(id=id)
        # get = q.get(id=id)
        r = get.id
        inputvar = []
        get.save()
        if int(get.iop) in range(10,21):
            e_a = 1
        else:
            e_a = 0
        if int(get.visual_acuity)<=20:
            e_b = 1
        else:
            e_b = 0
        if int(get.corneal_thickness) in range(500,600):
            e_c = 1
        else:
            e_c = 0
        if get.corneal_topo == "good":
            e_d = 1
        else:
            e_d = 0
        iop = e_a
        visual_acuity = e_b
        corneal_thickness = e_c
        corneal_topo = e_d

        inputvar.append(iop)
        inputvar.append(visual_acuity)
        inputvar.append(corneal_thickness)
        inputvar.append(corneal_topo)

        print('input:', inputvar)
        o = "eye"
        ka = algo(inputvar, r, o)
        print('OUTPUT:', ka)
        st = patient_eye_registration.objects.filter(id=r).update(disease=ka)
        print('st:', st)

        if iop == 0:
            dis = patient_eye_registration.objects.filter(id=r).update(p_type_disease="Glaucoma")

        elif visual_acuity == 0:
            dis = patient_eye_registration.objects.filter(id=r).update(p_type_disease="Legally blind")

        elif corneal_thickness == 0:
            dis = patient_eye_registration.objects.filter(id=r).update(p_type_disease="Keratoconus")

        elif corneal_topo == 0:
            dis = patient_eye_registration.objects.filter(id=r).update(p_type_disease="Change of shape of Eye")

        else:
            dis = patient_eye_registration.objects.filter(id=r).update(p_type_disease="No eye defect")

        bol = patient_eye_registration.objects.filter(id=r).update(boolean="True")
        messages.success(request, 'Sucessfully Predicted.')

    elif table_name=="eye_details":
        get = eye_details.objects.get(id=id)
        r = get.id
        inputvar = []
        get.save()

        if int(get.tonometry) in range(10, 21):
            d_a = 1
        else:
            d_a = 0
        if get.slit_lamp.lower() == "normal exam":
            d_b = 1
        else:
            d_b = 0
        if int(get.pachymetry) in range(520, 550):
            d_c = 1
        else:
            d_c = 0
        if get.serological_testing.lower() == "negative":
            d_d = 1
        else:
            d_d = 0
        if get.culture.lower() == "negative":
            d_e = 1
        else:
            d_e = 0
        if get.microscopy.lower() == "negative":
            d_f = 1
        else:
            d_f = 0

        tonometry = d_a
        slit_lamp = d_b
        pachymetry = d_c
        serological_testing = d_d
        culture = d_e
        microscopy = d_f



        inputvar.append(tonometry)
        inputvar.append(slit_lamp)
        inputvar.append(pachymetry)
        inputvar.append(serological_testing)
        inputvar.append(culture)
        inputvar.append(microscopy)

        print('input:', inputvar)
        o = "donor_eye"
        ka = algo(inputvar, r, o)
        print('OUTPUT:', ka)
        st = eye_details.objects.filter(id=r).update(disease=ka)
        print('st:', st)

        if tonometry == 0:
            dis = eye_details.objects.filter(id=r).update(d_type_disease="Glaucoma")

        elif slit_lamp == 0:
            dis = eye_details.objects.filter(id=r).update(d_type_disease="Conjunctivitis")

        elif pachymetry == 0:
            dis = eye_details.objects.filter(id=r).update(d_type_disease="Keratoconus")
        elif serological_testing == 0:
            dis = eye_details.objects.filter(id=r).update(d_type_disease="Viral Infection")
        elif culture == 0:
            dis = eye_details.objects.filter(id=r).update(d_type_disease="Presence of bacteria, viruses, or fungi")
        elif microscopy == 0:
            dis = eye_details.objects.filter(id=r).update(d_type_disease="Acanthamoeba Keratitis")
        else:
            dis = eye_details.objects.filter(id=r).update(d_type_disease="No eye defect")
        bol = eye_details.objects.filter(id=r).update(boolean="True")
        messages.success(request, 'Sucessfully Predicted.')

    elif table_name == 'patient_heart_re' or table_name == "heart_details":
        if table_name=="patient_heart_re":
            get = patient_heart_re.objects.get(id=id)
        else:
            get = heart_details.objects.get(id=id)
        r = get.id
        print("id:",r)
        inputvar = []
        get.save()

        if int(get.ejection_fraction) > 55:
            a = 1
        else:
            a = 0
        if int(get.pap) in range(8, 20):
            b = 1
        else:
            b = 0
        if int(get.pvg) < 36:
            c = 1
        else:
            c = 0
        if int(get.aortic_valve) < 20:
            d = 1
        else:
            d=0
        if int(get.lavi) < 34:
            e = 1
        else:
            e = 0
        if int(get.lvef) in range(50, 70):
            f = 1
        else:
            f = 0
        if int(get.mitral_valve_regurgitation) < 45:
            g = 1
        else:
            g = 0
        if int(get.mitral_valve_stenosis) <5 :
            h = 1
        else:
            h = 0
        if int(get.wall_motion) in range(0,4):
            i = 1
        else:
            i = 0
        if int(get.qt_interval) in range(350,460):
            j = 1
        else:
            j = 0
        if int(get.qrs_duration) < 12:
            k=1
        else:
            k=0
        if int(get.atrial) in range(60,100):
            l=1
        else:
            l=0
        if int(get.bradycardia) > 60:
            m = 1
        else:
            m=0
        if int(get.heart_rate) in range(60,100):
            n=1
        else:
            n=0
        if int(get.p_wave) in range(80,120):
            o=1
        else:
            o=0
        if int(get.pulmonary) in range(6,12):
            p = 1
        else:
            p=0
        if int(get.cardiac_o) in range(4,8):
            q = 1
        else:
            q=0
        if int(get.coronary_art) in range(6,12):
            r_ = 1
        else:
            r_ = 0
        if int(get.coronary_ani) < 50:
            s = 1
        else:
            s = 0
        if int(get.mild_stenosis) in range(5,25):
            t = 1
        else:
            t = 0
        if int(get.moderate_stenosis) in range(25,50):
            u = 1
        else:
            u = 0
        if int(get.ffr) > 75:
            v = 1
        else:
            v = 0
        if int(get.stenosis) >70:
            w = 1
        else:
            w = 0
        ejection_fraction = a
        pap = b
        pvg = c
        aortic_valve = d
        lavi = e
        lvef = f
        mitral_valve_regurgitation = g
        mitral_valve_stenosis = h
        wall_motion = i
        qt_interval = j
        qrs_duration = k
        atrial = l
        bradycardia = m
        heart_rate = n
        p_wave = o
        pulmonary = p
        cardiac_o = q
        coronary_art = r_
        coronary_ani = s
        mild_stenosis = t
        moderate_stenosis = u
        ffr = v
        stenosis = w

        inputvar.append(ejection_fraction)
        inputvar.append(pap)
        inputvar.append(pvg)
        inputvar.append(aortic_valve)
        inputvar.append(lavi)
        inputvar.append(lvef)
        inputvar.append(mitral_valve_regurgitation)
        inputvar.append(mitral_valve_stenosis)
        inputvar.append(wall_motion)
        inputvar.append(qt_interval)
        inputvar.append(qrs_duration)
        inputvar.append(atrial)
        inputvar.append(bradycardia)
        inputvar.append(heart_rate)
        inputvar.append(p_wave)
        inputvar.append(pulmonary)
        inputvar.append(cardiac_o)
        inputvar.append(coronary_art)
        inputvar.append(coronary_ani)
        inputvar.append(mild_stenosis)
        inputvar.append(moderate_stenosis)
        inputvar.append(ffr)
        inputvar.append(stenosis)

        print('input:', inputvar)
        o = "heart"
        ka = algo(inputvar, r, o)
        print('OUTPUT:', ka)
        if table_name=="patient_heart_re":
            st = patient_heart_re.objects.filter(id=r).update(disease=ka)
            if any(var == 0 for var in
                   [ejection_fraction, pap, pvg, aortic_valve, lavi, lvef, qrs_duration,  pulmonary,
                    cardiac_o, coronary_art, coronary_ani]):
                dis = patient_heart_re.objects.filter(id=r).update(p_type_disease="Congenital heart disease")
            elif any(var == 0 for var in
                     [mitral_valve_regurgitation, mitral_valve_stenosis, atrial, bradycardia,
                      mild_stenosis, moderate_stenosis]):
                dis = patient_heart_re.objects.filter(id=r).update(p_type_disease="Valve Disease")
            elif any(var == 0 for var in
                     [wall_motion, qt_interval, heart_rate, p_wave, ffr, stenosis]):
                dis = patient_heart_re.objects.filter(id=r).update(p_type_disease="Coronary artery disease (CAD)")
            else:
                dis = patient_heart_re.objects.filter(id=r).update(p_type_disease="No disease")
            bol = patient_heart_re.objects.filter(id=r).update(boolean="True")

        else:
            st = heart_details.objects.filter(id=r).update(disease=ka)
            if any(var == 0 for var in
                   [ejection_fraction, pap, pvg, aortic_valve, lavi, lvef, qrs_duration,  pulmonary,
                    cardiac_o, coronary_art, coronary_ani]):
                dis = heart_details.objects.filter(id=r).update(d_type_disease="Congenital heart disease")
            elif any(var == 0 for var in
                     [mitral_valve_regurgitation, mitral_valve_stenosis, atrial, bradycardia,
                      mild_stenosis, moderate_stenosis]):
                dis = heart_details.objects.filter(id=r).update(d_type_disease="Valve Disease")
            elif any(var == 0 for var in
                     [wall_motion, qt_interval, heart_rate, p_wave, ffr, stenosis]):
                dis = heart_details.objects.filter(id=r).update(d_type_disease="Coronary artery disease (CAD)")
            else:
                dis = heart_details.objects.filter(id=r).update(d_type_disease="No disease")
            bol = heart_details.objects.filter(id=r).update(boolean="True")
        print('st:', st)
        messages.success(request, 'Sucessfully Predicted.')

    elif table_name == 'patient_liver_re' or table_name =="liv_reg":
        if table_name == "patient_liver_re":
            get = patient_liver_re.objects.get(id=id)
        else:
            get = liv_reg.objects.get(id=id)
        r = get.id
        inputvar = []
        get.save()

        if int(get.aspartate) in range(10,40):
            l_a = 1
        else:
            l_a = 0
        if int(get.alanine) in range(7,56):
            l_b = 1
        else:
            l_b = 0
        if 0.1 <= float(get.bilirubin) <= 1.2:
            l_c = 1
        else:
            l_c = 0
        if int(get.platelets) in range(150000,450000):
            l_d = 1
        else:
            l_d = 0
        if int(get.alkaline) in range(30,120):
            l_e = 1
        else:
            l_e = 0
        if 3.4 <= float(get.albumin) <= 5.4:
            l_f = 1
        else:
            l_f=0
        if get.hepatitis.lower() == "negative":
            l_g = 1
        else:
            l_g = 0
        if int(get.afp) <=10:
            l_h = 1
        else:
            l_h = 0
        if get.liver_biopsy.lower() == "negative":
            l_i = 1
        else:
            l_i = 0
        if get.imaging_test.lower() == "negative":
            l_j = 1
        else:
            l_j = 0
        if 0.1 <= float(get.CDT) <= 1.2:
            l_k = 1
        else:
            l_k = 0
        if int(get.EtG) > 500:
            l_l = 1
        else:
            l_l = 0
        if int(get.PEth)>20:
            l_m = 1
        else:
            l_m = 0

        aspartate = l_a
        alanine = l_b
        bilirubin = l_c
        platelets = l_d
        alkaline = l_e
        albumin = l_f
        hepatitis = l_g
        afp = l_h
        liver_biopsy = l_i
        imaging_test = l_j
        CDT = l_k
        EtG = l_l
        PEth = l_m

        inputvar.append(aspartate)
        inputvar.append(alanine)
        inputvar.append(bilirubin)
        inputvar.append(platelets)
        inputvar.append(alkaline)
        inputvar.append(albumin)
        inputvar.append(hepatitis)
        inputvar.append(afp)
        inputvar.append(liver_biopsy)
        inputvar.append(imaging_test)
        inputvar.append(CDT)
        inputvar.append(EtG)
        inputvar.append(PEth)

        print('input:', inputvar)
        o = "liver"
        ka = algo(inputvar, r, o)
        print('OUTPUT:', ka)
        if table_name=="patient_liver_re":
            st = patient_liver_re.objects.filter(id=r).update(disease=ka)

            if any(var == 0 for var in
                   [aspartate, alanine, bilirubin, platelets, alkaline, albumin]):
                dis = patient_liver_re.objects.filter(id=r).update(p_type_disease="Cirrhosis")
            elif any(var == 0 for var in
                   [aspartate, alanine, bilirubin, platelets, alkaline, hepatitis]):
                dis = patient_liver_re.objects.filter(id=r).update(p_type_disease="Hepatitis")
            elif any(var == 0 for var in
                   [afp, liver_biopsy, imaging_test]):
                dis = patient_liver_re.objects.filter(id=r).update(p_type_disease="Liver Cancer")
            elif any(var == 0 for var in
                   [CDT, EtG, PEth]):
                dis = patient_liver_re.objects.filter(id=r).update(p_type_disease="Alcoholic liver disease (ALD)")
            else:
                dis = patient_liver_re.objects.filter(id=r).update(p_type_disease="No Disease Healthy")
            bol = patient_liver_re.objects.filter(id=r).update(boolean="True")

        else:
            st = liv_reg.objects.filter(id=r).update(disease=ka)

            if any(var == 0 for var in
                   [aspartate, alanine, bilirubin, platelets, alkaline, albumin]):
                dis = liv_reg.objects.filter(id=r).update(d_type_disease="Cirrhosis")
            elif any(var == 0 for var in
                   [aspartate, alanine, bilirubin, platelets, alkaline, hepatitis]):
                dis = liv_reg.objects.filter(id=r).update(d_type_disease="Hepatitis")
            elif any(var == 0 for var in
                   [afp, liver_biopsy, imaging_test]):
                dis = liv_reg.objects.filter(id=r).update(d_type_disease="Liver Cancer")
            elif any(var == 0 for var in
                   [CDT, EtG, PEth]):
                dis = liv_reg.objects.filter(id=r).update(d_type_disease="Alcoholic liver disease (ALD)")
            else:
                dis = liv_reg.objects.filter(id=r).update(d_type_disease="No Disease Healthy")

            bol = liv_reg.objects.filter(id=r).update(boolean="True")
        messages.success(request, 'Sucessfully Predicted.')


    elif table_name == 'patient_lungs_re' or table_name == "lun_reg":

        if table_name == "patient_lungs_re":
            get = patient_lungs_re.objects.get(id=id)
        else:
            get = lun_reg.objects.get(id=id)

        r = get.id
        inputvar = []
        get.save()

        if int(get.fev)>75:
            lu_a = 1
        else:
            lu_a = 0
        if get.chest_x_ray.lower() == "positive":
            lu_b = 1
        else:
            lu_b = 0
        if int(get.pef) > 80:
            lu_c = 1
        else:
            lu_c = 0
        if int(get.bpt) > 20:
            lu_d = 1
        else:
            lu_d = 0
        if get.blood_test.lower() == "negative":
            lu_e = 1
        else:
            lu_e = 0
        if get.tumor_size.lower() == "negative":
            lu_f = 1
        else:
            lu_f = 0
        if get.sputum_culture.lower() == "negative":
            lu_g = 1
        else:
            lu_g = 0
        if get.tst.lower() == "no tb <5mm":
            lu_h = 1
        else:
            lu_h = 0
        if get.igras.lower() == "negative":
            lu_i = 1
        else:
            lu_i = 0
        if get.ct_scan.lower() == "clean and clear":
            lu_j = 1
        else:
            lu_j = 0
        if get.mri_scan.lower() == "negative":
            lu_k = 1
        else:
            lu_k = 0
        if get.pet_scan.lower() == "negative":
            lu_l = 1
        else:
            lu_l = 0


        fev = lu_a
        chest_x_ray = lu_b
        pef = lu_c
        bpt = lu_d
        blood_test = lu_e
        tumor_size = lu_f
        sputum_culture = lu_g
        tst = lu_h
        igras = lu_i
        ct_scan = lu_j
        mri_scan = lu_k
        pet_scan = lu_l

        inputvar.append(fev)
        inputvar.append(chest_x_ray)
        inputvar.append(pef)
        inputvar.append(bpt)
        inputvar.append(blood_test)
        inputvar.append(tumor_size)
        inputvar.append(sputum_culture)
        inputvar.append(tst)
        inputvar.append(igras)
        inputvar.append(ct_scan)
        inputvar.append(mri_scan)
        inputvar.append(pet_scan)

        print('input:', inputvar)
        o = "lungs"
        ka = algo(inputvar, r, o)
        print('OUTPUT:', ka)
        if table_name == "patient_lungs_re":
            st = patient_lungs_re.objects.filter(id=r).update(disease=ka)

            if any(var == 0 for var in [fev, chest_x_ray, pef, bpt]):
                dis = patient_lungs_re.objects.filter(id=r).update(p_type_disease="Asthma")
            elif any(var == 0 for var in [blood_test, tumor_size, sputum_culture]):
                dis = patient_lungs_re.objects.filter(id=r).update(p_type_disease="Pneumonia ")
            elif any(var == 0 for var in [tst, igras]):
                dis = patient_lungs_re.objects.filter(id=r).update(p_type_disease="TB")
            elif any(var == 0 for var in [ct_scan, mri_scan,pet_scan]):
                dis = patient_lungs_re.objects.filter(id=r).update(p_type_disease="Lung Cancer")
            else:
                dis = patient_lungs_re.objects.filter(id=r).update(p_type_disease="No Disease")
            bol = patient_lungs_re.objects.filter(id=r).update(boolean="True")
        else:
            st = lun_reg.objects.filter(id=r).update(disease=ka)

            if any(var == 0 for var in [fev, chest_x_ray, pef, bpt]):
                dis = lun_reg.objects.filter(id=r).update(d_type_disease="Asthma")
            elif any(var == 0 for var in [blood_test, tumor_size, sputum_culture]):
                dis = lun_reg.objects.filter(id=r).update(d_type_disease="Pneumonia ")
            elif any(var == 0 for var in [tst, igras]):
                dis = lun_reg.objects.filter(id=r).update(d_type_disease="TB")
            elif any(var == 0 for var in [ct_scan, mri_scan,pet_scan]):
                dis = lun_reg.objects.filter(id=r).update(d_type_disease="Lung Cancer")
            else:
                dis = lun_reg.objects.filter(id=r).update(d_type_disease="No Disease")
            bol = lun_reg.objects.filter(id=r).update(boolean="True")
        print('st:', st)
        messages.success(request, 'Sucessfully Predicted.')

    elif table_name == 'patient_kidney_re' or table_name == "kid_reg":

        if table_name == "patient_kidney_re":
            get = patient_kidney_re.objects.get(id=id)
        else:
            get = kid_reg.objects.get(id=id)

        r = get.id
        inputvar = []
        get.save()
        if 0.5 <= float(get.creatinine) <= 1.3:
            k_a = 1
        else:
            k_a = 0
        if int(get.bun) in range(7,20):
            k_b = 1
        else:
            k_b = 0
        if int(get.urine_albumin) < 30:
            k_c = 1
        else:
            k_c = 0
        if int(get.urine_protien) < 150:
            k_d = 1
        else:
            k_d = 0
        if 0.5 <= float(get.serum_creatinine) <= 1.3:
            k_e = 1
        else:
            k_e = 0
        if 0.5 <= float(get.urine_output) <= 1:
            k_f = 1
        else:
            k_f = 0
        if int(get.urinalysis) < 150:
            k_g = 1
        else:
            k_g = 0
        if int(get.rbc) in range(0,5):
            k_h = 1
        else:
            k_h = 0
        if get.kidney_biopsy.lower() == "extent":
            k_i = 1
        else:
            k_i = 0
        if get.immunological.lower() == "no evidence":
            k_j = 1
        else:
            k_j = 0

        creatinine = k_a
        bun = k_b
        urine_albumin = k_c
        urine_protien = k_d
        serum_creatinine = k_e
        urine_output = k_f
        urinalysis = k_g
        rbc = k_h
        kidney_biopsy = k_i
        immunological = k_j

        inputvar.append(creatinine)
        inputvar.append(bun)
        inputvar.append(urine_albumin)
        inputvar.append(urine_protien)
        inputvar.append(serum_creatinine)
        inputvar.append(urine_output)
        inputvar.append(urinalysis)
        inputvar.append(rbc)
        inputvar.append(kidney_biopsy)
        inputvar.append(immunological)

        print('input:', inputvar)
        o = "kidney"
        ka = algo(inputvar, r, o)
        print('OUTPUT:', ka)

        if table_name == "patient_kidney_re":
            st = patient_kidney_re.objects.filter(id=r).update(disease=ka)

            if any(var == 0 for var in [creatinine, bun, urine_albumin, urine_protien]):
                dis = patient_kidney_re.objects.filter(id=r).update(p_type_disease="Chronic Kidney Disease (CKD)")
            elif any(var == 0 for var in [serum_creatinine, urine_output]):
                dis = patient_kidney_re.objects.filter(id=r).update(p_type_disease="Acute kidney injury (AKI)")
            elif any(var == 0 for var in [urinalysis, rbc, kidney_biopsy, immunological]):
                dis = patient_kidney_re.objects.filter(id=r).update(p_type_disease="Glomerulonephritis")
            else:
                dis = patient_kidney_re.objects.filter(id=r).update(p_type_disease="No Disease")

            bol = patient_kidney_re.objects.filter(id=r).update(boolean="True")
            messages.success(request, 'Sucessfully Predicted.')
            return redirect("/re_pat_p/")

        else:
            st = kid_reg.objects.filter(id=r).update(disease=ka)

            if any(var == 0 for var in [creatinine, bun, urine_albumin, urine_protien]):
                dis = kid_reg.objects.filter(id=r).update(d_type_disease="Chronic Kidney Disease (CKD)")
            elif any(var == 0 for var in [serum_creatinine, urine_output]):
                dis = kid_reg.objects.filter(id=r).update(d_type_disease="Acute kidney injury (AKI)")
            elif any(var == 0 for var in [urinalysis, rbc, kidney_biopsy, immunological]):
                dis = kid_reg.objects.filter(id=r).update(d_type_disease="Glomerulonephritis")
            else:
                dis = kid_reg.objects.filter(id=r).update(d_type_disease="No Disease")

            bol = kid_reg.objects.filter(id=r).update(boolean="True")
            messages.success(request, 'Sucessfully Predicted.')
            return redirect("/do_pat_p/")

    return render(request,'research/re_home.html')