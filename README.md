# DeepTable

ETH DFAB 2018 Project for Frame Mobel by Nicolas & Yuta


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
* CUDA 9.0


#### Mesh Generator
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


## Misc
* [how to activate an environment in anaconda navigator](https://conda.io/docs/user-guide/tasks/manage-environments.html#activating-an-environment)
* [Jupyter notebook config](https://jupyter-notebook.readthedocs.io/en/stable/config.html)
* [Algorithm for generating a triangular mesh from a cloud of points](https://stackoverflow.com/questions/7879160/algorithm-for-generating-a-triangular-mesh-from-a-cloud-of-points)
* [Using CGAL and Xcode](https://3d.bk.tudelft.nl/ken/en/2016/03/16/using-cgal-and-xcode.html)
* [3D Alpha Shapes](https://doc.cgal.org/latest/Alpha_shapes_3/index.html)
* [Everything You Always Wanted to Know About Alpha Shapes But Were Afraid to Ask](http://cgm.cs.mcgill.ca/~godfried/teaching/projects97/belair/alpha.html)
