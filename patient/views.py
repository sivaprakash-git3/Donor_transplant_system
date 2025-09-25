from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home/home.html')

def patient_home(request):
    return render(request,'patient/patient_home.html')

def patient_signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        patient_details(name=name,email=email,password=password,phone=phone,address=address).save()
        messages.success(request, 'Sucessfully Signed Up.')
    else:
        messages.success(request, 'Something Went Wrong.')
    return render(request,'patient/patient_login.html')

def patient_login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp=patient_details.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['patient'] = emp.email
            return render(request,'patient/patient_home.html')

        except:
            messages.success(request, 'Invalid Email And Password')
            return redirect('/patient_login/')

    return render(request,'patient/patient_login.html')

def patient_logout(request):
    if 'patient' in request.session:
        request.session.pop('patient',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/')

def eye_details(request):
    if request.method=="POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        iop = request.POST["iop"]
        visual_acuity = request.POST["visual_acuity"]
        corneal_thickness = request.POST["corneal_thickness"]
        corneal_topo = request.POST["corneal_topo"]
        tissue_type = request.POST["tissue_type"]
        corneal_curvature = request.POST["corneal_curvature"]
        corneal_dia = request.POST["corneal_dia"]
        endothelial = request.POST["endothelial"]
        patient_eye_registration(full_name=full_name, email=email, iop=iop, visual_acuity=visual_acuity,
        corneal_thickness=corneal_thickness,corneal_topo=corneal_topo, tissue_type=tissue_type,
        corneal_curvature=corneal_curvature, corneal_dia=corneal_dia,endothelial=endothelial).save()
        admin_patient(full_name=full_name,email=email,organ="Eye",disease_status="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'patient/patient_eye_regi.html')

def heart_details(request):
    if request.method=="POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        ejection_fraction = request.POST["ejection_fraction"]
        pap = request.POST["pap"]
        pvg = request.POST["pvg"]
        aortic_valve = request.POST["aortic_valve"]
        lavi = request.POST["lavi"]
        lvef = request.POST["lvef"]
        mitral_valve_regurgitation = request.POST["mitral_valve_regurgitation"]
        mitral_valve_stenosis = request.POST["mitral_valve_stenosis"]
        wall_motion = request.POST["wall_motion"]
        qt_interval = request.POST["qt_interval"]
        qrs_duration = request.POST["qrs_duration"]
        atrial = request.POST["atrial"]
        bradycardia = request.POST["bradycardia"]
        heart_rate = request.POST["heart_rate"]
        p_wave = request.POST["p_wave"]
        pulmonary = request.POST["pulmonary"]
        cardiac_o = request.POST["cardiac_o"]
        coronary_art = request.POST["coronary_art"]
        coronary_ani = request.POST["coronary_ani"]
        mild_stenosis = request.POST["mild_stenosis"]
        moderate_stenosis = request.POST["moderate_stenosis"]
        ffr = request.POST["ffr"]
        stenosis = request.POST["stenosis"]
        heart_size = request.POST["heart_size"]
        hemo = request.POST["hemo"]
        blood_type = request.POST["blood_type"]
        tissue_type = request.POST["tissue_type"]
        patient_heart_re(full_name=full_name, email=email, ejection_fraction=ejection_fraction, pap=pap, pvg=pvg,aortic_valve=aortic_valve,lavi=lavi, lvef=lvef, mitral_valve_regurgitation=mitral_valve_regurgitation,mitral_valve_stenosis=mitral_valve_stenosis, wall_motion=wall_motion,
                      qt_interval=qt_interval, qrs_duration=qrs_duration, atrial=atrial, bradycardia=bradycardia, heart_rate=heart_rate, p_wave=p_wave, pulmonary=pulmonary, cardiac_o=cardiac_o, coronary_art=coronary_art, coronary_ani=coronary_ani,mild_stenosis=mild_stenosis, moderate_stenosis=moderate_stenosis, ffr=ffr, stenosis=stenosis, heart_size=heart_size, hemo=hemo, blood_type=blood_type, tissue_type=tissue_type).save()
        admin_patient(full_name=full_name, email=email, organ="Heart", disease_status="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')

    return render(request, 'patient/patient_heart_regi.html')

def liver_details(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        aspartate = request.POST["aspartate"]
        alanine = request.POST["alanine"]
        bilirubin = request.POST["bilirubin"]
        platelets = request.POST["platelets"]
        alkaline = request.POST["alkaline"]
        albumin = request.POST["albumin"]
        hepatitis = request.POST["hepatitis"]
        afp = request.POST["afp"]
        liver_biopsy = request.POST["liver_biopsy"]
        imaging_test = request.POST["imaging_test"]
        CDT = request.POST["CDT"]
        EtG = request.POST["EtG"]
        PEth = request.POST["PEth"]
        blood_type = request.POST["blood_type"]
        tissue_type = request.POST["tissue_type"]
        cross_test = request.POST["cross_test"]
        viral_test = request.POST["viral_test"]
        patient_liver_re(full_name=full_name, email=email, aspartate=aspartate, alanine=alanine, bilirubin=bilirubin,
                platelets=platelets,alkaline=alkaline, albumin=albumin, hepatitis=hepatitis,afp=afp, liver_biopsy=liver_biopsy,
                imaging_test=imaging_test, CDT=CDT, EtG=EtG, PEth=PEth,blood_type=blood_type,tissue_type=tissue_type,
                cross_test=cross_test,viral_test=viral_test).save()
        admin_patient(full_name=full_name, email=email, organ="Liver", disease_status="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'patient/patient_liver_regi.html')

def lungs_details(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        fev = request.POST["fev"]
        chest_x_ray = request.POST["chest_x_ray"]
        pef = request.POST["pef"]
        bpt = request.POST["bpt"]
        blood_test = request.POST["blood_test"]
        tumor_size = request.POST["tumor_size"]
        sputum_culture = request.POST["sputum_culture"]
        tst = request.POST["tst"]
        igras = request.POST["igras"]
        ct_scan = request.POST["ct_scan"]
        mri_scan = request.POST["mri_scan"]
        pet_scan = request.POST["pet_scan"]
        blood_type = request.POST["blood_type"]
        tissue_type = request.POST["tissue_type"]
        crossmatch = request.POST["crossmatch"]
        viral_test = request.POST["viral_test"]
        patient_lungs_re(full_name=full_name, email=email, fev=fev, chest_x_ray=chest_x_ray, pef=pef,
                bpt=bpt, blood_test=blood_test, tumor_size=tumor_size, sputum_culture=sputum_culture, tst=tst,igras=igras,
                ct_scan=ct_scan, mri_scan=mri_scan, pet_scan=pet_scan, blood_type=blood_type, tissue_type=tissue_type,
                crossmatch=crossmatch,viral_test=viral_test).save()
        admin_patient(full_name=full_name, email=email, organ="Lungs", disease_status="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'patient/patient_lungs_regi.html')

def kidney_details(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        creatinine = request.POST["creatinine"]
        bun = request.POST["bun"]
        urine_albumin = request.POST["urine_albumin"]
        urine_protien = request.POST["urine_protien"]
        serum_creatinine = request.POST["serum_creatinine"]
        urine_output = request.POST["urine_output"]
        urinalysis = request.POST["urinalysis"]
        rbc = request.POST["rbc"]
        kidney_biopsy = request.POST["kidney_biopsy"]
        immunological = request.POST["immunological"]
        blood_type = request.POST["blood_type"]
        tissue_type = request.POST["tissue_type"]
        cross_test = request.POST["cross_test"]
        imaging = request.POST["imaging"]
        viral_test = request.POST["viral_test"]
        patient_kidney_re(full_name=full_name, email=email, creatinine=creatinine, bun=bun, urine_albumin=urine_albumin,
                urine_protien=urine_protien, serum_creatinine=serum_creatinine, urine_output=urine_output, urinalysis=urinalysis, rbc=rbc,kidney_biopsy=kidney_biopsy,
                immunological=immunological, blood_type=blood_type, tissue_type=tissue_type, cross_test=cross_test, imaging=imaging,
                viral_test=viral_test).save()
        admin_patient(full_name=full_name, email=email, organ="Kidney", disease_status="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'patient/patient_kidney_regi.html')

def pat_agreement(request):
    eye = patient_eye_registration.objects.all()
    heart = patient_heart_re.objects.all()
    liv = patient_liver_re.objects.all()
    lun = patient_lungs_re.objects.all()
    kid = patient_kidney_re.objects.all()
    a = {'patient_eye_registration': eye,
          'patient_heart_re': heart,
          'patient_liver_re': liv,
          'patient_lungs_re': lun,
          'patient_kidney_re': kid}

    return render(request, 'patient/patient_agreement.html', {'a': a})

def pa_agree(request, id, table_):
    if table_ == 'patient_eye_registration':
        user_app = patient_eye_registration.objects.get(id=id)
        user_app.approved = 1
        user_app.save()
    elif table_ == 'patient_heart_re':
        user_app = patient_heart_re.objects.get(id=id)
        user_app.approved = 1
        user_app.save()
    elif table_ == 'patient_liver_re':
        user_app = patient_liver_re.objects.get(id=id)
        user_app.approved = 1
        user_app.save()
    elif table_ == 'patient_lungs_re':
        user_app = patient_lungs_re.objects.get(id=id)
        user_app.approved = 1
        user_app.save()
    elif table_ == 'patient_kidney_re':
        user_app = patient_kidney_re.objects.get(id=id)
        user_app.approved = 1
        user_app.save()
    else:
        messages.success(request, 'No match.')
        pass

    messages.success(request, 'Approved Sucessfully.')
    return redirect('/pat_agree/')

def pat_ignore(request, id, table_):
    if table_ == 'patient_eye_registration':
        user_app = patient_eye_registration.objects.get(id=id)
        user_app.delete()
    elif table_ == 'patient_heart_re':
        user_app = patient_heart_re.objects.get(id=id)
        user_app.delete()
    elif table_ == 'patient_liver_re':
        user_app = patient_liver_re.objects.get(id=id)
        user_app.delete()
    elif table_ == 'patient_lungs_re':
        user_app = patient_lungs_re.objects.get(id=id)
        user_app.delete()
    elif table_ == 'patient_kidney_re':
        user_app = patient_kidney_re.objects.get(id=id)
        user_app.delete()
    else:

        pass
    messages.success(request, 'Deleted Sucessfully.')
    return redirect('/pat_agree/')



def pat_de(request):
    eye = patient_eye_registration.objects.all()
    heart = patient_heart_re.objects.all()
    liv = patient_liver_re.objects.all()
    lun = patient_lungs_re.objects.all()
    kid = patient_kidney_re.objects.all()

    for i in eye:
        if i.boolean == True:
            d = i

    for i in heart:
        if i.boolean == True:
            d = i
    for i in liv:
        if i.boolean == True:
            d = i
    for i in lun:
        if i.boolean == True:
            d = i
    for i in kid:
        if i.boolean == True:
            d = i
    return render(request, 'patient/patient_organ_details.html', {'d': d})
