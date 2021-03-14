/*
    Create AmMap using JSON data from server
*/

// global parameters object for filtering
let PARAMS = {};


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
        "scale": 5,
        "cases": 1248
    },
    {
        "title": "Vancouver",
        "longitude": -123.1207,
        "latitude": 49.2827,
        "scale": 2,
        "cases": 943
    },
    {
        "title": "Yellowknife",
        "latitude": 62.4540,
        "longitude": -114.3718,
        "scale": 1,
        "cases": 67
    }
]

const EXAMPLE2 = [
    {
        "title": "Toronto",
        "latitude": 43.6532,
        "longitude": -79.3832,
        "scale": 10,
        "cases": 4348
    },
    {
        "title": "Calgary",
        "longitude": -114.0719,
        "latitude": 51.0447,
        "scale": 3,
        "cases": 1290
    },
    {
        "title": "Yellowknife",
        "latitude": 62.4540,
        "longitude": -114.3718,
        "scale": 0.5,
        "cases": 16
    },
    {
        "title": "Edmonton",
        "latitude": 53.5461,
        "longitude": -113.4938,
        "scale": 2.5,
        "cases": 1904
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

/* API Request */

/**
 * Send a get request to retrive data 
 */
function getData() {
    showSpinner();
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        const json = JSON.parse(this.responseText);
        let data = [];
        for (const region in json) {
            data.push({
                "title": region,
                "latitude": json[region]["latitude"],
                "longitude": json[region]["longitude"],
                "cases": json[region]["cases"],
                "scale": 3
            })
        }
        plotImageSeries(imageSeries, data);
        hideSpinner();
        console.log(data)
      }
    };
    xhttp.open("GET", `/api/cases${formatParams(PARAMS)}`, true);
    xhttp.send();
}

// wrapper function to update params and get data
function APIwrapper(f) {
    f();
    getData();
}

/* Helper functions */

/**
 * Create and return a new image series for plotting coordinates.
 */
function makeImageSeries() {
    let imageSeries = new am4maps.MapImageSeries();
    imageSeries.mapImages.template.propertyFields.longitude = "longitude";
    imageSeries.mapImages.template.propertyFields.latitude = "latitude";
    imageSeries.mapImages.template.tooltipText = "{title}: {cases} cases";
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
        event.target.animate([{ property: "opacity", from: 0, to: 0.8 }], 1000, am4core.ease.circleOut)
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
 * @param {MapImageSeries} series - The image series to remove
 */
function removeImageSeries(series) {
    canadaMap.series.removeIndex(canadaMap.series.indexOf(series)).dispose();
}


/** 
 * Format get query string. Modified from:
 * https://stackoverflow.com/questions/8064691/how-do-i-pass-along-variables-with-xmlhttprequest
 * @param {Object} params - The get parameters
 */
function formatParams(params){
    if (Object.keys(params).length === 0) // no params
        return "";
    return "?" + Object
          .keys(params)
          .map(function(key){
            return params[key] !== null ? key+"="+encodeURIComponent(params[key]) : ''
          })
          .filter(s => {return s !== ''})
          .join("&");
}


/**
 * Display the spinner
 */
function showSpinner() {
    document.getElementById("spinner").style.visibility = "visible";
}

/**
 * Hide the spinner
 */
function hideSpinner() {
    document.getElementById("spinner").style.visibility = "hidden";
}