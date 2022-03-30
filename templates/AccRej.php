{% extends "base.php" %}

{% block title %}
User site
{% endblock %}

{% block details %}
User Name
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
{% endblock %}

{% block script %}

<script>
    
    function showAllApps(CID) {

        var request = new XMLHttpRequest();
        request.open('GET', 'http://127.0.0.1:5003/applications/company/'+CID, true);
        
        request.onload = function() {  

            var json_obj = JSON.parse(request.responseText);
            var jobs = JSON.parse(json_obj.data);
            var job_list ='<table class="table"><thead><tr><th scope="col">Job Title</th><th scope="col">Company</th><th scope="col">Employment Type</th><th scope="col">Datetime Posted</th><th scope="col">Vacancy</th></tr></thead><tbody id="myTable">';

            for (var job in jobs) {
                var job_title = jobs[job].job_title;
                var company = jobs[job].company_name;
                var employment_type = jobs[job].employment_type;
                var datetime = jobs[job].posted_timestamp;
                var vacancy = jobs[job].vacancy;
                //var date = datetime.substring(0,10); - want to show only date

                temp = '<tr><th scope="row"><a href="http://127.0.0.1:5010/job/'+"'"+job+"'"+'" class="link-primary">'+job_title+'</th><td>'+company+'</td><td>'+employment_type+'</td><td>'+datetime+'</td><td>'+vacancy+'</td></tr>';
                job_list += temp;
            }
            job_list += '</tbody></table>'
            document.getElementById("all_jobs").innerHTML=job_list;
        };           
        
        request.send();
        //console.log('OPENED', request.readyState); // readyState will be 1
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