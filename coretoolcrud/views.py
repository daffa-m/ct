from django.shortcuts import render, redirect
from .models import Xbarr, Cross, Nested, Linearity, Survey, User
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

import numpy
from numpy import sqrt
import pandas as pd
import seaborn as sns
from scipy.stats import f
from scipy import stats
import pingouin as pg
import math
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import f
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import LinearAxis

from random import randint


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

# Create your views here.

# Login

def viewLogin(request):
    return render(request,'login/login.html')

def login(request):
    uname = request.POST.get('uname')
    password = request.POST.get('password')
    check = User.objects.filter(user_username=uname, user_password=password)

    if check:
        if 'user' in request.session:
            if request.session['user'] == uname:
                messages.error(request, "Akun sedang digunakan di perangkat lain")
                return redirect('/logout')
        else:
            user = User.objects.get(user_username=uname)
            request.session['user'] = uname
            request.session['company'] = user.user_company
            request.session['id'] = user.id
            request.session['role'] = user.user_role

        return redirect('/viewListSurvey')
    else:
        messages.error(request, "Username atau password salah")
        return redirect('/logout')

def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('/')
    return redirect('/logout')


# Survey

def viewListSurvey(request):
    if 'user' in request.session:
        survey = Survey.objects.filter(survey_user_id=request.session['id'])
        return render(request,'survey/list_survey.html',{'survey':survey})
    else:
        return redirect('/logout')

def viewDetailSurvey(request, pk):
    if 'user' in request.session:
        survey = Survey.objects.get(id = pk)
        if survey.survey_user_id == request.session['id']:
            return render(request,'survey/survey_result.html',{'survey':survey})
        else:
            return redirect('/logout')
    else:
        return redirect('/logout')

def deleteSurvey(request, pk):
    if 'user' in request.session:
        survey = Survey.objects.get(id = pk)
        survey.delete()
        messages.success(request, "Survey berhasil dihapus")
        return redirect('coretoolcrud:viewListSurvey')
    else:
        return redirect('/logout')

def viewSurvey(request):
    if 'user' in request.session:
        return render(request,'survey/survey1.html')
    else:
        return redirect('/logout')

def viewEditSurvey(request, pk):
    if 'user' in request.session:
        survey = Survey.objects.get(id = pk)
        if survey.survey_user_id == request.session['id']:
            return render(request,'survey/edit_survey.html',{'survey':survey})
        else:
            return redirect('/logout')
    else:
        return redirect('/logout')

def viewManual(request):
    if 'user' in request.session:
        return render(request,'survey/manual.html')
    else:
        return redirect('/logout')

def viewEditManual(request, pk):
    if 'user' in request.session:
        survey = Survey.objects.get(id = pk)
        if survey.survey_user_id == request.session['id']:
            return render(request,'survey/edit_manual.html',{'survey':survey})
        else:
            return redirect('/logout')
    else:
        return redirect('/logout')

def storeManual(request):
    if 'user' in request.session:
        survey = Survey()
        user = User.objects.get(user_username=request.session['user'])

        survey.survey_user_id = user.id
        survey.survey_date_project = request.POST.get('survey_date_project')
        survey.survey_cust_name = request.POST.get('survey_cust_name')
        survey.survey_part_name = request.POST.get('survey_part_name')
        survey.survey_part_number = request.POST.get('survey_part_number')
        survey.survey_character = request.POST.get('survey_character')
        survey.survey_category = request.POST.get('survey_category')
        survey.survey_process_name = request.POST.get('survey_process_name')
        survey.survey_symbol = request.POST.get('survey_symbol')
        survey.survey_ref = request.POST.get('survey_ref')
        survey.survey_range_max = request.POST.get('survey_range_max')
        survey.survey_range_min = request.POST.get('survey_range_min')
        survey.survey_fmea = request.POST.get('survey_fmea')
        survey.survey_control_plan = request.POST.get('survey_control_plan')
        survey.survey_name = request.POST.get('survey_name')
        survey.survey_sn = request.POST.get('survey_sn')
        survey.survey_resolution = request.POST.get('survey_resolution')
        survey.survey_unit = request.POST.get('survey_unit')
        survey.survey_next_cal = request.POST.get('survey_next_cal')
        survey.survey_plan = request.POST.get('survey_plan')
        # survey.survey_actual = request.POST.get('survey_actual')
        survey.survey_reason = request.POST.get('survey_reason')

        survey.survey_study = request.POST.getlist('survey_study')

        survey.save()
        survey = Survey.objects.latest('id')
        print(type(survey.survey_plan))
        messages.success(request, "Data Survey Berhasil Disimpan")
        return redirect('coretoolcrud:viewDetailSurvey',survey.id )
    else:
        return redirect('/logout')

def storeEditManual(request, pk):
    if 'user' in request.session:
        survey = Survey.objects.get(id = pk)
        user = User.objects.get(user_username=request.session['user'])

        survey.survey_user_id = user.id
        survey.survey_date_project = request.POST.get('survey_date_project')
        survey.survey_cust_name = request.POST.get('survey_cust_name')
        survey.survey_part_name = request.POST.get('survey_part_name')
        survey.survey_part_number = request.POST.get('survey_part_number')
        survey.survey_character = request.POST.get('survey_character')
        survey.survey_category = request.POST.get('survey_category')
        survey.survey_process_name = request.POST.get('survey_process_name')
        survey.survey_symbol = request.POST.get('survey_symbol')
        survey.survey_ref = request.POST.get('survey_ref')
        survey.survey_range_max = request.POST.get('survey_range_max')
        survey.survey_range_min = request.POST.get('survey_range_min')
        survey.survey_fmea = request.POST.get('survey_fmea')
        survey.survey_control_plan = request.POST.get('survey_control_plan')
        survey.survey_name = request.POST.get('survey_name')
        survey.survey_sn = request.POST.get('survey_sn')
        survey.survey_resolution = request.POST.get('survey_resolution')
        survey.survey_unit = request.POST.get('survey_unit')
        survey.survey_next_cal = request.POST.get('survey_next_cal')
        survey.survey_plan = request.POST.get('survey_plan')
        # survey.survey_actual = request.POST.get('survey_actual')
        survey.survey_reason = request.POST.get('survey_reason')

        survey.survey_study = request.POST.getlist('survey_study')

        survey.save()
        survey = Survey.objects.latest('id')
        print(type(survey.survey_plan))
        messages.success(request, "Data Survey Berhasil Disimpan")
        return redirect('coretoolcrud:viewDetailSurvey',survey.id )
    else:
        return redirect('/logout')

def storeSurvey(request):
    if 'user' in request.session:
        survey = Survey()
        user = User.objects.get(user_username=request.session['user'])

        survey.survey_user_id = user.id
        survey.survey_date_project = request.POST.get('survey_date_project')
        survey.survey_cust_name = request.POST.get('survey_cust_name')
        survey.survey_part_name = request.POST.get('survey_part_name')
        survey.survey_part_number = request.POST.get('survey_part_number')
        survey.survey_character = request.POST.get('survey_character')
        survey.survey_category = request.POST.get('survey_category')
        survey.survey_process_name = request.POST.get('survey_process_name')
        survey.survey_symbol = request.POST.get('survey_symbol')
        survey.survey_ref = request.POST.get('survey_ref')
        survey.survey_range_max = request.POST.get('survey_range_max')
        survey.survey_range_min = request.POST.get('survey_range_min')
        survey.survey_fmea = request.POST.get('survey_fmea')
        survey.survey_control_plan = request.POST.get('survey_control_plan')
        survey.survey_name = request.POST.get('survey_name')
        survey.survey_sn = request.POST.get('survey_sn')
        survey.survey_resolution = request.POST.get('survey_resolution')
        survey.survey_unit = request.POST.get('survey_unit')
        survey.survey_next_cal = request.POST.get('survey_next_cal')
        survey.survey_plan = request.POST.get('survey_plan')
        # survey.survey_actual = request.POST.get('survey_actual')
        survey.survey_reason = request.POST.get('survey_reason')

        survey.survey_data = request.POST.get('survey_data')
        survey.survey_att_prod_unit = request.POST.get('survey_att_prod_unit')
        survey.survey_att_qty = request.POST.get('survey_att_qty')
        survey.survey_att_cat = request.POST.get('survey_att_cat')

        survey.survey_var_bias_working = request.POST.get('survey_var_bias_working')
        survey.survey_var_bias_over = request.POST.get('survey_var_bias_over')
        survey.survey_var_homogen = request.POST.get('survey_var_homogen')
        survey.survey_var_part_sample = request.POST.get('survey_var_part_sample')
        survey.survey_var_subgroup = request.POST.get('survey_var_subgroup')
        survey.survey_var_variation = request.POST.get('survey_var_variation')
        survey.survey_var_review = request.POST.get('survey_var_review')
        survey.survey_var_ave = request.POST.get('survey_var_ave')

        study = []
        if survey.survey_data == "att":
            if survey.survey_att_prod_unit == "no":
                if survey.survey_att_qty == "yes":
                    study.append("U Chart")
                    study.append("C Chart")
                elif survey.survey_att_qty == "no":
                    study.append("U Chart")
            elif survey.survey_att_prod_unit == "yes":
                if survey.survey_att_qty == "yes":
                    study.append("P Chart")
                    study.append("NP Chart")
                elif survey.survey_att_qty == "no":
                    study.append("P Chart")
            if survey.survey_att_cat == "no":
                study.append("Fleis Kappa")
            elif survey.survey_att_cat == "yes":
                study.append("Kendall")
        elif survey.survey_data == "var":
            #SPC
            if survey.survey_var_bias_working == "no":
                study.append("Bias")
            if survey.survey_var_bias_working == "yes" or survey.survey_var_bias_over == "no":
                study.append("Linearity")
            # if survey.survey_var_bias_over == "no":
            #     study.append("Linearity")
            if survey.survey_var_bias_over == "yes":
                study.append("Stability")
            if survey.survey_var_variation == "yes":
                if survey.survey_var_part_sample == "nested":
                    study.append("GRR Nested")
                elif survey.survey_var_part_sample == "cross":
                    if survey.survey_var_review == "no":
                        study.append("GRR Xbar-R")
                    elif survey.survey_var_review == "yes":
                        study.append("GRR Anova") 
            #MSA
            if survey.survey_var_homogen == "yes":
                study.append("I-MR")
            elif survey.survey_var_homogen == "no":
                if survey.survey_var_subgroup == "less than 10":
                    if survey.survey_var_ave == "yes":
                        study.append("Median-R")
                    elif survey.survey_var_ave == "no":
                        study.append("Xbar-R")
                elif survey.survey_var_subgroup == "more or equal than 10":
                    study.append("Xbar-S")
            
            print(survey.survey_var_variation, survey.survey_var_part_sample, survey.survey_var_review)


            ####################
            # if survey.survey_var_homogen == "yes":
            #     study.append("I-MR")
            # elif survey.survey_var_homogen == "no":
            #     if survey.survey_var_subgroup == "less than 10":
            #         if survey.survey_var_ave == "yes":
            #             study.append("Median-R")
            #         elif survey.survey_var_ave == "no":
            #             study.append("Xbar-R")
            #     elif survey.survey_var_subgroup == "more or equal than 10":
            #         study.append("Xbar-S")
            # if survey.survey_var_variation == "yes":
            #     if survey.survey_var_part_sample == "nested":
            #         study.append("GRR Nested")
            #     elif survey.survey_var_part_sample == "cross":
            #         if survey.survey_var_review == "no":
            #             study.append("GRR Xbar-R")
            #         elif survey.survey_var_review == "no":
            #             study.append("GRR Anova")
            # elif survey.survey_var_variation == "no":
            #     if survey.survey_var_bias_working == "no":
            #         study.append("Bias")
            #     elif survey.survey_var_bias_working == "yes":
            #         study.append("Linearity")
            #         if survey.survey_var_bias_over == "yes":
            #             study.append("Stability")


        survey.survey_study = study
        survey.save()
        survey = Survey.objects.latest('id')
        print(type(survey.survey_plan))
        messages.success(request, "Data Survey Berhasil Disimpan")
        # return render(request,'survey/survey_result.html',{'survey':survey})
        return redirect('coretoolcrud:viewDetailSurvey',survey.id )
    else:
        return redirect('/logout')

def storeEditSurvey(request, pk):
    if 'user' in request.session:
        survey = Survey.objects.get(id = pk)
        user = User.objects.get(user_username=request.session['user'])

        survey.survey_user_id = user.id
        survey.survey_date_project = request.POST.get('survey_date_project')
        survey.survey_cust_name = request.POST.get('survey_cust_name')
        survey.survey_part_name = request.POST.get('survey_part_name')
        survey.survey_part_number = request.POST.get('survey_part_number')
        survey.survey_character = request.POST.get('survey_character')
        survey.survey_category = request.POST.get('survey_category')
        survey.survey_process_name = request.POST.get('survey_process_name')
        survey.survey_symbol = request.POST.get('survey_symbol')
        survey.survey_ref = request.POST.get('survey_ref')
        survey.survey_range_max = request.POST.get('survey_range_max')
        survey.survey_range_min = request.POST.get('survey_range_min')
        survey.survey_fmea = request.POST.get('survey_fmea')
        survey.survey_control_plan = request.POST.get('survey_control_plan')
        survey.survey_name = request.POST.get('survey_name')
        survey.survey_sn = request.POST.get('survey_sn')
        survey.survey_resolution = request.POST.get('survey_resolution')
        survey.survey_unit = request.POST.get('survey_unit')
        survey.survey_next_cal = request.POST.get('survey_next_cal')
        survey.survey_plan = request.POST.get('survey_plan')
        # survey.survey_actual = request.POST.get('survey_actual')
        survey.survey_reason = request.POST.get('survey_reason')

        survey.survey_data = request.POST.get('survey_data')
        survey.survey_att_prod_unit = request.POST.get('survey_att_prod_unit')
        survey.survey_att_qty = request.POST.get('survey_att_qty')
        survey.survey_att_cat = request.POST.get('survey_att_cat')

        survey.survey_var_bias_working = request.POST.get('survey_var_bias_working')
        survey.survey_var_bias_over = request.POST.get('survey_var_bias_over')
        survey.survey_var_homogen = request.POST.get('survey_var_homogen')
        survey.survey_var_part_sample = request.POST.get('survey_var_part_sample')
        survey.survey_var_subgroup = request.POST.get('survey_var_subgroup')
        survey.survey_var_variation = request.POST.get('survey_var_variation')
        survey.survey_var_review = request.POST.get('survey_var_review')
        survey.survey_var_ave = request.POST.get('survey_var_ave')

        study = []
        if survey.survey_data == "att":
            if survey.survey_att_prod_unit == "no":
                if survey.survey_att_qty == "yes":
                    study.append("U Chart")
                    study.append("C Chart")
                elif survey.survey_att_qty == "no":
                    study.append("U Chart")
            elif survey.survey_att_prod_unit == "yes":
                if survey.survey_att_qty == "yes":
                    study.append("P Chart")
                    study.append("NP Chart")
                elif survey.survey_att_qty == "no":
                    study.append("P Chart")
            if survey.survey_att_cat == "no":
                study.append("Fleis Kappa")
            elif survey.survey_att_cat == "yes":
                study.append("Kendall")
        elif survey.survey_data == "var":
            #SPC
            if survey.survey_var_bias_working == "no":
                study.append("Bias")
            if survey.survey_var_bias_working == "yes" or survey.survey_var_bias_over == "no":
                study.append("Linearity")
            if survey.survey_var_bias_over == "yes":
                study.append("Stability")
            if survey.survey_var_variation == "yes":
                if survey.survey_var_part_sample == "nested":
                    study.append("GRR Nested")
                elif survey.survey_var_part_sample == "cross":
                    if survey.survey_var_review == "no":
                        study.append("GRR Xbar-R")
                    elif survey.survey_var_review == "yes":
                        study.append("GRR Anova") 
            #MSA
            if survey.survey_var_homogen == "yes":
                study.append("I-MR")
            elif survey.survey_var_homogen == "no":
                if survey.survey_var_subgroup == "less than 10":
                    if survey.survey_var_ave == "yes":
                        study.append("Median-R")
                    elif survey.survey_var_ave == "no":
                        study.append("Xbar-R")
                elif survey.survey_var_subgroup == "more or equal than 10":
                    study.append("Xbar-S")
            
            print(survey.survey_var_variation, survey.survey_var_part_sample, survey.survey_var_review)


        survey.survey_study = study
        survey.save()
        survey = Survey.objects.latest('id')
        print(type(survey.survey_plan))
        messages.success(request, "Data Survey Berhasil Disimpan")
        # return render(request,'survey/survey_result.html',{'survey':survey})
        return redirect('coretoolcrud:viewDetailSurvey',survey.id )
    else:
        return redirect('/logout')

# GRR Xbarr

def viewGrrXbarr(request, pk):
    if 'user' in request.session:
        try:
            xbarr = Xbarr.objects.get(xbarr_survey_id = pk)
            if xbarr.xbarr_all:
                return redirect('coretoolcrud:viewFinalGrrXbarr', pk)
            else:
                namas = xbarr.xbarr_karyawan
                part = range(1, int(xbarr.xbarr_npart)+1)
                karyawan = range(int(xbarr.xbarr_nkaryawan))
                trial = range(int(xbarr.xbarr_ntrial))
                karyawan = range(int(xbarr.xbarr_nkaryawan))
                return render(request,'grr_xbarr/all_xbarr.html',{'part':part, 'karyawan':karyawan, 'trial':trial, 'namas':namas, 'xbarr':xbarr})
            
        except Xbarr.DoesNotExist:
            return render(request,'grr_xbarr/xbarr.html',{'pk':pk})
    else:
        return redirect('/logout')

def storeGrrXbarr(request, pk):
    if 'user' in request.session:
        try:
            xbarr = Xbarr.objects.get(xbarr_survey_id = pk)
            xbarr.delete()
        except Xbarr.DoesNotExist:
            pass

        xbarr = Xbarr()
        xbarr.xbarr_survey_id = pk
        xbarr.xbarr_nkaryawan = request.POST.get('xbarr_nkaryawan')
        xbarr.xbarr_npart = request.POST.get('xbarr_npart')
        xbarr.xbarr_ntrial = request.POST.get('xbarr_ntrial')
        xbarr.xbarr_stdev = request.POST.get('xbarr_stdev')
        xbarr.xbarr_stdevmax = request.POST.get('xbarr_stdevmax')
        xbarr.xbarr_stdevmin = request.POST.get('xbarr_stdevmin')
        xbarr.xbarr_karyawan = request.POST.getlist('xbarr_karyawan')
        
        xbarr.save()

        namas = xbarr.xbarr_karyawan
        part = range(1, int(xbarr.xbarr_npart)+1)
        karyawan = range(int(xbarr.xbarr_nkaryawan))
        trial = range(int(xbarr.xbarr_ntrial))
        karyawan = range(int(xbarr.xbarr_nkaryawan))
        return render(request,'grr_xbarr/all_xbarr.html',{'part':part, 'karyawan':karyawan, 'trial':trial, 'namas':namas, 'xbarr':xbarr})
    else:
        return redirect('/logout')

def storeAllGrrXbarr(request, pk):
    if 'user' in request.session:
        xbarr = Xbarr.objects.get(xbarr_survey_id = pk)
        temppart = []
        temptrial = []
        tempkaryawan = []
        iter = 1

        xbarr.xbarr_all = request.POST.getlist('xbarr_all')
        for i in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            if iter % int(xbarr.xbarr_npart) != 0:
                temppart.append(xbarr.xbarr_all[i])
                iter = iter + 1
            else:
                if iter % (int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)) == 0:
                    temppart.append(xbarr.xbarr_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    tempkaryawan.append(temptrial)
                    temptrial = []
                    temppart = []
                    iter = iter + 1
                else:
                    temppart.append(xbarr.xbarr_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    temppart = []
                    iter = iter + 1
        
        xbarr.xbarr_all = tempkaryawan
        xbarr.save()
        return redirect('coretoolcrud:viewCommentGrrXbarr', pk)    
    else:
        return redirect('/logout')        

def viewCommentGrrXbarr(request, pk):
    if 'user' in request.session:
        xbarr = Xbarr.objects.get(xbarr_survey_id = pk)
        ################
        avepart = []
        avetrial = []
        rpart = []
        person = 2
        trial = 2
        sumtemp = 0
        iter = 0
        temp = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                for j in range(int(xbarr.xbarr_ntrial)):
                    sumtemp = sumtemp + xbarr.xbarr_all[i][j][k]
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_ntrial) == 0:
                        sumtemp = sumtemp / int(xbarr.xbarr_ntrial)
                        temp.append(sumtemp)
                        sumtemp = 0
            avepart.append(temp)
            temp = []

        iter = 0
        maxtemp = 0
        mintemp = 0
        temp = []
        tempmaxmin = []
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                for j in range(int(xbarr.xbarr_ntrial)): 
                    tempmaxmin.append(xbarr.xbarr_all[i][j][k])
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_ntrial) == 0:
                        maxtemp = max(tempmaxmin)
                        mintemp = min(tempmaxmin)
                        temp.append(maxtemp - mintemp)
                        tempmaxmin = []
            rpart.append(temp)
            temp = []

        xx = []
        rx = []
        sumtemp = 0

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                sumtemp = sumtemp + avepart[i][k]
            xx.append(sumtemp / int(xbarr.xbarr_npart))
            sumtemp = 0

        sumtemp = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                sumtemp = sumtemp + rpart[i][k]
            rx.append(sumtemp / int(xbarr.xbarr_npart))
            sumtemp = 0

        sumtemp = 0
        iter = 0
        temp = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_ntrial)):
                for k in range(int(xbarr.xbarr_npart)):
                    sumtemp = sumtemp + xbarr.xbarr_all[i][j][k]
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_npart) == 0:
                        sumtemp = sumtemp / int(xbarr.xbarr_npart)
                        temp.append(sumtemp)
                        sumtemp = 0
            avetrial.append(temp)
            temp = []

        sumavepart = []
        sumtemp = 0
        iter = 0

        for k in range(int(xbarr.xbarr_npart)):
            for i in range(int(xbarr.xbarr_nkaryawan)):
                sumtemp = sumtemp + avepart[i][k]
                iter = iter + 1
                if iter % int(xbarr.xbarr_nkaryawan) == 0:
                    sumavepart.append(sumtemp / int(xbarr.xbarr_nkaryawan))
                    sumtemp = 0

        xbar2 = sum(sumavepart) / int(xbarr.xbarr_npart)
        rp = max(sumavepart) - min(sumavepart)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]
        rbar = sum(rx) / int(xbarr.xbarr_nkaryawan)
        xbardiff = max(xx) - min(xx)

        for i in range(4):
            if subgroup[i][0] == int(xbarr.xbarr_ntrial):
                d4 = subgroup[i][1]
                

        ulcr = d4 * rbar
        lclr = 0

        a2 = 0

        # npart > 5 gimana?

        for i in range(4):
            if subgroup[i][0] == int(xbarr.xbarr_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]

        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar

        trial = [[2, 0.886525], [3, 0.590667], [4, 0.485673], [5, 0.429923], [6, 0.394633], [7, 0.369822], [8, 0.351247], [9, 0.3367], [10, 0.324886], [11, 0.315159], [12, 0.306843], [13, 0.29976], [14, 0.293513], [15, 0.288018]]

        for i in range(14):
            if trial[i][0] == int(xbarr.xbarr_ntrial):
                k1 = trial[i][1]
        
        ev = rbar * k1
        varrepeat = 6 * ev

        appraisal = [[2, 0.707109], [3, 0.523136], [4, 0.446654], [5, 0.403024], [6, 0.374177], [7, 0.353381], [8, 0.337509], [9, 0.324893], [10, 0.314559], [11, 0.305896], [12, 0.298493], [13, 0.292075], [14, 0.286438], [15, 0.281426], [16, 0.276954], [17, 0.272909], [18, 0.269234], [19, 0.265874], [20, 0.262787]]

        for i in range(19):
            if appraisal[i][0] == int(xbarr.xbarr_nkaryawan):
                k2 = appraisal[i][1]
        
        xdiffk2 = pow((xbardiff * k2), 2)
        ev2 = (ev ** 2) / (int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial))

        if xdiffk2 > ev2:
            av = sqrt(pow(xbardiff * k2, 2) - pow(ev, 2) / (int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)))
        else:
            av = 0

        varreproduce = 6 * av
        grr = sqrt(pow(ev, 2) + pow(av, 2))
        vargrr = 6 * grr

        #parts = [[2, 0.70711], [3, 0.52314], [4, 0.44665], [5, 0.4030], [6, 0.3742], [7, 0.3534], [8, 0.3375], [9, 0.3249], [10, 0.3146]]
        parts = [[2, 0.707109], [3, 0.523136], [4, 0.446654], [5, 0.403024], [6, 0.374177], [7, 0.353381], [8, 0.337509], [9, 0.324893], [10, 0.314559], [11, 0.305896], [12, 0.298493], [13, 0.292075], [14, 0.286438], [15, 0.281426], [16, 0.276954], [17, 0.272909], [18, 0.269234], [19, 0.265874], [20, 0.262787]]

        
        for i in range(19):
            if parts[i][0] == int(xbarr.xbarr_npart):
                k3 = parts[i][1]
        pv = rp * k3
        varpart = 6 * pv

        tv = sqrt(pow(grr, 2) + pow(pv, 2))
        vartv = 6 * tv
        pev = ev / tv * 100
        pav = av / tv * 100
        pgrr = grr / tv * 100
        ppv = pv / tv * 100
        ndc = 1.41 * (pv / grr)

        stdev6 = int(xbarr.xbarr_stdev) * 6
        vcev = pow(ev, 2)
        vcav = pow(av, 2)
        vcgrr = pow(grr, 2)
        vcpv = pow(pv, 2)
        vcndc = vcpv + vcgrr

        pvcev = vcev / vcndc * 100
        pvcav = vcav / vcndc * 100
        pvcgrr = vcgrr / vcndc * 100
        pvcpv = vcpv / vcndc * 100
        pvcndc = vcndc / vcndc * 100

        if int(xbarr.xbarr_stdevmax) == 0 and int(xbarr.xbarr_stdevmin) == 0:
            ptev = 0
            ptav = 0
            ptgrr = 0
            ptpv = 0
            ptndc = 0
        else:
            ptev = varrepeat / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptav = varreproduce / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptgrr = vargrr / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptpv = varpart / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptndc = vartv / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100

        if stdev6 == 0:
            ppev = 0
            ppav = 0
            ppgrr = 0
            pppv = 0
            ppndc = 0
        else:
            ppev = varrepeat / stdev6 * 100
            ppav = varreproduce / stdev6 * 100
            ppgrr = vargrr / stdev6 * 100
            pppv = varpart / stdev6 * 100
            ppndc = vartv / stdev6 * 100

        resume = []
        temp = []

        temp.append("GRR")
        temp.append(pgrr)
        temp.append(pvcgrr)
        temp.append(ptgrr)
        temp.append(ppgrr)
        resume.append(temp)

        temp = []
        temp.append("Repeatability")
        temp.append(pev)
        temp.append(pvcev)
        temp.append(ptev)
        temp.append(ppev)
        resume.append(temp)

        temp = []
        temp.append("Reproducibility")
        temp.append(pav)
        temp.append(pvcav)
        temp.append(ptav)
        temp.append(ppav)
        resume.append(temp)

        temp = []
        temp.append("Part to Part")
        temp.append(ppv)
        temp.append(pvcpv)
        temp.append(ptpv)
        temp.append(pppv)
        resume.append(temp)

        
        xbarr.xbarr_resume = resume
        xbarr.save()

        resumes = xbarr.xbarr_resume

        ###############
        #% Study var contribution
        x, a, b, c, d = [*zip(*resume)]
        
        if all(ele == 0 for ele in c) and all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b}, index=x)
        elif all(ele == 0 for ele in c) and not all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Process': d}, index=x)
        elif not all(ele == 0 for ele in c) and all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Tolerance': c}, index=x)
        else:
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Tolerance': c, '% Process': d}, index=x)
        plt.figure()
        dfres.plot(kind='bar', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)


        listulcr = []
        listlclr = []

        for j in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                listulcr.append(ulcr)
                listlclr.append(lclr)

        ##################

        bot = []
        top = []
        urut = []
        temp = 0

        flat = [x for l in rpart for x in l]
        flat = np.array(flat)
        print(xbarr.xbarr_nkaryawan)
        print(xbarr.xbarr_karyawan)
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart)):
                urut.append(temp)
                bot.append(str(j+1))
                # if int(xbarr.xbarr_npart) % 2 == 0:
                #     if j == 0 or j == int(xbarr.xbarr_npart) - 1:
                #         top.append("|")
                #     elif j == (int(xbarr.xbarr_npart) / 2):
                #         top.append(xbarr.xbarr_karyawan[i])
                #     else:
                #         top.append("")
                # elif int(xbarr.xbarr_npart) % 2 != 0:
                #     if j == 0 or j == int(xbarr.xbarr_npart) - 1:
                #         top.append("|")
                #     elif j == int(round(int(xbarr.xbarr_npart) / 2, 0)):
                #         top.append(xbarr.xbarr_karyawan[i])
                #     else:
                #         top.append("")
                if j == 0:
                    top.append(xbarr.xbarr_karyawan[i])
                elif j == int(xbarr.xbarr_npart) - 1:
                    top.append("|")
                else:
                    top.append("")
                temp = temp + 1



        # urut = np.array(urut)
        plt.clf()
        fig, ax = plt.subplots()

        ax.plot(flat, label='Range')
        ax.plot(listulcr, label='UCLRbar')
        ax.plot(listlclr, label='LCLRbar')
        ax.set_xticks(urut)
        ax.set_xticklabels(bot)
        x1, x2 = ax.get_xlim() 
        ax2 = ax.twiny()
        ax2.set_xlim(x1,x2)
        ax2.set_xticks(urut)
        ax2.set_xticklabels(top)
        ax.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)
        plt.title("Range vs Appraisal")
        ax.set_ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        rva = urllib.parse.quote(string)
        
        ####################################

        perpart = [x for l in xbarr.xbarr_all for x in l]
        perpart = np.array(perpart)
        perpart = perpart.T
        perpart = perpart.tolist()

        pertrial = [x for l in xbarr.xbarr_all for x in l]
        allnontt = [x for l in pertrial for x in l]
        perkaryawan = []
        temp = []
        iter = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
                temp.append(allnontt[iter])
                iter = iter + 1
            perkaryawan.append(temp)
            temp = []

        urut = []
        temp = []
        for i in range(int(xbarr.xbarr_npart)):
            for j in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
                temp.append(i+1)
            urut.append(temp)
            temp = []
        
        perperkaryawan = np.array(perkaryawan)
        perperkaryawan = perperkaryawan.T
        perperkaryawan = perperkaryawan.tolist()

        allflatflat =  [x for l in perpart for x in l]
        urutflat =  [x for l in urut for x in l]

        urutline = [i+1 for i in range(int(xbarr.xbarr_npart))]

        urutlineline = []

        for i in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
            urutlineline.append(urutline)

        avepertrial = []
        for ele in perpart:
            avepertrial.append(sum(ele) / len(ele))

        #colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"])
        colors = []
        
        plt.clf()
        for i in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            plt.scatter(urutlineline[i], pertrial[i],c=colors[i])

        # for i in range(int(xbarr.xbarr_npart)):
        #     plt.scatter((sum(urut)))
        plt.plot(urutline, avepertrial, label='Average')
        plt.xlabel('Part No')
        plt.ylabel('Measurement')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(xbarr.xbarr_nkaryawan))
        plt.ylabel("Value")
        plt.title('Data by Sample')

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        dbs = urllib.parse.quote(string)

        #####################################

        urutline = [i+1 for i in range(int(xbarr.xbarr_nkaryawan))]
        urutlineline = []
        namaline = []

        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            urutlineline.append(urutline)


        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            namaline.append(xbarr.xbarr_karyawan)

        aveperkaryawan = []
        for ele in perkaryawan:
            aveperkaryawan.append(sum(ele) / len(ele))

        plt.clf()
        colors = []
        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            plt.scatter(namaline[i], perperkaryawan[i],c=colors[i])

        plt.plot(xbarr.xbarr_karyawan, aveperkaryawan, label='Average')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(xbarr.xbarr_nkaryawan))
        plt.title('Data by Appraisal')
        plt.xlabel('Appraisal')
        plt.ylabel('Measurement')

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        dba = urllib.parse.quote(string)

        #####################################

        urutline = [i+1 for i in range(int(xbarr.xbarr_npart))]
        urutlineline = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            urutlineline.append(urutline)

        plt.clf()
        colors = []
        for i in range(int(xbarr.xbarr_nkaryawan)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            plt.scatter(urutlineline[i], avepart[i], c=colors[i], label=xbarr.xbarr_karyawan[i])
            plt.plot(urutlineline[i], avepart[i], c=colors[i])
        plt.title('Average Appraisal By Part')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(xbarr.xbarr_nkaryawan))
        plt.xlabel('Part No')
        plt.ylabel('Measurement')

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        aabp = urllib.parse.quote(string)
        ####################################

        listuclx = []
        listlclx = []

        for j in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                listuclx.append(uclx)
                listlclx.append(lclx)

        flat = [x for l in avepart for x in l]
        flat = np.array(flat)
        urut = []
        temp = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart)):
                urut.append(temp)
                
                temp = temp + 1

        plt.clf()
        fig, ax3 = plt.subplots()

        ax3.plot(flat, label='Xbar')
        ax3.plot(listuclx, label='UCLXbar2')
        ax3.plot(listlclx, label='LCLXbar2')

        ax3.set_xticks(urut)
        ax3.set_xticklabels(bot)
        x1, x2 = ax3.get_xlim() 
        ax4 = ax3.twiny()
        ax4.set_xlim(x1,x2)
        ax4.set_xticks(urut)
        ax4.set_xticklabels(top)
        ax3.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(xbarr.xbarr_nkaryawan))

        plt.title('Xbar vs Appraisal')
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        xva = urllib.parse.quote(string)

        ####################################

        gabung = zip(xbarr.xbarr_karyawan, range(1, int(xbarr.xbarr_nkaryawan)+1))
        survey = Survey.objects.get(id = xbarr.xbarr_survey_id)
        return render(request,'grr_xbarr/comment_xbarr.html',{'psvc':psvc, 'rva':rva, 'xva':xva, 'dbs':dbs, 'dba':dba, 'aabp':aabp, 'xbarr':xbarr, 'survey':survey, 'gabung':gabung})
        # return render(request,'xbarr/result_xbarr.html',{'resumes':resumes})
    else:
        return redirect('/logout')

def storeCommentGrrXbarr(request, pk):
    if 'user' in request.session:
        xbarr = Xbarr.objects.get(id = pk)
        
        xbarr.xbarr_recommendation = request.POST.getlist('xbarr_recommendation')
        xbarr.xbarr_psvc = request.POST.get('xbarr_psvc')
        xbarr.xbarr_rva = request.POST.get('xbarr_rva')
        xbarr.xbarr_dbs = request.POST.get('xbarr_dbs')
        xbarr.xbarr_dba = request.POST.get('xbarr_dba')
        xbarr.xbarr_aabp = request.POST.get('xbarr_aabp')
        xbarr.save()

        return redirect('coretoolcrud:viewFinalGrrXbarr',xbarr.xbarr_survey_id )
        # return render(request,'xbarr/final_xbarr.html',{'psvc':psvc, 'rva':rva, 'dbs':dbs, 'dba':dba, 'aabp':aabp, 'xbarr':xbarr, 'survey':survey})
    else:
        return redirect('/logout')

def viewFinalGrrXbarr(request, pk):
    if 'user' in request.session:
        xbarr = Xbarr.objects.get(xbarr_survey_id = pk)
        survey = Survey.objects.get(id = xbarr.xbarr_survey_id)

        ################
        avepart = []
        avetrial = []
        rpart = []
        person = 2
        trial = 2
        sumtemp = 0
        iter = 0
        temp = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                for j in range(int(xbarr.xbarr_ntrial)):
                    sumtemp = sumtemp + xbarr.xbarr_all[i][j][k]
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_ntrial) == 0:
                        sumtemp = sumtemp / int(xbarr.xbarr_ntrial)
                        temp.append(sumtemp)
                        sumtemp = 0
            avepart.append(temp)
            temp = []

        iter = 0
        maxtemp = 0
        mintemp = 0
        temp = []
        tempmaxmin = []
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                for j in range(int(xbarr.xbarr_ntrial)): 
                    tempmaxmin.append(xbarr.xbarr_all[i][j][k])
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_ntrial) == 0:
                        maxtemp = max(tempmaxmin)
                        mintemp = min(tempmaxmin)
                        temp.append(maxtemp - mintemp)
                        tempmaxmin = []
            rpart.append(temp)
            temp = []

        xx = []
        rx = []
        sumtemp = 0

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                sumtemp = sumtemp + avepart[i][k]
            xx.append(sumtemp / int(xbarr.xbarr_npart))
            sumtemp = 0

        sumtemp = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                sumtemp = sumtemp + rpart[i][k]
            rx.append(sumtemp / int(xbarr.xbarr_npart))
            sumtemp = 0

        sumtemp = 0
        iter = 0
        temp = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_ntrial)):
                for k in range(int(xbarr.xbarr_npart)):
                    sumtemp = sumtemp + xbarr.xbarr_all[i][j][k]
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_npart) == 0:
                        sumtemp = sumtemp / int(xbarr.xbarr_npart)
                        temp.append(sumtemp)
                        sumtemp = 0
            avetrial.append(temp)
            temp = []

        sumavepart = []
        sumtemp = 0
        iter = 0

        for k in range(int(xbarr.xbarr_npart)):
            for i in range(int(xbarr.xbarr_nkaryawan)):
                sumtemp = sumtemp + avepart[i][k]
                iter = iter + 1
                if iter % int(xbarr.xbarr_nkaryawan) == 0:
                    sumavepart.append(sumtemp / int(xbarr.xbarr_nkaryawan))
                    sumtemp = 0

        xbar2 = sum(sumavepart) / int(xbarr.xbarr_npart)
        rp = max(sumavepart) - min(sumavepart)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]
        rbar = sum(rx) / int(xbarr.xbarr_nkaryawan)
        xbardiff = max(xx) - min(xx)

        for i in range(4):
            if subgroup[i][0] == int(xbarr.xbarr_ntrial):
                d4 = subgroup[i][1]
                

        ulcr = d4 * rbar
        lclr = 0

        a2 = 0

        # npart > 5 gimana?

        for i in range(4):
            if subgroup[i][0] == int(xbarr.xbarr_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]
        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar

        trial = [[2, 0.886525], [3, 0.590667], [4, 0.485673], [5, 0.429923], [6, 0.394633], [7, 0.369822], [8, 0.351247], [9, 0.3367], [10, 0.324886], [11, 0.315159], [12, 0.306843], [13, 0.29976], [14, 0.293513], [15, 0.288018]]

        for i in range(14):
            if trial[i][0] == int(xbarr.xbarr_ntrial):
                k1 = trial[i][1]
        
        ev = rbar * k1
        varrepeat = 6 * ev

        appraisal = [[2, 0.707109], [3, 0.523136], [4, 0.446654], [5, 0.403024], [6, 0.374177], [7, 0.353381], [8, 0.337509], [9, 0.324893], [10, 0.314559], [11, 0.305896], [12, 0.298493], [13, 0.292075], [14, 0.286438], [15, 0.281426], [16, 0.276954], [17, 0.272909], [18, 0.269234], [19, 0.265874], [20, 0.262787]]

        for i in range(19):
            if appraisal[i][0] == int(xbarr.xbarr_nkaryawan):
                k2 = appraisal[i][1]
        
        xdiffk2 = pow((xbardiff * k2), 2)
        ev2 = (ev ** 2) / (int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial))

        if xdiffk2 > ev2:
            av = sqrt(pow(xbardiff * k2, 2) - pow(ev, 2) / (int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)))
        else:
            av = 0

        varreproduce = 6 * av
        grr = sqrt(pow(ev, 2) + pow(av, 2))
        vargrr = 6 * grr

        #parts = [[2, 0.70711], [3, 0.52314], [4, 0.44665], [5, 0.4030], [6, 0.3742], [7, 0.3534], [8, 0.3375], [9, 0.3249], [10, 0.3146]]
        parts = [[2, 0.707109], [3, 0.523136], [4, 0.446654], [5, 0.403024], [6, 0.374177], [7, 0.353381], [8, 0.337509], [9, 0.324893], [10, 0.314559], [11, 0.305896], [12, 0.298493], [13, 0.292075], [14, 0.286438], [15, 0.281426], [16, 0.276954], [17, 0.272909], [18, 0.269234], [19, 0.265874], [20, 0.262787]]

        
        for i in range(19):
            if parts[i][0] == int(xbarr.xbarr_npart):
                k3 = parts[i][1]
        pv = rp * k3
        varpart = 6 * pv

        tv = sqrt(pow(grr, 2) + pow(pv, 2))
        vartv = 6 * tv
        pev = ev / tv * 100
        pav = av / tv * 100
        pgrr = grr / tv * 100
        ppv = pv / tv * 100
        ndc = 1.41 * (pv / grr)

        stdev6 = int(xbarr.xbarr_stdev) * 6
        vcev = pow(ev, 2)
        vcav = pow(av, 2)
        vcgrr = pow(grr, 2)
        vcpv = pow(pv, 2)
        vcndc = vcpv + vcgrr

        pvcev = vcev / vcndc * 100
        pvcav = vcav / vcndc * 100
        pvcgrr = vcgrr / vcndc * 100
        pvcpv = vcpv / vcndc * 100
        pvcndc = vcndc / vcndc * 100

        if int(xbarr.xbarr_stdevmax) == 0 and int(xbarr.xbarr_stdevmin) == 0:
            ptev = 0
            ptav = 0
            ptgrr = 0
            ptpv = 0
            ptndc = 0
        else:
            ptev = varrepeat / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptav = varreproduce / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptgrr = vargrr / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptpv = varpart / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptndc = vartv / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100

        if stdev6 == 0:
            ppev = 0
            ppav = 0
            ppgrr = 0
            pppv = 0
            ppndc = 0
        else:
            ppev = varrepeat / stdev6 * 100
            ppav = varreproduce / stdev6 * 100
            ppgrr = vargrr / stdev6 * 100
            pppv = varpart / stdev6 * 100
            ppndc = vartv / stdev6 * 100

        resume = []
        temp = []

        temp.append("GRR")
        temp.append(pgrr)
        temp.append(pvcgrr)
        temp.append(ptgrr)
        temp.append(ppgrr)
        resume.append(temp)

        temp = []
        temp.append("Repeatability")
        temp.append(pev)
        temp.append(pvcev)
        temp.append(ptev)
        temp.append(ppev)
        resume.append(temp)

        temp = []
        temp.append("Reproducibility")
        temp.append(pav)
        temp.append(pvcav)
        temp.append(ptav)
        temp.append(ppav)
        resume.append(temp)

        temp = []
        temp.append("Part to Part")
        temp.append(ppv)
        temp.append(pvcpv)
        temp.append(ptpv)
        temp.append(pppv)
        resume.append(temp)

        
        xbarr.xbarr_resume = resume
        xbarr.save()

        resumes = xbarr.xbarr_resume

        ###############
        #% Study var contribution
        x, a, b, c, d = [*zip(*resume)]
        
        if all(ele == 0 for ele in c) and all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b}, index=x)
        elif all(ele == 0 for ele in c) and not all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Process': d}, index=x)
        elif not all(ele == 0 for ele in c) and all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Tolerance': c}, index=x)
        else:
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Tolerance': c, '% Process': d}, index=x)
        plt.figure()
        dfres.plot(kind='bar', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)

        ####bokeh#######

        p = figure(title="Resume", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Value', x_axis_label='Trial')
        # p.vbar(x = dfres.Jenis, source = dfres)

        scriptresume, divresume = components(p)

        ###################

        listulcr = []
        listlclr = []

        for j in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                listulcr.append(ulcr)
                listlclr.append(lclr)



        bot = []
        urut = []
        temp = 0

        flat = [x for l in rpart for x in l]
        flat = np.array(flat)
        print(xbarr.xbarr_nkaryawan)
        print(xbarr.xbarr_karyawan)
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart)):
                urut.append(temp)
                bot.append(xbarr.xbarr_karyawan[i] + "-" + str(j+1))

        ####bokeh#######

        p = figure(title="Range vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range = bot, y_axis_label='Measurement', x_axis_label='Appraiser-Trial')
        p.line(bot, flat, legend_label="Range", line_width=2)
        p.line(bot, listulcr, legend_label="UCLRbar", color="green", line_width=2)
        p.line(bot, listlclr, legend_label="LCLRbar", color="red", line_width=2)
        p.xaxis.major_label_orientation = "vertical"

        scriptrva, divrva = components(p)
        
        ####################################

        perpart = [x for l in xbarr.xbarr_all for x in l]
        perpart = np.array(perpart)
        perpart = perpart.T
        perpart = perpart.tolist()

        pertrial = [x for l in xbarr.xbarr_all for x in l]
        allnontt = [x for l in pertrial for x in l]
        perkaryawan = []
        temp = []
        iter = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
                temp.append(allnontt[iter])
                iter = iter + 1
            perkaryawan.append(temp)
            temp = []

        urut = []
        temp = []
        for i in range(int(xbarr.xbarr_npart)):
            for j in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
                temp.append(i+1)
            urut.append(temp)
            temp = []
        
        perperkaryawan = np.array(perkaryawan)
        perperkaryawan = perperkaryawan.T
        perperkaryawan = perperkaryawan.tolist()

        allflatflat =  [x for l in perpart for x in l]
        urutflat =  [x for l in urut for x in l]

        urutline = [i+1 for i in range(int(xbarr.xbarr_npart))]

        urutlineline = []

        for i in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
            urutlineline.append(urutline)

        avepertrial = []
        for ele in perpart:
            avepertrial.append(sum(ele) / len(ele))

        #colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"])
        colors = []
        

        ####bokeh#######

        p = figure(title="Data by Sample", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        p.line(urutline, avepertrial, legend_label="Average", line_width=2)
        for i in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutlineline[i], pertrial[i], color=colors[i], marker="circle")
        scriptdbs, divdbs = components(p)

        #####################################

        urutline = [i+1 for i in range(int(xbarr.xbarr_nkaryawan))]
        urutlineline = []
        namaline = []

        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            urutlineline.append(urutline)


        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            namaline.append(xbarr.xbarr_karyawan)

        aveperkaryawan = []
        for ele in perkaryawan:
            aveperkaryawan.append(sum(ele) / len(ele))

       
        ######bokeh######

        p = figure(title="Data by Appraisal", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range = xbarr.xbarr_karyawan, x_axis_label='Appraiser', y_axis_label='Measurement')
        p.line(xbarr.xbarr_karyawan, aveperkaryawan, legend_label="Average", line_width=2)
        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(namaline[i], perperkaryawan[i], color=colors[i], marker="circle")

        p.xaxis.major_label_orientation = "vertical"
        scriptdba, divdba = components(p)

        #####################################

        urutline = [i+1 for i in range(int(xbarr.xbarr_npart))]
        urutlineline = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            urutlineline.append(urutline)

        ####bokeh#######

        p = figure(title="Average Appraiser by Part", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        # p.line(urutline, avepertrial, legend_label="Average", line_width=2)
        for i in range(int(xbarr.xbarr_nkaryawan)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutlineline[i], avepart[i], color="(0.5, 0.75, 0.5)", marker="circle")
            p.line(urutlineline[i], avepart[i], legend_label=xbarr.xbarr_karyawan[i], color=colors[i], line_width=2)
        scriptaabp, divaabp = components(p)

        ####################################

        listuclx = []
        listlclx = []

        for j in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                listuclx.append(uclx)
                listlclx.append(lclx)

        flat = [x for l in avepart for x in l]
        flat = np.array(flat)
        urut = []
        temp = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart)):
                urut.append(temp)
                
                temp = temp + 1

        ####bokeh#######

        p = figure(title="Xbar vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range = bot, y_axis_label='Measurement', x_axis_label='Appraiser-Trial')
        p.line(bot, flat, legend_label="Xbar", line_width=2)
        p.line(bot, listuclx, legend_label="UCLXbar2", color="green", line_width=2)
        p.line(bot, listlclx, legend_label="LCLXbar2", color="red", line_width=2)
        p.xaxis.major_label_orientation = "vertical"

        scriptxva, divxva = components(p)

        ####################################
        namas = xbarr.xbarr_karyawan
        part = range(int(xbarr.xbarr_npart))
        part1 = range(1, int(xbarr.xbarr_npart)+1)
        karyawan = range(int(xbarr.xbarr_nkaryawan))
        trial = range(int(xbarr.xbarr_ntrial))
        gabung = zip(xbarr.xbarr_all, xbarr.xbarr_karyawan)
        gabung2 = zip(xbarr.xbarr_karyawan, range(1, int(xbarr.xbarr_nkaryawan)+1))
        gabungave = zip(xbarr.xbarr_karyawan, avepart)
        gabungr = zip(xbarr.xbarr_karyawan, rpart)

        ###################
        

        tabeltambahan = [tv, vartv, pev, pav, pgrr, ppv, ndc, vcev, vcav, vcgrr, vcpv, vcndc, pvcev, pvcav, pvcgrr, pvcpv, pvcndc, ptev, ptav, ptgrr, ptpv, ptndc, ppev, ppav, ppgrr, pppv, ppndc, ev, av, grr, pv]

        return render(request,'grr_xbarr/collection_xbarr3.html',{'tabeltambahan':tabeltambahan, 'gabung':gabung, 'gabung2':gabung2, 'gabungave':gabungave, 'gabungr':gabungr, 'namas': namas, 'part1':part1, 'part':part, 'karyawan':karyawan, 'trial':trial, 'xbarr':xbarr, 'survey':survey, 'psvc':psvc, 'scriptdbs':scriptdbs, 'divdbs':divdbs, 'scriptdba':scriptdba, 'divdba':divdba, 'scriptrva':scriptrva, 'divrva':divrva, 'scriptresume':scriptresume, 'divresume':divresume, 'scriptaabp':scriptaabp, 'divaabp':divaabp, 'scriptxva':scriptxva, 'divxva':divxva})
    else:
        return redirect('/logout')

def viewPrintGrrXbarr(request, pk):
    if 'user' in request.session:
        xbarr = Xbarr.objects.get(xbarr_survey_id = pk)
        survey = Survey.objects.get(id = xbarr.xbarr_survey_id)

        ################
        avepart = []
        avetrial = []
        rpart = []
        person = 2
        trial = 2
        sumtemp = 0
        iter = 0
        temp = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                for j in range(int(xbarr.xbarr_ntrial)):
                    sumtemp = sumtemp + xbarr.xbarr_all[i][j][k]
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_ntrial) == 0:
                        sumtemp = sumtemp / int(xbarr.xbarr_ntrial)
                        temp.append(sumtemp)
                        sumtemp = 0
            avepart.append(temp)
            temp = []

        iter = 0
        maxtemp = 0
        mintemp = 0
        temp = []
        tempmaxmin = []
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                for j in range(int(xbarr.xbarr_ntrial)): 
                    tempmaxmin.append(xbarr.xbarr_all[i][j][k])
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_ntrial) == 0:
                        maxtemp = max(tempmaxmin)
                        mintemp = min(tempmaxmin)
                        temp.append(maxtemp - mintemp)
                        tempmaxmin = []
            rpart.append(temp)
            temp = []

        xx = []
        rx = []
        sumtemp = 0

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                sumtemp = sumtemp + avepart[i][k]
            xx.append(sumtemp / int(xbarr.xbarr_npart))
            sumtemp = 0

        sumtemp = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                sumtemp = sumtemp + rpart[i][k]
            rx.append(sumtemp / int(xbarr.xbarr_npart))
            sumtemp = 0

        sumtemp = 0
        iter = 0
        temp = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_ntrial)):
                for k in range(int(xbarr.xbarr_npart)):
                    sumtemp = sumtemp + xbarr.xbarr_all[i][j][k]
                    iter = iter + 1
                    if iter % int(xbarr.xbarr_npart) == 0:
                        sumtemp = sumtemp / int(xbarr.xbarr_npart)
                        temp.append(sumtemp)
                        sumtemp = 0
            avetrial.append(temp)
            temp = []

        sumavepart = []
        sumtemp = 0
        iter = 0

        for k in range(int(xbarr.xbarr_npart)):
            for i in range(int(xbarr.xbarr_nkaryawan)):
                sumtemp = sumtemp + avepart[i][k]
                iter = iter + 1
                if iter % int(xbarr.xbarr_nkaryawan) == 0:
                    sumavepart.append(sumtemp / int(xbarr.xbarr_nkaryawan))
                    sumtemp = 0

        xbar2 = sum(sumavepart) / int(xbarr.xbarr_npart)
        rp = max(sumavepart) - min(sumavepart)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]
        rbar = sum(rx) / int(xbarr.xbarr_nkaryawan)
        xbardiff = max(xx) - min(xx)

        for i in range(4):
            if subgroup[i][0] == int(xbarr.xbarr_ntrial):
                d4 = subgroup[i][1]
                

        ulcr = d4 * rbar
        lclr = 0

        a2 = 0

        # npart > 5 gimana?

        for i in range(4):
            if subgroup[i][0] == int(xbarr.xbarr_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]
        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar

        trial = [[2, 0.886525], [3, 0.590667], [4, 0.485673], [5, 0.429923], [6, 0.394633], [7, 0.369822], [8, 0.351247], [9, 0.3367], [10, 0.324886], [11, 0.315159], [12, 0.306843], [13, 0.29976], [14, 0.293513], [15, 0.288018]]

        for i in range(14):
            if trial[i][0] == int(xbarr.xbarr_ntrial):
                k1 = trial[i][1]
        
        ev = rbar * k1
        varrepeat = 6 * ev

        appraisal = [[2, 0.707109], [3, 0.523136], [4, 0.446654], [5, 0.403024], [6, 0.374177], [7, 0.353381], [8, 0.337509], [9, 0.324893], [10, 0.314559], [11, 0.305896], [12, 0.298493], [13, 0.292075], [14, 0.286438], [15, 0.281426], [16, 0.276954], [17, 0.272909], [18, 0.269234], [19, 0.265874], [20, 0.262787]]

        for i in range(19):
            if appraisal[i][0] == int(xbarr.xbarr_nkaryawan):
                k2 = appraisal[i][1]
        
        xdiffk2 = pow((xbardiff * k2), 2)
        ev2 = (ev ** 2) / (int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial))

        if xdiffk2 > ev2:
            av = sqrt(pow(xbardiff * k2, 2) - pow(ev, 2) / (int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)))
        else:
            av = 0

        varreproduce = 6 * av
        grr = sqrt(pow(ev, 2) + pow(av, 2))
        vargrr = 6 * grr

        #parts = [[2, 0.70711], [3, 0.52314], [4, 0.44665], [5, 0.4030], [6, 0.3742], [7, 0.3534], [8, 0.3375], [9, 0.3249], [10, 0.3146]]
        parts = [[2, 0.707109], [3, 0.523136], [4, 0.446654], [5, 0.403024], [6, 0.374177], [7, 0.353381], [8, 0.337509], [9, 0.324893], [10, 0.314559], [11, 0.305896], [12, 0.298493], [13, 0.292075], [14, 0.286438], [15, 0.281426], [16, 0.276954], [17, 0.272909], [18, 0.269234], [19, 0.265874], [20, 0.262787]]

        
        for i in range(19):
            if parts[i][0] == int(xbarr.xbarr_npart):
                k3 = parts[i][1]
        pv = rp * k3
        varpart = 6 * pv

        tv = sqrt(pow(grr, 2) + pow(pv, 2))
        vartv = 6 * tv
        pev = ev / tv * 100
        pav = av / tv * 100
        pgrr = grr / tv * 100
        ppv = pv / tv * 100
        ndc = 1.41 * (pv / grr)

        stdev6 = int(xbarr.xbarr_stdev) * 6
        vcev = pow(ev, 2)
        vcav = pow(av, 2)
        vcgrr = pow(grr, 2)
        vcpv = pow(pv, 2)
        vcndc = vcpv + vcgrr

        pvcev = vcev / vcndc * 100
        pvcav = vcav / vcndc * 100
        pvcgrr = vcgrr / vcndc * 100
        pvcpv = vcpv / vcndc * 100
        pvcndc = vcndc / vcndc * 100

        if int(xbarr.xbarr_stdevmax) == 0 and int(xbarr.xbarr_stdevmin) == 0:
            ptev = 0
            ptav = 0
            ptgrr = 0
            ptpv = 0
            ptndc = 0
        else:
            ptev = varrepeat / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptav = varreproduce / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptgrr = vargrr / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptpv = varpart / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100
            ptndc = vartv / (int(xbarr.xbarr_stdevmax) - int(xbarr.xbarr_stdevmin)) * 100

        if stdev6 == 0:
            ppev = 0
            ppav = 0
            ppgrr = 0
            pppv = 0
            ppndc = 0
        else:
            ppev = varrepeat / stdev6 * 100
            ppav = varreproduce / stdev6 * 100
            ppgrr = vargrr / stdev6 * 100
            pppv = varpart / stdev6 * 100
            ppndc = vartv / stdev6 * 100

        resume = []
        temp = []

        temp.append("GRR")
        temp.append(pgrr)
        temp.append(pvcgrr)
        temp.append(ptgrr)
        temp.append(ppgrr)
        resume.append(temp)

        temp = []
        temp.append("Repeatability")
        temp.append(pev)
        temp.append(pvcev)
        temp.append(ptev)
        temp.append(ppev)
        resume.append(temp)

        temp = []
        temp.append("Reproducibility")
        temp.append(pav)
        temp.append(pvcav)
        temp.append(ptav)
        temp.append(ppav)
        resume.append(temp)

        temp = []
        temp.append("Part to Part")
        temp.append(ppv)
        temp.append(pvcpv)
        temp.append(ptpv)
        temp.append(pppv)
        resume.append(temp)

        
        xbarr.xbarr_resume = resume
        xbarr.save()

        resumes = xbarr.xbarr_resume

        ###############
        #% Study var contribution
        x, a, b, c, d = [*zip(*resume)]
        
        if all(ele == 0 for ele in c) and all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b}, index=x)
        elif all(ele == 0 for ele in c) and not all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Process': d}, index=x)
        elif not all(ele == 0 for ele in c) and all(ele == 0 for ele in d):
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Tolerance': c}, index=x)
        else:
            dfres = pd.DataFrame(data={'% Study Var': a, '% Var Comp': b, '% Tolerance': c, '% Process': d}, index=x)
        plt.figure()
        dfres.plot(kind='bar', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)

        ####bokeh#######

        p = figure(title="Resume", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Value', x_axis_label='Trial')
        # p.vbar(x = dfres.Jenis, source = dfres)

        scriptresume, divresume = components(p)

        ###################

        listulcr = []
        listlclr = []

        for j in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                listulcr.append(ulcr)
                listlclr.append(lclr)



        bot = []
        urut = []
        temp = 0

        flat = [x for l in rpart for x in l]
        flat = np.array(flat)
        print(xbarr.xbarr_nkaryawan)
        print(xbarr.xbarr_karyawan)
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart)):
                urut.append(temp)
                bot.append(xbarr.xbarr_karyawan[i] + "-" + str(j+1))

        ####bokeh#######

        p = figure(title="Range vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range = bot, y_axis_label='Measurement', x_axis_label='Appraiser-Trial')
        p.line(bot, flat, legend_label="Range", line_width=2)
        p.line(bot, listulcr, legend_label="UCLRbar", color="green", line_width=2)
        p.line(bot, listlclr, legend_label="LCLRbar", color="red", line_width=2)
        p.xaxis.major_label_orientation = "vertical"

        scriptrva, divrva = components(p)
        
        ####################################

        perpart = [x for l in xbarr.xbarr_all for x in l]
        perpart = np.array(perpart)
        perpart = perpart.T
        perpart = perpart.tolist()

        pertrial = [x for l in xbarr.xbarr_all for x in l]
        allnontt = [x for l in pertrial for x in l]
        perkaryawan = []
        temp = []
        iter = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
                temp.append(allnontt[iter])
                iter = iter + 1
            perkaryawan.append(temp)
            temp = []

        urut = []
        temp = []
        for i in range(int(xbarr.xbarr_npart)):
            for j in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
                temp.append(i+1)
            urut.append(temp)
            temp = []
        
        perperkaryawan = np.array(perkaryawan)
        perperkaryawan = perperkaryawan.T
        perperkaryawan = perperkaryawan.tolist()

        allflatflat =  [x for l in perpart for x in l]
        urutflat =  [x for l in urut for x in l]

        urutline = [i+1 for i in range(int(xbarr.xbarr_npart))]

        urutlineline = []

        for i in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
            urutlineline.append(urutline)

        avepertrial = []
        for ele in perpart:
            avepertrial.append(sum(ele) / len(ele))

        #colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"])
        colors = []
        

        ####bokeh#######

        p = figure(title="Data by Sample", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        p.line(urutline, avepertrial, legend_label="Average", line_width=2)
        for i in range(int(xbarr.xbarr_nkaryawan) * int(xbarr.xbarr_ntrial)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutlineline[i], pertrial[i], color=colors[i], marker="circle")
        scriptdbs, divdbs = components(p)

        #####################################

        urutline = [i+1 for i in range(int(xbarr.xbarr_nkaryawan))]
        urutlineline = []
        namaline = []

        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            urutlineline.append(urutline)


        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            namaline.append(xbarr.xbarr_karyawan)

        aveperkaryawan = []
        for ele in perkaryawan:
            aveperkaryawan.append(sum(ele) / len(ele))

       
        ######bokeh######

        p = figure(title="Data by Appraisal", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range = xbarr.xbarr_karyawan, x_axis_label='Appraiser', y_axis_label='Measurement')
        p.line(xbarr.xbarr_karyawan, aveperkaryawan, legend_label="Average", line_width=2)
        for i in range(int(xbarr.xbarr_npart) * int(xbarr.xbarr_ntrial)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(namaline[i], perperkaryawan[i], color=colors[i], marker="circle")

        p.xaxis.major_label_orientation = "vertical"
        scriptdba, divdba = components(p)

        #####################################

        urutline = [i+1 for i in range(int(xbarr.xbarr_npart))]
        urutlineline = []

        for i in range(int(xbarr.xbarr_nkaryawan)):
            urutlineline.append(urutline)

        ####bokeh#######

        p = figure(title="Average Appraiser by Part", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        # p.line(urutline, avepertrial, legend_label="Average", line_width=2)
        for i in range(int(xbarr.xbarr_nkaryawan)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutlineline[i], avepart[i], color="(0.5, 0.75, 0.5)", marker="circle")
            p.line(urutlineline[i], avepart[i], legend_label=xbarr.xbarr_karyawan[i], color=colors[i], line_width=2)
        scriptaabp, divaabp = components(p)

        ####################################

        listuclx = []
        listlclx = []

        for j in range(int(xbarr.xbarr_nkaryawan)):
            for k in range(int(xbarr.xbarr_npart)):
                listuclx.append(uclx)
                listlclx.append(lclx)

        flat = [x for l in avepart for x in l]
        flat = np.array(flat)
        urut = []
        temp = 0
        for i in range(int(xbarr.xbarr_nkaryawan)):
            for j in range(int(xbarr.xbarr_npart)):
                urut.append(temp)
                
                temp = temp + 1

        ####bokeh#######

        p = figure(title="Xbar vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range = bot, y_axis_label='Measurement', x_axis_label='Appraiser-Trial')
        p.line(bot, flat, legend_label="Xbar", line_width=2)
        p.line(bot, listuclx, legend_label="UCLXbar2", color="green", line_width=2)
        p.line(bot, listlclx, legend_label="LCLXbar2", color="red", line_width=2)
        p.xaxis.major_label_orientation = "vertical"

        scriptxva, divxva = components(p)

        ####################################
        namas = xbarr.xbarr_karyawan
        part = range(int(xbarr.xbarr_npart))
        part1 = range(1, int(xbarr.xbarr_npart)+1)
        karyawan = range(int(xbarr.xbarr_nkaryawan))
        trial = range(int(xbarr.xbarr_ntrial))
        gabung = zip(xbarr.xbarr_all, xbarr.xbarr_karyawan)
        gabung2 = zip(xbarr.xbarr_karyawan, range(1, int(xbarr.xbarr_nkaryawan)+1))
        gabungave = zip(xbarr.xbarr_karyawan, avepart)
        gabungr = zip(xbarr.xbarr_karyawan, rpart)

        ###################
        

        tabeltambahan = [tv, vartv, pev, pav, pgrr, ppv, ndc, vcev, vcav, vcgrr, vcpv, vcndc, pvcev, pvcav, pvcgrr, pvcpv, pvcndc, ptev, ptav, ptgrr, ptpv, ptndc, ppev, ppav, ppgrr, pppv, ppndc, ev, av, grr, pv]

        return render(request,'grr_xbarr/print_xbarr.html',{'tabeltambahan':tabeltambahan, 'gabung':gabung, 'gabung2':gabung2, 'gabungave':gabungave, 'gabungr':gabungr, 'namas': namas, 'part1':part1, 'part':part, 'karyawan':karyawan, 'trial':trial, 'xbarr':xbarr, 'survey':survey, 'psvc':psvc, 'scriptdbs':scriptdbs, 'divdbs':divdbs, 'scriptdba':scriptdba, 'divdba':divdba, 'scriptrva':scriptrva, 'divrva':divrva, 'scriptresume':scriptresume, 'divresume':divresume, 'scriptaabp':scriptaabp, 'divaabp':divaabp, 'scriptxva':scriptxva, 'divxva':divxva})
    else:
        return redirect('/logout')

def deleteGrrXbarr(request, pk):
    if 'user' in request.session:
        xbarr = Xbarr.objects.get(xbarr_survey_id = pk)
        xbarr.delete()
        messages.success(request, "Xbarr berhasil dihapus")
        return redirect('coretoolcrud:viewDetailSurvey', pk)
    else:
        return redirect('/logout')

# GRR Cross

def viewCross(request, pk):
    if 'user' in request.session:
        try:
            cross = Cross.objects.get(cross_survey_id = pk)
            if cross.cross_all:
                return redirect('coretoolcrud:viewFinalCross',pk )
            else:
                namas = cross.cross_karyawan
                part = range(1, int(cross.cross_npart)+1)
                karyawan = range(int(cross.cross_nkaryawan))
                trial = range(int(cross.cross_ntrial))
                return render(request,'cross/all_cross.html',{'part':part, 'karyawan':karyawan, 'trial':trial, 'namas':namas, 'cross':cross})
        except Cross.DoesNotExist:
            return render(request,'cross/cross.html',{'pk':pk})
    else:
        return redirect('/logout')

def storeCross(request, pk):
    if 'user' in request.session:
        try:
            cross = Cross.objects.get(cross_survey_id = pk)
            cross.delete()
        except Cross.DoesNotExist:
            pass
            
        cross = Cross()
        cross.cross_survey_id = pk
        cross.cross_nkaryawan = request.POST.get('cross_nkaryawan')
        cross.cross_npart = request.POST.get('cross_npart')
        cross.cross_ntrial = request.POST.get('cross_ntrial')
        cross.cross_stdev = request.POST.get('cross_stdev')
        cross.cross_stdevmax = request.POST.get('cross_stdevmax')
        cross.cross_stdevmin = request.POST.get('cross_stdevmin')
        cross.cross_karyawan = request.POST.getlist('cross_karyawan')
        
        cross.save()
        # karyawan = range(int(cross.cross_nkaryawan))
        # return render(request,'cross/karyawan_cross.html',{'karyawan':karyawan})

        namas = cross.cross_karyawan
        part = range(1, int(cross.cross_npart)+1)
        karyawan = range(int(cross.cross_nkaryawan))
        trial = range(int(cross.cross_ntrial))
        return render(request,'cross/all_cross.html',{'part':part, 'karyawan':karyawan, 'trial':trial, 'namas':namas, 'cross':cross})
    else:
        return redirect('/logout')

def storeAllCross(request, pk):
    if 'user' in request.session:
        cross = Cross.objects.get(cross_survey_id = pk)
        temppart = []
        temptrial = []
        tempkaryawan = []
        iter = 1

        cross.cross_all = request.POST.getlist('cross_all')
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart) * int(cross.cross_ntrial)):
            if iter % int(cross.cross_npart) != 0:
                temppart.append(cross.cross_all[i])
                iter = iter + 1
            else:
                if iter % (int(cross.cross_npart) * int(cross.cross_ntrial)) == 0:
                    temppart.append(cross.cross_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    tempkaryawan.append(temptrial)
                    temptrial = []
                    temppart = []
                    iter = iter + 1
                else:
                    temppart.append(cross.cross_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    temppart = []
                    iter = iter + 1
        
        cross.cross_all = tempkaryawan
        cross.save()
        return redirect('coretoolcrud:viewCommentCross', pk)
    else:
        return redirect('/logout')

def viewCommentCross(request, pk):
    if 'user' in request.session:
        cross = Cross.objects.get(cross_survey_id = pk)
        ###############

        temp = []
        perpart = []
        for ele in cross.cross_all:
            temp =  [x for l in ele for x in l]
            perpart.append(temp)
            temp = []

        perpart = [x for l in perpart for x in l]

        all = []
        iter = 0
        temp = []

        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_ntrial)):
                for k in range(int(cross.cross_npart)):
                    p = k + 1
                    p = str(p)
                    t = j + 1
                    t = str(t)
                    temp.append(float(perpart[iter]))
                    temp.append("P"+p)
                    temp.append("T"+t)
                    temp.append(cross.cross_karyawan[i])
                    all.append(temp)
                    temp = []
                    iter = iter + 1
        
        df = pd.DataFrame(all, columns =['Uk', 'Part', 'Trial', 'Karyawan'])

        aov = pg.anova(dv='Uk', between=['Part', 'Karyawan'], data=df, detailed=True)
        aov.loc[0, 'F'] = aov['MS'][0] / aov['MS'][2]
        aov.loc[1, 'F'] = aov['MS'][1] / aov['MS'][2]

        aov.loc[0, 'p-unc'] = 1 - f.cdf(aov['F'][0], aov['DF'][0], aov['DF'][2])
        aov.loc[1, 'p-unc'] = 1 - f.cdf(aov['F'][1], aov['DF'][1], aov['DF'][2])
        aov.loc[2, 'p-unc'] = 1 - f.cdf(aov['F'][2], aov['DF'][2], aov['DF'][3])
        aov = aov.rename(columns={'p-unc': 'P Value'})
        aov = aov.rename(columns={'np2': 'Ket'})

        if aov['P Value'][0] >= 0.05:
            aov.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aov['P Value'][0] < 0.05:
            aov.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aov['P Value'][1] >= 0.05:
            aov.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aov['P Value'][1] < 0.05:
            aov.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        if aov['P Value'][2] >= 0.05:
            aov.loc[2, 'Ket'] = 'Not significant, interactions dont contribute variation'
        if aov['P Value'][2] < 0.05:
            aov.loc[2, 'Ket'] = 'Significant, interactions contribute variation'
        
        evrepeat = 6 * aov['MS'][3] ** 0.5
        av = 0
        if aov['MS'][1] - aov['MS'][2] > 0:
            av = (aov['MS'][1] - aov['MS'][2]) / (int(cross.cross_npart) * int(cross.cross_ntrial)) ** 0.5 * 6

        intt = (((aov['MS'][2] - aov['MS'][3]) / int(cross.cross_ntrial)) ** 0.5) * 6
        pv = 6 * ((aov['MS'][0] - aov['MS'][2]) / (int(cross.cross_nkaryawan) * int(cross.cross_ntrial))) ** 0.5
        grr = (evrepeat ** 2 + av ** 2 + intt ** 2) ** 0.5
        evrepro = (av ** 2 + intt ** 2) ** 0.5
        tv = (grr ** 2 + pv ** 2) ** 0.5
        ndc = 1
        
        if 1.41 * pv / grr > 1:
            ndc = math.floor(1.41 * pv / grr)

        sv = [grr, evrepeat, evrepro, av, intt, pv, tv]
        vc = []
        for i in range(7):
            vc.append((sv[i] / 6) ** 2)
        psv = []
        for i in range(7):
            psv.append(sv[i] / sv[6] * 100)
        pc = []
        for i in range(7):
            pc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sv[i] / (int(cross.cross_stdevmax) - int(cross.cross_stdevmin)) * 100)
        pp = []
        if int(cross.cross_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sv[i] / (6 * int(cross.cross_stdev)) * 100)
        resinteraksi = [sv, vc, psv, pc, pt, pp]
        resinteraksi = np.array(resinteraksi)
        resinteraksi = resinteraksi.T
        resinteraksi = resinteraksi.tolist()
        dfinteraksi = pd.DataFrame(resinteraksi, columns =['Study Variation', 'Var Comp', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfinteraksi.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'AV', 'INT', 'PV', 'TV'])
        
        aovnon = aov.copy()
        aovnon.loc[2, 'Source'] = 'Repeatability'
        aovnon.loc[3, 'Source'] = 'Total'
        aovnon.loc[2, 'DF'] = (int(cross.cross_npart) - 1) * (int(cross.cross_nkaryawan) - 1) + int(cross.cross_nkaryawan) * int(cross.cross_npart) * (int(cross.cross_ntrial) - 1)
        aovnon.loc[3, 'DF'] =  aovnon['DF'][0] +  aovnon['DF'][1] +  aovnon['DF'][2]
        aovnon.loc[2, 'SS'] = aovnon['SS'][2] + aovnon['SS'][3]
        aovnon.loc[2, 'SS'] = aov['SS'][2] + aov['SS'][3]
        aovnon.loc[3, 'SS'] =  aovnon['SS'][0] + aovnon['SS'][1] +  aovnon['SS'][2]
        aovnon.loc[2, 'MS'] =  aovnon['SS'][2] / aovnon['DF'][2]
        aovnon.loc[3, 'MS'] = "NaN"
        aovnon.loc[0, 'F'] =  aovnon['MS'][0] / aovnon['MS'][2]
        aovnon.loc[1, 'F'] =  aovnon['MS'][1] / aovnon['MS'][2]
        aovnon.loc[3, 'F'] = 0
        aovnon.loc[0, 'P Value'] = 1 - f.cdf(aovnon['F'][0], aovnon['DF'][0], aovnon['DF'][2])
        aovnon.loc[1, 'P Value'] = 1 - f.cdf(aovnon['F'][1], aovnon['DF'][1], aovnon['DF'][2])
        if aovnon['P Value'][0] >= 0.05:
            aovnon.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aovnon['P Value'][0] < 0.05:
            aovnon.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aovnon['P Value'][1] >= 0.05:
            aovnon.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aovnon['P Value'][1] < 0.05:
            aovnon.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        aovnon.loc[2, 'Ket'] = 0

        sd6ev =  6 * aovnon['MS'][2] ** 0.5
        sd6av = 0
        if aovnon['MS'][1] - aovnon['MS'][2] > 0:
            sd6av = ((aovnon['MS'][1] - aovnon['MS'][2]) / (int(cross.cross_npart) * int(cross.cross_ntrial))) ** 0.5 * 6
        sd6pv = 0
        if aovnon['MS'][0] - aovnon['MS'][2] > 0:
            sd6pv = 6 * ((aovnon['MS'][0] - aovnon['MS'][2]) / (int(cross.cross_nkaryawan) * int(cross.cross_ntrial))) ** 0.5
        sd6int = 0
        sd6int2 = 0
        sd6grr = (sd6ev ** 2 + sd6av ** 2 + sd6int ** 2) ** 0.5
        sd6tv = (sd6grr ** 2 + sd6pv ** 2) ** 0.5
        sd6 = [sd6grr, sd6ev, sd6av, sd6int, sd6int2, sd6pv, sd6tv]

        sd = []
        for i in range(7):
            sd.append(sd6[i] / 6)
        vc = []
        for i in range(7):
            vc.append(sd[i] ** 2)
        psv = []
        for i in range(7):
            psv.append(sd6[i] / sd6[6] * 100)
        pvc = []
        for i in range(7):
            pvc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sd6[i] / (int(cross.cross_stdevmax) - int(cross.cross_stdevmin)) * 100)
        pp = []
        if int(cross.cross_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sd6[i] / (6 * int(cross.cross_stdev)) * 100)

        resnon = [sd, vc, sd6, psv, pvc, pt, pp]
        resnon = np.array(resnon)
        resnon = resnon.T
        resnon = resnon.tolist()

        dfnon = pd.DataFrame(resnon, columns =['Stdev', 'Var Comp', '6 * Stdev', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfnon.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'INT', 'INT', 'PV', 'TV'])
        ndcnon = 1
        if 1.41 * pv / grr > 1:
            ndcnon = math.floor(1.41 * sd6pv / sd6grr)

        iter = 1
        temp = []
        r = []
        urut = []
        listulcr = []
        # for i in range(100):
        #   urut.append(i + 1)
        #   listulcr.append(ulcr)
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_ntrial) * int(cross.cross_npart)):
            temp.append(all[i][0])
            if iter % int(cross.cross_ntrial) == 0:
                r.append(max(temp) - min(temp))
                temp = []
            iter = iter + 1
        
        allt = []
        allplain = all.copy()
        allplain = []
        for ele in cross.cross_all:
            ele = np.array(ele)
            ele = ele.T
            ele = ele.tolist()
            allplain.append(ele)

        allplain = [x for l in allplain for x in l]
        allplain = [x for l in allplain for x in l]

        
        tempall = []
        temp = []
        iter = 1
        for i in range (int(cross.cross_nkaryawan) * int(cross.cross_ntrial) * int(cross.cross_npart)):
            temp.append(allplain[i])
            if iter % int(cross.cross_ntrial) == 0:
                tempall.append(temp)
                temp = []
            iter = iter + 1

        tempallt = np.array(tempall)
        tempallt = tempallt.T
        tempallt = tempallt.tolist()
        pertrial = []
        temp2 = []
        iter = 1
        a = 0
        b = int(cross.cross_npart)
        for h in range(int(cross.cross_nkaryawan)):
            for i in range(int(cross.cross_ntrial)):
                for j in range(a, b):
                    temp2.append(tempallt[i][j])
                pertrial.append(temp2)
                temp2 = []
            a = a + int(cross.cross_npart)
            b = b + int(cross.cross_npart)
        
        iter = 1
        tempave = []
        tempr = []
        avepart = []
        rpart = []
        avepart = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            tempr.append(max(list(map(float, tempall[i]))) - min(list(map(float, tempall[i]))))
            tempave.append(sum(list(map(float, tempall[i]))) / len(list(map(float, tempall[i]))))
            if iter % int(cross.cross_npart) == 0:
                rpart.append(tempr)
                avepart.append(tempave)
                tempr = []
                tempave = []
            iter = iter + 1
        
        avepartall = []
        temp = []
        for i in range(int(cross.cross_npart)):
            for ele in avepart:
                temp.append(ele[i])
            avepartall.append(sum(temp) / int(cross.cross_nkaryawan))
            temp = []
        xbar2 = sum(avepartall) / int(cross.cross_npart)
        rp = max(avepartall) - min(avepartall)

        xx = []
        rx = []

        for i in range(int(cross.cross_nkaryawan)):
            xx.append(sum(avepart[i]) / len(avepart[i]))
            rx.append(sum(rpart[i]) / len(rpart[i]))
        
        rbar = sum(rx) / int(cross.cross_nkaryawan)
        xdiff = max(xx) - min(xx)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]

        for i in range(4):
            if subgroup[i][0] == int(cross.cross_ntrial):
                d4 = subgroup[i][1]
            else:
                d4 = subgroup[3][1]

        ulcr = d4 * rbar
        lclr = 0

        for i in range(4):
            if subgroup[i][0] == int(cross.cross_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]

        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar
        
        rpartflat =  [x for l in rpart for x in l]
        ulcrflat = []
        lclrflat = []
        urutflat = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            ulcrflat.append(ulcr)
            lclrflat.append(lclr)
            urutflat.append(i+1)

        avepartflat =  [x for l in avepart for x in l]
        uclxflat = []
        lclxflat = []
        xbar2flat = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            uclxflat.append(uclx)
            lclxflat.append(lclx)
            xbar2flat.append(xbar2)
        
        urutpart = []
        urutallpart = []
        temp = []
        avepertrial = []
        iter = 1

        for i in range(int(cross.cross_npart)):
            urutpart.append(i+1)

        for i in range(int(cross.cross_ntrial) * int(cross.cross_nkaryawan)):
            urutallpart.append(urutpart)
            temp.append(sum(list(map(float, pertrial[i]))) / len(list(map(float, pertrial[i]))))
            if iter % int(cross.cross_ntrial) == 0:
                avepertrial.append(temp)
                temp = []
            iter = iter + 1
        
        iter = 1
        temp = []
        tempperkaryawan = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            temp.append(tempall[i])
            if iter % int(cross.cross_npart) == 0:
                tempperkaryawan.append(temp)
                temp = []
            iter = iter + 1

        temp = []
        perkaryawan = []
        for ele in tempperkaryawan:
            temp =  [x for l in ele for x in l]
            perkaryawan.append(temp)
            temp = []
        
        temp = []
        urutnama = []
        avekaryawan = []
        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_npart) * int(cross.cross_ntrial)):
                temp.append(i+1)
            urutnama.append(temp)
            temp = []

        for i in range(int(cross.cross_nkaryawan)):
            avekaryawan.append(sum(list(map(float, perkaryawan[i]))) / len(list(map(float, perkaryawan[i]))))
            temp.append(i+1)

        urutpart2 = []
        for i in range(int(cross.cross_nkaryawan)):
            urutpart2.append(urutpart)

        a, b, c, d, e, g = [*zip(*resinteraksi)]
        source = ['GRR', 'Repeatability', 'Reproducibility', 'Total Variation'] 
        psv = list(c)
        pc = list(d)
        del psv[3:6]
        del pc[3:6]
        psv = tuple(psv)
        pc = tuple(pc)

        if aov['P Value'][2] < 0.05:
            dfdisplay = dfinteraksi.copy()
            dfdisplay = dfdisplay.drop('Study Variation', 1)
            dfdisplay = dfdisplay.drop('Var Comp', 1)
            if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
                dfdisplay = dfdisplay.drop('% Process', 1)
            if int(cross.cross_stdev) == 0:
                dfdisplay = dfdisplay.drop('% Tolerance', 1)
            dfdisplay = dfdisplay.drop(3)
            dfdisplay = dfdisplay.drop(4)
            dfdisplay = dfdisplay.drop(6)
        elif aov['P Value'][2] >= 0.05:
            dfdisplay = dfnon.copy()
            dfdisplay = dfdisplay.drop('Stdev', 1)
            dfdisplay = dfdisplay.drop('Var Comp', 1)
            dfdisplay = dfdisplay.drop('6 * Stdev', 1)
            if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
                dfdisplay = dfdisplay.drop('% Process', 1)
            if int(cross.cross_stdev) == 0:
                dfdisplay = dfdisplay.drop('% Tolerance', 1)
            dfdisplay = dfdisplay.drop(3)
            dfdisplay = dfdisplay.drop(4)
            dfdisplay = dfdisplay.drop(6)    

        aov1 = aov.to_html(classes='table table-hover table-condensed mv-20', index=False)
        dfinteraksi2 = dfdisplay.to_html(classes='table table-hover table-condensed mv-20', index=False)

        ###########graf

        plt.figure()
        dfdisplay.plot(kind='bar', x='Source', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)
        
        ###################################
        plt.clf()
        rpart = plt.scatter(urutflat, rpartflat)
        ulcr = plt.scatter(urutflat, ulcrflat)
        lclr = plt.scatter(urutflat, lclrflat)
        plt.legend((rpart, ulcr, lclr), ('R', 'UCLRbar', 'LCLRbar'), bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)
        plt.title("Range vs Appraisal")
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        rva = urllib.parse.quote(string)

        ####################################
        
        plt.clf()
        plt.plot(urutflat, avepartflat, label='Xbar')
        plt.plot(urutflat, uclxflat, label='UCLxbar2')
        plt.plot(urutflat, lclxflat, label='LCLxbar2')
        plt.plot(urutflat, xbar2flat, label='Xbar2')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)
        plt.title("Xbar vs Appraisal")
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        xva = urllib.parse.quote(string)

        #####################################

        plt.clf()
        plt.scatter(urutallpart, pertrial)
        plt.plot(urutpart, avepartall, label='Average')
        plt.title('Data by Sample')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(cross.cross_nkaryawan))
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        dbs = urllib.parse.quote(string)

        #####################################

        plt.clf()
        plt.xticks(temp, cross.cross_karyawan)
        plt.scatter(urutnama, perkaryawan)
        plt.plot(temp, avekaryawan, label='Average')
        plt.title('Data by Appraiser')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(cross.cross_nkaryawan))
        plt.ylabel("Value")
        
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        dba = urllib.parse.quote(string)

        ######################################

        plt.clf()
        for i in range(int(cross.cross_nkaryawan)):
            plt.scatter(urutpart2[i], avepart[i])
            plt.plot(urutpart2[i], avepart[i], label=cross.cross_karyawan[i])
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(cross.cross_nkaryawan))
        plt.title("Average Data by Appraiser")
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        aabp = urllib.parse.quote(string)


        gabung = zip(cross.cross_karyawan, range(1, int(cross.cross_nkaryawan)+1))
        survey = Survey.objects.get(id = cross.cross_survey_id)

        return render(request,'cross/comment_cross.html', {'cross':cross, 'survey':survey, 'dfinteraksi': dfinteraksi2, 'gabung':gabung, 'aov':aov1, 'psvc':psvc, 'rva':rva, 'xva':xva, 'dbs':dbs, 'dba':dba, 'aabp':aabp})
    else:
        return redirect('/logout')

def storeCommentCross(request, pk):
    if 'user' in request.session:
        cross = Cross.objects.get(id = pk)
        
        cross.cross_recommendation = request.POST.getlist('cross_recommendation')
        cross.cross_psvc = request.POST.get('cross_psvc')
        cross.cross_rva = request.POST.get('cross_rva')
        cross.cross_dbs = request.POST.get('cross_dbs')
        cross.cross_dba = request.POST.get('cross_dba')
        cross.cross_aabp = request.POST.get('cross_aabp')
        cross.save()

        return redirect('coretoolcrud:viewFinalCross',cross.cross_survey_id )
    else:
        return redirect('/logout')

def viewFinalCross(request, pk):
    if 'user' in request.session:
        cross = Cross.objects.get(cross_survey_id = pk)
        survey = Survey.objects.get(id = cross.cross_survey_id)

        ##############################

        temp = []
        perpart = []
        for ele in cross.cross_all:
            temp =  [x for l in ele for x in l]
            perpart.append(temp)
            temp = []

        perpart = [x for l in perpart for x in l]

        all = []
        iter = 0
        temp = []

        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_ntrial)):
                for k in range(int(cross.cross_npart)):
                    p = k + 1
                    p = str(p)
                    t = j + 1
                    t = str(t)
                    temp.append(float(perpart[iter]))
                    temp.append("P"+p)
                    temp.append("T"+t)
                    temp.append(cross.cross_karyawan[i])
                    all.append(temp)
                    temp = []
                    iter = iter + 1
        
        df = pd.DataFrame(all, columns =['Uk', 'Part', 'Trial', 'Karyawan'])

        aov = pg.anova(dv='Uk', between=['Part', 'Karyawan'], data=df, detailed=True)
        aov.loc[0, 'F'] = aov['MS'][0] / aov['MS'][2]
        aov.loc[1, 'F'] = aov['MS'][1] / aov['MS'][2]

        aov.loc[0, 'p-unc'] = 1 - f.cdf(aov['F'][0], aov['DF'][0], aov['DF'][2])
        aov.loc[1, 'p-unc'] = 1 - f.cdf(aov['F'][1], aov['DF'][1], aov['DF'][2])
        aov.loc[2, 'p-unc'] = 1 - f.cdf(aov['F'][2], aov['DF'][2], aov['DF'][3])
        aov = aov.rename(columns={'p-unc': 'P Value'})
        aov = aov.rename(columns={'np2': 'Ket'})

        if aov['P Value'][0] >= 0.05:
            aov.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aov['P Value'][0] < 0.05:
            aov.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aov['P Value'][1] >= 0.05:
            aov.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aov['P Value'][1] < 0.05:
            aov.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        if aov['P Value'][2] >= 0.05:
            aov.loc[2, 'Ket'] = 'Not significant, interactions dont contribute variation'
        if aov['P Value'][2] < 0.05:
            aov.loc[2, 'Ket'] = 'Significant, interactions contribute variation'
        
        evrepeat = 6 * aov['MS'][3] ** 0.5
        av = 0
        if aov['MS'][1] - aov['MS'][2] > 0:
            av = (aov['MS'][1] - aov['MS'][2]) / (int(cross.cross_npart) * int(cross.cross_ntrial)) ** 0.5 * 6

        intt = (((aov['MS'][2] - aov['MS'][3]) / int(cross.cross_ntrial)) ** 0.5) * 6
        pv = 6 * ((aov['MS'][0] - aov['MS'][2]) / (int(cross.cross_nkaryawan) * int(cross.cross_ntrial))) ** 0.5
        grr = (evrepeat ** 2 + av ** 2 + intt ** 2) ** 0.5
        evrepro = (av ** 2 + intt ** 2) ** 0.5
        tv = (grr ** 2 + pv ** 2) ** 0.5
        ndc = 1
        
        if 1.41 * pv / grr > 1:
            ndc = math.floor(1.41 * pv / grr)

        sv = [grr, evrepeat, evrepro, av, intt, pv, tv]
        vc = []
        for i in range(7):
            vc.append((sv[i] / 6) ** 2)
        psv = []
        for i in range(7):
            psv.append(sv[i] / sv[6] * 100)
        pc = []
        for i in range(7):
            pc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sv[i] / (int(cross.cross_stdevmax) - int(cross.cross_stdevmin)) * 100)
        pp = []
        if int(cross.cross_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sv[i] / (6 * int(cross.cross_stdev)) * 100)
        resinteraksi = [sv, vc, psv, pc, pt, pp]
        resinteraksi = np.array(resinteraksi)
        resinteraksi = resinteraksi.T
        resinteraksi = resinteraksi.tolist()
        dfinteraksi = pd.DataFrame(resinteraksi, columns =['Study Variation', 'Var Comp', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfinteraksi.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'AV', 'INT', 'PV', 'TV'])
        
        aovnon = aov.copy()
        aovnon.loc[2, 'Source'] = 'Repeatability'
        aovnon.loc[3, 'Source'] = 'Total'
        aovnon.loc[2, 'DF'] = (int(cross.cross_npart) - 1) * (int(cross.cross_nkaryawan) - 1) + int(cross.cross_nkaryawan) * int(cross.cross_npart) * (int(cross.cross_ntrial) - 1)
        aovnon.loc[3, 'DF'] =  aovnon['DF'][0] +  aovnon['DF'][1] +  aovnon['DF'][2]
        aovnon.loc[2, 'SS'] = aovnon['SS'][2] + aovnon['SS'][3]
        aovnon.loc[2, 'SS'] = aov['SS'][2] + aov['SS'][3]
        aovnon.loc[3, 'SS'] =  aovnon['SS'][0] + aovnon['SS'][1] +  aovnon['SS'][2]
        aovnon.loc[2, 'MS'] =  aovnon['SS'][2] / aovnon['DF'][2]
        aovnon.loc[3, 'MS'] = "NaN"
        aovnon.loc[0, 'F'] =  aovnon['MS'][0] / aovnon['MS'][2]
        aovnon.loc[1, 'F'] =  aovnon['MS'][1] / aovnon['MS'][2]
        aovnon.loc[3, 'F'] = 0
        aovnon.loc[0, 'P Value'] = 1 - f.cdf(aovnon['F'][0], aovnon['DF'][0], aovnon['DF'][2])
        aovnon.loc[1, 'P Value'] = 1 - f.cdf(aovnon['F'][1], aovnon['DF'][1], aovnon['DF'][2])
        if aovnon['P Value'][0] >= 0.05:
            aovnon.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aovnon['P Value'][0] < 0.05:
            aovnon.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aovnon['P Value'][1] >= 0.05:
            aovnon.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aovnon['P Value'][1] < 0.05:
            aovnon.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        aovnon.loc[2, 'Ket'] = 0

        sd6ev =  6 * aovnon['MS'][2] ** 0.5
        sd6av = 0
        if aovnon['MS'][1] - aovnon['MS'][2] > 0:
            sd6av = ((aovnon['MS'][1] - aovnon['MS'][2]) / (int(cross.cross_npart) * int(cross.cross_ntrial))) ** 0.5 * 6
        sd6pv = 0
        if aovnon['MS'][0] - aovnon['MS'][2] > 0:
            sd6pv = 6 * ((aovnon['MS'][0] - aovnon['MS'][2]) / (int(cross.cross_nkaryawan) * int(cross.cross_ntrial))) ** 0.5
        sd6int = 0
        sd6int2 = 0
        sd6grr = (sd6ev ** 2 + sd6av ** 2 + sd6int ** 2) ** 0.5
        sd6tv = (sd6grr ** 2 + sd6pv ** 2) ** 0.5
        sd6 = [sd6grr, sd6ev, sd6av, sd6int, sd6int2, sd6pv, sd6tv]

        sd = []
        for i in range(7):
            sd.append(sd6[i] / 6)
        vc = []
        for i in range(7):
            vc.append(sd[i] ** 2)
        psv = []
        for i in range(7):
            psv.append(sd6[i] / sd6[6] * 100)
        pvc = []
        for i in range(7):
            pvc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sd6[i] / (int(cross.cross_stdevmax) - int(cross.cross_stdevmin)) * 100)
        pp = []
        if int(cross.cross_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sd6[i] / (6 * int(cross.cross_stdev)) * 100)

        resnon = [sd, vc, sd6, psv, pvc, pt, pp]
        resnon = np.array(resnon)
        resnon = resnon.T
        resnon = resnon.tolist()

        dfnon = pd.DataFrame(resnon, columns =['Stdev', 'Var Comp', '6 * Stdev', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfnon.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'INT', 'INT', 'PV', 'TV'])
        ndcnon = 1
        if 1.41 * pv / grr > 1:
            ndcnon = math.floor(1.41 * sd6pv / sd6grr)

        iter = 1
        temp = []
        r = []
        urut = []
        listulcr = []
        # for i in range(100):
        #   urut.append(i + 1)
        #   listulcr.append(ulcr)
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_ntrial) * int(cross.cross_npart)):
            temp.append(all[i][0])
            if iter % int(cross.cross_ntrial) == 0:
                r.append(max(temp) - min(temp))
                temp = []
            iter = iter + 1
        
        allt = []
        allplain = all.copy()
        allplain = []
        for ele in cross.cross_all:
            ele = np.array(ele)
            ele = ele.T
            ele = ele.tolist()
            allplain.append(ele)

        allplain = [x for l in allplain for x in l]
        allplain = [x for l in allplain for x in l]

        
        tempall = []
        temp = []
        iter = 1
        for i in range (int(cross.cross_nkaryawan) * int(cross.cross_ntrial) * int(cross.cross_npart)):
            temp.append(allplain[i])
            if iter % int(cross.cross_ntrial) == 0:
                tempall.append(temp)
                temp = []
            iter = iter + 1

        tempallt = np.array(tempall)
        tempallt = tempallt.T
        tempallt = tempallt.tolist()
        pertrial = []
        temp2 = []
        iter = 1
        a = 0
        b = int(cross.cross_npart)
        for h in range(int(cross.cross_nkaryawan)):
            for i in range(int(cross.cross_ntrial)):
                for j in range(a, b):
                    temp2.append(tempallt[i][j])
                pertrial.append(temp2)
                temp2 = []
            a = a + int(cross.cross_npart)
            b = b + int(cross.cross_npart)
        
        iter = 1
        tempave = []
        tempr = []
        avepart = []
        rpart = []
        avepart = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            tempr.append(max(list(map(float, tempall[i]))) - min(list(map(float, tempall[i]))))
            tempave.append(sum(list(map(float, tempall[i]))) / len(list(map(float, tempall[i]))))
            if iter % int(cross.cross_npart) == 0:
                rpart.append(tempr)
                avepart.append(tempave)
                tempr = []
                tempave = []
            iter = iter + 1
        
        avepartall = []
        temp = []
        for i in range(int(cross.cross_npart)):
            for ele in avepart:
                temp.append(ele[i])
            avepartall.append(sum(temp) / int(cross.cross_nkaryawan))
            temp = []
        xbar2 = sum(avepartall) / int(cross.cross_npart)
        rp = max(avepartall) - min(avepartall)

        xx = []
        rx = []

        for i in range(int(cross.cross_nkaryawan)):
            xx.append(sum(avepart[i]) / len(avepart[i]))
            rx.append(sum(rpart[i]) / len(rpart[i]))
        
        rbar = sum(rx) / int(cross.cross_nkaryawan)
        xdiff = max(xx) - min(xx)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]

        for i in range(4):
            if subgroup[i][0] == int(cross.cross_ntrial):
                d4 = subgroup[i][1]
            else:
                d4 = subgroup[3][1]

        ulcr = d4 * rbar
        lclr = 0

        for i in range(4):
            if subgroup[i][0] == int(cross.cross_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]

        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar
        
        rpartflat =  [x for l in rpart for x in l]
        ulcrflat = []
        lclrflat = []
        urutflat = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            ulcrflat.append(ulcr)
            lclrflat.append(lclr)
            urutflat.append(i+1)

        avepartflat =  [x for l in avepart for x in l]
        uclxflat = []
        lclxflat = []
        xbar2flat = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            uclxflat.append(uclx)
            lclxflat.append(lclx)
            xbar2flat.append(xbar2)
        
        urutpart = []
        urutallpart = []
        temp = []
        avepertrial = []
        iter = 1

        for i in range(int(cross.cross_npart)):
            urutpart.append(i+1)

        for i in range(int(cross.cross_ntrial) * int(cross.cross_nkaryawan)):
            urutallpart.append(urutpart)
            temp.append(sum(list(map(float, pertrial[i]))) / len(list(map(float, pertrial[i]))))
            if iter % int(cross.cross_ntrial) == 0:
                avepertrial.append(temp)
                temp = []
            iter = iter + 1
        
        iter = 1
        temp = []
        tempperkaryawan = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            temp.append(tempall[i])
            if iter % int(cross.cross_npart) == 0:
                tempperkaryawan.append(temp)
                temp = []
            iter = iter + 1

        temp = []
        perkaryawan = []
        for ele in tempperkaryawan:
            temp =  [x for l in ele for x in l]
            perkaryawan.append(temp)
            temp = []
        
        temp = []
        urutnama = []
        avekaryawan = []
        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_npart) * int(cross.cross_ntrial)):
                temp.append(cross.cross_karyawan[i])
            urutnama.append(temp)
            temp = []

        for i in range(int(cross.cross_nkaryawan)):
            avekaryawan.append(sum(list(map(float, perkaryawan[i]))) / len(list(map(float, perkaryawan[i]))))
            temp.append(i+1)

        urutpart2 = []
        for i in range(int(cross.cross_nkaryawan)):
            urutpart2.append(urutpart)

        a, b, c, d, e, g = [*zip(*resinteraksi)]
        source = ['GRR', 'Repeatability', 'Reproducibility', 'Total Variation'] 
        psv = list(c)
        pc = list(d)
        del psv[3:6]
        del pc[3:6]
        psv = tuple(psv)
        pc = tuple(pc)

        if aov['P Value'][2] < 0.05:
            dfdisplay = dfinteraksi.copy()
            dfdisplay = dfdisplay.drop('Study Variation', 1)
            dfdisplay = dfdisplay.drop('Var Comp', 1)
            if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
                dfdisplay = dfdisplay.drop('% Process', 1)
            if int(cross.cross_stdev) == 0:
                dfdisplay = dfdisplay.drop('% Tolerance', 1)
            dfdisplay = dfdisplay.drop(3)
            dfdisplay = dfdisplay.drop(4)
            dfdisplay = dfdisplay.drop(6)
        elif aov['P Value'][2] >= 0.05:
            dfdisplay = dfnon.copy()
            dfdisplay = dfdisplay.drop('Stdev', 1)
            dfdisplay = dfdisplay.drop('Var Comp', 1)
            dfdisplay = dfdisplay.drop('6 * Stdev', 1)
            if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
                dfdisplay = dfdisplay.drop('% Process', 1)
            if int(cross.cross_stdev) == 0:
                dfdisplay = dfdisplay.drop('% Tolerance', 1)
            dfdisplay = dfdisplay.drop(3)
            dfdisplay = dfdisplay.drop(4)
            dfdisplay = dfdisplay.drop(6)    

        aov1 = aov.to_html(classes='table table-hover table-bordered results', index=False)
        dfinteraksi2 = dfdisplay.to_html(classes='table table-hover table-bordered results', index=False)

        ###########graf

        plt.figure()
        dfdisplay.plot(kind='bar', x='Source', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)

        
        ###################################

        bot = []

        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_npart)):
                bot.append(cross.cross_karyawan[i] + "-" + str(j+1))

        p = figure(title="Range vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.scatter(bot, rpartflat, legend_label="R", marker="circle")
        p.scatter(bot, ulcrflat, color="green", legend_label="UCLRbar", marker="circle")
        p.scatter(bot, lclrflat, color="red", legend_label="LCLRbar", marker="circle")
        p.xaxis.major_label_orientation = "vertical"
        scriptrva, divrva = components(p)

        ####################################

        p = figure(title="Xbar vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.line(bot, avepartflat, legend_label="Xbar", line_width=2)
        p.line(bot, uclxflat, legend_label="UCLXbar2", color="green", line_width=2)
        p.line(bot, lclxflat, legend_label="LCLXbar2", color="red", line_width=2)
        p.line(bot, xbar2flat, legend_label="Xbar2", color="black", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptxva, divxva = components(p)

        #####################################

        p = figure(title="Data by Sample", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(len(urutallpart)):
            p.scatter(urutallpart[i], pertrial[i], marker="circle")
        
        p.line(urutpart, avepartall, legend_label="Average", line_width=2)
        scriptdbs, divdbs = components(p)

        #####################################

        p = figure(title="Data by Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=cross.cross_karyawan, y_axis_label='Measurement', x_axis_label='Appraiser')
        for i in range(len(urutnama)):
            p.scatter(urutnama[i], perkaryawan[i], marker="circle")
        
        p.line(cross.cross_karyawan, avekaryawan, legend_label="Average", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptdba, divdba = components(p)

        ######################################


        colors = []

        p = figure(title="Average Data by Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(int(cross.cross_nkaryawan)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutpart2[i], avepart[i], marker="circle")
            p.line(urutpart2[i], avepart[i], color=colors[i], legend_label=cross.cross_karyawan[i], line_width=2)
        
        scriptaabp, divaabp = components(p)


        gabung = zip(cross.cross_all, cross.cross_karyawan)
        gabung2 = zip(cross.cross_karyawan, range(1, int(cross.cross_nkaryawan)+1))
        part1 = range(1, int(cross.cross_npart)+1)
        survey = Survey.objects.get(id = cross.cross_survey_id)
        gabungave = zip(cross.cross_karyawan, avepart)
        gabungr = zip(cross.cross_karyawan, rpart)

        return render(request,'cross/collection_cross.html', {'cross':cross, 'survey':survey, 'ndc':ndc, 'dfinteraksi': dfinteraksi2, 'aov':aov1, 'part1':part1, 'gabung':gabung, 'gabung2':gabung2, 'gabungave':gabungave, 'gabungr':gabungr, 'psvc':psvc, 'scriptrva':scriptrva, 'divrva':divrva, 'scriptxva':scriptxva, 'divxva':divxva, 'scriptdbs':scriptdbs, 'divdbs':divdbs, 'scriptdba':scriptdba, 'divdba':divdba, 'scriptaabp':scriptaabp, 'divaabp':divaabp})
    else:
        return redirect('/logout')

def viewPrintCross(request, pk):
    if 'user' in request.session:
        cross = Cross.objects.get(cross_survey_id = pk)
        survey = Survey.objects.get(id = cross.cross_survey_id)

        ##############################

        temp = []
        perpart = []
        for ele in cross.cross_all:
            temp =  [x for l in ele for x in l]
            perpart.append(temp)
            temp = []

        perpart = [x for l in perpart for x in l]

        all = []
        iter = 0
        temp = []

        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_ntrial)):
                for k in range(int(cross.cross_npart)):
                    p = k + 1
                    p = str(p)
                    t = j + 1
                    t = str(t)
                    temp.append(float(perpart[iter]))
                    temp.append("P"+p)
                    temp.append("T"+t)
                    temp.append(cross.cross_karyawan[i])
                    all.append(temp)
                    temp = []
                    iter = iter + 1
        
        df = pd.DataFrame(all, columns =['Uk', 'Part', 'Trial', 'Karyawan'])

        aov = pg.anova(dv='Uk', between=['Part', 'Karyawan'], data=df, detailed=True)
        aov.loc[0, 'F'] = aov['MS'][0] / aov['MS'][2]
        aov.loc[1, 'F'] = aov['MS'][1] / aov['MS'][2]

        aov.loc[0, 'p-unc'] = 1 - f.cdf(aov['F'][0], aov['DF'][0], aov['DF'][2])
        aov.loc[1, 'p-unc'] = 1 - f.cdf(aov['F'][1], aov['DF'][1], aov['DF'][2])
        aov.loc[2, 'p-unc'] = 1 - f.cdf(aov['F'][2], aov['DF'][2], aov['DF'][3])
        aov = aov.rename(columns={'p-unc': 'P Value'})
        aov = aov.rename(columns={'np2': 'Ket'})

        if aov['P Value'][0] >= 0.05:
            aov.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aov['P Value'][0] < 0.05:
            aov.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aov['P Value'][1] >= 0.05:
            aov.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aov['P Value'][1] < 0.05:
            aov.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        if aov['P Value'][2] >= 0.05:
            aov.loc[2, 'Ket'] = 'Not significant, interactions dont contribute variation'
        if aov['P Value'][2] < 0.05:
            aov.loc[2, 'Ket'] = 'Significant, interactions contribute variation'
        
        evrepeat = 6 * aov['MS'][3] ** 0.5
        av = 0
        if aov['MS'][1] - aov['MS'][2] > 0:
            av = (aov['MS'][1] - aov['MS'][2]) / (int(cross.cross_npart) * int(cross.cross_ntrial)) ** 0.5 * 6

        intt = (((aov['MS'][2] - aov['MS'][3]) / int(cross.cross_ntrial)) ** 0.5) * 6
        pv = 6 * ((aov['MS'][0] - aov['MS'][2]) / (int(cross.cross_nkaryawan) * int(cross.cross_ntrial))) ** 0.5
        grr = (evrepeat ** 2 + av ** 2 + intt ** 2) ** 0.5
        evrepro = (av ** 2 + intt ** 2) ** 0.5
        tv = (grr ** 2 + pv ** 2) ** 0.5
        ndc = 1
        
        if 1.41 * pv / grr > 1:
            ndc = math.floor(1.41 * pv / grr)

        sv = [grr, evrepeat, evrepro, av, intt, pv, tv]
        vc = []
        for i in range(7):
            vc.append((sv[i] / 6) ** 2)
        psv = []
        for i in range(7):
            psv.append(sv[i] / sv[6] * 100)
        pc = []
        for i in range(7):
            pc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sv[i] / (int(cross.cross_stdevmax) - int(cross.cross_stdevmin)) * 100)
        pp = []
        if int(cross.cross_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sv[i] / (6 * int(cross.cross_stdev)) * 100)
        resinteraksi = [sv, vc, psv, pc, pt, pp]
        resinteraksi = np.array(resinteraksi)
        resinteraksi = resinteraksi.T
        resinteraksi = resinteraksi.tolist()
        dfinteraksi = pd.DataFrame(resinteraksi, columns =['Study Variation', 'Var Comp', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfinteraksi.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'AV', 'INT', 'PV', 'TV'])
        
        aovnon = aov.copy()
        aovnon.loc[2, 'Source'] = 'Repeatability'
        aovnon.loc[3, 'Source'] = 'Total'
        aovnon.loc[2, 'DF'] = (int(cross.cross_npart) - 1) * (int(cross.cross_nkaryawan) - 1) + int(cross.cross_nkaryawan) * int(cross.cross_npart) * (int(cross.cross_ntrial) - 1)
        aovnon.loc[3, 'DF'] =  aovnon['DF'][0] +  aovnon['DF'][1] +  aovnon['DF'][2]
        aovnon.loc[2, 'SS'] = aovnon['SS'][2] + aovnon['SS'][3]
        aovnon.loc[2, 'SS'] = aov['SS'][2] + aov['SS'][3]
        aovnon.loc[3, 'SS'] =  aovnon['SS'][0] + aovnon['SS'][1] +  aovnon['SS'][2]
        aovnon.loc[2, 'MS'] =  aovnon['SS'][2] / aovnon['DF'][2]
        aovnon.loc[3, 'MS'] = "NaN"
        aovnon.loc[0, 'F'] =  aovnon['MS'][0] / aovnon['MS'][2]
        aovnon.loc[1, 'F'] =  aovnon['MS'][1] / aovnon['MS'][2]
        aovnon.loc[3, 'F'] = 0
        aovnon.loc[0, 'P Value'] = 1 - f.cdf(aovnon['F'][0], aovnon['DF'][0], aovnon['DF'][2])
        aovnon.loc[1, 'P Value'] = 1 - f.cdf(aovnon['F'][1], aovnon['DF'][1], aovnon['DF'][2])
        if aovnon['P Value'][0] >= 0.05:
            aovnon.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aovnon['P Value'][0] < 0.05:
            aovnon.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aovnon['P Value'][1] >= 0.05:
            aovnon.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aovnon['P Value'][1] < 0.05:
            aovnon.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        aovnon.loc[2, 'Ket'] = 0

        sd6ev =  6 * aovnon['MS'][2] ** 0.5
        sd6av = 0
        if aovnon['MS'][1] - aovnon['MS'][2] > 0:
            sd6av = ((aovnon['MS'][1] - aovnon['MS'][2]) / (int(cross.cross_npart) * int(cross.cross_ntrial))) ** 0.5 * 6
        sd6pv = 0
        if aovnon['MS'][0] - aovnon['MS'][2] > 0:
            sd6pv = 6 * ((aovnon['MS'][0] - aovnon['MS'][2]) / (int(cross.cross_nkaryawan) * int(cross.cross_ntrial))) ** 0.5
        sd6int = 0
        sd6int2 = 0
        sd6grr = (sd6ev ** 2 + sd6av ** 2 + sd6int ** 2) ** 0.5
        sd6tv = (sd6grr ** 2 + sd6pv ** 2) ** 0.5
        sd6 = [sd6grr, sd6ev, sd6av, sd6int, sd6int2, sd6pv, sd6tv]

        sd = []
        for i in range(7):
            sd.append(sd6[i] / 6)
        vc = []
        for i in range(7):
            vc.append(sd[i] ** 2)
        psv = []
        for i in range(7):
            psv.append(sd6[i] / sd6[6] * 100)
        pvc = []
        for i in range(7):
            pvc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sd6[i] / (int(cross.cross_stdevmax) - int(cross.cross_stdevmin)) * 100)
        pp = []
        if int(cross.cross_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sd6[i] / (6 * int(cross.cross_stdev)) * 100)

        resnon = [sd, vc, sd6, psv, pvc, pt, pp]
        resnon = np.array(resnon)
        resnon = resnon.T
        resnon = resnon.tolist()

        dfnon = pd.DataFrame(resnon, columns =['Stdev', 'Var Comp', '6 * Stdev', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfnon.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'INT', 'INT', 'PV', 'TV'])
        ndcnon = 1
        if 1.41 * pv / grr > 1:
            ndcnon = math.floor(1.41 * sd6pv / sd6grr)

        iter = 1
        temp = []
        r = []
        urut = []
        listulcr = []
        # for i in range(100):
        #   urut.append(i + 1)
        #   listulcr.append(ulcr)
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_ntrial) * int(cross.cross_npart)):
            temp.append(all[i][0])
            if iter % int(cross.cross_ntrial) == 0:
                r.append(max(temp) - min(temp))
                temp = []
            iter = iter + 1
        
        allt = []
        allplain = all.copy()
        allplain = []
        for ele in cross.cross_all:
            ele = np.array(ele)
            ele = ele.T
            ele = ele.tolist()
            allplain.append(ele)

        allplain = [x for l in allplain for x in l]
        allplain = [x for l in allplain for x in l]

        
        tempall = []
        temp = []
        iter = 1
        for i in range (int(cross.cross_nkaryawan) * int(cross.cross_ntrial) * int(cross.cross_npart)):
            temp.append(allplain[i])
            if iter % int(cross.cross_ntrial) == 0:
                tempall.append(temp)
                temp = []
            iter = iter + 1

        tempallt = np.array(tempall)
        tempallt = tempallt.T
        tempallt = tempallt.tolist()
        pertrial = []
        temp2 = []
        iter = 1
        a = 0
        b = int(cross.cross_npart)
        for h in range(int(cross.cross_nkaryawan)):
            for i in range(int(cross.cross_ntrial)):
                for j in range(a, b):
                    temp2.append(tempallt[i][j])
                pertrial.append(temp2)
                temp2 = []
            a = a + int(cross.cross_npart)
            b = b + int(cross.cross_npart)
        
        iter = 1
        tempave = []
        tempr = []
        avepart = []
        rpart = []
        avepart = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            tempr.append(max(list(map(float, tempall[i]))) - min(list(map(float, tempall[i]))))
            tempave.append(sum(list(map(float, tempall[i]))) / len(list(map(float, tempall[i]))))
            if iter % int(cross.cross_npart) == 0:
                rpart.append(tempr)
                avepart.append(tempave)
                tempr = []
                tempave = []
            iter = iter + 1
        
        avepartall = []
        temp = []
        for i in range(int(cross.cross_npart)):
            for ele in avepart:
                temp.append(ele[i])
            avepartall.append(sum(temp) / int(cross.cross_nkaryawan))
            temp = []
        xbar2 = sum(avepartall) / int(cross.cross_npart)
        rp = max(avepartall) - min(avepartall)

        xx = []
        rx = []

        for i in range(int(cross.cross_nkaryawan)):
            xx.append(sum(avepart[i]) / len(avepart[i]))
            rx.append(sum(rpart[i]) / len(rpart[i]))
        
        rbar = sum(rx) / int(cross.cross_nkaryawan)
        xdiff = max(xx) - min(xx)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]

        for i in range(4):
            if subgroup[i][0] == int(cross.cross_ntrial):
                d4 = subgroup[i][1]
            else:
                d4 = subgroup[3][1]

        ulcr = d4 * rbar
        lclr = 0

        for i in range(4):
            if subgroup[i][0] == int(cross.cross_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]

        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar
        
        rpartflat =  [x for l in rpart for x in l]
        ulcrflat = []
        lclrflat = []
        urutflat = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            ulcrflat.append(ulcr)
            lclrflat.append(lclr)
            urutflat.append(i+1)

        avepartflat =  [x for l in avepart for x in l]
        uclxflat = []
        lclxflat = []
        xbar2flat = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            uclxflat.append(uclx)
            lclxflat.append(lclx)
            xbar2flat.append(xbar2)
        
        urutpart = []
        urutallpart = []
        temp = []
        avepertrial = []
        iter = 1

        for i in range(int(cross.cross_npart)):
            urutpart.append(i+1)

        for i in range(int(cross.cross_ntrial) * int(cross.cross_nkaryawan)):
            urutallpart.append(urutpart)
            temp.append(sum(list(map(float, pertrial[i]))) / len(list(map(float, pertrial[i]))))
            if iter % int(cross.cross_ntrial) == 0:
                avepertrial.append(temp)
                temp = []
            iter = iter + 1
        
        iter = 1
        temp = []
        tempperkaryawan = []
        for i in range(int(cross.cross_nkaryawan) * int(cross.cross_npart)):
            temp.append(tempall[i])
            if iter % int(cross.cross_npart) == 0:
                tempperkaryawan.append(temp)
                temp = []
            iter = iter + 1

        temp = []
        perkaryawan = []
        for ele in tempperkaryawan:
            temp =  [x for l in ele for x in l]
            perkaryawan.append(temp)
            temp = []
        
        temp = []
        urutnama = []
        avekaryawan = []
        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_npart) * int(cross.cross_ntrial)):
                temp.append(cross.cross_karyawan[i])
            urutnama.append(temp)
            temp = []

        for i in range(int(cross.cross_nkaryawan)):
            avekaryawan.append(sum(list(map(float, perkaryawan[i]))) / len(list(map(float, perkaryawan[i]))))
            temp.append(i+1)

        urutpart2 = []
        for i in range(int(cross.cross_nkaryawan)):
            urutpart2.append(urutpart)

        a, b, c, d, e, g = [*zip(*resinteraksi)]
        source = ['GRR', 'Repeatability', 'Reproducibility', 'Total Variation'] 
        psv = list(c)
        pc = list(d)
        del psv[3:6]
        del pc[3:6]
        psv = tuple(psv)
        pc = tuple(pc)

        if aov['P Value'][2] < 0.05:
            dfdisplay = dfinteraksi.copy()
            dfdisplay = dfdisplay.drop('Study Variation', 1)
            dfdisplay = dfdisplay.drop('Var Comp', 1)
            if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
                dfdisplay = dfdisplay.drop('% Process', 1)
            if int(cross.cross_stdev) == 0:
                dfdisplay = dfdisplay.drop('% Tolerance', 1)
            dfdisplay = dfdisplay.drop(3)
            dfdisplay = dfdisplay.drop(4)
            dfdisplay = dfdisplay.drop(6)
        elif aov['P Value'][2] >= 0.05:
            dfdisplay = dfnon.copy()
            dfdisplay = dfdisplay.drop('Stdev', 1)
            dfdisplay = dfdisplay.drop('Var Comp', 1)
            dfdisplay = dfdisplay.drop('6 * Stdev', 1)
            if int(cross.cross_stdevmax) == 0 and int(cross.cross_stdevmin) == 0:
                dfdisplay = dfdisplay.drop('% Process', 1)
            if int(cross.cross_stdev) == 0:
                dfdisplay = dfdisplay.drop('% Tolerance', 1)
            dfdisplay = dfdisplay.drop(3)
            dfdisplay = dfdisplay.drop(4)
            dfdisplay = dfdisplay.drop(6)    

        aov1 = aov.to_html(classes='table table-hover table-bordered results', index=False)
        dfinteraksi2 = dfdisplay.to_html(classes='table table-hover table-bordered results', index=False)

        ###########graf

        plt.figure()
        dfdisplay.plot(kind='bar', x='Source', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)

        
        ###################################

        bot = []

        for i in range(int(cross.cross_nkaryawan)):
            for j in range(int(cross.cross_npart)):
                bot.append(cross.cross_karyawan[i] + "-" + str(j+1))

        p = figure(title="Range vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.scatter(bot, rpartflat, legend_label="R", marker="circle")
        p.scatter(bot, ulcrflat, color="green", legend_label="UCLRbar", marker="circle")
        p.scatter(bot, lclrflat, color="red", legend_label="LCLRbar", marker="circle")
        p.xaxis.major_label_orientation = "vertical"
        scriptrva, divrva = components(p)

        ####################################

        p = figure(title="Xbar vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.line(bot, avepartflat, legend_label="Xbar", line_width=2)
        p.line(bot, uclxflat, legend_label="UCLXbar2", color="green", line_width=2)
        p.line(bot, lclxflat, legend_label="LCLXbar2", color="red", line_width=2)
        p.line(bot, xbar2flat, legend_label="Xbar2", color="black", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptxva, divxva = components(p)

        #####################################

        p = figure(title="Data by Sample", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(len(urutallpart)):
            p.scatter(urutallpart[i], pertrial[i], marker="circle")
        
        p.line(urutpart, avepartall, legend_label="Average", line_width=2)
        scriptdbs, divdbs = components(p)

        #####################################

        p = figure(title="Data by Appraiser", sizing_mode="stretch_width", x_range=cross.cross_karyawan, y_axis_label='Measurement', x_axis_label='Appraiser')
        for i in range(len(urutnama)):
            p.scatter(urutnama[i], perkaryawan[i], marker="circle")
        
        p.line(cross.cross_karyawan, avekaryawan, legend_label="Average", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptdba, divdba = components(p)

        ######################################


        colors = []

        p = figure(title="Average Data by Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(int(cross.cross_nkaryawan)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutpart2[i], avepart[i], marker="circle")
            p.line(urutpart2[i], avepart[i], color=colors[i], legend_label=cross.cross_karyawan[i], line_width=2)
        
        scriptaabp, divaabp = components(p)


        gabung = zip(cross.cross_all, cross.cross_karyawan)
        gabung2 = zip(cross.cross_karyawan, range(1, int(cross.cross_nkaryawan)+1))
        part1 = range(1, int(cross.cross_npart)+1)
        survey = Survey.objects.get(id = cross.cross_survey_id)
        gabungave = zip(cross.cross_karyawan, avepart)
        gabungr = zip(cross.cross_karyawan, rpart)

        return render(request,'cross/print_cross.html', {'cross':cross, 'survey':survey, 'ndc':ndc, 'dfinteraksi': dfinteraksi2, 'aov':aov1, 'part1':part1, 'gabung':gabung, 'gabung2':gabung2, 'gabungave':gabungave, 'gabungr':gabungr, 'psvc':psvc, 'scriptrva':scriptrva, 'divrva':divrva, 'scriptxva':scriptxva, 'divxva':divxva, 'scriptdbs':scriptdbs, 'divdbs':divdbs, 'scriptdba':scriptdba, 'divdba':divdba, 'scriptaabp':scriptaabp, 'divaabp':divaabp})
    else:
        return redirect('/logout')

def deleteCross(request, pk):
    if 'user' in request.session:
        cross = Cross.objects.get(cross_survey_id = pk)
        cross.delete()
        messages.success(request, "GRR Cross berhasil dihapus")
        return redirect('coretoolcrud:viewDetailSurvey', pk)
    else:
        return redirect('/logout')

# GRR Nested

def viewNested(request, pk):
    if 'user' in request.session:
        try:
            nested = Nested.objects.get(nested_survey_id = pk)
            if nested.nested_all:
                return redirect('coretoolcrud:viewFinalNested',pk )
            else:
                namas = nested.nested_karyawan
                part = range(1, int(nested.nested_npart)+1)
                karyawan = range(int(nested.nested_nkaryawan))
                trial = range(int(nested.nested_ntrial))
                return render(request,'nested/all_nested.html',{'part':part, 'karyawan':karyawan, 'trial':trial, 'namas':namas, 'nested':nested})
        except Nested.DoesNotExist:
            return render(request,'nested/nested.html',{'pk':pk})
    else:
        return redirect('/logout')

def storeNested(request, pk):
    if 'user' in request.session:
        try:
            nested = Nested.objects.get(nested_survey_id = pk)
            nested.delete()
        except Nested.DoesNotExist:
            pass
            
        nested = Nested()
        nested.nested_survey_id = pk
        nested.nested_nkaryawan = request.POST.get('nested_nkaryawan')
        nested.nested_npart = request.POST.get('nested_npart')
        nested.nested_ntrial = request.POST.get('nested_ntrial')
        nested.nested_stdev = request.POST.get('nested_stdev')
        nested.nested_stdevmax = request.POST.get('nested_stdevmax')
        nested.nested_stdevmin = request.POST.get('nested_stdevmin')
        nested.nested_karyawan = request.POST.getlist('nested_karyawan')
        
        nested.save()
        # karyawan = range(int(cross.cross_nkaryawan))
        # return render(request,'cross/karyawan_cross.html',{'karyawan':karyawan})

        namas = nested.nested_karyawan
        part = range(1, int(nested.nested_npart)+1)
        karyawan = range(int(nested.nested_nkaryawan))
        trial = range(int(nested.nested_ntrial))
        return render(request,'nested/all_nested.html',{'part':part, 'karyawan':karyawan, 'trial':trial, 'namas':namas, 'nested':nested})
    else:
        return redirect('/logout')

def storeAllNested(request, pk):
    if 'user' in request.session:
        nested = Nested.objects.get(nested_survey_id = pk)
        temppart = []
        temptrial = []
        tempkaryawan = []
        iter = 1

        nested.nested_all = request.POST.getlist('nested_all')
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart) * int(nested.nested_ntrial)):
            if iter % int(nested.nested_npart) != 0:
                temppart.append(nested.nested_all[i])
                iter = iter + 1
            else:
                if iter % (int(nested.nested_npart) * int(nested.nested_ntrial)) == 0:
                    temppart.append(nested.nested_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    tempkaryawan.append(temptrial)
                    temptrial = []
                    temppart = []
                    iter = iter + 1
                else:
                    temppart.append(nested.nested_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    temppart = []
                    iter = iter + 1
        
        nested.nested_all = tempkaryawan
        nested.save()
        return redirect('coretoolcrud:viewCommentNested', pk)
    else:
        return redirect('/logout')

def viewCommentNested(request, pk):
    if 'user' in request.session:
        nested = Nested.objects.get(nested_survey_id = pk)
        ###############

        temp = []
        perpart = []
        for ele in nested.nested_all:
            temp =  [x for l in ele for x in l]
            perpart.append(temp)
            temp = []

        perpart = [x for l in perpart for x in l]

        all = []
        iter = 0
        temp = []

        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_ntrial)):
                for k in range(int(nested.nested_npart)):
                    p = k + 1
                    p = str(p)
                    t = j + 1
                    t = str(t)
                    temp.append(float(perpart[iter]))
                    temp.append("P"+p)
                    temp.append("T"+t)
                    temp.append(nested.nested_karyawan[i])
                    all.append(temp)
                    temp = []
                    iter = iter + 1
        
        df = pd.DataFrame(all, columns =['Uk', 'Part', 'Trial', 'Karyawan'])

        aov = pg.anova(dv='Uk', between=['Part', 'Karyawan'], data=df, detailed=True)
        aov.loc[0, 'F'] = aov['MS'][0] / aov['MS'][2]
        aov.loc[1, 'F'] = aov['MS'][1] / aov['MS'][2]

        aov.loc[0, 'p-unc'] = 1 - f.cdf(aov['F'][0], aov['DF'][0], aov['DF'][2])
        aov.loc[1, 'p-unc'] = 1 - f.cdf(aov['F'][1], aov['DF'][1], aov['DF'][2])
        aov.loc[2, 'p-unc'] = 1 - f.cdf(aov['F'][2], aov['DF'][2], aov['DF'][3])
        aov = aov.rename(columns={'p-unc': 'P Value'})
        aov = aov.rename(columns={'np2': 'Ket'})

        if aov['P Value'][0] >= 0.05:
            aov.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aov['P Value'][0] < 0.05:
            aov.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aov['P Value'][1] >= 0.05:
            aov.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aov['P Value'][1] < 0.05:
            aov.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        if aov['P Value'][2] >= 0.05:
            aov.loc[2, 'Ket'] = 'Not significant, interactions dont contribute variation'
        if aov['P Value'][2] < 0.05:
            aov.loc[2, 'Ket'] = 'Significant, interactions contribute variation'
        
        evrepeat = 6 * aov['MS'][3] ** 0.5
        av = 0
        if aov['MS'][1] - aov['MS'][2] > 0:
            av = (aov['MS'][1] - aov['MS'][2]) / (int(nested.nested_npart) * int(nested.nested_ntrial)) ** 0.5 * 6

        intt = (((aov['MS'][2] - aov['MS'][3]) / int(nested.nested_ntrial)) ** 0.5) * 6
        pv = 6 * ((aov['MS'][0] - aov['MS'][2]) / (int(nested.nested_nkaryawan) * int(nested.nested_ntrial))) ** 0.5
        grr = (evrepeat ** 2 + av ** 2 + intt ** 2) ** 0.5
        evrepro = (av ** 2 + intt ** 2) ** 0.5
        tv = (grr ** 2 + pv ** 2) ** 0.5
        ndc = 1
        
        if 1.41 * pv / grr > 1:
            ndc = math.floor(1.41 * pv / grr)

        sv = [grr, evrepeat, evrepro, av, intt, pv, tv]
        vc = []
        for i in range(7):
            vc.append((sv[i] / 6) ** 2)
        psv = []
        for i in range(7):
            psv.append(sv[i] / sv[6] * 100)
        pc = []
        for i in range(7):
            pc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sv[i] / (int(nested.nested_stdevmax) - int(nested.nested_stdevmin)) * 100)
        pp = []
        if int(nested.nested_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sv[i] / (6 * int(nested.nested_stdev)) * 100)
        resinteraksi = [sv, vc, psv, pc, pt, pp]
        resinteraksi = np.array(resinteraksi)
        resinteraksi = resinteraksi.T
        resinteraksi = resinteraksi.tolist()
        dfinteraksi = pd.DataFrame(resinteraksi, columns =['Study Variation', 'Var Comp', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfinteraksi.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'AV', 'INT', 'Part To Part', 'Total Variation'])
        
        aovnon = aov.copy()
        aovnon.loc[2, 'Source'] = 'Repeatability'
        aovnon.loc[3, 'Source'] = 'Total'
        aovnon.loc[2, 'DF'] = (int(nested.nested_npart) - 1) * (int(nested.nested_nkaryawan) - 1) + int(nested.nested_nkaryawan) * int(nested.nested_npart) * (int(nested.nested_ntrial) - 1)
        aovnon.loc[3, 'DF'] =  aovnon['DF'][0] +  aovnon['DF'][1] +  aovnon['DF'][2]
        aovnon.loc[2, 'SS'] = aovnon['SS'][2] + aovnon['SS'][3]
        aovnon.loc[2, 'SS'] = aov['SS'][2] + aov['SS'][3]
        aovnon.loc[3, 'SS'] =  aovnon['SS'][0] + aovnon['SS'][1] +  aovnon['SS'][2]
        aovnon.loc[2, 'MS'] =  aovnon['SS'][2] / aovnon['DF'][2]
        aovnon.loc[3, 'MS'] = "NaN"
        aovnon.loc[0, 'F'] =  aovnon['MS'][0] / aovnon['MS'][2]
        aovnon.loc[1, 'F'] =  aovnon['MS'][1] / aovnon['MS'][2]
        aovnon.loc[3, 'F'] = 0
        aovnon.loc[0, 'P Value'] = 1 - f.cdf(aovnon['F'][0], aovnon['DF'][0], aovnon['DF'][2])
        aovnon.loc[1, 'P Value'] = 1 - f.cdf(aovnon['F'][1], aovnon['DF'][1], aovnon['DF'][2])
        if aovnon['P Value'][0] >= 0.05:
            aovnon.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aovnon['P Value'][0] < 0.05:
            aovnon.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aovnon['P Value'][1] >= 0.05:
            aovnon.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aovnon['P Value'][1] < 0.05:
            aovnon.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        aovnon.loc[2, 'Ket'] = 0

        sd6ev =  6 * aovnon['MS'][2] ** 0.5
        sd6av = 0
        if aovnon['MS'][1] - aovnon['MS'][2] > 0:
            sd6av = ((aovnon['MS'][1] - aovnon['MS'][2]) / (int(nested.nested_npart) * int(nested.nested_ntrial))) ** 0.5 * 6
        sd6pv = 0
        if aovnon['MS'][0] - aovnon['MS'][2] > 0:
            sd6pv = 6 * ((aovnon['MS'][0] - aovnon['MS'][2]) / (int(nested.nested_nkaryawan) * int(nested.nested_ntrial))) ** 0.5
        sd6int = 0
        sd6int2 = 0
        sd6grr = (sd6ev ** 2 + sd6av ** 2 + sd6int ** 2) ** 0.5
        sd6tv = (sd6grr ** 2 + sd6pv ** 2) ** 0.5
        sd6 = [sd6grr, sd6ev, sd6av, sd6int, sd6int2, sd6pv, sd6tv]

        sd = []
        for i in range(7):
            sd.append(sd6[i] / 6)
        vc = []
        for i in range(7):
            vc.append(sd[i] ** 2)
        psv = []
        for i in range(7):
            psv.append(sd6[i] / sd6[6] * 100)
        pvc = []
        for i in range(7):
            pvc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sd6[i] / (int(nested.nested_stdevmax) - int(nested.nested_stdevmin)) * 100)
        pp = []
        if int(nested.nested_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sd6[i] / (6 * int(nested.nested_stdev)) * 100)

        resnon = [sd, vc, sd6, psv, pvc, pt, pp]
        resnon = np.array(resnon)
        resnon = resnon.T
        resnon = resnon.tolist()

        dfnon = pd.DataFrame(resnon, columns =['Stdev', 'Var Comp', '6 * Stdev', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfnon.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'INT', 'INT', 'PV', 'TV'])
        ndcnon = 1
        if 1.41 * pv / grr > 1:
            ndcnon = math.floor(1.41 * sd6pv / sd6grr)

        iter = 1
        temp = []
        r = []
        urut = []
        listulcr = []
        # for i in range(100):
        #   urut.append(i + 1)
        #   listulcr.append(ulcr)
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_ntrial) * int(nested.nested_npart)):
            temp.append(all[i][0])
            if iter % int(nested.nested_ntrial) == 0:
                r.append(max(temp) - min(temp))
                temp = []
            iter = iter + 1
        
        allt = []
        allplain = all.copy()
        allplain = []
        for ele in nested.nested_all:
            ele = np.array(ele)
            ele = ele.T
            ele = ele.tolist()
            allplain.append(ele)

        allplain = [x for l in allplain for x in l]
        allplain = [x for l in allplain for x in l]

        
        tempall = []
        temp = []
        iter = 1
        for i in range (int(nested.nested_nkaryawan) * int(nested.nested_ntrial) * int(nested.nested_npart)):
            temp.append(allplain[i])
            if iter % int(nested.nested_ntrial) == 0:
                tempall.append(temp)
                temp = []
            iter = iter + 1

        tempallt = np.array(tempall)
        tempallt = tempallt.T
        tempallt = tempallt.tolist()
        pertrial = []
        temp2 = []
        iter = 1
        a = 0
        b = int(nested.nested_npart)
        for h in range(int(nested.nested_nkaryawan)):
            for i in range(int(nested.nested_ntrial)):
                for j in range(a, b):
                    temp2.append(tempallt[i][j])
                pertrial.append(temp2)
                temp2 = []
            a = a + int(nested.nested_npart)
            b = b + int(nested.nested_npart)
        
        iter = 1
        tempave = []
        tempr = []
        avepart = []
        rpart = []
        avepart = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            tempr.append(max(list(map(float, tempall[i]))) - min(list(map(float, tempall[i]))))
            tempave.append(sum(list(map(float, tempall[i]))) / len(list(map(float, tempall[i]))))
            if iter % int(nested.nested_npart) == 0:
                rpart.append(tempr)
                avepart.append(tempave)
                tempr = []
                tempave = []
            iter = iter + 1
        
        avepartall = []
        temp = []
        for i in range(int(nested.nested_npart)):
            for ele in avepart:
                temp.append(ele[i])
            avepartall.append(sum(temp) / int(nested.nested_nkaryawan))
            temp = []
        xbar2 = sum(avepartall) / int(nested.nested_npart)
        rp = max(avepartall) - min(avepartall)

        xx = []
        rx = []

        for i in range(int(nested.nested_nkaryawan)):
            xx.append(sum(avepart[i]) / len(avepart[i]))
            rx.append(sum(rpart[i]) / len(rpart[i]))
        
        rbar = sum(rx) / int(nested.nested_nkaryawan)
        xdiff = max(xx) - min(xx)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]

        for i in range(4):
            if subgroup[i][0] == int(nested.nested_ntrial):
                d4 = subgroup[i][1]
            else:
                d4 = subgroup[3][1]

        ulcr = d4 * rbar
        lclr = 0

        for i in range(4):
            if subgroup[i][0] == int(nested.nested_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]

        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar
        
        rpartflat =  [x for l in rpart for x in l]
        ulcrflat = []
        lclrflat = []
        urutflat = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            ulcrflat.append(ulcr)
            lclrflat.append(lclr)
            urutflat.append(i+1)

        avepartflat =  [x for l in avepart for x in l]
        uclxflat = []
        lclxflat = []
        xbar2flat = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            uclxflat.append(uclx)
            lclxflat.append(lclx)
            xbar2flat.append(xbar2)
        
        urutpart = []
        urutallpart = []
        temp = []
        avepertrial = []
        iter = 1

        for i in range(int(nested.nested_npart)):
            urutpart.append(i+1)

        for i in range(int(nested.nested_ntrial) * int(nested.nested_nkaryawan)):
            urutallpart.append(urutpart)
            temp.append(sum(list(map(float, pertrial[i]))) / len(list(map(float, pertrial[i]))))
            if iter % int(nested.nested_ntrial) == 0:
                avepertrial.append(temp)
                temp = []
            iter = iter + 1
        
        iter = 1
        temp = []
        tempperkaryawan = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            temp.append(tempall[i])
            if iter % int(nested.nested_npart) == 0:
                tempperkaryawan.append(temp)
                temp = []
            iter = iter + 1

        temp = []
        perkaryawan = []
        for ele in tempperkaryawan:
            temp =  [x for l in ele for x in l]
            perkaryawan.append(temp)
            temp = []
        
        temp = []
        urutnama = []
        avekaryawan = []
        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_npart) * int(nested.nested_ntrial)):
                temp.append(i+1)
            urutnama.append(temp)
            temp = []

        for i in range(int(nested.nested_nkaryawan)):
            avekaryawan.append(sum(list(map(float, perkaryawan[i]))) / len(list(map(float, perkaryawan[i]))))
            temp.append(i+1)

        urutpart2 = []
        for i in range(int(nested.nested_nkaryawan)):
            urutpart2.append(urutpart)

        a, b, c, d, e, g = [*zip(*resinteraksi)]
        source = ['GRR', 'Repeatability', 'Reproducibility', 'Total Variation'] 
        psv = list(c)
        pc = list(d)
        del psv[3:6]
        del pc[3:6]
        psv = tuple(psv)
        pc = tuple(pc)

        # if aov['P Value'][2] < 0.05:
        #     dfdisplay = dfinteraksi.copy()
        #     dfdisplay = dfdisplay.drop('Study Variation', 1)
        #     dfdisplay = dfdisplay.drop('Var Comp', 1)
        #     if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
        #         dfdisplay = dfdisplay.drop('% Process', 1)
        #     if int(nested.nested_stdev) == 0:
        #         dfdisplay = dfdisplay.drop('% Tolerance', 1)
        #     dfdisplay = dfdisplay.drop(3)
        #     dfdisplay = dfdisplay.drop(4)
        #     dfdisplay = dfdisplay.drop(6)
        # elif aov['P Value'][2] >= 0.05:
        #     dfdisplay = dfnon.copy()
        #     dfdisplay = dfdisplay.drop('Stdev', 1)
        #     dfdisplay = dfdisplay.drop('Var Comp', 1)
        #     dfdisplay = dfdisplay.drop('6 * Stdev', 1)
        #     if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
        #         dfdisplay = dfdisplay.drop('% Process', 1)
        #     if int(nested.nested_stdev) == 0:
        #         dfdisplay = dfdisplay.drop('% Tolerance', 1)
        #     dfdisplay = dfdisplay.drop(3)
        #     dfdisplay = dfdisplay.drop(4)
        #     dfdisplay = dfdisplay.drop(6)    

        aov1 = aov.copy()
        aov1.loc[0, 'SS'] = aov1['SS'][0] + aov1['SS'][2]
        aov1.loc[0, 'DF'] = aov1['DF'][0] + aov1['DF'][2]
        aov1.loc[0, 'MS'] = aov1['SS'][0] / aov1['DF'][0]
        aov1.loc[0, 'F'] = aov1['MS'][0] / aov1['MS'][3]
        aov1.loc[1, 'F'] = aov1['MS'][1] / aov1['MS'][0]
        aov1.loc[0, 'P Value'] = 1 - f.cdf(aov1['F'][0], aov1['DF'][0], aov1['DF'][3])
        aov1.loc[1, 'P Value'] = 1 - f.cdf(aov1['F'][1], aov1['DF'][1], aov1['DF'][2])
        aov1 = aov1.drop(2)
        new_row = {'Source':'Total', 'SS':'NaN', 'DF':'NaN', 'MS':'NaN', 'F':'NaN', 'P Value':'NaN', 'Ket':'NaN'}
        aov1 = aov1.append(new_row, ignore_index=True)
        aov1.loc[3, 'SS'] = aov1['SS'][0] + aov1['SS'][1] + aov1['SS'][2]
        aov1.loc[3, 'DF'] = aov1['DF'][0] + aov1['DF'][1] + aov1['DF'][2]
        # aov1.loc[aov1.shape[0]] = ['Total', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        ms = aov1['MS'].tolist()
        df = aov1['DF'].tolist()
        fvalue = aov1['F'].tolist()
        pval = aov1['P Value'].tolist()
        
        aov1 = aov1.to_html(classes='table table-hover table-condensed mv-20', index=False)

        dfdisplay = dfinteraksi.copy()
        dfdisplay = dfdisplay.drop('Study Variation', 1)
        dfdisplay = dfdisplay.drop('Var Comp', 1)
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            dfdisplay = dfdisplay.drop('% Process', 1)
        if int(nested.nested_stdev) == 0:
            dfdisplay = dfdisplay.drop('% Tolerance', 1)
        dfdisplay = dfdisplay.drop(3)
        dfdisplay = dfdisplay.drop(4)

        varcomp = []
        studyvar = []
        sd6 = []
        psv = []
        pvc = []
        pt = []
        pp = []
        
        
        varcomp.append(ms[2])
        if nested.nested_nkaryawan * (ms[1] - ms[0]) / (nested.nested_npart * nested.nested_ntrial) > 0:
            varcomp.append(nested.nested_nkaryawan * (ms[1] - ms[0]) / (nested.nested_npart * nested.nested_ntrial))
        else:
            varcomp.append(0)
        varcomp.append((ms[0] - ms[2]) / nested.nested_ntrial)
        tempdisplay = (varcomp[0] ** 2 + varcomp[1] ** 2) ** 0.5
        varcomp.insert(0,tempdisplay)
        tempdisplay = varcomp[0] + varcomp[3]
        varcomp.append(tempdisplay)

        for ele in varcomp:
            studyvar.append(ele ** 0.5)
            pvc.append(ele / varcomp[4] * 100)
        
        for ele in studyvar:
            sd6.append(ele * 6)

        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0 and int(nested.nested_stdev) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(0)
                pp.append(0)
        elif int(nested.nested_stdev) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(ele / (nested.nested_stdevmax - nested.nested_stdevmin) * 100)
                pp.append(0)
        elif int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(0)
                pp.append(ele / (nested.nested_stdev * 6) * 100)
        else:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(ele / (nested.nested_stdevmax - nested.nested_stdevmin) * 100)
                pp.append(ele / (nested.nested_stdev * 6) * 100)
        
        dfdisplay['Var Comp'] = pd.Series(varcomp, index=dfdisplay.index)
        dfdisplay['Study Var'] = pd.Series(studyvar, index=dfdisplay.index)
        dfdisplay['6 x Stdev'] = pd.Series(sd6, index=dfdisplay.index)
        dfdisplay['% Study Var'] = pd.Series(psv, index=dfdisplay.index)
        dfdisplay['% Var Comp'] = pd.Series(pvc, index=dfdisplay.index)
        dfdisplay['% Tolerance'] = pd.Series(pt, index=dfdisplay.index)
        dfdisplay['% Process'] = pd.Series(pp, index=dfdisplay.index)

        dfinteraksi2 = dfdisplay.to_html(classes='table table-hover table-condensed mv-20', index=False)

        dfdisplay = dfdisplay.drop('Study Var', 1)
        dfdisplay = dfdisplay.drop('Var Comp', 1)
        dfdisplay = dfdisplay.drop('6 x Stdev', 1)
        if int(nested.nested_stdev) == 0:
            dfdisplay = dfdisplay.drop('% Tolerance', 1)
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            dfdisplay = dfdisplay.drop('% Process', 1)

        ###########graf

        plt.figure()
        dfdisplay.plot(kind='bar', x='Source', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)
        
        ###################################
        plt.clf()
        rpart = plt.scatter(urutflat, rpartflat)
        ulcr = plt.scatter(urutflat, ulcrflat)
        lclr = plt.scatter(urutflat, lclrflat)
        plt.legend((rpart, ulcr, lclr), ('R', 'UCLRbar', 'LCLRbar'), bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)
        plt.title("Range vs Appraisal")
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        rva = urllib.parse.quote(string)

        ####################################
        
        plt.clf()
        plt.plot(urutflat, avepartflat, label='Xbar')
        plt.plot(urutflat, uclxflat, label='UCLxbar2')
        plt.plot(urutflat, lclxflat, label='LCLxbar2')
        plt.plot(urutflat, xbar2flat, label='Xbar2')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=5)
        plt.title("Xbar vs Appraisal")
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        xva = urllib.parse.quote(string)

        #####################################

        plt.clf()
        plt.scatter(urutallpart, pertrial)
        plt.plot(urutpart, avepartall, label='Average')
        plt.title('Data by Sample')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(nested.nested_nkaryawan))
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        dbs = urllib.parse.quote(string)

        #####################################

        plt.clf()
        plt.xticks(temp, nested.nested_karyawan)
        plt.scatter(urutnama, perkaryawan)
        plt.plot(temp, avekaryawan, label='Average')
        plt.title('Data by Appraiser')
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(nested.nested_nkaryawan))
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        dba = urllib.parse.quote(string)

        ######################################

        plt.clf()
        for i in range(int(nested.nested_nkaryawan)):
            plt.scatter(urutpart2[i], avepart[i])
            plt.plot(urutpart2[i], avepart[i], label=nested.nested_karyawan[i])
        plt.legend(bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=int(nested.nested_nkaryawan))
        plt.title("Average Data by Appraiser")
        plt.ylabel("Value")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        aabp = urllib.parse.quote(string)


        gabung = zip(nested.nested_karyawan, range(1, int(nested.nested_nkaryawan)+1))
        survey = Survey.objects.get(id = nested.nested_survey_id)

        return render(request,'nested/comment_nested.html', {'nested':nested, 'survey':survey, 'dfinteraksi': dfinteraksi2, 'gabung':gabung, 'aov':aov1, 'psvc':psvc, 'rva':rva, 'xva':xva, 'dbs':dbs, 'dba':dba, 'aabp':aabp})
    else:
        return redirect('/logout')

def storeCommentNested(request, pk):
    if 'user' in request.session:
        nested = Nested.objects.get(nested_survey_id = pk)
        
        nested.nested_recommendation = request.POST.getlist('nested_recommendation')
        nested.nested_psvc = request.POST.get('nested_psvc')
        nested.nested_rva = request.POST.get('nested_rva')
        nested.nested_dbs = request.POST.get('nested_dbs')
        nested.nested_dba = request.POST.get('nested_dba')
        nested.nested_xva = request.POST.get('nested_xva')
        nested.nested_aabp = request.POST.get('nested_aabp')
        nested.save()

        return redirect('coretoolcrud:viewFinalNested',nested.nested_survey_id )
    else:
        return redirect('/logout')

def viewFinalNested(request, pk):
    if 'user' in request.session:
        nested = Nested.objects.get(nested_survey_id = pk)
        survey = Survey.objects.get(id = nested.nested_survey_id)

        ##############################

        temp = []
        perpart = []
        for ele in nested.nested_all:
            temp =  [x for l in ele for x in l]
            perpart.append(temp)
            temp = []

        perpart = [x for l in perpart for x in l]

        all = []
        iter = 0
        temp = []

        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_ntrial)):
                for k in range(int(nested.nested_npart)):
                    p = k + 1
                    p = str(p)
                    t = j + 1
                    t = str(t)
                    temp.append(float(perpart[iter]))
                    temp.append("P"+p)
                    temp.append("T"+t)
                    temp.append(nested.nested_karyawan[i])
                    all.append(temp)
                    temp = []
                    iter = iter + 1
        
        df = pd.DataFrame(all, columns =['Uk', 'Part', 'Trial', 'Karyawan'])

        aov = pg.anova(dv='Uk', between=['Part', 'Karyawan'], data=df, detailed=True)
        aov.loc[0, 'F'] = aov['MS'][0] / aov['MS'][2]
        aov.loc[1, 'F'] = aov['MS'][1] / aov['MS'][2]

        aov.loc[0, 'p-unc'] = 1 - f.cdf(aov['F'][0], aov['DF'][0], aov['DF'][2])
        aov.loc[1, 'p-unc'] = 1 - f.cdf(aov['F'][1], aov['DF'][1], aov['DF'][2])
        aov.loc[2, 'p-unc'] = 1 - f.cdf(aov['F'][2], aov['DF'][2], aov['DF'][3])
        aov = aov.rename(columns={'p-unc': 'P Value'})
        aov = aov.rename(columns={'np2': 'Ket'})

        if aov['P Value'][0] >= 0.05:
            aov.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aov['P Value'][0] < 0.05:
            aov.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aov['P Value'][1] >= 0.05:
            aov.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aov['P Value'][1] < 0.05:
            aov.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        if aov['P Value'][2] >= 0.05:
            aov.loc[2, 'Ket'] = 'Not significant, interactions dont contribute variation'
        if aov['P Value'][2] < 0.05:
            aov.loc[2, 'Ket'] = 'Significant, interactions contribute variation'
        
        evrepeat = 6 * aov['MS'][3] ** 0.5
        av = 0
        if aov['MS'][1] - aov['MS'][2] > 0:
            av = (aov['MS'][1] - aov['MS'][2]) / (int(nested.nested_npart) * int(nested.nested_ntrial)) ** 0.5 * 6

        intt = (((aov['MS'][2] - aov['MS'][3]) / int(nested.nested_ntrial)) ** 0.5) * 6
        pv = 6 * ((aov['MS'][0] - aov['MS'][2]) / (int(nested.nested_nkaryawan) * int(nested.nested_ntrial))) ** 0.5
        grr = (evrepeat ** 2 + av ** 2 + intt ** 2) ** 0.5
        evrepro = (av ** 2 + intt ** 2) ** 0.5
        tv = (grr ** 2 + pv ** 2) ** 0.5
        ndc = 1
        
        if 1.41 * pv / grr > 1:
            ndc = math.floor(1.41 * pv / grr)

        sv = [grr, evrepeat, evrepro, av, intt, pv, tv]
        vc = []
        for i in range(7):
            vc.append((sv[i] / 6) ** 2)
        psv = []
        for i in range(7):
            psv.append(sv[i] / sv[6] * 100)
        pc = []
        for i in range(7):
            pc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sv[i] / (int(nested.nested_stdevmax) - int(nested.nested_stdevmin)) * 100)
        pp = []
        if int(nested.nested_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sv[i] / (6 * int(nested.nested_stdev)) * 100)
        resinteraksi = [sv, vc, psv, pc, pt, pp]
        resinteraksi = np.array(resinteraksi)
        resinteraksi = resinteraksi.T
        resinteraksi = resinteraksi.tolist()
        dfinteraksi = pd.DataFrame(resinteraksi, columns =['Study Variation', 'Var Comp', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfinteraksi.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'AV', 'INT', 'Part To Part', 'Total Variation'])
        
        aovnon = aov.copy()
        aovnon.loc[2, 'Source'] = 'Repeatability'
        aovnon.loc[3, 'Source'] = 'Total'
        aovnon.loc[2, 'DF'] = (int(nested.nested_npart) - 1) * (int(nested.nested_nkaryawan) - 1) + int(nested.nested_nkaryawan) * int(nested.nested_npart) * (int(nested.nested_ntrial) - 1)
        aovnon.loc[3, 'DF'] =  aovnon['DF'][0] +  aovnon['DF'][1] +  aovnon['DF'][2]
        aovnon.loc[2, 'SS'] = aovnon['SS'][2] + aovnon['SS'][3]
        aovnon.loc[2, 'SS'] = aov['SS'][2] + aov['SS'][3]
        aovnon.loc[3, 'SS'] =  aovnon['SS'][0] + aovnon['SS'][1] +  aovnon['SS'][2]
        aovnon.loc[2, 'MS'] =  aovnon['SS'][2] / aovnon['DF'][2]
        aovnon.loc[3, 'MS'] = "NaN"
        aovnon.loc[0, 'F'] =  aovnon['MS'][0] / aovnon['MS'][2]
        aovnon.loc[1, 'F'] =  aovnon['MS'][1] / aovnon['MS'][2]
        aovnon.loc[3, 'F'] = 0
        aovnon.loc[0, 'P Value'] = 1 - f.cdf(aovnon['F'][0], aovnon['DF'][0], aovnon['DF'][2])
        aovnon.loc[1, 'P Value'] = 1 - f.cdf(aovnon['F'][1], aovnon['DF'][1], aovnon['DF'][2])
        if aovnon['P Value'][0] >= 0.05:
            aovnon.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aovnon['P Value'][0] < 0.05:
            aovnon.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aovnon['P Value'][1] >= 0.05:
            aovnon.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aovnon['P Value'][1] < 0.05:
            aovnon.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        aovnon.loc[2, 'Ket'] = 0

        sd6ev =  6 * aovnon['MS'][2] ** 0.5
        sd6av = 0
        if aovnon['MS'][1] - aovnon['MS'][2] > 0:
            sd6av = ((aovnon['MS'][1] - aovnon['MS'][2]) / (int(nested.nested_npart) * int(nested.nested_ntrial))) ** 0.5 * 6
        sd6pv = 0
        if aovnon['MS'][0] - aovnon['MS'][2] > 0:
            sd6pv = 6 * ((aovnon['MS'][0] - aovnon['MS'][2]) / (int(nested.nested_nkaryawan) * int(nested.nested_ntrial))) ** 0.5
        sd6int = 0
        sd6int2 = 0
        sd6grr = (sd6ev ** 2 + sd6av ** 2 + sd6int ** 2) ** 0.5
        sd6tv = (sd6grr ** 2 + sd6pv ** 2) ** 0.5
        sd6 = [sd6grr, sd6ev, sd6av, sd6int, sd6int2, sd6pv, sd6tv]

        sd = []
        for i in range(7):
            sd.append(sd6[i] / 6)
        vc = []
        for i in range(7):
            vc.append(sd[i] ** 2)
        psv = []
        for i in range(7):
            psv.append(sd6[i] / sd6[6] * 100)
        pvc = []
        for i in range(7):
            pvc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sd6[i] / (int(nested.nested_stdevmax) - int(nested.nested_stdevmin)) * 100)
        pp = []
        if int(nested.nested_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sd6[i] / (6 * int(nested.nested_stdev)) * 100)

        resnon = [sd, vc, sd6, psv, pvc, pt, pp]
        resnon = np.array(resnon)
        resnon = resnon.T
        resnon = resnon.tolist()

        dfnon = pd.DataFrame(resnon, columns =['Stdev', 'Var Comp', '6 * Stdev', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfnon.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'INT', 'INT', 'PV', 'TV'])
        ndcnon = 1
        if 1.41 * pv / grr > 1:
            ndcnon = math.floor(1.41 * sd6pv / sd6grr)

        iter = 1
        temp = []
        r = []
        urut = []
        listulcr = []
        # for i in range(100):
        #   urut.append(i + 1)
        #   listulcr.append(ulcr)
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_ntrial) * int(nested.nested_npart)):
            temp.append(all[i][0])
            if iter % int(nested.nested_ntrial) == 0:
                r.append(max(temp) - min(temp))
                temp = []
            iter = iter + 1
        
        allt = []
        allplain = all.copy()
        allplain = []
        for ele in nested.nested_all:
            ele = np.array(ele)
            ele = ele.T
            ele = ele.tolist()
            allplain.append(ele)

        allplain = [x for l in allplain for x in l]
        allplain = [x for l in allplain for x in l]

        
        tempall = []
        temp = []
        iter = 1
        for i in range (int(nested.nested_nkaryawan) * int(nested.nested_ntrial) * int(nested.nested_npart)):
            temp.append(allplain[i])
            if iter % int(nested.nested_ntrial) == 0:
                tempall.append(temp)
                temp = []
            iter = iter + 1

        tempallt = np.array(tempall)
        tempallt = tempallt.T
        tempallt = tempallt.tolist()
        pertrial = []
        temp2 = []
        iter = 1
        a = 0
        b = int(nested.nested_npart)
        for h in range(int(nested.nested_nkaryawan)):
            for i in range(int(nested.nested_ntrial)):
                for j in range(a, b):
                    temp2.append(tempallt[i][j])
                pertrial.append(temp2)
                temp2 = []
            a = a + int(nested.nested_npart)
            b = b + int(nested.nested_npart)
        
        iter = 1
        tempave = []
        tempr = []
        avepart = []
        rpart = []
        avepart = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            tempr.append(max(list(map(float, tempall[i]))) - min(list(map(float, tempall[i]))))
            tempave.append(sum(list(map(float, tempall[i]))) / len(list(map(float, tempall[i]))))
            if iter % int(nested.nested_npart) == 0:
                rpart.append(tempr)
                avepart.append(tempave)
                tempr = []
                tempave = []
            iter = iter + 1
        
        
        avepartall = []
        temp = []
        for i in range(int(nested.nested_npart)):
            for ele in avepart:
                temp.append(ele[i])
            avepartall.append(sum(temp) / int(nested.nested_nkaryawan))
            temp = []
        xbar2 = sum(avepartall) / int(nested.nested_npart)
        rp = max(avepartall) - min(avepartall)

        xx = []
        rx = []

        for i in range(int(nested.nested_nkaryawan)):
            xx.append(sum(avepart[i]) / len(avepart[i]))
            rx.append(sum(rpart[i]) / len(rpart[i]))
        
        rbar = sum(rx) / int(nested.nested_nkaryawan)
        xdiff = max(xx) - min(xx)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]

        for i in range(4):
            if subgroup[i][0] == int(nested.nested_ntrial):
                d4 = subgroup[i][1]
            else:
                d4 = subgroup[3][1]

        ulcr = d4 * rbar
        lclr = 0

        for i in range(4):
            if subgroup[i][0] == int(nested.nested_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]

        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar
        
        rpartflat =  [x for l in rpart for x in l]
        ulcrflat = []
        lclrflat = []
        urutflat = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            ulcrflat.append(ulcr)
            lclrflat.append(lclr)
            urutflat.append(i+1)

        avepartflat =  [x for l in avepart for x in l]
        uclxflat = []
        lclxflat = []
        xbar2flat = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            uclxflat.append(uclx)
            lclxflat.append(lclx)
            xbar2flat.append(xbar2)
        
        urutpart = []
        urutallpart = []
        temp = []
        avepertrial = []
        iter = 1

        for i in range(int(nested.nested_npart)):
            urutpart.append(i+1)

        for i in range(int(nested.nested_ntrial) * int(nested.nested_nkaryawan)):
            urutallpart.append(urutpart)
            temp.append(sum(list(map(float, pertrial[i]))) / len(list(map(float, pertrial[i]))))
            if iter % int(nested.nested_ntrial) == 0:
                avepertrial.append(temp)
                temp = []
            iter = iter + 1
        
        iter = 1
        temp = []
        tempperkaryawan = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            temp.append(tempall[i])
            if iter % int(nested.nested_npart) == 0:
                tempperkaryawan.append(temp)
                temp = []
            iter = iter + 1

        temp = []
        perkaryawan = []
        for ele in tempperkaryawan:
            temp =  [x for l in ele for x in l]
            perkaryawan.append(temp)
            temp = []
        
        temp = []
        urutnama = []
        avekaryawan = []
        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_npart) * int(nested.nested_ntrial)):
                temp.append(nested.nested_karyawan[i])
            urutnama.append(temp)
            temp = []

        for i in range(int(nested.nested_nkaryawan)):
            avekaryawan.append(sum(list(map(float, perkaryawan[i]))) / len(list(map(float, perkaryawan[i]))))
            temp.append(i+1)

        urutpart2 = []
        for i in range(int(nested.nested_nkaryawan)):
            urutpart2.append(urutpart)

        a, b, c, d, e, g = [*zip(*resinteraksi)]
        source = ['GRR', 'Repeatability', 'Reproducibility', 'Total Variation'] 
        psv = list(c)
        pc = list(d)
        del psv[3:6]
        del pc[3:6]
        psv = tuple(psv)
        pc = tuple(pc)

        # if aov['P Value'][2] < 0.05:
        #     dfdisplay = dfinteraksi.copy()
        #     dfdisplay = dfdisplay.drop('Study Variation', 1)
        #     dfdisplay = dfdisplay.drop('Var Comp', 1)
        #     if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
        #         dfdisplay = dfdisplay.drop('% Process', 1)
        #     if int(nested.nested_stdev) == 0:
        #         dfdisplay = dfdisplay.drop('% Tolerance', 1)
        #     dfdisplay = dfdisplay.drop(3)
        #     dfdisplay = dfdisplay.drop(4)
        #     dfdisplay = dfdisplay.drop(6)
        # elif aov['P Value'][2] >= 0.05:
        #     dfdisplay = dfnon.copy()
        #     dfdisplay = dfdisplay.drop('Stdev', 1)
        #     dfdisplay = dfdisplay.drop('Var Comp', 1)
        #     dfdisplay = dfdisplay.drop('6 * Stdev', 1)
        #     if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
        #         dfdisplay = dfdisplay.drop('% Process', 1)
        #     if int(nested.nested_stdev) == 0:
        #         dfdisplay = dfdisplay.drop('% Tolerance', 1)
        #     dfdisplay = dfdisplay.drop(3)
        #     dfdisplay = dfdisplay.drop(4)
        #     dfdisplay = dfdisplay.drop(6)    

        aov1 = aov.copy()
        aov1.loc[0, 'SS'] = aov1['SS'][0] + aov1['SS'][2]
        aov1.loc[0, 'DF'] = aov1['DF'][0] + aov1['DF'][2]
        aov1.loc[0, 'MS'] = aov1['SS'][0] / aov1['DF'][0]
        aov1.loc[0, 'F'] = aov1['MS'][0] / aov1['MS'][3]
        aov1.loc[1, 'F'] = aov1['MS'][1] / aov1['MS'][0]
        aov1.loc[0, 'P Value'] = 1 - f.cdf(aov1['F'][0], aov1['DF'][0], aov1['DF'][3])
        aov1.loc[1, 'P Value'] = 1 - f.cdf(aov1['F'][1], aov1['DF'][1], aov1['DF'][2])
        aov1 = aov1.drop(2)
        new_row = {'Source':'Total', 'SS':'NaN', 'DF':'NaN', 'MS':'NaN', 'F':'NaN', 'P Value':'NaN', 'Ket':'NaN'}
        aov1 = aov1.append(new_row, ignore_index=True)
        aov1.loc[3, 'SS'] = aov1['SS'][0] + aov1['SS'][1] + aov1['SS'][2]
        aov1.loc[3, 'DF'] = aov1['DF'][0] + aov1['DF'][1] + aov1['DF'][2]
        # aov1.loc[aov1.shape[0]] = ['Total', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        ms = aov1['MS'].tolist()
        df = aov1['DF'].tolist()
        fvalue = aov1['F'].tolist()
        pval = aov1['P Value'].tolist()
        
        aov1 = aov1.to_html(classes='table table-hover table-condensed mv-20', index=False)

        dfdisplay = dfinteraksi.copy()
        dfdisplay = dfdisplay.drop('Study Variation', 1)
        dfdisplay = dfdisplay.drop('Var Comp', 1)
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            dfdisplay = dfdisplay.drop('% Process', 1)
        if int(nested.nested_stdev) == 0:
            dfdisplay = dfdisplay.drop('% Tolerance', 1)
        dfdisplay = dfdisplay.drop(3)
        dfdisplay = dfdisplay.drop(4)

        varcomp = []
        studyvar = []
        sd6 = []
        psv = []
        pvc = []
        pt = []
        pp = []
        
        
        varcomp.append(ms[2])
        if nested.nested_nkaryawan * (ms[1] - ms[0]) / (nested.nested_npart * nested.nested_ntrial) > 0:
            varcomp.append(nested.nested_nkaryawan * (ms[1] - ms[0]) / (nested.nested_npart * nested.nested_ntrial))
        else:
            varcomp.append(0)
        varcomp.append((ms[0] - ms[2]) / nested.nested_ntrial)
        tempdisplay = (varcomp[0] ** 2 + varcomp[1] ** 2) ** 0.5
        varcomp.insert(0,tempdisplay)
        tempdisplay = varcomp[0] + varcomp[3]
        varcomp.append(tempdisplay)

        for ele in varcomp:
            studyvar.append(ele ** 0.5)
            pvc.append(ele / varcomp[4] * 100)
        
        for ele in studyvar:
            sd6.append(ele * 6)

        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0 and int(nested.nested_stdev) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(0)
                pp.append(0)
        elif int(nested.nested_stdev) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(ele / (nested.nested_stdevmax - nested.nested_stdevmin) * 100)
                pp.append(0)
        elif int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(0)
                pp.append(ele / (nested.nested_stdev * 6) * 100)
        else:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(ele / (nested.nested_stdevmax - nested.nested_stdevmin) * 100)
                pp.append(ele / (nested.nested_stdev * 6) * 100)
        
        dfdisplay['Var Comp'] = pd.Series(varcomp, index=dfdisplay.index)
        dfdisplay['Study Var'] = pd.Series(studyvar, index=dfdisplay.index)
        dfdisplay['6 x Stdev'] = pd.Series(sd6, index=dfdisplay.index)
        dfdisplay['% Study Var'] = pd.Series(psv, index=dfdisplay.index)
        dfdisplay['% Var Comp'] = pd.Series(pvc, index=dfdisplay.index)
        dfdisplay['% Tolerance'] = pd.Series(pt, index=dfdisplay.index)
        dfdisplay['% Process'] = pd.Series(pp, index=dfdisplay.index)

        dfinteraksi2 = dfdisplay.to_html(classes='table table-hover table-condensed mv-20', index=False)

        dfdisplay = dfdisplay.drop('Study Var', 1)
        dfdisplay = dfdisplay.drop('Var Comp', 1)
        dfdisplay = dfdisplay.drop('6 x Stdev', 1)
        if int(nested.nested_stdev) == 0:
            dfdisplay = dfdisplay.drop('% Process', 1)
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            dfdisplay = dfdisplay.drop('% Tolerance', 1)

        ###########graf

        plt.figure()
        dfdisplay.plot(kind='bar', x='Source', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)
        
        ###################################

        bot = []

        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_npart)):
                bot.append(nested.nested_karyawan[i] + "-" + str(j+1))

        p = figure(title="Range vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.scatter(bot, rpartflat, legend_label="R", marker="circle")
        p.scatter(bot, ulcrflat, color="green", legend_label="UCLRbar", marker="circle")
        p.scatter(bot, lclrflat, color="red", legend_label="LCLRbar", marker="circle")
        p.xaxis.major_label_orientation = "vertical"
        scriptrva, divrva = components(p)

        ####################################

        p = figure(title="Xbar vs Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.line(bot, avepartflat, legend_label="Xbar", line_width=2)
        p.line(bot, uclxflat, legend_label="UCLXbar2", color="green", line_width=2)
        p.line(bot, lclxflat, legend_label="LCLXbar2", color="red", line_width=2)
        p.line(bot, xbar2flat, legend_label="Xbar2", color="black", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptxva, divxva = components(p)

        #####################################

        p = figure(title="Data by Sample", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(len(urutallpart)):
            p.scatter(urutallpart[i], pertrial[i], marker="circle")
        
        p.line(urutpart, avepartall, legend_label="Average", line_width=2)
        scriptdbs, divdbs = components(p)

        #####################################

        p = figure(title="Data by Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", x_range=nested.nested_karyawan, y_axis_label='Measurement', x_axis_label='Appraiser')
        for i in range(len(urutnama)):
            p.scatter(urutnama[i], perkaryawan[i], marker="circle")
        
        p.line(nested.nested_karyawan, avekaryawan, legend_label="Average", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptdba, divdba = components(p)

        ######################################

        colors = []

        p = figure(title="Average Data by Appraiser", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(int(nested.nested_nkaryawan)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutpart2[i], avepart[i], color=colors[i], marker="circle")
            p.line(urutpart2[i], avepart[i], color=colors[i], legend_label=nested.nested_karyawan[i], line_width=2)
        
        scriptaabp, divaabp = components(p)



        gabung = zip(nested.nested_all, nested.nested_karyawan)
        part1 = range(1, int(nested.nested_npart)+1)
        survey = Survey.objects.get(id = nested.nested_survey_id)
        gabung2 = zip(nested.nested_karyawan, range(1, int(nested.nested_nkaryawan)+1))
        gabungave = zip(nested.nested_karyawan, avepart)
        gabungr = zip(nested.nested_karyawan, rpart)
        

        return render(request,'nested/collection_nested.html', {'nested':nested, 'survey':survey, 'dfinteraksi': dfinteraksi2, 'aov':aov1, 'ndc':ndc, 'psvc':psvc, 'gabung':gabung, 'gabung2':gabung2, 'gabungave':gabungave, 'gabungr':gabungr, 'part1':part1, 'scriptrva':scriptrva, 'divrva':divrva, 'scriptxva':scriptxva, 'divxva':divxva, 'scriptdbs':scriptdbs, 'divdbs':divdbs, 'scriptdba':scriptdba, 'divdba':divdba, 'scriptaabp':scriptaabp, 'divaabp':divaabp})
    else:
        return redirect('/logout')

def viewPrintNested(request, pk):
    if 'user' in request.session:
        nested = Nested.objects.get(nested_survey_id = pk)
        survey = Survey.objects.get(id = nested.nested_survey_id)

        ##############################

        temp = []
        perpart = []
        for ele in nested.nested_all:
            temp =  [x for l in ele for x in l]
            perpart.append(temp)
            temp = []

        perpart = [x for l in perpart for x in l]

        all = []
        iter = 0
        temp = []

        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_ntrial)):
                for k in range(int(nested.nested_npart)):
                    p = k + 1
                    p = str(p)
                    t = j + 1
                    t = str(t)
                    temp.append(float(perpart[iter]))
                    temp.append("P"+p)
                    temp.append("T"+t)
                    temp.append(nested.nested_karyawan[i])
                    all.append(temp)
                    temp = []
                    iter = iter + 1
        
        df = pd.DataFrame(all, columns =['Uk', 'Part', 'Trial', 'Karyawan'])

        aov = pg.anova(dv='Uk', between=['Part', 'Karyawan'], data=df, detailed=True)
        aov.loc[0, 'F'] = aov['MS'][0] / aov['MS'][2]
        aov.loc[1, 'F'] = aov['MS'][1] / aov['MS'][2]

        aov.loc[0, 'p-unc'] = 1 - f.cdf(aov['F'][0], aov['DF'][0], aov['DF'][2])
        aov.loc[1, 'p-unc'] = 1 - f.cdf(aov['F'][1], aov['DF'][1], aov['DF'][2])
        aov.loc[2, 'p-unc'] = 1 - f.cdf(aov['F'][2], aov['DF'][2], aov['DF'][3])
        aov = aov.rename(columns={'p-unc': 'P Value'})
        aov = aov.rename(columns={'np2': 'Ket'})

        if aov['P Value'][0] >= 0.05:
            aov.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aov['P Value'][0] < 0.05:
            aov.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aov['P Value'][1] >= 0.05:
            aov.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aov['P Value'][1] < 0.05:
            aov.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        if aov['P Value'][2] >= 0.05:
            aov.loc[2, 'Ket'] = 'Not significant, interactions dont contribute variation'
        if aov['P Value'][2] < 0.05:
            aov.loc[2, 'Ket'] = 'Significant, interactions contribute variation'
        
        evrepeat = 6 * aov['MS'][3] ** 0.5
        av = 0
        if aov['MS'][1] - aov['MS'][2] > 0:
            av = (aov['MS'][1] - aov['MS'][2]) / (int(nested.nested_npart) * int(nested.nested_ntrial)) ** 0.5 * 6

        intt = (((aov['MS'][2] - aov['MS'][3]) / int(nested.nested_ntrial)) ** 0.5) * 6
        pv = 6 * ((aov['MS'][0] - aov['MS'][2]) / (int(nested.nested_nkaryawan) * int(nested.nested_ntrial))) ** 0.5
        grr = (evrepeat ** 2 + av ** 2 + intt ** 2) ** 0.5
        evrepro = (av ** 2 + intt ** 2) ** 0.5
        tv = (grr ** 2 + pv ** 2) ** 0.5
        ndc = 1
        
        if 1.41 * pv / grr > 1:
            ndc = math.floor(1.41 * pv / grr)

        sv = [grr, evrepeat, evrepro, av, intt, pv, tv]
        vc = []
        for i in range(7):
            vc.append((sv[i] / 6) ** 2)
        psv = []
        for i in range(7):
            psv.append(sv[i] / sv[6] * 100)
        pc = []
        for i in range(7):
            pc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sv[i] / (int(nested.nested_stdevmax) - int(nested.nested_stdevmin)) * 100)
        pp = []
        if int(nested.nested_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sv[i] / (6 * int(nested.nested_stdev)) * 100)
        resinteraksi = [sv, vc, psv, pc, pt, pp]
        resinteraksi = np.array(resinteraksi)
        resinteraksi = resinteraksi.T
        resinteraksi = resinteraksi.tolist()
        dfinteraksi = pd.DataFrame(resinteraksi, columns =['Study Variation', 'Var Comp', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfinteraksi.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'AV', 'INT', 'Part To Part', 'Total Variation'])
        
        aovnon = aov.copy()
        aovnon.loc[2, 'Source'] = 'Repeatability'
        aovnon.loc[3, 'Source'] = 'Total'
        aovnon.loc[2, 'DF'] = (int(nested.nested_npart) - 1) * (int(nested.nested_nkaryawan) - 1) + int(nested.nested_nkaryawan) * int(nested.nested_npart) * (int(nested.nested_ntrial) - 1)
        aovnon.loc[3, 'DF'] =  aovnon['DF'][0] +  aovnon['DF'][1] +  aovnon['DF'][2]
        aovnon.loc[2, 'SS'] = aovnon['SS'][2] + aovnon['SS'][3]
        aovnon.loc[2, 'SS'] = aov['SS'][2] + aov['SS'][3]
        aovnon.loc[3, 'SS'] =  aovnon['SS'][0] + aovnon['SS'][1] +  aovnon['SS'][2]
        aovnon.loc[2, 'MS'] =  aovnon['SS'][2] / aovnon['DF'][2]
        aovnon.loc[3, 'MS'] = "NaN"
        aovnon.loc[0, 'F'] =  aovnon['MS'][0] / aovnon['MS'][2]
        aovnon.loc[1, 'F'] =  aovnon['MS'][1] / aovnon['MS'][2]
        aovnon.loc[3, 'F'] = 0
        aovnon.loc[0, 'P Value'] = 1 - f.cdf(aovnon['F'][0], aovnon['DF'][0], aovnon['DF'][2])
        aovnon.loc[1, 'P Value'] = 1 - f.cdf(aovnon['F'][1], aovnon['DF'][1], aovnon['DF'][2])
        if aovnon['P Value'][0] >= 0.05:
            aovnon.loc[0, 'Ket'] = 'Not significant, parts dont contribute variation'
        if aovnon['P Value'][0] < 0.05:
            aovnon.loc[0, 'Ket'] = 'Significant, parts contribute variation'
        if aovnon['P Value'][1] >= 0.05:
            aovnon.loc[1, 'Ket'] = 'Not significant, appraisals dont contribute variation'
        if aovnon['P Value'][1] < 0.05:
            aovnon.loc[1, 'Ket'] = 'Significant, appraisals contribute variation'
        aovnon.loc[2, 'Ket'] = 0

        sd6ev =  6 * aovnon['MS'][2] ** 0.5
        sd6av = 0
        if aovnon['MS'][1] - aovnon['MS'][2] > 0:
            sd6av = ((aovnon['MS'][1] - aovnon['MS'][2]) / (int(nested.nested_npart) * int(nested.nested_ntrial))) ** 0.5 * 6
        sd6pv = 0
        if aovnon['MS'][0] - aovnon['MS'][2] > 0:
            sd6pv = 6 * ((aovnon['MS'][0] - aovnon['MS'][2]) / (int(nested.nested_nkaryawan) * int(nested.nested_ntrial))) ** 0.5
        sd6int = 0
        sd6int2 = 0
        sd6grr = (sd6ev ** 2 + sd6av ** 2 + sd6int ** 2) ** 0.5
        sd6tv = (sd6grr ** 2 + sd6pv ** 2) ** 0.5
        sd6 = [sd6grr, sd6ev, sd6av, sd6int, sd6int2, sd6pv, sd6tv]

        sd = []
        for i in range(7):
            sd.append(sd6[i] / 6)
        vc = []
        for i in range(7):
            vc.append(sd[i] ** 2)
        psv = []
        for i in range(7):
            psv.append(sd6[i] / sd6[6] * 100)
        pvc = []
        for i in range(7):
            pvc.append(vc[i] / vc[6] * 100)
        pt = []
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for i in range(7):
                pt.append(0)
        else:
            for i in range(7):
                pt.append(sd6[i] / (int(nested.nested_stdevmax) - int(nested.nested_stdevmin)) * 100)
        pp = []
        if int(nested.nested_stdev) == 0:
            for i in range(7):
                pp.append(0)
        else:
            for i in range(7):
                pp.append(sd6[i] / (6 * int(nested.nested_stdev)) * 100)

        resnon = [sd, vc, sd6, psv, pvc, pt, pp]
        resnon = np.array(resnon)
        resnon = resnon.T
        resnon = resnon.tolist()

        dfnon = pd.DataFrame(resnon, columns =['Stdev', 'Var Comp', '6 * Stdev', '% Study Var', '% Var Comp', '% Tolerance', '% Process'])
        dfnon.insert(0, 'Source', ['GRR', 'Repeatability', 'Reproducibility', 'INT', 'INT', 'PV', 'TV'])
        ndcnon = 1
        if 1.41 * pv / grr > 1:
            ndcnon = math.floor(1.41 * sd6pv / sd6grr)

        iter = 1
        temp = []
        r = []
        urut = []
        listulcr = []
        # for i in range(100):
        #   urut.append(i + 1)
        #   listulcr.append(ulcr)
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_ntrial) * int(nested.nested_npart)):
            temp.append(all[i][0])
            if iter % int(nested.nested_ntrial) == 0:
                r.append(max(temp) - min(temp))
                temp = []
            iter = iter + 1
        
        allt = []
        allplain = all.copy()
        allplain = []
        for ele in nested.nested_all:
            ele = np.array(ele)
            ele = ele.T
            ele = ele.tolist()
            allplain.append(ele)

        allplain = [x for l in allplain for x in l]
        allplain = [x for l in allplain for x in l]

        
        tempall = []
        temp = []
        iter = 1
        for i in range (int(nested.nested_nkaryawan) * int(nested.nested_ntrial) * int(nested.nested_npart)):
            temp.append(allplain[i])
            if iter % int(nested.nested_ntrial) == 0:
                tempall.append(temp)
                temp = []
            iter = iter + 1

        tempallt = np.array(tempall)
        tempallt = tempallt.T
        tempallt = tempallt.tolist()
        pertrial = []
        temp2 = []
        iter = 1
        a = 0
        b = int(nested.nested_npart)
        for h in range(int(nested.nested_nkaryawan)):
            for i in range(int(nested.nested_ntrial)):
                for j in range(a, b):
                    temp2.append(tempallt[i][j])
                pertrial.append(temp2)
                temp2 = []
            a = a + int(nested.nested_npart)
            b = b + int(nested.nested_npart)
        
        iter = 1
        tempave = []
        tempr = []
        avepart = []
        rpart = []
        avepart = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            tempr.append(max(list(map(float, tempall[i]))) - min(list(map(float, tempall[i]))))
            tempave.append(sum(list(map(float, tempall[i]))) / len(list(map(float, tempall[i]))))
            if iter % int(nested.nested_npart) == 0:
                rpart.append(tempr)
                avepart.append(tempave)
                tempr = []
                tempave = []
            iter = iter + 1
        
        
        avepartall = []
        temp = []
        for i in range(int(nested.nested_npart)):
            for ele in avepart:
                temp.append(ele[i])
            avepartall.append(sum(temp) / int(nested.nested_nkaryawan))
            temp = []
        xbar2 = sum(avepartall) / int(nested.nested_npart)
        rp = max(avepartall) - min(avepartall)

        xx = []
        rx = []

        for i in range(int(nested.nested_nkaryawan)):
            xx.append(sum(avepart[i]) / len(avepart[i]))
            rx.append(sum(rpart[i]) / len(rpart[i]))
        
        rbar = sum(rx) / int(nested.nested_nkaryawan)
        xdiff = max(xx) - min(xx)

        subgroup = [[2, 3.268, 1.88, 0], [3, 2.574, 1.023, 0], [4, 2.282, 0.729, 0], [5, 2.114, 0.577, 0]]

        for i in range(4):
            if subgroup[i][0] == int(nested.nested_ntrial):
                d4 = subgroup[i][1]
            else:
                d4 = subgroup[3][1]

        ulcr = d4 * rbar
        lclr = 0

        for i in range(4):
            if subgroup[i][0] == int(nested.nested_npart):
                a2 = subgroup[i][2]
            else:
                a2 = subgroup[3][2]

        uclx = xbar2 + a2 * rbar #di excel beda rumus
        lclx = xbar2 - a2 * rbar
        
        rpartflat =  [x for l in rpart for x in l]
        ulcrflat = []
        lclrflat = []
        urutflat = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            ulcrflat.append(ulcr)
            lclrflat.append(lclr)
            urutflat.append(i+1)

        avepartflat =  [x for l in avepart for x in l]
        uclxflat = []
        lclxflat = []
        xbar2flat = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            uclxflat.append(uclx)
            lclxflat.append(lclx)
            xbar2flat.append(xbar2)
        
        urutpart = []
        urutallpart = []
        temp = []
        avepertrial = []
        iter = 1

        for i in range(int(nested.nested_npart)):
            urutpart.append(i+1)

        for i in range(int(nested.nested_ntrial) * int(nested.nested_nkaryawan)):
            urutallpart.append(urutpart)
            temp.append(sum(list(map(float, pertrial[i]))) / len(list(map(float, pertrial[i]))))
            if iter % int(nested.nested_ntrial) == 0:
                avepertrial.append(temp)
                temp = []
            iter = iter + 1
        
        iter = 1
        temp = []
        tempperkaryawan = []
        for i in range(int(nested.nested_nkaryawan) * int(nested.nested_npart)):
            temp.append(tempall[i])
            if iter % int(nested.nested_npart) == 0:
                tempperkaryawan.append(temp)
                temp = []
            iter = iter + 1

        temp = []
        perkaryawan = []
        for ele in tempperkaryawan:
            temp =  [x for l in ele for x in l]
            perkaryawan.append(temp)
            temp = []
        
        temp = []
        urutnama = []
        avekaryawan = []
        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_npart) * int(nested.nested_ntrial)):
                temp.append(nested.nested_karyawan[i])
            urutnama.append(temp)
            temp = []

        for i in range(int(nested.nested_nkaryawan)):
            avekaryawan.append(sum(list(map(float, perkaryawan[i]))) / len(list(map(float, perkaryawan[i]))))
            temp.append(i+1)

        urutpart2 = []
        for i in range(int(nested.nested_nkaryawan)):
            urutpart2.append(urutpart)

        a, b, c, d, e, g = [*zip(*resinteraksi)]
        source = ['GRR', 'Repeatability', 'Reproducibility', 'Total Variation'] 
        psv = list(c)
        pc = list(d)
        del psv[3:6]
        del pc[3:6]
        psv = tuple(psv)
        pc = tuple(pc)   

        aov1 = aov.copy()
        aov1.loc[0, 'SS'] = aov1['SS'][0] + aov1['SS'][2]
        aov1.loc[0, 'DF'] = aov1['DF'][0] + aov1['DF'][2]
        aov1.loc[0, 'MS'] = aov1['SS'][0] / aov1['DF'][0]
        aov1.loc[0, 'F'] = aov1['MS'][0] / aov1['MS'][3]
        aov1.loc[1, 'F'] = aov1['MS'][1] / aov1['MS'][0]
        aov1.loc[0, 'P Value'] = 1 - f.cdf(aov1['F'][0], aov1['DF'][0], aov1['DF'][3])
        aov1.loc[1, 'P Value'] = 1 - f.cdf(aov1['F'][1], aov1['DF'][1], aov1['DF'][2])
        aov1 = aov1.drop(2)
        new_row = {'Source':'Total', 'SS':'NaN', 'DF':'NaN', 'MS':'NaN', 'F':'NaN', 'P Value':'NaN', 'Ket':'NaN'}
        aov1 = aov1.append(new_row, ignore_index=True)
        aov1.loc[3, 'SS'] = aov1['SS'][0] + aov1['SS'][1] + aov1['SS'][2]
        aov1.loc[3, 'DF'] = aov1['DF'][0] + aov1['DF'][1] + aov1['DF'][2]
        # aov1.loc[aov1.shape[0]] = ['Total', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        ms = aov1['MS'].tolist()
        df = aov1['DF'].tolist()
        fvalue = aov1['F'].tolist()
        pval = aov1['P Value'].tolist()
        
        aov1 = aov1.to_html(classes='table table-hover table-condensed mv-20', index=False)

        dfdisplay = dfinteraksi.copy()
        dfdisplay = dfdisplay.drop('Study Variation', 1)
        dfdisplay = dfdisplay.drop('Var Comp', 1)
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            dfdisplay = dfdisplay.drop('% Process', 1)
        if int(nested.nested_stdev) == 0:
            dfdisplay = dfdisplay.drop('% Tolerance', 1)
        dfdisplay = dfdisplay.drop(3)
        dfdisplay = dfdisplay.drop(4)

        varcomp = []
        studyvar = []
        sd6 = []
        psv = []
        pvc = []
        pt = []
        pp = []
        
        
        varcomp.append(ms[2])
        if nested.nested_nkaryawan * (ms[1] - ms[0]) / (nested.nested_npart * nested.nested_ntrial) > 0:
            varcomp.append(nested.nested_nkaryawan * (ms[1] - ms[0]) / (nested.nested_npart * nested.nested_ntrial))
        else:
            varcomp.append(0)
        varcomp.append((ms[0] - ms[2]) / nested.nested_ntrial)
        tempdisplay = (varcomp[0] ** 2 + varcomp[1] ** 2) ** 0.5
        varcomp.insert(0,tempdisplay)
        tempdisplay = varcomp[0] + varcomp[3]
        varcomp.append(tempdisplay)

        for ele in varcomp:
            studyvar.append(ele ** 0.5)
            pvc.append(ele / varcomp[4] * 100)
        
        for ele in studyvar:
            sd6.append(ele * 6)

        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0 and int(nested.nested_stdev) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(0)
                pp.append(0)
        elif int(nested.nested_stdev) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(ele / (nested.nested_stdevmax - nested.nested_stdevmin) * 100)
                pp.append(0)
        elif int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(0)
                pp.append(ele / (nested.nested_stdev * 6) * 100)
        else:
            for ele in sd6:
                psv.append(ele / sd6[4] * 100)
                pt.append(ele / (nested.nested_stdevmax - nested.nested_stdevmin) * 100)
                pp.append(ele / (nested.nested_stdev * 6) * 100)
        
        dfdisplay['Var Comp'] = pd.Series(varcomp, index=dfdisplay.index)
        dfdisplay['Study Var'] = pd.Series(studyvar, index=dfdisplay.index)
        dfdisplay['6 x Stdev'] = pd.Series(sd6, index=dfdisplay.index)
        dfdisplay['% Study Var'] = pd.Series(psv, index=dfdisplay.index)
        dfdisplay['% Var Comp'] = pd.Series(pvc, index=dfdisplay.index)
        dfdisplay['% Tolerance'] = pd.Series(pt, index=dfdisplay.index)
        dfdisplay['% Process'] = pd.Series(pp, index=dfdisplay.index)

        dfinteraksi2 = dfdisplay.to_html(classes='table table-hover table-condensed mv-20', index=False)

        dfdisplay = dfdisplay.drop('Study Var', 1)
        dfdisplay = dfdisplay.drop('Var Comp', 1)
        dfdisplay = dfdisplay.drop('6 x Stdev', 1)
        if int(nested.nested_stdev) == 0:
            dfdisplay = dfdisplay.drop('% Tolerance', 1)
        if int(nested.nested_stdevmax) == 0 and int(nested.nested_stdevmin) == 0:
            dfdisplay = dfdisplay.drop('% Process', 1)

        ###########graf

        plt.figure()
        dfdisplay.plot(kind='bar', x='Source', rot=0, ylabel='Value', title='Resume', figsize=(6, 4))
        plt.legend(loc='upper center', ncol=5)

        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        psvc = urllib.parse.quote(string)
        
        ###################################

        bot = []

        for i in range(int(nested.nested_nkaryawan)):
            for j in range(int(nested.nested_npart)):
                bot.append(nested.nested_karyawan[i] + "-" + str(j+1))

        p = figure(title="Range vs Appraiser", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.scatter(bot, rpartflat, legend_label="R", marker="circle")
        p.scatter(bot, ulcrflat, color="green", legend_label="UCLRbar", marker="circle")
        p.scatter(bot, lclrflat, color="red", legend_label="LCLRbar", marker="circle")
        p.xaxis.major_label_orientation = "vertical"
        scriptrva, divrva = components(p)

        ####################################

        p = figure(title="Xbar vs Appraiser", sizing_mode="stretch_width", x_range=bot, y_axis_label='Measurement', x_axis_label='Appraiser-Sample')
        p.line(bot, avepartflat, legend_label="Xbar", line_width=2)
        p.line(bot, uclxflat, legend_label="UCLXbar2", color="green", line_width=2)
        p.line(bot, lclxflat, legend_label="LCLXbar2", color="red", line_width=2)
        p.line(bot, xbar2flat, legend_label="Xbar2", color="black", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptxva, divxva = components(p)

        #####################################

        p = figure(title="Data by Sample", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(len(urutallpart)):
            p.scatter(urutallpart[i], pertrial[i], marker="circle")
        
        p.line(urutpart, avepartall, legend_label="Average", line_width=2)
        scriptdbs, divdbs = components(p)

        #####################################

        p = figure(title="Data by Appraiser", sizing_mode="stretch_width", x_range=nested.nested_karyawan, y_axis_label='Measurement', x_axis_label='Appraiser')
        for i in range(len(urutnama)):
            p.scatter(urutnama[i], perkaryawan[i], marker="circle")
        
        p.line(nested.nested_karyawan, avekaryawan, legend_label="Average", line_width=2)
        p.xaxis.major_label_orientation = "vertical"
        scriptdba, divdba = components(p)

        ######################################

        colors = []

        p = figure(title="Average Data by Appraiser", sizing_mode="stretch_width", y_axis_label='Measurement', x_axis_label='Sample')
        for i in range(int(nested.nested_nkaryawan)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
            p.scatter(urutpart2[i], avepart[i], color=colors[i], marker="circle")
            p.line(urutpart2[i], avepart[i], color=colors[i], legend_label=nested.nested_karyawan[i], line_width=2)
        
        scriptaabp, divaabp = components(p)


        gabung = zip(nested.nested_all, nested.nested_karyawan)
        part1 = range(1, int(nested.nested_npart)+1)
        survey = Survey.objects.get(id = nested.nested_survey_id)
        gabung2 = zip(nested.nested_karyawan, range(1, int(nested.nested_nkaryawan)+1))
        gabungave = zip(nested.nested_karyawan, avepart)
        gabungr = zip(nested.nested_karyawan, rpart)
        

        return render(request,'nested/print_nested.html', {'nested':nested, 'survey':survey, 'dfinteraksi': dfinteraksi2, 'aov':aov1, 'ndc':ndc, 'psvc':psvc, 'gabung':gabung, 'gabung2':gabung2, 'gabungave':gabungave, 'gabungr':gabungr, 'part1':part1, 'scriptrva':scriptrva, 'divrva':divrva, 'scriptxva':scriptxva, 'divxva':divxva, 'scriptdbs':scriptdbs, 'divdbs':divdbs, 'scriptdba':scriptdba, 'divdba':divdba, 'scriptaabp':scriptaabp, 'divaabp':divaabp})
    else:
        return redirect('/logout')

def deleteNested(request, pk):
    if 'user' in request.session:
        nested = Nested.objects.get(nested_survey_id = pk)
        nested.delete()
        messages.success(request, "GRR Nested berhasil dihapus")
        return redirect('coretoolcrud:viewDetailSurvey', pk)
    else:
        return redirect('/logout')

#Linearity

def viewLinearity(request, pk):
    if 'user' in request.session:
        try:
            linearity = Linearity.objects.get(linearity_survey_id = pk)
            if linearity.linearity_all:
                return redirect('coretoolcrud:viewFinalLinearity',pk )
            else:
                part = range(1, int(linearity.linearity_npart)+1)
                measurement = range(1, int(linearity.linearity_nmeasurement)+1)
                return render(request,'linearity/all_linearity.html',{'part':part, 'measurement':measurement, 'linearity':linearity})
        except Linearity.DoesNotExist:
            return render(request,'linearity/linearity.html',{'pk':pk})
    else:
        return redirect('/logout')

def viewAverageLinearity(request):
    if 'user' in request.session:
        return render(request,'linearity/average_linearity.html')
    else:
        return redirect('/logout')

def storeLinearity(request, pk):
    if 'user' in request.session:
        try:
            linearity = Linearity.objects.get(linearity_survey_id = pk)
            linearity.delete()
        except Linearity.DoesNotExist:
            pass
            
        linearity = Linearity()
        linearity.linearity_survey_id = pk
        linearity.linearity_nmeasurement = request.POST.get('linearity_nmeasurement')
        linearity.linearity_npart = request.POST.get('linearity_npart')
        linearity.linearity_confidence = request.POST.get('linearity_confidence')
        linearity.linearity_working_max = request.POST.get('linearity_working_max')
        linearity.linearity_working_min = request.POST.get('linearity_working_min')
        linearity.linearity_ref = request.POST.get('linearity_ref')
        linearity.linearity_measured = request.POST.get('linearity_measured')
        linearity.linearity_reviewed = request.POST.get('linearity_reviewed')

        linearity.save()
        # karyawan = range(int(cross.cross_nkaryawan))
        # return render(request,'cross/karyawan_cross.html',{'karyawan':karyawan})

        part = range(1, int(linearity.linearity_npart)+1)
        measurement = range(int(linearity.linearity_nmeasurement))

        if linearity.linearity_ref == "master":
            return redirect('coretoolcrud:viewMasterLinearity',pk )
            
        else:
            return redirect('coretoolcrud:viewAverageLinearity',pk )
            # return render(request,'linearity/all_linearity.html',{'part':part, 'measurement':measurement, 'linearity':linearity})
    else:
        return redirect('/logout')

def viewMasterLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        part = range(1, int(linearity.linearity_npart)+1)
        measurement = range(1, int(linearity.linearity_nmeasurement)+1)
        return render(request,'linearity/master_linearity.html',{'part':part, 'measurement':measurement, 'linearity':linearity})
    else:
        return redirect('/logout')

def viewAverageLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        part = range(1, int(linearity.linearity_npart)+1)
        measurement = range(1, int(linearity.linearity_nmeasurement)+1)
        return render(request,'linearity/average_linearity.html',{'part':part, 'measurement':measurement, 'linearity':linearity})
    else:
        return redirect('/logout')

def storeMasterLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        linearity.linearity_master = request.POST.getlist('linearity_master')
        linearity.save()

        return redirect('coretoolcrud:viewLinearity',pk )
    else:
        return redirect('/logout')

def storeAverageLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        linearity.linearity_average = request.POST.getlist('linearity_average')
        linearity.linearity_ave_measured = request.POST.get('linearity_ave_measured')
        linearity.linearity_ave_reviewed = request.POST.get('linearity_ave_reviewed')

        temppart = []
        temptrial = []
        iter = 1

        for i in range(int(linearity.linearity_npart) * int(linearity.linearity_nmeasurement)):
            if iter % int(linearity.linearity_nmeasurement) != 0:
                temppart.append(linearity.linearity_average[i])
                iter = iter + 1
            else:
                if iter % (int(linearity.linearity_npart) * int(linearity.linearity_nmeasurement)) == 0:
                    temppart.append(linearity.linearity_average[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    temppart = []
                    iter = iter + 1
                else:
                    temppart.append(linearity.linearity_average[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    temppart = []
                    iter = iter + 1
        
        linearity.linearity_average = temptrial

        tempmaster = []
        for ele in linearity.linearity_average:
            tempmaster.append(sum(ele) / len(ele))

        linearity.linearity_master = [float(i) for i in tempmaster]
        linearity.save()

        part = range(1, int(linearity.linearity_npart)+1)
        measurement = range(int(linearity.linearity_nmeasurement))
        return render(request,'linearity/all_linearity.html',{'part':part, 'measurement':measurement, 'linearity':linearity})
    else:
        return redirect('/logout')

def storeAllLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)

        temppart = []
        temptrial = []
        iter = 1

        linearity.linearity_all = request.POST.getlist('linearity_all')
        for i in range(int(linearity.linearity_npart) * int(linearity.linearity_nmeasurement)):
            if iter % int(linearity.linearity_nmeasurement) != 0:
                temppart.append(linearity.linearity_all[i])
                iter = iter + 1
            else:
                if iter % (int(linearity.linearity_npart) * int(linearity.linearity_nmeasurement)) == 0:
                    temppart.append(linearity.linearity_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    temppart = []
                    iter = iter + 1
                else:
                    temppart.append(linearity.linearity_all[i])
                    temppart = [float(i) for i in temppart]
                    temptrial.append(temppart)
                    temppart = []
                    iter = iter + 1
        
        linearity.linearity_all = temptrial
        linearity.save()
        return redirect('coretoolcrud:viewCommentLinearity', pk)
    else:
        return redirect('/logout')

def viewCommentLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        linearity.linearity_master = [float(i) for i in linearity.linearity_master]
        avemaster = sum(linearity.linearity_master) / len(linearity.linearity_master)

        xbar = []
        for i in linearity.linearity_all:
            xbar.append(sum(i) / len(i))
        
        stdev = []
        for i in linearity.linearity_all:
            stdev.append(np.std(i, ddof=1))
        
        n1 = []
        for i in range(int(linearity.linearity_npart)):
            n1.append(abs((xbar[i] - linearity.linearity_master[i]) * 12 ** 0.5 / stdev[i]))
        
        pvalue = []
        for i in range(int(linearity.linearity_npart)):
            pvalue.append(stats.t.sf(n1[i], df=int(linearity.linearity_nmeasurement)-1) * 2)
        
        bias = []
        temp = []
        for i in  range(int(linearity.linearity_npart)):
            for j in  range(int(linearity.linearity_nmeasurement)):
                temp.append(linearity.linearity_all[i][j] - linearity.linearity_master[i])
            bias.append(temp)
            temp = []
        
        averagebias = []
        temp = []
        for i in range(int(linearity.linearity_npart)):
            for j in range(int(linearity.linearity_nmeasurement)):
                temp.append(bias[i][j])
            averagebias.append(sum(temp) / len(temp))
            temp = []

        averagebiasall = sum(averagebias) / len(averagebias)

        x = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(linearity.linearity_master[j])
            x.append(temp)
            temp = []
        
        y = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(bias[j][i])
            y.append(temp)
            temp = []
        
        xy = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(x[i][j] * y[i][j])
            xy.append(temp)
            temp = []
        
        xx = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(x[i][j] * x[i][j])
            xx.append(temp)
            temp = []

        yy = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(y[i][j] * y[i][j])
            yy.append(temp)
            temp = []
        
        jmlx = 0
        avex = 0
        jmly = 0
        avey = 0
        jmlxy = 0
        avexy = 0
        jmlxx = 0
        avexx = 0
        jmlyy = 0
        aveyy = 0
        gm = 0
        gm2 = 0
        sgm = 0

        for i in x:
            jmlx = jmlx + sum(i)
            avex = avex + len(i)
        avex = jmlx / avex

        for i in y:
            jmly = jmly + sum(i)
            avey = avey + len(i)
        avey = jmly / avey

        for i in xy:
            jmlxy = jmlxy + sum(i)
            avexy = avexy + len(i)
        avexy = jmlxy / avexy

        for i in xx:
            jmlxx = jmlxx + sum(i)
            avexx = avexx + len(i)
        avexx = jmlxx / avexx

        for i in yy:
            jmlyy = jmlyy + sum(i)
            aveyy = aveyy + len(i)
        aveyy = jmlyy / aveyy

        gm = int(linearity.linearity_npart) * int(linearity.linearity_nmeasurement)
        gm2 = gm - 2
        sgm = 1 / gm2

        a = (jmlxy - (jmlx * jmly / gm)) / (jmlxx - jmlx ** 2 / 60)
        b = avey - a * avex
        s = ((jmlyy - b * jmly - a * jmlxy) / gm2) ** 0.5

        temp =(1 - linearity.linearity_confidence) / 2
        print("temp", temp)
        t = stats.t.ppf(1-temp, gm2)

        xoxbar = []
        xoxbar2 = []

        for i in linearity.linearity_master:
            xoxbar.append((i - avemaster) ** 2)
            xoxbar2.append(((i - avemaster) ** 2) ** 2)

        sumxoxbar = sum(xoxbar) * int(linearity.linearity_nmeasurement)
        sumxoxbar2 = sum(xoxbar2)

        rasio = []
        for i in xoxbar:
            rasio.append(i / sumxoxbar)
        
        sum05 = []
        for i in rasio:
            sum05.append((i + sgm) ** 0.5)
        
        cbv = []
        for i in sum05:
            cbv.append(i * s * t)
        
        baxo = []
        for i in linearity.linearity_master:
            baxo.append(b + a * i)
        
        upper = []
        lower = []

        for i in range(int(linearity.linearity_npart)):
            upper.append(baxo[i] + cbv[i])
            lower.append(baxo[i] - cbv[i])
        
        print("gm2", gm2)
        print("i s t", i, s, t)

        tabs = abs(abs(a) / (s / (sumxoxbar ** 0.5)))
        tb =  abs(b) / (sgm + avemaster ** 2 / sumxoxbar2) ** 0.5 / s

        p = figure(title="Linearity", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Bias', x_axis_label='Reference Value')
        for i in range(int(linearity.linearity_nmeasurement)):
            p.scatter(x[i], y[i], marker="circle")
        
        p.scatter(linearity.linearity_master, upper, color="green")
        p.line(linearity.linearity_master, upper, color="green", legend_label='Upper', line_width=2)
        p.scatter(linearity.linearity_master, lower, color="red")
        p.line(linearity.linearity_master, lower, color="red", legend_label='Lower', line_width=2)
        p.scatter(linearity.linearity_master, averagebias, color="orange")
        p.line(linearity.linearity_master, averagebias, color="orange", legend_label='Average Bias', line_width=2)
        
        scriptbiasref, divbiasref = components(p)

        survey = Survey.objects.get(id = linearity.linearity_survey_id)
        
        npart = range(1, int(linearity.linearity_npart)+1)
        nmeasurement = range(1, int(linearity.linearity_nmeasurement)+1)
        gabung = zip(linearity.linearity_all, range(1, int(linearity.linearity_npart)+1))
        gabung2 = zip(bias, range(1, int(linearity.linearity_npart)+1))
        gabung3 = zip(xbar, averagebias, range(1, int(linearity.linearity_npart)+1))
        gabung4 = zip(linearity.linearity_master, averagebias, pvalue, range(1, int(linearity.linearity_npart)+1))
        

        return render(request,'linearity/comment_linearity.html', {'linearity':linearity, 'survey':survey, 'a':a, 'b':b, 's':s, 't':t, 'tabs':tabs, 'tb':tb, 'npart':npart, 'nmeasurement':nmeasurement, 'gabung':gabung, 'gabung2':gabung2, 'gabung3':gabung3, 'gabung4':gabung4, 'scriptbiasref':scriptbiasref, 'divbiasref':divbiasref})
    else:
        return redirect('/logout')

def storeCommentLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)

        linearity.linearity_biasref = request.POST.get('linearity_biasref')
        linearity.linearity_recommendation = request.POST.get('linearity_recommendation')
        linearity.save()

        # return render(request,'linearity/comment_linearity.html', {'linearity':linearity, 'survey':survey})
        return redirect('coretoolcrud:viewFinalLinearity',linearity.linearity_survey_id )
    else:
        return redirect('/logout')

def viewFinalLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        linearity.linearity_master = [float(i) for i in linearity.linearity_master]
        avemaster = sum(linearity.linearity_master) / len(linearity.linearity_master)

        xbar = []
        for i in linearity.linearity_all:
            xbar.append(sum(i) / len(i))
        
        stdev = []
        for i in linearity.linearity_all:
            stdev.append(np.std(i, ddof=1))
        
        n1 = []
        for i in range(int(linearity.linearity_npart)):
            n1.append(abs((xbar[i] - linearity.linearity_master[i]) * 12 ** 0.5 / stdev[i]))
        
        pvalue = []
        for i in range(int(linearity.linearity_npart)):
            pvalue.append(stats.t.sf(n1[i], df=int(linearity.linearity_nmeasurement)-1) * 2)
        
        bias = []
        temp = []
        for i in  range(int(linearity.linearity_npart)):
            for j in  range(int(linearity.linearity_nmeasurement)):
                temp.append(linearity.linearity_all[i][j] - linearity.linearity_master[i])
            bias.append(temp)
            temp = []
        

        averagebias = []
        temp = []
        for i in range(int(linearity.linearity_npart)):
            for j in range(int(linearity.linearity_nmeasurement)):
                temp.append(bias[i][j])
            averagebias.append(sum(temp) / len(temp))
            temp = []

        averagebiasall = sum(averagebias) / len(averagebias)

        x = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(linearity.linearity_master[j])
            x.append(temp)
            temp = []
        
        y = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(bias[j][i])
            y.append(temp)
            temp = []
        
        xy = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(x[i][j] * y[i][j])
            xy.append(temp)
            temp = []
        
        xx = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(x[i][j] * x[i][j])
            xx.append(temp)
            temp = []

        yy = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(y[i][j] * y[i][j])
            yy.append(temp)
            temp = []
        
        jmlx = 0
        avex = 0
        jmly = 0
        avey = 0
        jmlxy = 0
        avexy = 0
        jmlxx = 0
        avexx = 0
        jmlyy = 0
        aveyy = 0
        gm = 0
        gm2 = 0
        sgm = 0

        for i in x:
            jmlx = jmlx + sum(i)
            avex = avex + len(i)
        avex = jmlx / avex

        for i in y:
            jmly = jmly + sum(i)
            avey = avey + len(i)
        avey = jmly / avey

        for i in xy:
            jmlxy = jmlxy + sum(i)
            avexy = avexy + len(i)
        avexy = jmlxy / avexy

        for i in xx:
            jmlxx = jmlxx + sum(i)
            avexx = avexx + len(i)
        avexx = jmlxx / avexx

        for i in yy:
            jmlyy = jmlyy + sum(i)
            aveyy = aveyy + len(i)
        aveyy = jmlyy / aveyy

        gm = int(linearity.linearity_npart) * int(linearity.linearity_nmeasurement)
        gm2 = gm - 2
        sgm = 1 / gm2

        a = (jmlxy - (jmlx * jmly / gm)) / (jmlxx - jmlx ** 2 / 60)
        b = avey - a * avex
        s = ((jmlyy - b * jmly - a * jmlxy) / gm2) ** 0.5

        temp =(1 - linearity.linearity_confidence) / 2
        print("temp", temp)
        t = stats.t.ppf(1-temp, gm2)

        xoxbar = []
        xoxbar2 = []

        for i in linearity.linearity_master:
            xoxbar.append((i - avemaster) ** 2)
            xoxbar2.append(((i - avemaster) ** 2) ** 2)

        sumxoxbar = sum(xoxbar) * int(linearity.linearity_nmeasurement)
        sumxoxbar2 = sum(xoxbar2)

        rasio = []
        for i in xoxbar:
            rasio.append(i / sumxoxbar)
        
        sum05 = []
        for i in rasio:
            sum05.append((i + sgm) ** 0.5)
        
        cbv = []
        for i in sum05:
            cbv.append(i * s * t)
        
        baxo = []
        for i in linearity.linearity_master:
            baxo.append(b + a * i)
        
        upper = []
        lower = []

        for i in range(int(linearity.linearity_npart)):
            upper.append(baxo[i] + cbv[i])
            lower.append(baxo[i] - cbv[i])
        
        # print("gm2", gm2)
        # print("i s t", i, s, t)

        tabs = abs(abs(a) / (s / (sumxoxbar ** 0.5)))
        tb =  abs(b) / (sgm + avemaster ** 2 / sumxoxbar2) ** 0.5 / s

        p = figure(title="Linearity", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Bias', x_axis_label='Reference Value')
        for i in range(int(linearity.linearity_nmeasurement)):
            p.scatter(x[i], y[i], marker="circle")
        
        p.scatter(linearity.linearity_master, upper, color="green")
        p.line(linearity.linearity_master, upper, color="green", legend_label='Upper', line_width=2)
        p.scatter(linearity.linearity_master, lower, color="red")
        p.line(linearity.linearity_master, lower, color="red", legend_label='Lower', line_width=2)
        p.scatter(linearity.linearity_master, averagebias, color="orange")
        p.line(linearity.linearity_master, averagebias, color="orange", legend_label='Average Bias', line_width=2)
        
        scriptbiasref, divbiasref = components(p)

        survey = Survey.objects.get(id = linearity.linearity_survey_id)
        
        npart = range(1, int(linearity.linearity_npart)+1)
        nmeasurement = range(1, int(linearity.linearity_nmeasurement)+1)
        gabung = zip(linearity.linearity_all, range(1, int(linearity.linearity_npart)+1))
        gabung2 = zip(bias, range(1, int(linearity.linearity_npart)+1))
        gabung3 = zip(xbar, averagebias, range(1, int(linearity.linearity_npart)+1))
        gabung4 = zip(linearity.linearity_master, averagebias, pvalue, range(1, int(linearity.linearity_npart)+1))
        

        return render(request,'linearity/collection_linearity.html', {'linearity':linearity, 'survey':survey, 'a':a, 'b':b, 's':s, 't':t, 'tabs':tabs, 'tb':tb, 'npart':npart, 'nmeasurement':nmeasurement, 'gabung':gabung, 'gabung2':gabung2, 'gabung3':gabung3, 'gabung4':gabung4, 'scriptbiasref':scriptbiasref, 'divbiasref':divbiasref})
    else:
        return redirect('/logout')

def viewPrintLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        linearity.linearity_master = [float(i) for i in linearity.linearity_master]
        avemaster = sum(linearity.linearity_master) / len(linearity.linearity_master)

        xbar = []
        for i in linearity.linearity_all:
            xbar.append(sum(i) / len(i))
        
        stdev = []
        for i in linearity.linearity_all:
            stdev.append(np.std(i, ddof=1))
        
        n1 = []
        for i in range(int(linearity.linearity_npart)):
            n1.append(abs((xbar[i] - linearity.linearity_master[i]) * 12 ** 0.5 / stdev[i]))
        
        pvalue = []
        for i in range(int(linearity.linearity_npart)):
            pvalue.append(stats.t.sf(n1[i], df=int(linearity.linearity_nmeasurement)-1) * 2)
        
        bias = []
        temp = []
        for i in  range(int(linearity.linearity_npart)):
            for j in  range(int(linearity.linearity_nmeasurement)):
                temp.append(linearity.linearity_all[i][j] - linearity.linearity_master[i])
            bias.append(temp)
            temp = []
        

        averagebias = []
        temp = []
        for i in range(int(linearity.linearity_npart)):
            for j in range(int(linearity.linearity_nmeasurement)):
                temp.append(bias[i][j])
            averagebias.append(sum(temp) / len(temp))
            temp = []

        averagebiasall = sum(averagebias) / len(averagebias)

        x = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(linearity.linearity_master[j])
            x.append(temp)
            temp = []
        
        y = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(bias[j][i])
            y.append(temp)
            temp = []
        
        xy = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(x[i][j] * y[i][j])
            xy.append(temp)
            temp = []
        
        xx = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(x[i][j] * x[i][j])
            xx.append(temp)
            temp = []

        yy = []
        temp = []
        for i in range(int(linearity.linearity_nmeasurement)):
            for j in range(int(linearity.linearity_npart)):
                temp.append(y[i][j] * y[i][j])
            yy.append(temp)
            temp = []
        
        jmlx = 0
        avex = 0
        jmly = 0
        avey = 0
        jmlxy = 0
        avexy = 0
        jmlxx = 0
        avexx = 0
        jmlyy = 0
        aveyy = 0
        gm = 0
        gm2 = 0
        sgm = 0

        for i in x:
            jmlx = jmlx + sum(i)
            avex = avex + len(i)
        avex = jmlx / avex

        for i in y:
            jmly = jmly + sum(i)
            avey = avey + len(i)
        avey = jmly / avey

        for i in xy:
            jmlxy = jmlxy + sum(i)
            avexy = avexy + len(i)
        avexy = jmlxy / avexy

        for i in xx:
            jmlxx = jmlxx + sum(i)
            avexx = avexx + len(i)
        avexx = jmlxx / avexx

        for i in yy:
            jmlyy = jmlyy + sum(i)
            aveyy = aveyy + len(i)
        aveyy = jmlyy / aveyy

        gm = int(linearity.linearity_npart) * int(linearity.linearity_nmeasurement)
        gm2 = gm - 2
        sgm = 1 / gm2

        a = (jmlxy - (jmlx * jmly / gm)) / (jmlxx - jmlx ** 2 / 60)
        b = avey - a * avex
        s = ((jmlyy - b * jmly - a * jmlxy) / gm2) ** 0.5

        temp =(1 - linearity.linearity_confidence) / 2
        print("temp", temp)
        t = stats.t.ppf(1-temp, gm2)

        xoxbar = []
        xoxbar2 = []

        for i in linearity.linearity_master:
            xoxbar.append((i - avemaster) ** 2)
            xoxbar2.append(((i - avemaster) ** 2) ** 2)

        sumxoxbar = sum(xoxbar) * int(linearity.linearity_nmeasurement)
        sumxoxbar2 = sum(xoxbar2)

        rasio = []
        for i in xoxbar:
            rasio.append(i / sumxoxbar)
        
        sum05 = []
        for i in rasio:
            sum05.append((i + sgm) ** 0.5)
        
        cbv = []
        for i in sum05:
            cbv.append(i * s * t)
        
        baxo = []
        for i in linearity.linearity_master:
            baxo.append(b + a * i)
        
        upper = []
        lower = []

        for i in range(int(linearity.linearity_npart)):
            upper.append(baxo[i] + cbv[i])
            lower.append(baxo[i] - cbv[i])
        
        # print("gm2", gm2)
        # print("i s t", i, s, t)

        tabs = abs(abs(a) / (s / (sumxoxbar ** 0.5)))
        tb =  abs(b) / (sgm + avemaster ** 2 / sumxoxbar2) ** 0.5 / s

        p = figure(title="Linearity", tools="pan,wheel_zoom,box_zoom,reset,hover", sizing_mode="stretch_width", y_axis_label='Bias', x_axis_label='Reference Value')
        for i in range(int(linearity.linearity_nmeasurement)):
            p.scatter(x[i], y[i], marker="circle")
        
        p.scatter(linearity.linearity_master, upper, color="green")
        p.line(linearity.linearity_master, upper, color="green", legend_label='Upper', line_width=2)
        p.scatter(linearity.linearity_master, lower, color="red")
        p.line(linearity.linearity_master, lower, color="red", legend_label='Lower', line_width=2)
        
        scriptbiasref, divbiasref = components(p)

        survey = Survey.objects.get(id = linearity.linearity_survey_id)
        
        npart = range(1, int(linearity.linearity_npart)+1)
        nmeasurement = range(1, int(linearity.linearity_nmeasurement)+1)
        gabung = zip(linearity.linearity_all, range(1, int(linearity.linearity_npart)+1))
        gabung2 = zip(bias, range(1, int(linearity.linearity_npart)+1))
        gabung3 = zip(xbar, averagebias, range(1, int(linearity.linearity_npart)+1))
        

        return render(request,'linearity/print_linearity.html', {'linearity':linearity, 'survey':survey, 'a':a, 'b':b, 's':s, 't':t, 'tabs':tabs, 'tb':tb, 'npart':npart, 'nmeasurement':nmeasurement, 'gabung':gabung, 'gabung2':gabung2, 'gabung3':gabung3, 'scriptbiasref':scriptbiasref, 'divbiasref':divbiasref})
    else:
        return redirect('/logout')

def deleteLinearity(request, pk):
    if 'user' in request.session:
        linearity = Linearity.objects.get(linearity_survey_id = pk)
        linearity.delete()
        messages.success(request, "Linearity berhasil dihapus")
        return redirect('coretoolcrud:viewDetailSurvey', pk)
    else:
        return redirect('/logout')