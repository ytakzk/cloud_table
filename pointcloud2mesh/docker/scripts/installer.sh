# from local console

# docker run -it --name pointcloud2mesh -v {ABSOLUTE PATH}/DeepTable/pointcloud2mesh/mount:/DeepTable/pointcloud2mesh/mount pointcloud2mesh
# docker run -it --name pointcloud2mesh -v C:/Users/ytakzk/ml/DeepTable/pointcloud2mesh/mount:/DeepTable/pointcloud2mesh/mount pointcloud2mesh

# inside of docker container
cd DeepTable
git init
git remote add origin https://github.com/ytakzk/DeepTable.git
git pull origin master
cd pointcloud2mesh
mkdir build
cd build
cmake ..
make

