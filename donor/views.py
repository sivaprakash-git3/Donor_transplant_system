from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages


def home(request):
    return render(request,'home/home.html')

def donor_home(request):

    return render(request,'donor/donor_home.html')

def donor_signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        donor_details(name=name,email=email,password=password,phone=phone,address=address).save()
        messages.success(request, 'Sucessfully Signed Up.')
    else:
        messages.success(request, 'Something Went Wrong.')
    return render(request,'donor/signup.html')

def donor_login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp=donor_details.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['donor'] = emp.email
            request.session['email'] = emp.email
            return render(request,'donor/donor_home.html')

        except:
            messages.success(request, 'Invalid Email And Password')
            return redirect('/donor_login/')

    return render(request,'donor/signup.html')

def donor_logout(request):
    if 'donor' in request.session:
        request.session.pop('donor',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/')

def donor_registration(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        dod = request.POST["dod"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        martial_status = request.POST["martial_status"]
        cause_of_death = request.POST["cause_of_death"]
        address = request.POST["address"]
        enroll_details(name=name,email=email,gender=gender,phone=phone,dob=dob,dod=dod,height=height,weight=weight,martial_status=martial_status,cause_of_death=cause_of_death,address=address).save()
        messages.success(request, 'Enrolled Sucessfully.')

    return render(request,'donor/donor_registration.html')

def donor_organ_details(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        gender = request.POST["gender"]
        aadhaar_no = request.POST["aadhaar_no"]
        cause_of_death = request.POST["cause_of_death"]
        blood = request.POST["blood"]
        organ_name = request.POST["organ_name"]
        f_consent = request.POST["f_consent"]
        dod = request.POST["dod"]
        medical_conditions = request.POST["medical_conditions"]
        general_appearance = request.POST["general_appearance"]
        cardi_exam = request.POST["cardi_exam"]
        respiratory_health = request.POST["respiratory_health"]
        liver_function = request.POST["liver_function"]
        renal_function = request.POST["renal_function"]
        drug_usage = request.POST["drug_usage"]
        organ_function = request.POST["organ_function"]
        cold_ischemia = request.POST["cold_ischemia"]
        ecg = request.POST["ecg"]
        biopsy = request.POST["biopsy"]
        imaging_test = request.POST["imaging_test"]
        visual_acuity = request.POST["visual_acuity"]
        organ_details(name=name,age=age,email=email,phone=phone,gender=gender,aadhaar_no=aadhaar_no,
                      cause_of_death=cause_of_death,blood=blood,organ_name=organ_name,f_consent=f_consent,dod=dod,
                      medical_conditions=medical_conditions,general_appearance=general_appearance,cardi_exam=cardi_exam
                      ,respiratory_health=respiratory_health,liver_function=liver_function,renal_function=renal_function,
                      drug_usage=drug_usage,organ_function=organ_function,cold_ischemia=cold_ischemia,
                      ecg=ecg,biopsy=biopsy,imaging_test=imaging_test,visual_acuity=visual_acuity).save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'donor/donor_organ_details.html')

def eye_reg(request):
    if request.method == "POST":
        donor_name = request.POST["donor_name"]
        donor_id = request.POST["donor_id"]
        tonometry = request.POST["tonometry"]
        slit_lamp = request.POST["slit_lamp"]
        pachymetry = request.POST["pachymetry"]
        serological_testing = request.POST["serological_testing"]
        culture = request.POST["culture"]
        microscopy = request.POST["microscopy"]
        tissue_type = request.POST["tissue_type"]
        hla = request.POST["hla"]
        corneal_mes = request.POST["corneal_mes"]
        corneal_curv = request.POST["corneal_curv"]
        corneal_topo = request.POST["corneal_topo"]
        corneal_dia = request.POST["corneal_dia"]
        endothelial_cell = request.POST["endothelial_cell"]
        eye_details(donor_name=donor_name, donor_id=donor_id, tonometry=tonometry, slit_lamp=slit_lamp, pachymetry=pachymetry, serological_testing=serological_testing,
                      culture=culture, microscopy=microscopy, tissue_type=tissue_type, hla=hla, corneal_mes=corneal_mes,
                      corneal_curv=corneal_curv, corneal_topo=corneal_topo, corneal_dia=corneal_dia
                      , endothelial_cell=endothelial_cell,organ="Eye").save()
        admin_donor(donor_name=donor_name,donor_id=donor_id,organ="Eye",disease="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'donor/eye_reg.html')

def heart_reg(request):
    if request.method=="POST":
        donor_name = request.POST["donor_name"]
        donor_id = request.POST["donor_id"]
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
        heart_details(donor_name=donor_name, donor_id=donor_id, ejection_fraction=ejection_fraction, pap=pap,pvg=pvg, aortic_valve=aortic_valve,
                    lavi=lavi, lvef=lvef, mitral_valve_regurgitation=mitral_valve_regurgitation, mitral_valve_stenosis=mitral_valve_stenosis, wall_motion=wall_motion,
                    qt_interval=qt_interval, qrs_duration=qrs_duration, atrial=atrial
                    , bradycardia=bradycardia, heart_rate=heart_rate, p_wave=p_wave, pulmonary=pulmonary
                    , cardiac_o=cardiac_o, coronary_art=coronary_art, coronary_ani=coronary_ani, mild_stenosis=mild_stenosis
                    , moderate_stenosis=moderate_stenosis, ffr=ffr, stenosis=stenosis, heart_size=heart_size
                    , hemo=hemo, blood_type=blood_type, tissue_type=tissue_type, organ="Heart").save()
        admin_donor(donor_name=donor_name, donor_id=donor_id, organ="Heart", disease="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'donor/heart_reg.html')

def liver_reg(request):
    if request.method == "POST":
        donor_name = request.POST["donor_name"]
        donor_id = request.POST["donor_id"]
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
        liv_reg(donor_name=donor_name, donor_id=donor_id, aspartate=aspartate, alanine=alanine, bilirubin=bilirubin,
                platelets=platelets,alkaline=alkaline, albumin=albumin, hepatitis=hepatitis,afp=afp, liver_biopsy=liver_biopsy,
                imaging_test=imaging_test, CDT=CDT, EtG=EtG, PEth=PEth,blood_type=blood_type,tissue_type=tissue_type,
                cross_test=cross_test,viral_test=viral_test, organ="Liver").save()
        admin_donor(donor_name=donor_name, donor_id=donor_id, organ="Liver", disease="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'donor/liver_reg.html')

def lungs_reg(request):
    if request.method == "POST":
        donor_name = request.POST["donor_name"]
        donor_id = request.POST["donor_id"]
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
        lun_reg(donor_name=donor_name, donor_id=donor_id, fev=fev, chest_x_ray=chest_x_ray, pef=pef,
                bpt=bpt, blood_test=blood_test, tumor_size=tumor_size, sputum_culture=sputum_culture, tst=tst,igras=igras,
                ct_scan=ct_scan, mri_scan=mri_scan, pet_scan=pet_scan, blood_type=blood_type, tissue_type=tissue_type,
                crossmatch=crossmatch,viral_test=viral_test, organ="Lungs").save()
        admin_donor(donor_name=donor_name, donor_id=donor_id, organ="Lungs", disease="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'donor/lungs_reg.html')

def kidney_reg(request):
    if request.method == "POST":
        donor_name = request.POST["donor_name"]
        donor_id = request.POST["donor_id"]
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
        kid_reg(donor_name=donor_name, donor_id=donor_id, creatinine=creatinine, bun=bun, urine_albumin=urine_albumin,
                urine_protien=urine_protien, serum_creatinine=serum_creatinine, urine_output=urine_output, urinalysis=urinalysis, rbc=rbc,kidney_biopsy=kidney_biopsy,
                immunological=immunological, blood_type=blood_type, tissue_type=tissue_type, cross_test=cross_test, imaging=imaging,
                viral_test=viral_test, organ="Kidney").save()
        admin_donor(donor_name=donor_name, donor_id=donor_id, organ="Kidney", disease="pending").save()
        messages.success(request, 'Enrolled Sucessfully.')
    return render(request,'donor/kidney_reg.html')


def donor_agree(request):
    user_email = request.session.get('email')
    donor = donor_details.objects.get(email=user_email)
    print(donor.name)

    # Filter queryset for each organ detail model to only include objects whose donor name matches user email
    eye_apps = eye_details.objects.filter(donor_name=donor.name)
    heart_apps = heart_details.objects.filter(donor_name=donor.name)
    liv_apps = liv_reg.objects.filter(donor_name=donor.name)
    lun_apps = lun_reg.objects.filter(donor_name=donor.name)
    kid_apps = kid_reg.objects.filter(donor_name=donor.name)

    pa = {
        'eye_details': eye_apps,
        'heart_details': heart_apps,
        'liv_reg': liv_apps,
        'lun_reg': lun_apps,
        'kid_reg': kid_apps
    }
    return render(request, 'donor/donor_agree.html', {'pa': pa})


def agree(request, id, table_name):
    if table_name == 'eye_details':
        user_app = eye_details.objects.get(id=id)
    elif table_name == 'heart_details':
        user_app = heart_details.objects.get(id=id)
    elif table_name == 'liv_reg':
        user_app = liv_reg.objects.get(id=id)
    elif table_name == 'lun_reg':
        user_app = lun_reg.objects.get(id=id)
    elif table_name == 'kid_reg':
        user_app = kid_reg.objects.get(id=id)
    else:

        pass
    user_app.approved = 1
    user_app.save()
    messages.success(request, 'Approved Sucessfully.')
    return redirect('/donor_agree/')
    # return render(request,'donor/donor_agree.html',{'user_app':user_app})


def ignore(request, id, table_name):
    if table_name == 'eye_details':
        user_app = eye_details.objects.get(id=id)
        user_app.delete()
    elif table_name == 'heart_details':
        user_app = heart_details.objects.get(id=id)
        user_app.delete()
    elif table_name == 'liv_reg':
        user_app = liv_reg.objects.get(id=id)
        user_app.delete()
    elif table_name == 'lun_reg':
        user_app = lun_reg.objects.get(id=id)
        user_app.delete()
    elif table_name == 'kid_reg':
        user_app = kid_reg.objects.get(id=id)
        user_app.delete()
    else:

        pass
    messages.success(request, 'Deleted Sucessfully.')
    return redirect('/donor_agree/')

def donor_og_details(request):
    eye = eye_details.objects.all()
    heart = heart_details.objects.all()
    liv = liv_reg.objects.all()
    lun = lun_reg.objects.all()
    kid = kid_reg.objects.all()

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

    return render(request, 'donor/donor_test_details.html',{'d':d})