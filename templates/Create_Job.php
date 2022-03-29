{% extends "base.php" %}

{% block title %}
Owner site
{% endblock %}

{% block details %}
Company Name
{% endblock %}

{% block body %}
{% endblock %}

{% block navbar_links %}
<li class="nav-item">
    <a class="nav-link active" aria-current="page" href="/owner">
        Home Dashboard
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" aria-current="page" href="/create">
        Create a Job
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" aria-current="page" href="/view">
        View applications
    </a>
</li>
{% endblock %}


{% block content %}
<h1 class="h2 mt-3 mb-4">All Jobs</h1>

<div style= "max-height: 500px;"class="overflow-auto mb-4" id="company_jobs"></div>

<div id="bt-center">
    <button type="button" class="btn btn-secondary btn-block" data-toggle="modal" onclick="showAllJobs('Google')">
    See Jobs
    </button>
</div>
<br>
<div id="bt-center">
    <button type="button" class="btn btn-primary btn-block" data-toggle="modal" data-target="#addJob">
    Create a Job
    </button>
</div>
{% endblock %}

{% block popup %} 

<div class="modal fade" id="addJob" tabindex="-1" role="dialog" aria-labelledby="addJob" aria-hidden="true">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">

            <div class="modal-header">
                <h5 class="modal-title">Create a New Job</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>

            <div class="modal-body">
                <form action="http://10.120.1.251:5009/create_job" method="POST">

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="job_title">Job Title</label>
                            <input type="text" class="form-control" id="job_title" placeholder="Type here...">
                        </div>
                    </div>

                    <!-- second row category  -->
                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="company_name" class="form-label">Company</label>
                            <input type="text" class="form-control" id="company_name" placeholder="Type here...">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="employment_type" class="form-label">Employment Type</label>
                            <input type="text" class="form-control" id="employment_type" placeholder="Full-time/Contract/Internship">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="industry" class="form-label">Industry</label>
                            <input type="text" class="form-control" id="industry" placeholder="">
                        </div>
                    </div>

                    <!-- second row category  -->
                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="job_description" class="form-label">Job Description</label>
                            <textarea class="form-control" id="job_description" rows="3"></textarea>
                        </div>
                    </div>

                    <!-- prereqs checkbox  -->
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="salary" class="form-label">Salary</label>
                            <input type="number" class="form-control" id="salary">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="location" class="form-label">Location</label>
                            <input type="text" class="form-control" id="location" placeholder="">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="person" class="form-label">Contact Person</label>
                            <input type="text" class="form-control" id="person" placeholder="">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group col-md-12">
                            <label for="email" class="form-label">Contact Email</label>
                            <input type="text" class="form-control" id="email" placeholder="">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="vacancy" class="form-label">Vacancy</label>
                            <input type="number" class="form-control" id="vacancy">
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button id="closemodal" type="submit" class="btn btn-primary" data-dismiss="modal" onclick="addJob()">Add</button>
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
    
    function showAllJobs(CompanyName) {

        var request = new XMLHttpRequest();
        request.open('GET', 'http://127.0.0.1:5001/jobs/company/'+CompanyName, true);
        
        request.onload = function() {  

            var json_obj = JSON.parse(request.responseText);
            var jobs = JSON.parse(json_obj.data);
            console.log(jobs);
            var job_list ='<table class="table"><thead><tr><th scope="col">Job Title</th><th scope="col">Employment Type</th><th scope="col">Datetime Posted</th><th scope="col">Vacancy</th></tr></thead><tbody>';

            for (var job in jobs) {
                var job_title = jobs[job].job_title;
                var employment_type = jobs[job].employment_type;
                var datetime = jobs[job].posted_timestamp;
                var vacancy = jobs[job].vacancy;

                temp = '<tr><th scope="row">'+job_title+'</th><td>'+employment_type+'</td><td>'+datetime+'</td><td>'+vacancy+'</td></tr>';
                job_list += temp;
            }
            job_list += '</tbody></table>'
            document.getElementById("company_jobs").innerHTML=job_list;
        };           
        
        request.send();
        //console.log('OPENED', request.readyState); // readyState will be 1
    }

    function addJob(){

        var request = new XMLHttpRequest();

        var job_title = document.getElementById("job_title").value;
        var company_name = document.getElementById("company_name").value;
        var employment_type = document.getElementById("employment_type").value;
        var industry = document.getElementById("industry").value;
        var job_description = document.getElementById("job_description").value;
        var salary = document.getElementById("salary").value;
        var location = document.getElementById("location").value;
        var contact_email = document.getElementById("email").value;
        var contact_person = document.getElementById("person").value;
        var vacancy = document.getElementById("vacancy").value;
         
        console.log(job_title);
        console.log(employment_type);

        var createJobCMS = "http://10.120.1.251:5009/create_job"
        var params = '{'+'"job_title":"'+job_title+'","company_name":"'+company_name+'","employment_type":"'+employment_type+'","industry":"'+industry+'","job_description":"'+job_description+'","salary":"'+salary+'","location":"'+location+'","contact_email":"'+contact_email+'","contact_person":"'+contact_person+'","vacancy":"'+vacancy+'"}';
        console.log(params);
        request.open('POST',createJobCMS, true);

        request.onload = function() {  
            var json_obj = JSON.parse(request.responseText);
            console.log("this is json_obj",json_obj)

            if (json_obj.code >= 200 & json_obj.code < 400) {
                alert('Your job has been added!');
                location.reload();
            } 
            else {
                alert('Oops! Something went wrong...');
            }
        };
        request.send(params);
    }
    
</script>
 
{% endblock %}