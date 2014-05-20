{% extends 'base.html' %}

{% block content %}

<div id="map"></div>

<script type="text/javascript">

// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 18, attribution: osmAttrib});		

	map.setView(new L.LatLng(39.980524,-75.127945),13);
	map.addLayer(osm);
</script>

{% endblock %}
