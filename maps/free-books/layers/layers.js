var wms_layers = [];


        var lyr_ESRIWorldTopo_0 = new ol.layer.Tile({
            'title': 'ESRI World Topo',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' ',
                url: 'http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
            })
        });
var format_freebooks_1 = new ol.format.GeoJSON();
var features_freebooks_1 = format_freebooks_1.readFeatures(json_freebooks_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_freebooks_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_freebooks_1.addFeatures(features_freebooks_1);
var lyr_freebooks_1 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_freebooks_1, 
                style: style_freebooks_1,
                interactive: true,
                title: '<img src="styles/legend/freebooks_1.png" /> free-books'
            });

lyr_ESRIWorldTopo_0.setVisible(true);lyr_freebooks_1.setVisible(true);
var layersList = [lyr_ESRIWorldTopo_0,lyr_freebooks_1];
lyr_freebooks_1.set('fieldAliases', {'title': 'title', 'latitude': 'latitude', 'longitude': 'longitude', 'address': 'address', });
lyr_freebooks_1.set('fieldImages', {'title': 'TextEdit', 'latitude': 'TextEdit', 'longitude': 'TextEdit', 'address': 'TextEdit', });
lyr_freebooks_1.set('fieldLabels', {'title': 'no label', 'latitude': 'no label', 'longitude': 'no label', 'address': 'no label', });
lyr_freebooks_1.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});