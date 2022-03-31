{% extends "base.php" %}

{% block title %}
Owner site
{% endblock %}

{% block details %}
Company Name
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
<h1 class="h2 mt-3 mb-4"></h1>
<div class="jumbotron jumbotron-fluid">
    <div class="container">
        <h1 class="display-4">Welcome to the Owner Dashboard!</h1>
        <p class="lead">Click on the buttons below to complete today's tasks.</p>
    </div>
</div>

<div class="row">
    <div class="col-sm-3">
        <div class="card">
        <div class="card-body">
            <h5 class="card-title">Create a Job</h5>
            <p class="card-text">Create jobs for your start up</p>
            <a href="/create" class="btn btn-primary">Create a Job</a>
        </div>
        </div>
    </div>
    <div class="col-sm-3">
        <div class="card">
        <div class="card-body">
            <h5 class="card-title">View Applications</h5>
            <p class="card-text">View the applications you have have recieved and update their status</p>
            <a href="/view_apps" class="btn btn-primary">View applications</a>
        </div>
        </div>
    </div>
</div> 
{% endblock %}