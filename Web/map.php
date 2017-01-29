<?php $url = $_SERVER['SERVER_NAME'];?>
<!DOCTYPE html>
<html>
  <head>
  <script src="/Hackathon/Web/ext/jquery-1.12.1.min.js"></script>
<script src="/Hackathon/Web/ext/jquery-ui-1.11.4/jquery-ui.min.js"></script>
<script src="/Hackathon/Web/ext/bootstrap-3.3.6-dist/js/bootstrap.js"></script>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">			
<link rel="stylesheet" href=" http://192.168.199.109/Hackathon/Web/map.css">
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
	var parcours_index = 0;
	var all_pts;

	function loadPoints() {
		all_pts = 
			    <?php
			    $output =array();
			    if(isset($_POST['request']) && isset($_POST['nb']) && isset($_POST['max_duration'])){			    	
			    	exec ('/usr/bin/python2.7 /var/www/html/Hackathon/Python/main.py "'. $_POST['request'].' " '. $_POST['max_duration'].' '.$_POST['nb'],$output);
			    }else{
			    	exec('/usr/bin/python2.7 /var/www/html/Hackathon/Python/main.py',$output);			    	
			    }
			    	//var_dump($output);
			    echo implode(' ',$output);?>;
          return all_pts[parcours_index];
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
	   /* service.nearbySearch({
	      location: {lat: pts[i].lat, lng: pts[i].lng},
	      radius: '30',
	      //name: pts[i].name
	      keyword : pts[i].adresse
	    }, callback);*/
    	    createMarker(pts[i]);
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
	    //position:place.geometry.location,
	    position: {lat: place.lat, lng: place.lng},
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
      </div>
      </div>
</nav>
</div>
    <div id="map"></div>
    <div class="container">
    <div class="col-md-6">
    
    <FORM method="post" action="" id="ourForm">
    <div class="form-group">
    <label class="col-form-label"> Vos envies</label>
      <input type="hidden" id='request' name="request" placeholder="Que souhaitez-vous faire?"/>
		<ul id="user_inputs" class="form-group" style="list-style-type: none;padding-left:0px">
		      
						<li class="form-group row" ><textarea class="user_inputs form-control" data-position="0"
								id="user_inputs_0" rows="1" cols="50"></textarea></li>
		</ul>

<script type="text/javascript">
		<!--
		
		//-->
		
		$(function (){
			mmh('#user_inputs_0');
			});
		
		function mmh(element){
		$(element).keydown(function (e) {
			//console.log(e);
			//console.log(e.keyCode);
			// Entree
			  if ( (e.keyCode == 13 || e.keyCode == 10) && !e.shiftKey) {
				  var tableau = document.getElementsByClassName('user_inputs');
				  var indice = tableau.length;
				  //console.log(indice);
				  var nvtext = e.currentTarget.value.substring(e.currentTarget.selectionStart);
				  e.currentTarget.value = e.currentTarget.value.substring(0,e.currentTarget.selectionStart);
				  $(e.target.parentNode).after('<li class="form-group row"> <textarea class="user_inputs form-control" data-position="'+indice+'" id="user_inputs_'+indice+'" rows="1" cols="50">'+nvtext+'</textarea></li>');
				    e.preventDefault();
				    e.stopPropagation();
				    mmh('#user_inputs_'+indice);
					document.getElementById('user_inputs_'+indice).focus();
			  }
			  //Retour
			  if (e.keyCode == 8) {
				  if(document.getElementsByClassName('user_inputs').length > 1){
					  if( 0 == e.currentTarget.selectionEnd){
						  //console.log('#'+e.currentTarget.id);
						  $(e.currentTarget).parent().prev().find("textarea").focus();
						  var ancien = $(e.currentTarget).parent().prev().find("textarea").val().length;

						  //console.log("ancien "+ancien);
						   $(e.currentTarget).parent().prev().find("textarea").val($(e.currentTarget).parent().prev().find("textarea").val()+e.currentTarget.value);
						   $(e.currentTarget).parent().prev().find("textarea")[0].setSelectionRange(ancien,ancien);
							  
							$(e.currentTarget).parent().remove();
						  e.preventDefault();
						  e.stopPropagation();
					  }
				  }
			  }
			  //Suppr
			  if (e.keyCode == 46) {
				  if(document.getElementsByClassName('user_inputs').length > 1){
					  if(e.currentTarget.value.length == e.currentTarget.selectionStart){
						  var ancien = e.currentTarget.value.length;
						  e.currentTarget.value = e.currentTarget.value+ ($(e.currentTarget).parent().next().find("textarea").val());
						  e.currentTarget.setSelectionRange(ancien,ancien);
						  $(e.currentTarget).parent().next().remove();
						  if(e.currentTarget.value == 'undefined' ){
							  $(e.currentTarget).parent().prev().find("user_inputs").focus();
							  $(e.currentTarget).parent().remove();
						  }
						  e.preventDefault();
						  e.stopPropagation();
					  
					}
					//console.log('#'+e.currentTarget.id);
					  /* $(e.currentTarget).parent().next().find("textarea").focus();
					  $(e.currentTarget).parent().remove();
					  e.preventDefault();
					  e.stopPropagation();*/
				  }
			  }
			});
		}
		
		function sub(){
			var requete ='';
			var eu = document.getElementById('user_inputs').getElementsByClassName('user_inputs');
			for (indice = 0; indice< eu.length;indice++){
				requete += eu[indice].value +'|';
			}
			document.getElementById('request').value = requete;
			console.log($('#ourForm'));
			$('#ourForm').submit();
		}
		</script>
      <label class="col-form-label">Nombre de propositions</label>
      <input name="nb" type="number" class="form-control"  value = <?php echo (isset($_POST['nb']) ? $_POST['nb'] : 3 ) ?> min=0 max=10/>
      <label class="col-form-label" >Durée du parcours</label>
      <input name="max_duration" class="form-control" type="number" value=<?php echo (isset($_POST['max_duration']) ? $_POST['max_duration'] : 4 ) ?> min=0 max=10/>
      <button type="button" onclick="sub()" class="btn btn-default">OK</button>
    </div>
    </FORM>
	</div>
	<div class="col-md-6">
	</div>
	</div>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC_ETnxWmysf3X-ymcuLCUYwZVGgiCinWk&signed_in=true&libraries=places&callback=initMap" async defer></script>
  </body>
 
</html>
