{% extends "base.php" %}

{% block title %}
Choose role
{% endblock %}

{% block details %}

{% endblock %}

{% block navbar_links %}
<li class="nav-item">
    <a class="nav-link active" aria-current="page" href="/">
        Home
    </a>
</li>
{% endblock %}


{% block content %}


<div class="row">
    <div class="col-sm-3">
        <a href="/owner" class="btn btn-primary">Owner Site</a>
    </div>
    <div class="col-sm-3">
        <a href="/user" class="btn btn-primary">User Site</a>
    </div>
</div> 
{% endblock %}