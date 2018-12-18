import {PointCloud} from "./lib/pointcloud.js";
import {createWeatherTable} from "./lib/api.js";

(function() {

    // couple of constants
    var POS_X = 1800;
    var POS_Y = 500;
    var POS_Z = 1800;
    var WIDTH = 1000;
    var HEIGHT = 600;

    var FOV = 45;
    var NEAR = 1;
    var FAR = 4000;

    // some global variables and initialization code
    // simple basic renderer
    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    // setup a camera that points to the center
    let camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4000)
    camera.position.set(POS_X,POS_Y, POS_Z);
    camera.lookAt(new THREE.Vector3(0,0,0));

    var scene = new THREE.Scene();
    scene.add(camera);

    scene.background = new THREE.Color( 0x000000 );

    var spGeo = new THREE.SphereGeometry(600,50,50);
    var planetTexture = THREE.ImageUtils.loadTexture('/static/earth_specular_2048.jpg')
    var mat2 =  new THREE.MeshPhongMaterial( {
        map: planetTexture,
        shininess: 0.9 } )
    const sp = new THREE.Mesh(spGeo, mat2)
    scene.add(sp)


    const light = new THREE.DirectionalLight(0x3333ee, 3.5, 500 );
    scene.add( light );
    light.position.set(POS_X,POS_Y,POS_Z);

    function latLongToVector3(lat, lon, radius) {
        var phi = (lat)*Math.PI/180
        var theta = (lon-180)*Math.PI/180
 
        var x = -(radius) * Math.cos(phi) * Math.cos(theta)
        var y = (radius) * Math.sin(phi)
        var z = (radius) * Math.cos(phi) * Math.sin(theta)
 
        return new THREE.Vector3(x,y,z)
    }

    function render() {

        // var timer = Date.now() * 0.0001;
        // camera.position.x = -(Math.cos( timer ) *  1800);
        // camera.position.z = (Math.sin( timer ) *  1800) ;
        // camera.lookAt( scene.position );
        // light.position = camera.position

        light.lookAt(scene.position)
        renderer.render(scene, camera)
        requestAnimationFrame(render)
    }

    const pos = latLongToVector3(55.7522, 37.6156, 600)

    var geom = new THREE.Geometry()
    var cubeMat = new THREE.MeshLambertMaterial({color: 0xffffff,opacity:0.6, emissive:0xffffff})
    var cube = new THREE.Mesh(new THREE.CubeGeometry(10,10,1/8,1,1,1,cubeMat))

    // geom.position.x = pos.x
    // geom.position.y = pos.y
    // geom.position.z = pos.z

    scene.add(cube)

    render()

    
    createWeatherTable(numberOfTables, function(response) {

        const point_clouds = response.data.point_clouds

        const pc1 = new PointCloud(point_clouds[0])
        pc1.move(-24, 5, 0)
        pc1.add(scene)
        console.log(pc1)

    }, function(error) {

    })




})()
