{% extends "base.php" %}

{% block title %}
User site
{% endblock %}

{% block details %}
Company Name
{% endblock %}

{% block body %}
onload="showAllJobs()"
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
<h1 class="h2 mt-3 mb-4">All Jobs</h1>

<div class="container">
  <div class="row">
    <div class="col-md">
        <input class="form-control" id="myInput" type="text" placeholder="Search..">    
    </div>
    <div class="col-sm">
        <!-- filter table somehow based on values, dynamic -->
    </div>
  </div>
</div>
<br>
<div class="overflow-auto mb-4" id="all_jobs"></div>
{% endblock %}

{% block popup %} 
<div class="modal fade" id="AccRej" tabindex="-1" role="dialog" aria-labelledby="AccRej" aria-hidden="true">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">

            <div class="modal-header">
                <h5 class="modal-title">Application Details</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>

            <div class="modal-body" id="inhere">
                <table class="table">
                    <thead></thead>
                    <tbody>
                    <tr>
                    <th scope="row">Job Title</th>
                    <td id="job_title"></td>
                    </tr>
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

                <div class="modal-footer">
                    <div id="acceptButton"></div>
                    <div id="rejectButton"></div>
                    <button id="closemodal" type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                </div>

            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block script %}

<script>
    
    function showAllJobs() {

        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5005/get_applications/'+'johnsim@gmail.com', true);
        
        request.onload = function() {  

            var json_obj = JSON.parse(request.responseText);
            var jobs = JSON.parse(json_obj.data);
            var job_list ='<table class="table"><thead><tr><th scope="col">Name</th><th scope="col">Job Title</th><th scope="col">Datetime Applied</th><th scope="col">Owner Status</th><th scope="col">Applicant Decision</th><th scope="col">Details</th></tr></thead><tbody id="myTable">';

            for (var job in jobs) {
                var job_title = jobs[job].job_title;
                var name = jobs[job].first + " " + jobs[job].last;
                var datetime = jobs[job].applied_timestamp;
                var owner_status = jobs[job].app_status;
                var jid = jobs[job].JID;
                console.log("this",jid);
                console.log(owner_status);
                if ((owner_status === false)||(owner_status ==='false')) {
                    owner_status = 'Rejected';}
                else if (owner_status == null) {
                    owner_status = '';}
                else if ((owner_status === true)||(owner_status === "true")) {
                    owner_status = 'Accepted';}
                
                    
                var user_dec = jobs[job].user_dec;
                if (user_dec === false) {
                    user_dec = 'Rejected';}
                else if (user_dec == null) {
                    user_dec = '';}
                else if (user_dec == true) {
                    user_dec = 'Accepted';}
                
                //var date = datetime.substring(0,10); - want to show only date

                temp = '<tr><th scope="row">'+name+'</th><td>'+job_title+'</td><td>'+datetime+'</td><td>'+owner_status+'</td><td>'+user_dec+'</td><td><a href="" onclick="showDetails(\''+jid+'\',\''+job+'\')" class="link-primary" data-toggle="modal" data-target="#AccRej">View Details</td></tr>';
                job_list += temp;
            }
            job_list += '</tbody></table>'
            document.getElementById("all_jobs").innerHTML=job_list;
        };           
        
        request.send();
        //console.log('OPENED', request.readyState); // readyState will be 1
    }

    function showDetails(jid,aid) {
        console.log("jid",jid);
        console.log("aid",aid)

        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5005/view_job/'+jid, true);

        request.onload = function() {  
            console.log(request)

            var json_obj = JSON.parse(request.responseText);
            console.log(json_obj);
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

            document.getElementById("acceptButton").innerHTML='<button id="accept" type="button" class="btn btn-success" data-dismiss="modal" onclick="Accept('+'\''+aid+'\''+')">Accept</button>';
            document.getElementById("rejectButton").innerHTML='<button id="reject" type="button" class="btn btn-danger" data-dismiss="modal" onclick="Reject('+'\''+aid+'\''+')">Reject</button>';            
        };           

        request.send();
        //console.log('OPENED', request.readyState); // readyState will be 1
    }

    function Accept(AID) {
        var request = new XMLHttpRequest();
        request.open('PUT', 'http://localhost:5005/process_application/'+AID, true);

        request.onload = function() {
            console.log("acc_request",request)
            // var json_obj = JSON.parse(request.responseText);
            // console.log("this is json_obj",json_obj)

            if (request.status >= 200 & request.status < 400) {
                alert('Your status has been updated!');
                showAllJobs();
            } 
            else {
                alert('Oops! Something went wrong...');
            }
        };

        request.send('{"user_dec":true}');

    }

    function Reject(AID) {
        var request = new XMLHttpRequest();
        request.open('PUT', 'http://localhost:5005/process_application/'+AID, false);

        request.onload = function() {
            console.log("textt",request)
            // var json_obj = JSON.parse(request.responseText);
            // console.log("this is json_obj",json_obj)

            if (request.status >= 200 & request.status < 400) {
                alert('Your status has been updated!');
                showAllJobs();
            } 
            else {
                alert('Oops! Something went wrong...');
            }
        };

        request.send('{"user_dec":false}');

    }

    $(document).ready(function(){
        $("#myInput").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#myTable tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
    });

</script>
 
{% endblock %}