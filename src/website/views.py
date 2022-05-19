from tkinter import N
from unicodedata import category
from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import math
def selectbelt(hp,w1):
    if (w1/(2*math.pi))/hp > 40 or (w1/(2*math.pi))>=3225 :
        if hp<=100:
            v2 = 3
    elif 4 < (w1/(2*math.pi))/hp < 40 :
        if hp <= 400:
            v2 = 5
    elif 0.3<(w1/(2*math.pi))/hp<4 :
        if hp<=1000:
            v2 = 8
    return v2

def approximateRPM(d1 , w1 , SPD , v):
    VR = w1 / w2

    d2 = VR * d1

    for x in SPD[v]:
        if (x - d2)>=0:
            d2 = x
            break
        if x==SPD[v][-1]:
            d2 = x

    w2 = w1*d1/d2
    return w2

def AvailableDiameter(d , SPD , v):
    for x in SPD[v]:
        if (x - d)>=0:
         d = x
         break
        if x==SPD[v][-1]:
            d = x
    return d
def checkAvailable(d , SPD , v):
    check = False
    for x in SPD[v]:
        if x == d:
            check = True
    if check == False:
        return 'Not Available'
    if check == True:
        return 'Available'
        
def getSecondDiameter(d1 , w1 , w2 , SPD , v ):
    VR = w1 / w2

    d2 = VR * d1

    for x in SPD[v]:
        if (x - d2)>=0:
            d2 = x
            break
        if x==SPD[v][-1]:
            d2 = x
    return d2
def AvailableLength(L ,VBL , v):
    for x in VBL[v]:
        if (x - L)>0:
            L = x
            break
        if x==VBL[v][-1]:
            L = x
    return L
def BFormula(L, d1, d2):
    return 4*L - (2*math.pi*(d2+d1))
def CFormula(B, d1, d2):
    return (B + math.sqrt(B**2 - 32*(d2-d1)**2))/16
vb = 4500
status = True
SPD = {

    3: [2.2, 2.3, 2.5, 2.6, 2.8, 3.0, 3.1, 3.3, 3.6, 4.1, 4.5,
        4.7, 5.0, 5.3, 5.6, 6.0, 6.5, 6.9, 8.0, 10.6, 14.0, 19.0, 25.0, 33.5],

    5: [4.3, 4.5, 4.8, 4.9, 5.1, 5.4, 5.5, 5.8, 5.9, 6.2, 6.3, 6.6,
        6.7, 7.0, 7.1, 7.5, 8.1, 8.4, 8.9, 9.2, 9.7, 10.2, 11.1, 12.5,
        13.9, 15.5, 16.1, 18.5, 20.1, 23.5, 25.1, 27.9],

    8: [12.3, 13.0, 13.8, 14.8, 15.8, 16.8, 17.8, 18.8, 19.8, 21.0,
        22.2, 29.8, 39.8, 47.8, 52.8, 57.8, 63.8]

}
VBL = {

    3: [25.0, 26.5, 28.0, 30.0, 31.5, 33.5, 35.5, 37.5, 40.0, 42.5,
        45.0, 47.5, 50.0, 53.0, 56.0, 60.0, 63.0, 67.0, 71.0, 75.0,
        80.0, 85.0, 90.0, 95.0, 100.0, 106.0, 112.0, 118.0, 125.0, 132.0, 140.0],

    5: [50.0, 53.0, 56.0, 60.0, 63.0, 67.0, 71.0, 75.0, 80.0, 85.0,
        90.0, 95.0, 100.0, 106.0, 112.0, 118.0, 125.0, 132.0, 140.0,
        150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 212.0, 224.0, 263.0,
        250.0, 265.0, 280.0, 300.0, 315.0, 335.0, 355.0],

    8: [100.0, 112.0, 118.0, 125.0, 132.0, 140.0, 150.0, 160.0, 170.0,
        180.0, 190.0, 200.0, 212.0, 224.0, 236.0, 250.0, 265.0, 280.0,
        300.0, 315.0, 335.0, 355.0, 400.0, 450.0]

}

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
# @login_required
def home():
    result=None
    horsepower=None
    rpm1=None
    rpm2=None
    Test=None
    v=None
    calcd1=None
    C=None
    finalS=None
    L=None
    calcd2=None
    d2=None
    status=None
    d1=None
    if request.method=='POST':
        horsepower = (request.form.get('horsepower'))
        rpm1=(request.form.get('rpm1'))
        rpm2=(request.form.get('rpm2'))
        d2=(request.form.get('d2'))
        rpmP=str(request.form.get('precisionW'))    
        diameter2P=str(request.form.get('precisionD'))
        d1=request.form.get('d1')
        #Try=(rpm1)+(rpm2)
        #print(Try)
        if not horsepower==None and not rpm1==None and horsepower!="" and rpm1 != "":
            horsepower=float(horsepower)
            rpm1=float(rpm1)
            
            if not rpm2==None and rpm2!="":
                rpm2=float(rpm2)
                if rpm1 < rpm2:
                    w1 = rpm2*(2*math.pi)
                    w2 = rpm1*(2*math.pi)
                else:
                    w1 = rpm1*(2*math.pi)
                    w2 = rpm2*(2*math.pi)
                v = selectbelt(horsepower, w1)
                if not d1==None and d1!="":
                    d1=float(d1)                    
                    if checkAvailable(d1, SPD , v)=='Available':
                        calcd1=d1
                    else:
                        flash('The diameter desired for the primary shaft is not available, find below an appropriate one', category="error")
                if calcd1==None:
                    calcd1 = 2*(vb/w1)*12
                    calcd1 = AvailableDiameter(calcd1, SPD, v)
                if rpmP=='approximate':
                    if not d2==None and d2!="":
                        d2=float(d2)
                        if diameter2P=='exact':
                            if checkAvailable(d2,SPD,v)=='Available':
                                calcd2=d2
                                status=True
                            else:
                                status=False
                                flash('The desired diameter for the secondary shaft is NOT available', category="error")
                        else:
                            status=True
                            calcd2=AvailableDiameter(d2,SPD,v)
                    else:
                        calcd2 = getSecondDiameter(calcd1, w1, w2, SPD, v)
                        status=True
                        
                    if status==True:
                        w2 = w1*calcd1/calcd2
                        b = int((calcd1*w1)/(2*12))
                        C = math.ceil((calcd2 + (3*(calcd1+calcd2)))/2)
                        L = 2*C + (math.pi/2)*(calcd1+calcd2) + ((calcd2-calcd1)**2)/(4*C)
                        L = AvailableLength(L, VBL, v)
                        B = BFormula(L, calcd1, calcd2)
                        C = CFormula(B, calcd1, calcd2)
                        finalS= w2/(2*math.pi)
                else:
                    if not d2==None and d2!="":
                        d2=float(d2)
                        w1 = rpm1*(2*math.pi)
                        v = selectbelt(horsepower, w1)
                        if calcd1==None:
                            calcd1 = 2*(vb/w1)*12
                            calcd1 = AvailableDiameter(calcd1, SPD, v)
                        calcd2= calcd1*w1/w2
                        if calcd2==d2:
                            status=True
                        else:
                            status=False
                        
                    if status==True:
                        C = math.ceil((calcd2 + (3*(calcd1+calcd2)))/2)
                        L = 2*C + (math.pi/2)*(calcd1+calcd2) + ((calcd2-calcd1)**2)/(4*C)
                        L = AvailableLength(L, VBL, v)
                        B = BFormula(L, calcd1, calcd2)
                        C = CFormula(B, calcd1, calcd2)
                        finalS= int(w2/(2*math.pi))
                    else:
                        flash('There is no diameter for this exact speed of the secondary shaft', category="error")
            elif not d2==None and d2!="":
                
                d2=float(d2)
                w1 = rpm1*(2*math.pi)
                v = selectbelt(horsepower, w1)
                if diameter2P=='exact':
                    if checkAvailable(d2,SPD,v)=='Available':
                        calcd2=d2
                        status=True
                    else:
                        status=False
                        flash('The desired diameter for the secondary shaft is NOT available', category="error")
                else:
                    status=True
                    calcd2=AvailableDiameter(d2,SPD,v)
                if status==True:
                    if not d1==None and d1!="":
                        d1=float(d1)                    
                        if checkAvailable(d1, SPD , v)=='Available':
                            calcd1=d1
                        else:
                            flash('The diameter desired for the primary shaft is not available, find below an appropriate one', category="error")
                    if calcd1==None:
                        calcd1 = 2*(vb/w1)*12
                        calcd1 = AvailableDiameter(calcd1, SPD, v)
                
                    w2 = w1*calcd1/calcd2
                    C = math.ceil((calcd2 + (3*(calcd1+calcd2)))/2)
                    L = 2*C + (math.pi/2)*(calcd1+calcd2) + ((calcd2-calcd1)**2)/(4*C)
                    L = AvailableLength(L, VBL, v)
                    B = BFormula(L, calcd1, calcd2)
                    C = CFormula(B, calcd1, calcd2)
                    finalS= int(w2/(2*math.pi))
        
            else:
                flash('Please input the speed or the diameter of the second shaft', category="error")
        else:
            flash('Please input the Horsepower and the speed of the first shaft', category="error")
    return render_template('home.html',hp=horsepower,rpm_1=rpm1,rpm_2=rpm2, 
    d_2=d2,d_1=d1, beltsize=v, user=-1, diameter1=calcd1, diameter2=calcd2, CentralDistance=C, BeltSpeed=finalS,length=L)#,trying=Try )
