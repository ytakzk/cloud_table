# DeepTable

ETH DFAB 2018 Project for Frame Mobel by Nicolas & Yuta  

Exercice to design a fdm printed join for a space frame, aimed at a table.  
The general idea is to have as little human input as possible for the general design of the table.  
The join in contrast would have a strong emphasize on the human intent.  


## Workflow

1. Download mesh data of table from [ShapeNet](https://www.shapenet.org/)
1. Convert meshes into point clouds
1. Train a neural net (auto encoder) to get a latent space which could express fundamental features of table
1. Generate new tables as point clouds through the trained model. Either tweeking of an existing latent space, or complete creation of a new one.
(We might have several options how to use the model to generate a new shape. Need to be discussed.)
1. Selection process (Could be manual process) of the many possible outputs.
1. Convert point clouds to a mesh or edges (Egdes can be rods). 
  -Downsampling of the point cloud? 
  -Rules to pair points for the edges/rods?
1. Apply a joint system between connected edges
1. Completed

## How to Use

1. Clone this repository
1. Download [Point clouds](https://www.dropbox.com/s/vmsdrae6x5xws1v/shape_net_core_uniform_samples_2048.zip) and paste the directory of  `04379243` under `DeepCloud/table_generator/data/`
1. Build a docker image `cd cgal_on_ubuntu && docker build -t pointcloud2mesh`
1. Run a docker container `docker run -it -name pointcloud2mesh -v {ABSOLUTE PATH}/DeepTable/pointcloud2mesh/mount:/DeepTable/pointcloud2mesh/mount pointcloud2mesh`
1. In the docker container, paste the following scripts.
```
cd DeepTable
git init
git remote add origin https://github.com/ytakzk/DeepTable.git
cd pointcloud2mesh
mkdir build
cd build
cmake ..
make
```
1. exit from the container
1. Run a grasshopper file

## Data Source
* [Point clouds](https://www.dropbox.com/s/vmsdrae6x5xws1v/shape_net_core_uniform_samples_2048.zip)  
Mesh model of Shape-Net-Core download 1 point-cloud with 2048 points per model. 
For tables, refer the files under `04379243`.


## Dependences

* [PyTorch](https://pytorch.org/)
* [pyntcloud](https://github.com/daavoo/pyntcloud)  
* [CGAL](https://www.cgal.org/)


## Environments

#### Neural Nets
* Python 3.6.5
* PyTorch 0.4.1
* CUDA 9.0


#### Mesh Generator
* Docker
* C++14 (GNU++14)
* libc++
* CGAL 4.13


## References

#### Papers
* [deep cloud The Application of a Data-driven, Generative Model in Design](https://sites.google.com/site/artml2018/showcase/final-project)
* [PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation](https://arxiv.org/abs/1612.00593)
* [Three-Dimensional Alpha Shapes](http://pub.ist.ac.at/~edels/Papers/1994-J-04-3DAlphaShapes.pdf)


#### Codes
* [fxia22/pointnet.pytorch](https://github.com/fxia22/pointnet.pytorch)
* [optas/latent_3d_points](https://github.com/optas/latent_3d_points)


#### Works
* [Eigenchairs](https://vimeo.com/57901236)


## Misc
* [how to activate an environment in anaconda navigator](https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment)
* [Jupyter notebook config](https://jupyter-notebook.readthedocs.io/en/stable/config.html)
* [Algorithm for generating a triangular mesh from a cloud of points](https://stackoverflow.com/questions/7879160/algorithm-for-generating-a-triangular-mesh-from-a-cloud-of-points)
* [Using CGAL and Xcode](https://3d.bk.tudelft.nl/ken/en/2016/03/16/using-cgal-and-xcode.html)
* [3D Alpha Shapes](https://doc.cgal.org/latest/Alpha_shapes_3/index.html)
* [Everything You Always Wanted to Know About Alpha Shapes But Were Afraid to Ask](http://cgm.cs.mcgill.ca/~godfried/teaching/projects97/belair/alpha.html)
* [VAE with PyTorch](https://github.com/pytorch/examples/blob/master/vae/main.py)
* [Intuitively Understanding Variational Autoencoders](https://towardsdatascience.com/intuitively-understanding-variational-autoencoders-1bfe67eb5daf)
* [What The Heck Are VAE-GANs?](https://towardsdatascience.com/what-the-heck-are-vae-gans-17b86023588a)
