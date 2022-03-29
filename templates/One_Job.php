{% extends "base.php" %}

{% block title %}
User site
{% endblock %}

{% block details %}
User Name
{% endblock %}

{% block body %}
onload="showOneJob({{JID}})";
{% endblock %}

{% block navbar_links %}
<li class="nav-item">
    <a class="nav-link active" aria-current="page" href="/user">
        Home Dashboard
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" aria-current="page" href="/apply">
        Apply for a Job
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" aria-current="page" href="/applications">
        View applications
    </a>
</li>
{% endblock %}


{% block content %}
<h1 class="h2 mt-3 mb-4" id="job_title"></h1>
<table class="table">
  <thead>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Company</th>
      <td id="company"></td>
    </tr>
    <tr>
      <th scope="row">Industry</th>
      <td id="industry"></td>
    </tr>
    <tr>
      <th scope="row">Date Posted</th>
      <td id="date"></td>
    </tr>
    <tr>
      <th scope="row">Employment Type</th>
      <td id="type"></td>
    </tr>
    <tr>
      <th scope="row">Job Description</th>
      <td id="job_description"></td>
    </tr>
    <tr>
      <th scope="row">Location</th>
      <td id="location"></td>
    </tr>
    <tr>
      <th scope="row">Salary</th>
      <td id="salary"></td>
    </tr>
    <tr>
      <th scope="row">Vacancy</th>
      <td id="vacancy"></td>
    </tr>
    <tr>
      <th scope="row">Contact Person</th>
      <td id="person"></td>
    </tr>
    <tr>
      <th scope="row">Contact Email</th>
      <td id="email"></td>
    </tr>
  </tbody>
</table>
<button type="button" class="btn btn-success btn-lg">Apply</button>
{% endblock %}

{% block popup %} 
{% endblock %}

{% block script %}

<script>

    function showOneJob(JID) {

        var request = new XMLHttpRequest();
        request.open('GET', 'http://127.0.0.1:5001/jobs/'+JID, true);
        
        request.onload = function() {  

            var json_obj = JSON.parse(request.responseText);
            var jobs = JSON.parse(json_obj.data);

            var job_title = jobs[JID].job_title;
            var email = jobs[JID].contact_email;
            var person = jobs[JID].contact_person;
            var company = jobs[JID].company_name;
            var type = jobs[JID].employment_type;
            var date = jobs[JID].posted_timestamp;
            var vacancy = jobs[JID].vacancy;
            var location = jobs[JID].location;
            var salary = jobs[JID].salary;
            var job_description = jobs[JID].job_description;
            var industry = jobs[JID].industry;

            //var date = datetime.substring(0,10); - want to show only date
            document.getElementById("job_title").innerHTML=job_title;
            document.getElementById("company").innerHTML=company;
            document.getElementById("email").innerHTML=email;
            document.getElementById("person").innerHTML=person;
            document.getElementById("type").innerHTML=type;
            document.getElementById("industry").innerHTML=industry;
            document.getElementById("job_description").innerHTML=job_description;
            document.getElementById("location").innerHTML=location;
            document.getElementById("salary").innerHTML=salary;
            document.getElementById("vacancy").innerHTML=vacancy;
            document.getElementById("date").innerHTML=date;
        };           
        
        request.send();
        //console.log('OPENED', request.readyState); // readyState will be 1
    }


</script>
 
{% endblock %}