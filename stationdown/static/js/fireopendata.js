function FireIncident( data ) {

	if( 'fields' in data ) {
		incidentData = data.fields;
	}
	else {
		incidentData = data;
	}

	this.postTitleStr = incidentData.postTitleStr;
	this.fireDate = incidentData.fireDate;
	this.fireDetailsStr = incidentData.fireDetailsStr;
	this.fireDateStr = incidentData.fireDateStr;
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

FireIncidentMap.prototype.fetchIncidents = function( options ) {

	self = this;

	$.ajax({
		url: '/fire-incidents/?format=json&all='+options.all,
		success: function( data ) {

			var incidents = [];
			$.each( data, function( i, d ) {
				incidents.push( new FireIncident( d ) );
			});
			self.addIncidents( incidents );
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
