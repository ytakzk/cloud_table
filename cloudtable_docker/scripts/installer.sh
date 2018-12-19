# from local console

# docker build ./ -t cloud_table

# docker run -it --name cloud_table -v {ABSOLUTE PATH}/cloud_table/mount:/cloud_table/mount pointcloud2mesh
# docker run -it --name cloud_table -v C:/Users/ytakzk/ml/cloud_table/mount:/cloud_table/mount -p 9997-9999:9997-9999 cloud_table

# fetch repository
cd cloud_table
git init
git remote add origin https://github.com/ytakzk/cloud_table.git
git pull origin master

# build pointcloud2mesh
cd pointcloud2mesh
mkdir build
cd build
cmake ..
make

# fetch data source
cd /mount
curl -L -o ./04379243.zip https://www.dropbox.com/s/fpzchkh1zwvjkn6/04379243.zip?dl=0
unzip ./04379243.zip
rm -f 04379243.zip
mkdir 04379243_csv

cd /cloud_table/table_generator
python3 convert_ply_to_csv.py