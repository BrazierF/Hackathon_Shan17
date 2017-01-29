<?php $url = $_SERVER['SERVER_NAME'];
$output=array();?>
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
        height: 100vh;
        margin: 0;
        padding: 0;
      }
    </style>
    <script>
	var map;
	var infowindow;
	var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
	var labelIndex = 0;
	var parcours_index = 0;
	var bounds ;
	var all_pts = 
			    <?php
			    if(isset($_POST['request']) && isset($_POST['nb']) && isset($_POST['max_duration'])){			    	
			    	exec ('/usr/bin/python2.7 /var/www/html/Hackathon/Python/main.py "'. $_POST['request'].' " '. $_POST['max_duration'].' '.$_POST['nb'],$output);
			    }else{
			    	exec('/usr/bin/python2.7 /var/www/html/Hackathon/Python/main.py',$output);			    	
			    }
			    	$output= implode(' ',$output);;
			    echo $output ;
			    $output = json_decode($output);?>;
	var all_markers ;

	function initMap() {
	  map = new google.maps.Map(document.getElementById('map'), {
	    center: {lat: 46.5619, lng: -72.7435}, //center on shawinigan
	    zoom: 12
	  });
	  infowindow = new google.maps.InfoWindow();
	  console.log(all_pts);
	  all_markers = new Array(all_pts.length);
	  for(var j = 0 ; j < all_pts.length; j++){
		  all_markers[j] = new Array(all_pts[j].length);
		  for(var i = 0; i < all_pts[j].length; i++) {
	            all_markers[j][i]=createMarker(all_pts[j][i]);
		  }
	  }
	  console.log(all_markers);
	  afficherProp(0);
      
	}

	 // var service = new google.maps.places.PlacesService(map);
	

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
	  return marker;
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
      <a id="display_menu" class="navbar-brand clickable" href="/Hackathon/Web/home.php" ><h3 class='title' >ShawiniGo</h3></a>
      </div> 
      </div> 
</nav>
</div>
<div id="wrapper" class="container">
    <div class="col-md-6" style="height: 100%">
	<div id="cadre" style="background-color: #693806;  width :100%; padding:10px">
    <div id="map"></div>
    </div>
    </div>
    <div class="col-md-6">
    <FORM method="post" action="" id="ourForm">
    <div class="form-group">
    <label class="col-form-label"> Que veux-tu faire aujourd'hui ?</label>
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
      <label class="col-form-label">Combien de parcours souhaites-tu voir ?</label>
      <input name="nb" type="number" class="form-control"  value = <?php echo (isset($_POST['nb']) ? $_POST['nb'] : 1 ) ?> min=0 max=10/>
      <label class="col-form-label" style="color=#ddd !important;">De combien de temps disposes-tu ?</label>
      <input name="max_duration" class="form-control" type="number" value=<?php echo (isset($_POST['max_duration']) ? $_POST['max_duration'] : 6 ) ?> min=0 max=10/>
      <button type="button" onclick="sub()" class="btn btn-default">C'est parti !</button>
    </div>
    </FORM>
	</div>
	<script type="text/javascript">
	function afficherProp(i){
		bounds = new google.maps.LatLngBounds();
		for (var j = 0; j < all_pts.length; j++){
			for (var k = 0; k < all_pts[j].length; k++){
				all_markers[j][k].setVisible(false);
			}
		}
		for (var k = 0; k < all_pts[i].length; k++){
			all_markers[i][k].setVisible(true);
			latlng = new google.maps.LatLng (all_pts[i][k].lat,all_pts[i][k].lng);
	        bounds.extend(latlng);   	   
		}
		map.fitBounds(bounds);
	}
	</script>
	<div class="col-md-6">
	<?php
	//var_dump($output);
	for($i = 0 ; $i<count($output);$i++){?>
		<div class= "panel panel-default" onclick="afficherProp(<?php echo $i?>)">
		<div class= "panel-heading" style="font-weight: 700;">
			Circuit #<?php echo $i+1?>
		</div>
		<div class="panel-body">
		<ul>
			<?php for ( $j=0 ; $j < count($output[$i]);$j++){
				
			?>
			<li> <?php
			//var_dump($output[$i][$j]);
			echo $output[$i][$j]->name?></li>
		
			<?php }?>
			</ul>
		</div>
		</div>
	<?php }?>
	</div>
	</div>
      <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC_ETnxWmysf3X-ymcuLCUYwZVGgiCinWk&signed_in=true&libraries=places&callback=initMap" async defer></script>

</body>
 
</html>
