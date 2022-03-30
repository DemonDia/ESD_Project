<script src="https://apis.google.com/js/platform.js" async defer></script>

<meta name="google-signin-client_id" content="209394015065-oagp4hnfvthnokajqv8b7iql158h2gt8.apps.googleusercontent.com">

<div class="g-signin2" data-onsuccess="onSignIn"></div>

<a href="#" onclick="signOut();">Sign out</a>
<script>
  function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
  }
</script>