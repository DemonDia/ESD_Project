{% extends "base.php" %}

{% block title %}
Kitagawa Cosplay Pte Ltd | StartWork
{% endblock %}

{% block details %}
<h4>Kitagawa Cosplay Pte Ltd</h4>
{% endblock %}

{% block body %}
onload="showAllJobs()"
{% endblock %}

{% block navbar_links %}
<li class="nav-item">
    <a class="nav-link active" aria-current="page" href="/owner">
        Owner Dashboard
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" aria-current="page" href="/create">
        Create a Job
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" aria-current="page" href="/view_apps">
        View applications
    </a>
</li>
{% endblock %}


{% block content %}
<h1 class="h2 mt-3 mb-4">All Applications for Kitagawa Cosplay Pte Ltd</h1>

<div class="container">
    <div class="row">
        <input class="form-control" id="myInput" type="text" placeholder="Search..">
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
                <button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="Clear()">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>

            <div class="modal-body" id="inhere">
                <table class="table">
                    <thead></thead>
                    <tbody>
                        <tr>
                            <th scope="row">Name</th>
                            <td id="name"></td>
                        </tr>
                        <tr>
                            <th scope="row">Job Title</th>
                            <td id="job_title"></td>
                        </tr>
                        <tr>
                            <th scope="row">Date Applied</th>
                            <td id="date"></td>
                        </tr>
                        <tr>
                            <th scope="row">Nationality</th>
                            <td id="nationality"></td>
                        </tr>
                        <tr>
                            <th scope="row">Date of Birth</th>
                            <td id="dob"></td>
                        </tr>
                        <tr>
                            <th scope="row">Phone</th>
                            <td id="phone"></td>
                        </tr>
                        <tr>
                            <th scope="row">Email</th>
                            <td id="email"></td>
                        </tr>
                        <tr>
                            <th scope="row">Work Experience</th>
                            <td id="experience"></td>
                        </tr>
                        <tr>
                            <th scope="row">Skills</th>
                            <td id="skills"></td>
                        </tr>
                        <tr>
                            <th scope="row">Educational Background</th>
                            <td id="education"></td>
                        </tr>
                    </tbody>
                </table>

                <div class="modal-footer">
                    <div id="buttons" class="row"> 
                        <div class="col" id="acceptButton"></div>
                        <div class="col" id="rejectButton"></div>
                    </div>
                    <button id="closemodal" type="button" class="btn btn-secondary" data-dismiss="modal" onclick="Clear()">Cancel</button>
                </div>

            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block script %}

<script>

    function Clear() {
        document.getElementById("buttons").innerHTML='<div class="col" id="acceptButton"></div><div class="col" id="rejectButton"></div>';
    }
    
    function showAllJobs() {

        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5006/get_applications/'+'Kitagawa Cosplay Pte Ltd', true);
        
        request.onload = function() {  

            var json_obj = JSON.parse(request.responseText);
            var jobs = JSON.parse(json_obj.data);
            var job_list ='<table class="table"><thead><tr><th scope="col">Name</th><th scope="col">Job Title</th><th scope="col">Datetime Applied</th><th scope="col">Owner Status</th><th scope="col">Applicant Decision</th><th scope="col">Details</th></tr></thead><tbody id="myTable">';

            for (var job in jobs) {
                var job_title = jobs[job].job_title;
                var name = jobs[job].first + " " + jobs[job].last;
                var datetime = jobs[job].applied_timestamp;
                var owner_status = jobs[job].app_status;
                console.log(owner_status);

                if (owner_status === false) {
                    owner_status = 'Rejected';
                    console.log(owner_status);}
                else if (owner_status == null) {
                    owner_status = '';}
                else {
                    owner_status = 'Accepted';};
                
                    
                var user_dec = jobs[job].user_dec;
                if (user_dec === false) {
                    user_dec = 'Rejected';}
                else if (user_dec == null) {
                    user_dec = '';}
                else {
                    user_dec = 'Accepted';}
                
                
                //var date = datetime.substring(0,10); - want to show only date

                temp = '<tr><th scope="row">'+name+'</th><td>'+job_title+'</td><td>'+datetime+'</td><td>'+owner_status+'</td><td>'+user_dec+'</td><td><a href="" onclick="showDetails('+"'"+job+"','"+owner_status+"'"+')" class="link-primary" data-toggle="modal" data-target="#AccRej">View Details</td></tr>';
                job_list += temp;
            }
            job_list += '</tbody></table>'
            document.getElementById("all_jobs").innerHTML=job_list;
        };           
        
        request.send();
        //console.log('OPENED', request.readyState); // readyState will be 1
    }

    function showDetails(AID,app_status) {

        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5006/get_app/'+AID, true);

        request.onload = function() {  

            var json_obj = JSON.parse(request.responseText);
            var jobs = JSON.parse(json_obj.data);
            // var job_list ='<table class="table"><thead><tr><th scope="col">Name</th><th scope="col">Job Title</th><th scope="col">Datetime Applied</th><th scope="col">Owner Status</th><th scope="col">Applicant Decision</th><th scope="col">Details</th></tr></thead><tbody id="myTable">';
            
            var job_title = jobs.job_title;
            var email = jobs.email;
            var dob = jobs.dob;
            var name = jobs.first + " " + jobs.last;
            var date = jobs.applied_timestamp;
            var phone = jobs.phone;
            var nationality = jobs.nationality;
            var experience = jobs.experience;
            var skills = jobs.skills;
            var education = jobs.education;

            //var date = datetime.substring(0,10); - want to show only date
            document.getElementById("job_title").innerHTML=job_title;
            document.getElementById("name").innerHTML=name;
            document.getElementById("email").innerHTML=email;
            document.getElementById("phone").innerHTML=phone;
            document.getElementById("dob").innerHTML=dob;
            document.getElementById("experience").innerHTML=experience;
            document.getElementById("skills").innerHTML=skills;
            document.getElementById("education").innerHTML=education;
            document.getElementById("nationality").innerHTML=nationality;
            document.getElementById("date").innerHTML=date;

            if (app_status === 'Rejected') {
                document.getElementById("buttons").innerHTML='<p class="text-danger">You have rejected this application. We will inform the applicant.</p>';
            }
            else if (app_status === 'Accepted') {
                document.getElementById("buttons").innerHTML='<p class="text-success">Thank you for accepting this application! We will inform the applicant.</p>';
            }
            else if (app_status === '') {
                console.log("this is status", app_status);
                document.getElementById("acceptButton").innerHTML='<button id="accept" type="button" class="btn btn-success" data-dismiss="modal" onclick="Accept('+'\''+AID+'\''+')">Accept</button>';
                document.getElementById("rejectButton").innerHTML='<button id="reject" type="button" class="btn btn-danger" data-dismiss="modal" onclick="Reject('+'\''+AID+'\''+')">Reject</button>'; 
            };

                      
        };           

        request.send();
        //console.log('OPENED', request.readyState); // readyState will be 1
    }

    function Accept(AID) {
        var request = new XMLHttpRequest();
        request.open('PUT', 'http://localhost:5006/process_application/'+AID, true);

        request.onload = function() {
            var json_obj = JSON.parse(request.responseText);
            console.log("this is json_obj",json_obj)

            if (json_obj.code >= 200 & json_obj.code < 400) {
                alert('Your status has been updated!');
                location.reload();
            } 
            else {
                alert('Oops! Something went wrong...');
            }
        };

        request.send('{"app_status":true}');

    }

    function Reject(AID) {
        var request = new XMLHttpRequest();
        request.open('PUT', 'http://localhost:5006/process_application/'+AID, true);

        request.onload = function() {
            var json_obj = JSON.parse(request.responseText);
            console.log("this is json_obj",json_obj)

            if (json_obj.code >= 200 & json_obj.code < 400) {
                alert('Your status has been updated!');
                showAllJobs();
            } 
            else {
                alert('Oops! Something went wrong...');
            }
        };

        request.send('{"app_status":false}');

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