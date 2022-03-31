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
    <a class="nav-link" aria-current="page" href="/view">
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

<button type="button" class="btn btn-success btn-lg" data-toggle="modal" data-target="#newApp">Apply</button>
{% endblock %}

{% block popup %} 
<div class="modal fade" id="newApp" tabindex="-1" role="dialog" aria-labelledby="newApp" aria-hidden="true">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">

            <div class="modal-header">
                <h5 class="modal-title">Create a New Application</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>

            <div class="modal-body">
                <form method="POST">

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="job_title">First Name</label>
                            <input type="text" class="form-control" id="first" placeholder="Type here...">
                        </div>
                    </div>

                    <!-- second row category  -->
                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="company_name" class="form-label">Last Name</label>
                            <input type="text" class="form-control" id="last" placeholder="Type here...">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="employment_type" class="form-label">Nationality</label>
                            <input type="text" class="form-control" id="nationality">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="industry" class="form-label">Date of Birth</label>
                            <input type="date" class="form-control" id="dob">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="location" class="form-label">Phone</label>
                            <input type="number" class="form-control" id="phone" placeholder="">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="location" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email">
                        </div>
                    </div>

                    <!-- second row category  -->
                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="job_description" class="form-label">Work Experience</label>
                            <textarea class="form-control" id="experience" rows="3"></textarea>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="job_description" class="form-label">Skills</label>
                            <textarea class="form-control" id="skills" rows="3"></textarea>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="job_description" class="form-label">Educational Background</label>
                            <textarea class="form-control" id="education" rows="3"></textarea>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button id="closemodal" type="submit" class="btn btn-primary" data-dismiss="modal" onclick="addApp()">Send Application</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block script %}

<script>

    function showOneJob(JID) {

        var request = new XMLHttpRequest();
        request.open('GET', "http://127.0.0.1:5008/view_job/"+JID, true);
        request.onload = function() {  

            var json_obj = JSON.parse(request.responseText);
            console.log(json_obj);
            // var jobs = json.loads(json.obj);
            var jobs = JSON.parse(json_obj.result);

            console.log(jobs);

            var job_title = jobs.job_title;
            var email = jobs.contact_email;
            var person = jobs.contact_person;
            var company = jobs.company_name;
            var type = jobs.employment_type;
            var date = jobs.posted_timestamp;
            var vacancy = jobs.vacancy;
            var location = jobs.location;
            var salary = jobs.salary;
            var job_description = jobs.job_description;
            var industry = jobs.industry;

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

      function addApp(){

        var request = new XMLHttpRequest();

        var first = document.getElementById("first").value;
        var last = document.getElementById("last").value;
        var dob = document.getElementById("dob").value;
        var phone = document.getElementById("phone").value;
        var email = document.getElementById("email").value;
        var experience = document.getElementById("experience").value;
        var skills = document.getElementById("skills").value;
        var education = document.getElementById("education").value;
        var nationality = document.getElementById("nationality").value;
        var job_title = document.getElementById("job_title").value;
        
        console.log(first);
        console.log(email);

        var applyjobcms = "http://192.168.0.125:5008/apply_job"
        var params = '{'+'"JID":"'+{{JID}}+'","job_title":"'+job_title'","first":"'+first+'","last":"'+last+'","dob":"'+dob+'","phone":"'+phone+'","email":"'+email+'","experience":"'+experience+'","skills":"'+skills+'","education":"'+education+'","nationality":"'+nationality+'"}';
        console.log(params);
        request.open('POST',applyjobcms, true);

        request.onload = function() {  
            var json_obj = JSON.parse(request.responseText);
            console.log("this is json_obj",json_obj)

            if (json_obj.code >= 200 & json_obj.code < 400) {
                alert('Your application has been made!');
            } 
            else {
                alert('Oops! Something went wrong...');
            }
        };
        request.send(params);
   }
  

</script>
 
{% endblock %}