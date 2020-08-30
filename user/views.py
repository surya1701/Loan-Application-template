from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Prediction
import joblib
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.impute import SimpleImputer

res = 'X'


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        name = request.POST['username']
        pas = request.POST['password']
        user = auth.authenticate(username=name, password=pas)

        if user:
            auth.login(request, user)
            print(user.is_authenticated)
            return redirect("/")
        else:
            messages.info(request, "User does not exist")
            return redirect("login")
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        uname = request.POST['username']
        pas1 = request.POST['password1']
        pas2 = request.POST['password2']
        if pas1 == pas2:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "Username already exists")
                return render(request, "register.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exits")
                return render(request, "register.html")
            else:
                user = User.objects.create_user(username=uname, password=pas1, email=email, first_name=fname,
                                                last_name=lname)
                user.save()
                print('User Created')
                return redirect("login")
        else:
            messages.info(request, "Password does not match")
            return render(request, "register.html")
    else:
        return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


def form(request):
    if request.user.is_authenticated:
        uname = request.user.username
        print(request.user.first_name)
        if Prediction.objects.filter(uname=uname).exists():
            res = Prediction.objects.get(uname=uname).pred
            return redirect("predict")
        else:
            if request.method == "POST":
                gender = request.POST['gender']
                married = request.POST['married']
                depend = request.POST['depend']
                education = request.POST['education']
                self_employ = request.POST['self_employ']
                aincome = request.POST['aincome']
                caincome = request.POST['caincome']
                loanamt = request.POST['loanamt']
                loanterm = request.POST['loanterm']
                credhist = request.POST['credhist']
                area = request.POST['area']

                model = joblib.load('loan.pkl')
                f_new = 'test_Y3wMUE5_7gLdaTN.csv'
                temp = pd.read_csv(f_new, index_col=0)
                col_name_cat = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
                col_name_num = ['Dependents', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
                                'Credit_History']
                df = pd.DataFrame(
                    {"Gender": [gender], "Married": [married], "Dependents": [depend], "Education": [education],
                     "Self_Employed": [self_employ], "ApplicantIncome": [int(aincome)],
                     "CoapplicantIncome": [float(caincome)], "LoanAmount": [float(loanamt)],
                     "Loan_Amount_Term": [float(loanterm)], "Credit_History": [float(credhist)],
                     "Property_Area": [area]})
                print(df)
                df = df.append(temp)
                print(df.dtypes)
                print(df.iloc[0])
                df['Dependents'] = df['Dependents'].replace('3+', '3')
                df['Dependents'] = pd.to_numeric(df['Dependents'], errors='coerce')
                X = df
                categorical = []
                numerical = []
                for feature in list(X.columns):
                    if X[feature].dtypes == object:
                        categorical.append(X[feature])
                    else:
                        numerical.append(X[feature])
                categorical = pd.concat(categorical, axis=1)
                numerical = pd.concat(numerical, axis=1)
                imp_num = SimpleImputer(strategy='mean')
                imp_cat = SimpleImputer(strategy='most_frequent')
                imp_num.fit(numerical)
                imp_cat.fit(categorical)
                numerical = pd.DataFrame(imp_num.transform(numerical), index=df.index,
                                         columns=col_name_num)
                categorical = pd.DataFrame(imp_cat.transform(categorical), index=df.index)
                categorical = pd.get_dummies(categorical, drop_first=True)
                categorical.columns = ['Male', 'Married', 'Not Graduate', 'Self-Employed', 'SemiUrban', 'Urban']
                X = pd.concat([categorical, numerical], axis=1)
                X = scale(X)
                res = model.predict([X[0]])[0]
                user = Prediction(uname=uname,
                                  gender=gender,
                                  married=married,
                                  depend=depend,
                                  education=education,
                                  self_employ=self_employ,
                                  aincome=aincome,
                                  caincome=caincome,
                                  loanamt=loanamt,
                                  loanterm=loanterm,
                                  credhist=credhist,
                                  area=area,
                                  pred=res)
                user.save()
                print('User Created')
                return redirect("predict")
            else:
                return render(request, "form.html")
    else:
        return redirect("/")


def predict(request):
    if request.method == "POST":
        Prediction.objects.get(uname=request.user.username).delete()
        return redirect('form')
    else:
        user = Prediction.objects.get(uname=request.user.username)
        return render(request, "predict.html", {"user": user})
