import {PointCloud} from "./lib/pointcloud.js"
import {fetchPointClouds} from "./lib/api.js"

(function() {

    const numberOfTables = 20

    var app = new Vue({
        el: '#app',
        data: {
            table_index_1: 0,
            table_index_2: 9,
            alpha: 0.5,
            number_of_tables: numberOfTables,
            input_data: [],
            input_point_cloud_1: null,
            input_point_cloud_2: null,
            merged_point_clouds: []
        },
        watch: {

            table_index_1: function (newValue, oldValue) {

                if (app.input_point_cloud_1) {

                    app.input_point_cloud_1.update(this.input_data[newValue])
                    this.create(null)
                }

            },
            table_index_2: function (newValue, oldValue) {

                if (app.input_point_cloud_2) {

                    app.input_point_cloud_2.update(this.input_data[newValue])
                    this.create(null)
                }

            },
            alpha: function (newValue, oldValue) {
                this.create(null)
            }
        },
        methods: {
            create: function (event) {
                

                const array1 = this.input_data[this.table_index_1]
                const array2 = this.input_data[this.table_index_2]

                let x1List = []
                let y1List = []
                let z1List = []
                let x2List = []
                let y2List = []
                let z2List = []

                for (let i = 0; i < array1.length; i++) {

                    const coordinate1 = array1[i]
                    const coordinate2 = array2[i]

                    const x1  = coordinate1[0]
                    const y1  = coordinate1[1]
                    const z1  = coordinate1[2]

                    const x2  = coordinate1[0]
                    const y2  = coordinate2[1]
                    const z2  = coordinate2[2]

                    x1List.push(x1)
                    y1List.push(y1)
                    z1List.push(z1)
                    x2List.push(x2)
                    y2List.push(y2)
                    z2List.push(z2)
                }

                axios.post('/manipulate', {
                    x1: x1List,
                    y1: y1List,
                    z1: z1List,
                    x2: x2List,
                    y2: y2List,
                    z2: z2List,
                    alpha: this.alpha
                })
                .then(function (response) {

                    if (app.merged_point_clouds.length > 0) {

                        for (let i = 0; i < response.data.point_clouds.length; i++) {

                            const pc = app.merged_point_clouds[i]
                            pc.update(response.data.point_clouds[i])
                            //pc.resetRotation()
                        }

                    } else {

                        for (let i = 0; i < response.data.point_clouds.length; i++) {

                            const pc = new PointCloud(response.data.point_clouds[i])
                            pc.point.name = i
                            app.merged_point_clouds.push(pc)
                            pc.add(scene)
                            pc.move(-25 + 10 * i, -10, 0)
                        }
                    }

                    //app.input_point_cloud_1.resetRotation()
                    //app.input_point_cloud_2.resetRotation()

                })
                .catch(function (error) {
                    // handle error
                    console.log(error)
                })
                .then(function () {
                    // always executed
                })    
            
            }
        },
        delimiters: ['[[',']]']
    })

    
    fetchPointClouds(numberOfTables, function(response) {

        app.input_data = response.data.point_clouds

        const pc1 = new PointCloud(app.input_data[app.table_index_1])
        pc1.move(-24, 5, 0)
        pc1.add(scene)
        app.input_point_cloud_1 = pc1

        const pc2 = new PointCloud(app.input_data[app.table_index_2])
        pc2.move(24, 5, 0)
        pc2.add(scene)
        app.input_point_cloud_2 = pc2

        app.create(null)

    }, function(error) {

    })

    const scene  = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)

    const renderer = new THREE.WebGLRenderer()
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    scene.background = new THREE.Color( 0xffffff );
    camera.position.z = 30

    const raycaster = new THREE.Raycaster()

    const stats = new Stats();
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.top = '0px';
    stats.domElement.style.right = '0px';
    stats.domElement.style.zIndex = 100;
    document.body.appendChild(stats.domElement)

    let rotate = 0.015
    var animate = function () {

        requestAnimationFrame(animate)

        stats.update()

        if (app.input_point_cloud_1) {

            app.input_point_cloud_1.rotate(-0.012, 0.007, 0.001)
        }

        if (app.input_point_cloud_2) {

            app.input_point_cloud_2.rotate(-0.012, 0.007, 0.001)
        }

        app.merged_point_clouds.forEach(function(pc) {

            pc.rotate(-0.012, 0.007, 0.001)
        })

        renderer.render(scene, camera)
    }

    animate()

    window.addEventListener('mousedown', onDocumentMouseDown, false)
    function onDocumentMouseDown(event) {

        //event.preventDefault()

        if (app.merged_point_clouds.length == 0) { return }

        let rayReceiveObjects = []

        app.merged_point_clouds.forEach(function(pc) {

            rayReceiveObjects.push(pc.point)
        })

        let mouse = new THREE.Vector2()

        mouse.x = (event.clientX / window.innerWidth) * 2 - 1
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1

        raycaster.setFromCamera( mouse, camera )
        const intersects = raycaster.intersectObjects( rayReceiveObjects )

        if (intersects.length > 0) {

            const id = intersects[0].object.name

            const pc = app.merged_point_clouds[id]

            if (pc.meshVisible) {

                pc.switch()
                return
            }

            const array = pc.point_cloud

            let xList = []
            let yList = []
            let zList = []

            for (let i = 0; i < array.length; i++) {

                const coordinate = array[i]

                const x  = coordinate[0]
                const y  = coordinate[1]
                const z  = coordinate[2]

                xList.push(x)
                yList.push(y)
                zList.push(z)
            }

            axios.post('/generate_mesh', {
                x: xList,
                y: yList,
                z: zList,
            })
            .then(function (response) {

                let array = response.data.split('\n')
                array = array.slice(2, array.length - 1)

                app.merged_point_clouds[id].mesh(array)

            })


        }
    }


})()