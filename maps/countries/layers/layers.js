var wms_layers = [];


        var lyr_OSMStandard_0 = new ol.layer.Tile({
            'title': 'OSM Standard',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' &middot; <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors, CC-BY-SA</a>',
                url: 'http://tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
        });
var format_countries_1 = new ol.format.GeoJSON();
var features_countries_1 = format_countries_1.readFeatures(json_countries_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_countries_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_countries_1.addFeatures(features_countries_1);
var lyr_countries_1 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_countries_1, 
                style: style_countries_1,
                interactive: true,
                title: '<img src="styles/legend/countries_1.png" /> countries'
            });

lyr_OSMStandard_0.setVisible(true);lyr_countries_1.setVisible(true);
var layersList = [lyr_OSMStandard_0,lyr_countries_1];
lyr_countries_1.set('fieldAliases', {'name': 'name', 'latitude': 'latitude', 'longitude': 'longitude', });
lyr_countries_1.set('fieldImages', {'name': 'TextEdit', 'latitude': 'TextEdit', 'longitude': 'TextEdit', });
lyr_countries_1.set('fieldLabels', {'name': 'no label', 'latitude': 'no label', 'longitude': 'no label', });
lyr_countries_1.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});