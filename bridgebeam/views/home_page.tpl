<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BridgeBeam</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Create conference bridges with ease">
<meta name="author" content="Thomas Zakrajsek">

<!-- Le styles -->
<link href="/css/bootstrap.css" rel="stylesheet">
<style>
body {
padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
}
</style>
<link href="/css/bootstrap-responsive.css" rel="stylesheet">

<!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
<!--[if lt IE 9]>
<script src="/js/html5shiv.js"></script>
<![endif]-->

<!-- Fav and touch icons -->
<link rel="apple-touch-icon-precomposed" sizes="144x144" href="/ico/apple-touch-icon-144-precomposed.png">
<link rel="apple-touch-icon-precomposed" sizes="114x114" href="/ico/apple-touch-icon-114-precomposed.png">
<link rel="apple-touch-icon-precomposed" sizes="72x72" href="/ico/apple-touch-icon-72-precomposed.png">
                    <link rel="apple-touch-icon-precomposed" href="/ico/apple-touch-icon-57-precomposed.png">
                                   <link rel="shortcut icon" href="/ico/favicon.png">
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="brand" href="#">BridgeBeam</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="active"><a href="#">Home</a></li>
              <li><a href="/about">About</a></li>
              <li><a href="mailto:tzakrajsek@netflix.com">Contact</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
      <div style="float: left; width: 400px">
        <form id='beam'>
          <fieldset>
            <legend>Conference Join</legend>
            <label>Phone Number</label>
            <span class="help-block">International numbers please use E.164 format</span>
            <input id='phone_number' type="text" placeholder="408-555-5555">
            <br /><br />
            <label>Conference Name</label>
            <span class="help-block">Select an existing conference name, or enter a new one.</span>
            <select id='conference_name'><input id='conference_name' type="text" placeholder="New conference?">
            <br /><br />
            <span class="help-block">The number above will be called and invited into the conference bridge.</span>
            <button type="submit" id="beam" class="btn">Beam Me Up!</button><div id="loading" style="visibility: hidden; float: right; width: 100px; position: relative; right: 170px; top: 5px;"><img src="/img/loading_graphic.gif"></div>
          </fieldset>
        </form>
      </div>
      <div id="conferences" style="float: right; width: 300px">
      </div>

    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/js/jquery.js"></script>
    <script src="/js/bootstrap-transition.js"></script>
    <script src="/js/bootstrap-alert.js"></script>
    <script src="/js/bootstrap-modal.js"></script>
    <script src="/js/bootstrap-dropdown.js"></script>
    <script src="/js/bootstrap-scrollspy.js"></script>
    <script src="/js/bootstrap-tab.js"></script>
    <script src="/js/bootstrap-tooltip.js"></script>
    <script src="/js/bootstrap-popover.js"></script>
    <script src="/js/bootstrap-button.js"></script>
    <script src="/js/bootstrap-collapse.js"></script>
    <script src="/js/bootstrap-carousel.js"></script>
    <script src="/js/bootstrap-typeahead.js"></script>
    <script>

// variable to hold request
var request;
// bind to the submit event of our form
$("#beam").submit(function(event){
    // abort any pending request
    if (request) {
        request.abort();
    }
    $("div#loading").css('visibility', 'visible');
    if ($("input#conference_name").val() != "") {
        post_data="phone_number=" + $("input#phone_number").val() + "&conference_name=" + $("input#conference_name").val()
    } else {
        post_data="phone_number=" + $("input#phone_number").val() + "&conference_name=" + $("select#conference_name").val()
    }


    // fire off the request to /form.php
    var request = $.ajax({
        url: "/api/v1/conference/join",
        type: "post",
        data: post_data
    });

    // callback handler that will be called on success
    request.done(function (response, textStatus, jqXHR){
    // clear the old values
    $("input#phone_number").val('') 
    $("input#conference_name").val('')
    $("div#loading").css('visibility', 'hidden');
    });

    // callback handler that will be called on failure
    request.fail(function (jqXHR, textStatus, errorThrown){
        // log the error to the console
        console.error(
            "The following error occured: "+
            textStatus, errorThrown
        );
    $("div#loading").css('visibility', 'hidden');

    });

    // prevent default posting of form
    event.preventDefault();
});
function list_conferences(){   
  $.getJSON('/api/v1/conference/list', function (data, textStatus){
    console.log(data);
    var conferences = data
    $('div#conferences').empty();
    $('select#conference_name').empty();
    for (var key in conferences) {
      if (conferences.hasOwnProperty(key)) {
        $('div#conferences').append($('<h4/>', {
          id: key,
          className: 'conference',
          html: key
        }));
        $('select#conference_name').append($('<option/>').val(key).html(key));
        console.log(conferences[key])
        console.log(key)
        for (var phone_number in conferences[key]) {
            $('div#conferences').append($('<h5/>', {
              id: conferences[key][phone_number],
              className: 'phone_number',
              html: conferences[key][phone_number]
            }))
        }
      }
    }
  });
}

$(document).ready(list_conferences)
setInterval(
    list_conferences,
     10000  /* 10000 ms = 10 sec */
);
    </script>
  </body>
</html>

