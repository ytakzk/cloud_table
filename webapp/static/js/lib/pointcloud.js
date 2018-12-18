export class PointCloud {

    constructor(data, scale=12, size=0.1, color=0x111111) {

        this.point_cloud = data
        this.scale = scale

        const geometry = new THREE.BufferGeometry(0, 0, 0)

        let vertices = []
        for (let i = 0; i < data.length; i++) {

            vertices.push(data[i][0] * scale)
            vertices.push(data[i][1] * scale)
            vertices.push(data[i][2] * scale)

        }

        geometry.addAttribute('position', new THREE.BufferAttribute(new Float32Array(vertices), 3))

        const pointMaterial = new THREE.PointsMaterial({
            size: size,
            color: color,
        })

        const edgeMaterial = new THREE.MeshBasicMaterial({ color: color, wireframe: true})

        this.point = new THREE.Points(geometry, pointMaterial)
        this.lines = new THREE.Mesh(geometry, edgeMaterial)
        this.pivot = new THREE.Object3D()

        this.meshVisible = false
    }

    rotate(sx, sy, sz) {

        this.point.geometry.rotateX(sx)
        this.point.geometry.rotateY(sy)
        this.point.geometry.rotateZ(sz)
    }

    add(scene) {

        scene.add(this.pivot)
        this.pivot.add(this.point)
    }

    move(dx=0, dy=0, dz=0) {

        this.pivot.position.x = dx
        this.pivot.position.y = dy
        this.pivot.position.z = dz
    }

    update(data) {

        this.point_cloud = data

        let vertices = []
        let indices = []
        for (let i = 0; i < data.length; i++) {

            vertices.push(data[i][0] * this.scale)
            vertices.push(data[i][1] * this.scale)
            vertices.push(data[i][2] * this.scale)
            indices.push(i)
        }

        this.point.geometry.setIndex(indices)
        this.point.geometry.addAttribute('position', new THREE.BufferAttribute(new Float32Array(vertices), 3))
        this.point.geometry.verticesNeedUpdate = true

        this.pivot.add(this.point)
        this.pivot.remove(this.lines)

        this.meshVisible = false
    }

    switch() {

        if (this.meshVisible) {

            this.pivot.add(this.point)
            this.pivot.remove(this.lines)

        } else {

            this.pivot.remove(this.point)
            this.pivot.add(this.lines)

        }

        this.meshVisible = !this.meshVisible

    }

    mesh(array) {

        let vertices = []
        let indices  = []

        const that = this

        array.forEach(function(str) {

            const vals = str.split(' ')

            if (vals.length == 3) {

                vertices.push(parseFloat(vals[0]) * that.scale)
                vertices.push(parseFloat(vals[1]) * that.scale)
                vertices.push(parseFloat(vals[2]) * that.scale)
            
            } else {

                indices.push(parseInt(vals[1]))
                indices.push(parseInt(vals[2]))
                indices.push(parseInt(vals[3]))
        
            }
        })

        this.point.geometry.setIndex(new THREE.BufferAttribute(new Uint16Array(indices), 1))
        this.point.geometry.addAttribute('position', new THREE.BufferAttribute(new Float32Array(vertices), 3))

        this.point.geometry.verticesNeedUpdate = true

        this.pivot.remove(this.point)
        this.pivot.add(this.lines)

        this.meshVisible = true
    }

    resetRotation() {

        const val = Math.PI / 180 * 90
        this.point.geometry.rotation.x = val
        this.point.geometry.rotation.y = val
        this.point.geometry.rotation.z = val
    }

    recolor(color) {

        this.point.material.color.setHex(color)
        this.lines.material.color.setHex(color)
    }
}