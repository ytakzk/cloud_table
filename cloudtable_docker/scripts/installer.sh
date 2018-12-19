# from local console

# docker run -it --name pointcloud2mesh -v {ABSOLUTE PATH}/DeepTable/pointcloud2mesh/mount:/DeepTable/pointcloud2mesh/mount pointcloud2mesh
# docker run -it --name pointcloud2mesh -v C:/Users/ytakzk/ml/DeepTable/pointcloud2mesh/mount:/DeepTable/pointcloud2mesh/mount pointcloud2mesh

# fetch repository
cd DeepTable
git init
git remote add origin https://github.com/ytakzk/DeepTable.git
git pull origin master

# build pointcloud2mesh
cd pointcloud2mesh
mkdir build
cd build
cmake ..
make

# fetch data source
cd /DeepTable/table_generator/data
curl -L -o ./04379243.zip https://www.dropbox.com/s/fpzchkh1zwvjkn6/04379243.zip?dl=0
rm -f 04379243.zip
unzip ./04379243.zip
