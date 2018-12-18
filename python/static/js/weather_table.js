import {PointCloud} from "./lib/pointcloud.js";
import {createWeatherTable} from "./lib/api.js";

(function() {

    var app = new Vue({
        el: '#app',
        data: {
            time: 0,
            point_clouds: [],
            places: [],
            weathers: [],
            place_index: null
        },
        watch: {

            time: function (newValue, oldValue) {

                this.create(null)

            },

        },
        methods: {
            create: function (event) {   
            
                createWeatherTable(this.time, function(response) {

                    app.places   = response.data.places
                    app.weathers = JSON.parse(response.data.weathers)
                    const hasPc = app.point_clouds.length > 0

                    for (let i = 0; i < response.data.point_clouds.length; i++) {

                        const pcData = response.data.point_clouds[i]
                        const place  = app.places[i]

                        const pos = latLongToVector3(place.coord.lat, place.coord.lon, 650)
            
                        if (hasPc) {

                            const pc = app.point_clouds[i]
                            pc.update(pcData)
                            pc.rotate(-1.4, 0.8, 0.0)

                        } else {

                            const pc = new PointCloud(pcData, 65, 2.0, 0xff0044)
                            pc.move(pos.x, pos.y, pos.z)
                            pc.add(scene)
                            pc.rotate(-1.4, 0.8, 0.0)
                            pc.point.name = i

                            app.point_clouds.push(pc)
                        }

                    }
            
                }, function(error) {
            
                })

            }
        },
        delimiters: ['[[',']]']
    })

    app.create()

    // couple of constants
    var POS_X = 0;
    var POS_Y = 0;
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
    canvas.appendChild(renderer.domElement)

    // setup a camera that points to the center
    let camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4000)
    camera.position.set(POS_X,POS_Y, POS_Z);
    camera.lookAt(new THREE.Vector3(0,0,0));

    var scene = new THREE.Scene();
    scene.add(camera);

    //scene.background = new THREE.Color( 0x000000 );
    scene.background = new THREE.Color( 0xffffff );

    var spGeo = new THREE.SphereGeometry(630,50,50);
    var planetTexture = THREE.ImageUtils.loadTexture('/static/earth_specular_2048.jpg')
    var mat2 =  new THREE.MeshPhongMaterial( {
        map: planetTexture,
        shininess: 0.9 } )
    const sp = new THREE.Mesh(spGeo, mat2)
    scene.add(sp)


    let light = new THREE.AmbientLight(0xffffff);
    scene.add( light )

    const raycaster = new THREE.Raycaster()

    function latLongToVector3(lat, lon, radius) {
        var phi = (lat)*Math.PI/180
        var theta = (lon-180)*Math.PI/180
 
        var x = -(radius) * Math.cos(phi) * Math.cos(theta)
        var y = (radius) * Math.sin(phi)
        var z = (radius) * Math.cos(phi) * Math.sin(theta)
 
        return new THREE.Vector3(x,y,z)
    }

    const controls = new THREE.OrbitControls(camera, canvas)

    function render() {

        controls.update();

        renderer.render(scene, camera)
        requestAnimationFrame(render)
    }

    render()

    window.addEventListener('mousedown', onDocumentMouseDown, false)
    function onDocumentMouseDown(event) {

        //event.preventDefault()

        if (app.point_clouds.length == 0) { return }

        let rayReceiveObjects = []

        app.point_clouds.forEach(function(pc, i) {

            rayReceiveObjects.push(pc.point)
        })

        let mouse = new THREE.Vector2()

        mouse.x = (event.clientX / window.innerWidth) * 2 - 1
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1

        raycaster.setFromCamera( mouse, camera )
        const intersects = raycaster.intersectObjects( rayReceiveObjects )

        if (intersects.length > 0) {

            const id = intersects[0].object.name
            app.place_index = id

            app.point_clouds.forEach(function(pc, i) {

                const color = i == id ? 0x880022 : 0xff0044

                pc.recolor(color)
            })
            console.log(id)

        }
    }

})()