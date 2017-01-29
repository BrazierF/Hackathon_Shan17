<?php $url = $_SERVER['SERVER_NAME'];?>
<!DOCTYPE html>
<html>
  <head>
  <script src="/Hackathon/Web/ext/jquery-1.12.1.min.js"></script>
<script src="/Hackathon/Web/ext/jquery-ui-1.11.4/jquery-ui.min.js"></script>
<script src="/Hackathon/Web/ext/bootstrap-3.3.6-dist/js/bootstrap.js"></script>
<link rel="stylesheet" href="/Hackathon/Web/ext/material-icons/material-icons.css">
<link rel="stylesheet" href="/Hackathon/Web/ext/jquery-ui-1.11.4/jquery-ui.css">
<link rel="stylesheet" href="/Hackathon/Web/ext/jquery-ui-1.11.4/jquery-ui.theme.css">
<link rel="stylesheet" href="/Hackathon/Web/ext/bootstrap-3.3.6-dist/css/bootstrap.min.css">
<link rel="stylesheet" href="/Hackathon/Web/ext/bootstrap-3.3.6-dist/css/simple-sidebar.css">	
<link rel="stylesheet" href="/Hackathon/Web/ext/bootstrap-3.3.6-dist/css/full-slider.css">			
<link rel="stylesheet" href="/Hackathon/Web/map.css">
    <title>Place searches</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      html, body {
        height: 400px;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
    <script>
	var map;
	var infowindow;
	var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
	var labelIndex = 0;

	function loadPoints() {
          var diable = {id: 'diable', lat: 46.540344, lng: -72.753280};
	  var auger = {id:'auger', lat: 46.540518, lng: -72.748123};
	  var justice = {id:'justice', lat: 46.541789, lng: -72.745532};
	  var lido = {id:'lido', lat: 46.561191, lng: -72.744417}
	  var mcdo_1 = {id: 'burger', lat: 46.556636, lng: -72.751011}
          var amphi = {id: 'fishing', lat: 51.775322, lng: -101.724806}

	  pts = new Array();
	  pts[0] = diable;
	  pts[1] = auger;
	  pts[2] = justice;
	  pts[3] = lido;
	  pts[4] = mcdo_1;
          //pts[5] = amphi;

          return pts;
        }


	function initMap() {
          var bounds = new google.maps.LatLngBounds ();

          pts = loadPoints();

	  map = new google.maps.Map(document.getElementById('map'), {
	    center: {lat: 46.5619, lng: -72.7435}, //center on shawinigan
	    zoom: 12
	  });

	  infowindow = new google.maps.InfoWindow();
	  var service = new google.maps.places.PlacesService(map);
	  for(var i = 0; i < pts.length; i++) {
            latlng = new google.maps.LatLng (pts[i].lat,pts[i].lng);
            bounds.extend (latlng);
	    service.nearbySearch({
	      location: {lat: pts[i].lat, lng: pts[i].lng},
	      radius: '30',
	      name: pts[i].id
	    }, callback);
	  }
          map.fitBounds (bounds);
	}

	function callback(results, status) {
	  if (status === google.maps.places.PlacesServiceStatus.OK) {
	    for (var i = 0; i < results.length; i++) {
	      createMarker(results[i]);
	    }
	  }
	}

	function createMarker(place) {
	  var marker = new google.maps.Marker({
	    map: map,
	    position: place.geometry.location,
	    label: labels[labelIndex++]
	  });

	  google.maps.event.addListener(marker, 'click', function() {
	    infowindow.setContent(place.name);
	    infowindow.open(map, this);
	  });
	}

    </script>
  </head>
  <body>
  <div id="entete">
  <nav class="navbar navbar-default navbar-fixed-top">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a id="display_menu" class="navbar-brand clickable" href="/Hackathon/Web/home.php" >L'indispensable</a>
      
</nav>
</div>
    <div id="map"></div>
    <FORM>
      <TEXTAREA name="nom" rows=4 cols=40 placeholder="Que souhaitez-vous faire?"></TEXTAREA>
    </FORM>

    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC_ETnxWmysf3X-ymcuLCUYwZVGgiCinWk&signed_in=true&libraries=places&callback=initMap" async defer></script>
  </body>
 
</html>
