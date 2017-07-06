		
function ValidateForm()
{ 
	if(FormValidation()&&PriceValidation()&&WeightValidation()&&LitreValidation()&&UnitValidation()&&MinValidation()&&MaxValidation()&&discValidation()&&preddiscValidation()&&BrandValidation())
     {return true;}
 else {  console.log(FormValidation());  Materialize.toast('Fill the Form Correctly', 4000,'rounded'); return false;}



}


 function FormValidation(){
    //First Name Validation 
    var fn=document.getElementById('firstname').value;
    if(fn == ""){
        alert('Please Enter Product Name');
        document.getElementById('firstname').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('firstname').style.borderColor = "green";return true;
    }
    if (/^[0-9]+$/.test(document.getElementById("firstname").value)) {
        alert("Product Name Contains Numbers!");
        document.getElementById('firstname').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('firstname').style.borderColor = "green";return true;
    }
    if(fn.length <=2){
        alert('Your Product Name is To Short');
        document.getElementById('firstname').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('firstname').style.borderColor = "green";return true;
    }}
    function BrandValidation(){

    var brand=document.getElementById('pbrand').value;
    if(brand.length <=2){
        alert('Proper Brand Name');
        document.getElementById('pbrand').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('pbrand').style.borderColor = "green";return true;
    }}
    function PriceValidation(){
   
    
   var price=document.getElementById('price').value;
   var regex = /^[1-9]\d*(((,\d{3}){1})?(\.\d{0,2})?)$/;
  
    if(  !regex.test(price) ){
        alert('Improper Price');
        document.getElementById('price').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('price').style.borderColor = "green";return true;
    }




}

function MaxValidation(){
   

   var z=document.getElementById('pmax').value;
   
     if(!/^[0-9]+$/.test(z)){
    alert("Please only enter numeric characters only (Allowed input:0-9)"); document.getElementById('pmax').style.borderColor = "red";
  }else{
        document.getElementById('pmax').style.borderColor = "green";return true;
    }




}

function MinValidation(){
   

 
   var z=document.getElementById('pmin').value;
   
     if(!/^[0-9]+$/.test(z)){
    alert("Please only enter numeric characters only (Allowed input:0-9)"); document.getElementById('pmin').style.borderColor = "red";
  }else{
        document.getElementById('pmin').style.borderColor = "green";return true;
    }



}
function discValidation(){
   

 
   var x=document.getElementById('pdisc').value;
   
       if (isNaN(x) || x < 0 || x > 100) {
    alert("Inavlid Percentage"); document.getElementById('pdisc').style.borderColor = "red";
  }else{
        document.getElementById('pdisc').style.borderColor = "green";return true;
    }

   



}

function preddiscValidation(){
   

 
   
   var price=document.getElementById('preddisc').value;
   var regex = /^[1-9]\d*(((,\d{3}){1})?(\.\d{0,2})?)$/;
  
    if(  !regex.test(price) ){
        alert('Improper Price');
        document.getElementById('preddisc').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('preddisc').style.borderColor = "green";return true;
    }





}








function pexpValidation(){
   

 
   var z=document.getElementById('pmin').value;
   
     if(!/^[0-9]+$/.test(z)){
    alert("Please only enter numeric characters only (Allowed input:0-9)"); document.getElementById('pmin').style.borderColor = "red";
  }else{
        document.getElementById('pmin').style.borderColor = "green";return true;
    }



}




function LitreValidation(){
   

 
   var z=document.getElementById('plitres').value;
   var regex = /^[1-9]\d*(((,\d{3}){1})?(\.\d{0,2})?)$/;
  
    if(  !regex.test(z) ){
        alert('Improper Entry');
        document.getElementById('plitres').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('plitres').style.borderColor = "green";return true;
    }




}
function UnitValidation(){
   

 
   var z=document.getElementById('punit').value;
   
     if(!/^[0-9]+$/.test(z)){
    alert("Please only enter numeric characters only (Allowed input:0-9)"); document.getElementById('punit').style.borderColor = "red";
  }else{
        document.getElementById('punit').style.borderColor = "green";return true;
    }



}
function WeightValidation(){
   

 
    var price=document.getElementById('pweight').value;
   var regex = /^[1-9]\d*(((,\d{3}){1})?(\.\d{0,2})?)$/;
  
    if(  !regex.test(price) ){
        alert('Improper Entry');
        document.getElementById('pweight').style.borderColor = "red";
        return false;
    }else{
        document.getElementById('pweight').style.borderColor = "green";return true;
    }


}





