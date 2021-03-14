/*
    Create AmMap using JSON data from server
*/


// Create Map Chart
let canadaMap = am4core.create("map", am4maps.MapChart);
canadaMap.geodata = am4geodata_canadaLow; // lower resolution for performance

canadaMap.projection = new am4maps.projections.Miller();

let polygonSeries = canadaMap.series.push(new am4maps.MapPolygonSeries());
polygonSeries.useGeodata = true;

let polygonTemplate = polygonSeries.mapPolygons.template;

// Display region name on hover
polygonTemplate.tooltipText = "{name}";
polygonTemplate.fill = am4core.color("#888888");
let hs = polygonTemplate.states.create("hover");
hs.properties.fill = am4core.color("#555555");


// Zoom in on region when clicked
polygonSeries.mapPolygons.template.events.on("hit", function(ev) {
    canadaMap.zoomToMapObject(ev.target);
});



// Example JSON (replace with API call)
const EXAMPLE = [
    {
        "title": "Ottawa",
        "latitude": 45.4235,
        "longitude": -75.6979,
        "scale": 5
    },
    {
        "title": "Vancouver",
        "longitude": -123.1207,
        "latitude": 49.2827,
        "scale": 2
    },
    {
        "title": "Yellowknife",
        "latitude": 62.4540,
        "longitude": -114.3718,
        "scale": 1
    }
]

const EXAMPLE2 = [
    {
        "title": "Toronto",
        "latitude": 43.6532,
        "longitude": -79.3832,
        "scale": 10
    },
    {
        "title": "Calgary",
        "longitude": -114.0719,
        "latitude": 51.0447,
        "scale": 3
    },
    {
        "title": "Yellowknife",
        "latitude": 62.4540,
        "longitude": -114.3718,
        "scale": 0.5
    }
]

let imageSeries = makeImageSeries(EXAMPLE);
canadaMap.series.push(imageSeries);

function removeSeries() {
    plotImageSeries(imageSeries, EXAMPLE);
}

function addSeries() {
    plotImageSeries(imageSeries, EXAMPLE2);
}

/* Helper functions */

/**
 * Create and return a new image series for plotting coordinates.
 */
function makeImageSeries() {
    let imageSeries = new am4maps.MapImageSeries();
    imageSeries.mapImages.template.propertyFields.longitude = "longitude";
    imageSeries.mapImages.template.propertyFields.latitude = "latitude";
    imageSeries.mapImages.template.tooltipText = "{title}";
    // imageSeries.mapImages.template.propertyFields.url = "url"; redirect to data source maybe?

    // Create point to plot
    let circle = imageSeries.mapImages.template.createChild(am4core.Circle);

    // Fixed fields
    circle.radius = 4;
    circle.opacity = 0.8;

    // Variable fields
    circle.propertyFields.fill = "color";
    circle.propertyFields.scale = "scale";

    // Animate points
    circle.events.on("inited", event => {
        event.target.animate([{ property: "opacity", from: 0, to: 1 }], 1000, am4core.ease.circleOut)
    })

    return imageSeries;
}

/**
 * Plots the image series onto the canadaMap chart
 * @param {MapImageSeries} series - The image series object
 * @param {Array} data - The data to plot on the series
 */
function plotImageSeries(series, data) {
    // Fill in color
    const COLOUR = "#FF0000"
    let gradient = new am4core.RadialGradient();
    gradient.addColor("#8b0000");
    gradient.addColor(am4core.color("red"));
    data.forEach(region => {
        region.color = gradient;
    })

    // Plot points
    imageSeries.data = data;
}

/**
 * Removes the image series from the canadaMap chart.
 * @param {object} series - The image series to remove
 */
function removeImageSeries(series) {
    canadaMap.series.removeIndex(canadaMap.series.indexOf(series)).dispose();
}