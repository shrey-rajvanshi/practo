
function search(){
	city =document.getElementById("location").value;
	speciality= document.getElementById("specialization").value;
	if(speciality=="")	{window.location+=("search/"+city);}
	else{
	window.location+=("search/"+city+"/"+speciality);}
}

