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
		  pts = 
			    <?php
			    $output =array();
			    if(isset($_POST['request']) && isset($_POST['nb']) && isset($_POST['max_duration'])){			    	
			    	exec ('/usr/bin/python2.7 /var/www/html/Hackathon/Python/main.py "'. $_POST['request'].' " '. $_POST['max_duration'].' '.$_POST['nb'],$output);
			    }else{
			    	exec('/usr/bin/python2.7 /var/www/html/Hackathon/Python/main.py',$output);			    	
			    }
			    	//var_dump($output);
			    echo implode(' ',$output);?>;
          return pts[0];
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
    <script type="text/javascript">
    var toto = 
    <?php $output =array();
    	exec('/usr/bin/python2.7 /var/www/html/Hackathon/Python/main.py',$output);
    	//var_dump($output);
    	echo implode(' ',$output);?>;
    	console.log(toto);
    </script>
    <FORM method="post" action="">
      <input type="text" name="request" placeholder="Que souhaitez-vous faire?"/>
		<ul id="user_inputs">
						<li><textarea class="user_inputs" data-position="0"
								id="user_inputs_0" rows="1" cols="50"></textarea></li>
		</ul>
		</form>
	</div>
</div>
<script type="text/javascript">
		<!--
		
		//-->
		
		$(function (){
			mmh('#user_inputs');
			});
		
		function mmh(element){
		$(element).keydown(function (e) {
			//console.log(e);
			//console.log(e.keyCode);
			// Entree
			  if ( (e.keyCode == 13 || e.keyCode == 10) && !e.shiftKey) {
				  var tableau = document.getElementsByClassName('comments_areas');
				  var indice = tableau.length;
				  //console.log(indice);
				  var nvtext = e.currentTarget.value.substring(e.currentTarget.selectionStart);
				  e.currentTarget.value = e.currentTarget.value.substring(0,e.currentTarget.selectionStart);
				  $(e.target.parentNode).after('<li><textarea class="comments_areas" data-position="'+indice+'" id="comments_areas_'+indice+'" rows="1" cols="50">'+nvtext+'</textarea></li>');
				    e.preventDefault();
				    e.stopPropagation();
				    mmh('#comments_areas_'+indice);
					document.getElementById('comments_areas_'+indice).focus();
			  }
			  //Retour
			  if (e.keyCode == 8) {
				  if(document.getElementsByClassName('comments_areas').length > 1){
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
				  if(document.getElementsByClassName('comments_areas').length > 1){
					  if(e.currentTarget.value.length == e.currentTarget.selectionStart){
						  var ancien = e.currentTarget.value.length;
						  e.currentTarget.value = e.currentTarget.value+ ($(e.currentTarget).parent().next().find("textarea").val());
						  e.currentTarget.setSelectionRange(ancien,ancien);
						  $(e.currentTarget).parent().next().remove();
						  if(e.currentTarget.value == 'undefined' ){
							  $(e.currentTarget).parent().prev().find("textarea").focus();
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

		$(function(){
			note_toolpit();
			});
		
		function note_toolpit(){
			var span = document.getElementsByClassName('comments clickable');
			for (compteur = 0; compteur < span.length ; compteur++){
				var com = commentaires[span[compteur].dataset.episode_id];
			 	//console.log(com);
			 	com = com.split('|');
			 	if(com[0].length >0){
				 	//console.log(span[compteur].dataset.originalTitle);
				 	span[compteur].dataset.placement="right"
			 		span[compteur].dataset.originalTitle="<ul style='padding-left:7px;'>";
				 	for( compt = 0 ; compt <com.length;com++){
					 	//console.log(com);
					 	span[compteur].dataset.originalTitle= span[compteur].dataset.originalTitle+'<li>'+com[compt]+'</li>';
					}
				 	span[compteur].dataset.originalTitle= span[compteur].dataset.originalTitle+'</ul>';
			 	}else{
			 		span[compteur].dataset.placement="top"
			 		span[compteur].dataset.originalTitle="Notes";
				 }
			}
			
		}
		
		function envoyer_list(){
			//var donnees = $('#list_comment').serializeArray();
			var span = document.getElementById('myModalList'); 
			var donnees =[];
			var eu = span.getElementsByClassName('comments_areas');
			for (indice = 0; indice< eu.length;indice++){
				donnees.push(eu[indice].value);
			}
			//console.log(span);
			var donnees_b = {	
					//type : span.getAttribute('type'),
					series_id : span.getAttribute('data-series_id'),
					series_name : span.getAttribute('data-series_name'),
					episode_id :  span.getAttribute('data-episode_id'),
					comments : donnees,			
			};
			//var concatarray = $.extend(donnees,donnees_b); 
			//console.log(donnees_b);
			$.post( "Ajout_commentaires.php", donnees_b ).done(function( data ) {
				//console.log(data);
				var recu = JSON.parse(data);
				//console.log(recu);
				//$('body').append(data);
				var size = recu.size ;
				//$('#comments_Result').empty();
				if(!recu.succeed){
					for(i = 0; i<recu.feedback.length;i++){
						$('#list_comments').append('<li><div class="alert alert-danger" role="alert">'+recu.feedback[i]+'</div></li>');
					}	
					return ;
				}else{
					for(i = 0; i<recu.feedback.length;i++){
						$('#list_comments').append('<li><div class="alert alert-success" role="alert">'+recu.feedback[i]+'</div></li>');
					}
					commentaires[span.getAttribute('data-series_id')] = recu.comments;
					note_toolpit();
					window.setTimeout("document.getElementById('myModalList').style.display = 'none';", 1500);
				}
				});
		}
		</script>
      <label>Nombre de propositions</label>
      <input name="nb" type="number" value = <?php echo (isset($_POST['nb']) ? $_POST['nb'] : 3 ) ?> min=0 max=10/>
      <label>Durée du parcours</label>
      <input name="max_duration" type="number" value=<?php echo (isset($_POST['max_duration']) ? $_POST['max_duration'] : 4 ) ?> min=0 max=10/>
      <input type="submit"/>
    </FORM>

    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC_ETnxWmysf3X-ymcuLCUYwZVGgiCinWk&signed_in=true&libraries=places&callback=initMap" async defer></script>
  </body>
 
</html>
