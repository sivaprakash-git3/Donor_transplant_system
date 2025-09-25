from django.shortcuts import render,redirect
from django.contrib import messages
from patient.models import *
from donor.models import *
from django.db.models import Q
# Create your views here.
def home(request):
    return render(request,'home/home.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == "admin@gmail.com" and password == "admin":
            request.session['admin'] = 'admin@gmail.com'
            messages.info(request, "Successfully Login")
            return redirect('/admin_home/')
        elif email != "admin@gmail.com":
            messages.error(request, "Wrong Admin Email")
            return redirect('/admin_login/')
        elif password != "admin":
            messages.error(request, "Wrong Admin Password")
            return redirect('/admin_login/')
    return render(request, 'administration/admin_login.html')

def admin_logout(request):
    if 'admin' in request.session:
        request.session.pop('admin',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/admin_logout/')

def admin_home(request):
    eye_apps = eye_details.objects.all()
    heart_apps = heart_details.objects.all()
    liv_apps = liv_reg.objects.all()
    lun_apps = lun_reg.objects.all()
    kid_apps = kid_reg.objects.all()
    do = {'eye_details': eye_apps,
          'heart_details': heart_apps,
          'liv_reg': liv_apps,
          'lun_reg': lun_apps,
          'kid_reg': kid_apps}

    last_consent = []
    for table, queryset in do.items():
        last_consent.extend([(obj.donor_name, obj.consent) for obj in queryset])

    overall_last_consent = max([(obj[0], obj[1]) for obj in last_consent if obj[1]], default=None)
    overall_last_donor_name = overall_last_consent[0] if overall_last_consent else None

    return render(request,'administration/admin_home.html',{'do':do,'overall_last_donor_name':overall_last_donor_name})

def patient_stats(request):
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
    return render(request,'administration/patient_status.html',{'pa':pa})

def donor_match_prediction(request, table_, id):
    if table_ == 'patient_eye_registration':

        patient = patient_eye_registration.objects.get(id=id)
        # Query the Eye_details table for matching records
        matching_details = eye_details.objects.filter(
                tissue_type=patient.tissue_type,
                corneal_mes =patient.corneal_thickness,
                corneal_curv =patient.corneal_curvature,
                corneal_topo =patient.corneal_topo,
                corneal_dia =patient.corneal_dia,
                endothelial_cell =patient.endothelial
            )


    elif table_ == "patient_heart_re":
        patient = patient_heart_re.objects.get(id=id)
        # Query the Eye_details table for matching records
        matching_details = heart_details.objects.filter(
            heart_size=patient.heart_size,
            hemo=patient.hemo,
            blood_type=patient.blood_type,
            tissue_type=patient.tissue_type,
        )
    elif table_ == "patient_liver_re":
        patient = patient_liver_re.objects.get(id=id)
        # Query the Eye_details table for matching records
        matching_details = liv_reg.objects.filter(
            blood_type=patient.blood_type,
            tissue_type=patient.tissue_type,
            cross_test=patient.cross_test,
            viral_test=patient.viral_test,
        )
    elif table_ == "patient_lungs_re":
        patient = patient_lungs_re.objects.get(id=id)
        # Query the Eye_details table for matching records
        matching_details = lun_reg.objects.filter(
            blood_type=patient.blood_type,
            tissue_type=patient.tissue_type,
            crossmatch=patient.crossmatch,
            viral_test=patient.viral_test,
        )
    elif table_ == "patient_kidney_re":
        patient = patient_kidney_re.objects.get(id=id)
        # Query the Eye_details table for matching records
        matching_details = kid_reg.objects.filter(
            blood_type=patient.blood_type,
            tissue_type=patient.tissue_type,
            cross_test=patient.cross_test,
            viral_test=patient.viral_test
        )

    # Get a list of matching patient IDs
    matching_patient_ids = [eye_detail for eye_detail in matching_details]
    print(matching_patient_ids)
    if matching_patient_ids==[]:
        messages.success(request, 'No Match')
        return redirect('/patient_stats/')

    return render(request, 'administration/donor_match.html',{"matching_details":matching_details})


def donor_stats(request):
    eye_apps = eye_details.objects.all()
    heart_apps = heart_details.objects.all()
    liv_apps = liv_reg.objects.all()
    lun_apps = lun_reg.objects.all()
    kid_apps = kid_reg.objects.all()
    do = {'eye_details': eye_apps,
          'heart_details': heart_apps,
          'liv_reg': liv_apps,
          'lun_reg': lun_apps,
          'kid_reg': kid_apps}
    return render(request, 'administration/donor_status.html', {'do': do})

def don_match(request):
    eye_apps = eye_details.objects.all()
    heart_apps = heart_details.objects.all()
    liv_apps = liv_reg.objects.all()
    lun_apps = lun_reg.objects.all()
    kid_apps = kid_reg.objects.all()
    do = {'eye_details': eye_apps,
          'heart_details': heart_apps,
          'liv_reg': liv_apps,
          'lun_reg': lun_apps,
          'kid_reg': kid_apps}

    return render(request,'administration/donor_match.html',{'do':do})

def patient_per(request):
    if request.method == "POST":
        patient_id = request.POST["patient_id"]
        print(patient_id)
        # Filter queryset for each organ detail model to only include objects whose donor name matches user email

        if patient_id:
            # Search for donors with the matching donor ID
            eye_apps = patient_eye_registration.objects.filter(id=patient_id)
            heart_apps = patient_heart_re.objects.filter(id=patient_id)
            liv_apps = patient_liver_re.objects.filter(id=patient_id)
            lun_apps = patient_lungs_re.objects.filter(id=patient_id)
            kid_apps = patient_kidney_re.objects.filter(id=patient_id)

            pa = {
                'patient_eye_registration': eye_apps,
                'patient_heart_re': heart_apps,
                'patient_liver_re': liv_apps,
                'patient_lungs_re': lun_apps,
                'patient_kidney_re': kid_apps
            }
            print(pa)


            # Pass the matching donor details to the template
            return render(request, 'administration/pat_permission.html', {'pa': pa})
        else:
            messages.success(request, 'No Match')

    return render(request, 'administration/pat_permission.html',)

def donor_per(request):
    if request.method == "POST":
        donor_id = request.POST["donor_id"]
        print(donor_id)
        # Filter queryset for each organ detail model to only include objects whose donor name matches user email

        if donor_id:
            # Search for donors with the matching donor ID
            eye_apps = eye_details.objects.filter(donor_id=donor_id)
            heart_apps = heart_details.objects.filter(donor_id=donor_id)
            liv_apps = liv_reg.objects.filter(donor_id=donor_id)
            lun_apps = lun_reg.objects.filter(donor_id=donor_id)
            kid_apps = kid_reg.objects.filter(donor_id=donor_id)

            pa = {
                'eye_details': eye_apps,
                'heart_details': heart_apps,
                'liv_reg': liv_apps,
                'lun_reg': lun_apps,
                'kid_reg': kid_apps
            }
            print(pa)


            # Pass the matching donor details to the template
            return render(request, 'administration/don_permission.html', {'pa': pa})
        else:
            messages.success(request, 'No Match')
    return render(request, 'administration/don_permission.html')


def organ_users(request):
    eye_apps = eye_details.objects.filter(consent=True)
    heart_apps = heart_details.objects.filter(consent=True)
    liv_apps = liv_reg.objects.filter(consent=True)
    lun_apps = lun_reg.objects.filter(consent=True)
    kid_apps = kid_reg.objects.filter(consent=True)
    do = {'eye_details': eye_apps,
          'heart_details': heart_apps,
          'liv_reg': liv_apps,
          'lun_reg': lun_apps,
          'kid_reg': kid_apps
          }
    return render(request, 'administration/organ_users.html',{'do':do})

def donor_consent(request,id,table_):
    if table_ == 'eye_details':
        d = eye_details.objects.get(id=id)
        d.consent=True
        d.save()
    elif table_ == "heart_details":
        d = heart_details.objects.get(id=id)
        d.consent = True
        d.save()
    elif table_ == "liv_reg":
        d = liv_reg.objects.get(id=id)
        d.consent = True
        d.save()
    elif table_ == "lun_reg":
        d = lun_reg.objects.get(id=id)
        d.consent = True
        d.save()
    elif table_ == "kid_reg":
        d = kid_reg.objects.get(id=id)
        d.consent = True
        d.save()

    messages.success(request, 'Consented Details Added to DB')
    return render(request,'administration/don_permission.html')