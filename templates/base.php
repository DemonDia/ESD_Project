<?php
header("Access-Control-Allow-Origin: *");
?>
<!doctype html>
<html lang="en">
<head>
    <title>{% block title %}{% endblock %}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <!-- <link href="./css/style.css" rel="stylesheet"> -->
    <link href="dashboard.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
    <script src="jquery-3.6.0.js"></script>
</head>

<body {% block body %}{% endblock %}>
    <header class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
        <a class="navbar-brand col-md-3 col-lg-2 me-0 px-3" href="http://192.168.0.125:5010/">Start Ups website</a>
        <button class="navbar-toggler position-absolute d-md-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
    </header>

    <div class="container-fluid" id="app">
        <div class="row">
            <div class="col">
                <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
                    <div class="position-sticky pt-3">
                        <ul class="nav flex-column md-3">
                            <div class="logo-image center">
                                <span>
                                    <img v-bind:src="profilePhoto" class="rounded img_logo">
                                </span>
                            </div>
                            <li class="nav-item center">
                                <a class="nav-link">
                                    {% block details %}{% endblock %}
                                </a>
                                
                            </li>
                            <br>
                            {% block navbar_links %}{% endblock %}
                            <!-- user sign in -->
                            <div class="g-signin2" data-onsuccess="onSignIn" id = "g-in"></div>
                            <li><a href="/" onclick="signOut();" id = "g-out">Sign out</a></li>
                            <!-- user sign out -->
                            
                        </ul>
                    </div>
                </nav>
            </div>
            <div class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                {% block content %}{% endblock %}
            </div>
            {% block popup %}{% endblock %}
        </div>
    </div>

    {% block script %} {% endblock %}

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>


    <script src="https://apis.google.com/js/platform.js" async defer></script>
    <meta name="google-signin-client_id" content="209394015065-l9sd7toqemvo9dg09ofr62l0q19t7unb.apps.googleusercontent.com">    
    
    
    <script>

        if (document.getElementById("g-in").hidden == false) {
            document.getElementById("g-out").hidden = true;
        }

        function onSignIn(googleUser) {

            document.getElementById("g-in").hidden=true;
            document.getElementById("g-out").hidden=false;

            var profile = googleUser.getBasicProfile();
            // console.log('Name: ' + profile.getName());

            var email = profile.getEmail();
            console.log('Email: ' + email); // This is null if the 'email' scope is not present.

            if (email.includes("@gmail.com")) {
                // console.log('seeker');
                if(window.location.href != "http://localhost:5010/user") {
                    window.location.replace("http://localhost:5010/user");
                }
            }
            
            else {
                // console.log('owner');
                if(window.location.href != "http://localhost:5010/owner") {
                    window.location.replace("http://localhost:5010/owner");
                }
            }
        }

        function signOut() {
            var auth2 = gapi.auth2.getAuthInstance();
            auth2.signOut().then(function () {
            console.log('User signed out.');
            });
        }
    </script>


</body>

</html>