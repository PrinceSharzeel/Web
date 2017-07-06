from django import forms


class RegistrationForm(forms.Form):
	ffname= forms.CharField(max_length=50)
	flname = forms.CharField(max_length=50)
	fmail = forms.EmailField(max_length=50)
	
	fpswd = forms.CharField(max_length=50)
	fcpswd = forms.CharField(max_length=50)


	        
class StoreForm(forms.Form):
	fsname = forms.CharField( max_length=50)
	fpostcode = forms.CharField(max_length=50)
	fcont = forms.IntegerField(label="Contact")
	
	fadd1 = forms.CharField(label="Add1", max_length=50)
	fadd2 = forms.CharField(label="Add2", max_length=50)
	fcity = forms.CharField(label="City", max_length=50)
	fstate= forms.CharField(label="State", max_length=50)
	wstart=forms.TimeField(label="State")
	wstop=forms.TimeField(label="State")
	wdstart=forms.TimeField(label="State")
	wdstop=forms.TimeField(label="State")


	fcountry = forms.CharField(label="Country", max_length=50)

	fsmail = forms.EmailField(label="Store Mail Address", max_length=50)
	fid = forms.CharField(label="Company Registration ID", max_length=50)
	fvat = forms.CharField(label="VAT Number", max_length=50)

	fweb= forms.CharField(label="Web address", max_length=50)
	fcat= forms.CharField(label="Category", max_length=50)
	flogo=forms.FileField(label="Logo Image 60 X 60",widget=forms.FileInput(attrs={'required':'yes'}))	
	policy=forms.FileField(widget=forms.FileInput(attrs={'required':'yes'}))	


class LoginForm(forms.Form):
	fail=forms.EmailField(label="Email",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','required':'yes'}))
	fswd=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','required':'yes'}))





class Password_Change(forms.Form):
	current_password = forms.CharField(label="Old Password", max_length=30,
										widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'current_password','required':'yes','placeholder':'Old Password'}))
	new_password = forms.CharField(label="New Password", max_length=30,
										widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'new_password','required':'yes','placeholder':'New Password'}))
	retype_password = forms.CharField(label="Retype Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'retype_password','required':'yes','placeholder':'Retype Password'}))                                                    



class ProductForm(forms.Form):
	ptitle = forms.CharField(max_length=50)
	
	ppro=forms.FileField(widget=forms.FileInput(attrs={'required':'yes'}))	
	pbrand = forms.CharField(max_length=50)
	punit = forms.IntegerField()
	plitres = forms.IntegerField()
	pweight= forms.IntegerField()
	package= forms.CharField(max_length=50)
	pmin= forms.IntegerField()
	pmax = forms.IntegerField()
	price = forms.IntegerField()
	pdisc = forms.IntegerField()
	pexp= forms.CharField()
	preddisc = forms.IntegerField()
	pcat=forms.CharField(max_length=50)

class ProductNewForm(forms.Form):
	ptitle = forms.CharField(max_length=50)	
	pbrand = forms.CharField(max_length=50)
	punit = forms.IntegerField()
	plitres = forms.IntegerField()
	pweight= forms.IntegerField()
	package= forms.CharField(max_length=50)
	pmin= forms.IntegerField()
	pmax = forms.IntegerField()
	price = forms.IntegerField()
	pdisc = forms.IntegerField()
	pexp= forms.CharField()
	preddisc = forms.IntegerField()
	pcat=forms.CharField(max_length=50)

class ImageForm(forms.Form):
	ppro=forms.FileField(widget=forms.FileInput(attrs={'required':'yes'}))	

	

class CatForm(forms.Form):
	cat=forms.CharField(label="Item",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','required':'yes'}))



class StoreStatusForm(forms.Form):
	ftime = forms.CharField( max_length=50)
	fmsg= forms.CharField(max_length=50)


