function FireIncident( data ) {

	if( 'fields' in data ) {
		incidentData = data.fields;
	}
	else {
		incidentData = data;
	}

	if( false ) {
		console.log( 'in FireIncident constructor, got data:\n');
		console.log( incidentData );
	}

	this.postTitleStr = incidentData.postTitleStr;
	this.fireDate = incidentData.fireDate;
	this.fireAddressStr = incidentData.fireAddressStr;
	this.fireDetailsStr = incidentData.fireDetailsStr;
	this.fireDateStr = incidentData.fireDateStr;
	this.x = incidentData.x;
	this.y = incidentData.y;
};

function FireStation( data ) {

	if( 'fields' in data ) {
		incidentData = data.fields;
	}
	else {
		incidentData = data;
	}

	this.locationStr = incidentData.postTitleStr;
	this.x = incidentData.x;
	this.y = incidentData.y;
};

var FireIncidentMap = google.maps.Map;

FireIncidentMap.getMapOptions = function() {
	return {
		center: new google.maps.LatLng(39.970505,-75.148133),
		zoom: 12
	};
};

FireIncidentMap.prototype.googleMapsApiKey = function() {
	return "AIzaSyCUyKgIqRsJcdjrmOHDKJSBgyaBwDvfkbw";
}

FireIncidentMap.prototype.fetchIncidents = function( options ) {

	self = this;

	console.log( 'fetching incidents, when complete we will run ' + options.complete );

	url = '/fire-incidents/show?format=json&all='+options.all;

	console.log('loading fire incidents from:' );
	console.log( url );
	$.ajax({
		url: url,
		success: function( data ) {

			var incidents = [];
			$.each( data, function( i, d ) {
				incidents.push( new FireIncident( d ) );
			});
			self.incidents = incidents;
			self.addIncidents( incidents );
		}, // end success callback
		complete: options.complete
	}); // end ajax
}

FireIncidentMap.prototype.fetchStations = function( options ) {
	console.log( 'fetchStations is running' );

	self = this;

	url = '/fire-stations/get';

	console.log('loading stations from:' );
	console.log( url );
	$.ajax({
		url: url,
		success: function( data ) {

			var stations = [];
			$.each( data, function( i, d ) {
				stations.push( new FireIncident( d ) );
			});

			self.stations = stations;
		}, // end success callback
		complete: options.complete
	}); // end ajax
}

FireIncidentMap.prototype.getNearest = function( options ) {
	self = this;

	console.log('get nearest is running');

	incidents = this.incidents;

	deferreds = [];
	if( incidents !== null ) {
		$.each(incidents, function(index, incident){

			if( false ) {
				console.log( incident );
				console.log( incident.x + " " + incident.y );
			}

	    	deferreds.push(
		        // No success handler - don't want to trigger the deferred object
		        $.ajax({
		            url: self.googleDirectionsUrl(incident.x,incident.y),
		            type: 'GET',
		            success: function( data ) {
		            	console.log( data );
		            }
		        })
	    	);
		});
	}
	else {
		alert( 'there were no incidents retreived' );
	}
}

FireIncidentMap.prototype.googleDirectionsUrl = function( startX,startY,endX,endY ) {
	return 'https://maps.googleapis.com/maps/api/directions/xml?'
	+'origin='+startY+','+startX
	+'&destination='+endY+','+endX
	+'&sensor=false'
	+'&key='+this.googleMapsApiKey();
}

FireIncidentMap.prototype.getNearestStation = function( x,y ) {

	self = this;

	url = '/fire-stations/get';

	console.log('loading stations from:' );
	console.log( url );
	$.ajax({
		url: url,
		success: function( data ) {

			var stations = [];
			$.each( data, function( i, d ) {
				stations.push( new FireIncident( d ) );
			});

			self.stations = stations;
		} // end success callback
	}); // end ajax
}



FireIncidentMap.prototype.addIncidents = function( incidents ) {

	self = this;

	$.each( incidents, function(i,incident) {

	  var marker = new google.maps.Marker({
	      position: new google.maps.LatLng(incident.y, incident.x),
	      map: self,
	      title: incident.postTitleStr
	  });

	  var infowindow = new google.maps.InfoWindow({
	    content: "<div class='incident-window'>"
	    + incident.fireDateStr + " " + incident.postTitleStr + "<br/>"
	    + "<br/>"
	    + incident.fireDetailsStr
	    + "</div>"
	  });

	  google.maps.event.addListener(marker, 'click', function() {
	    infowindow.open(self, marker);
	  });

	}); // end each incident
};
