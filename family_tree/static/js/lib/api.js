
export function fetchPointClouds(numberOfTables, succeeded, failed) {

    axios.get('/fetch_point_clouds/' + numberOfTables)
    .then(function (response) {

        succeeded(response)

    })
    .catch(function (error) {

        console.log(error)
        failed(error)
    })
    .then(function () {
    })
}


export function createWeatherTable(time_index, succeeded, failed) {

    axios.get('/create_weather_table/' + time_index)
    .then(function (response) {

        succeeded(response)

    })
    .catch(function (error) {

        console.log(error)
        failed(error)
    })
    .then(function () {
    })
}