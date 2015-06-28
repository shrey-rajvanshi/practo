
function search(){
	city =document.getElementById("location").value;
	speciality= document.getElementById("specialization").value;
	if (city == "" ||speciality=="") {alert("Empty values");}
	if(speciality=="")	{window.location+=("search/"+city);}
	else{
	window.location+=("search/"+city+"/"+speciality);}
}

