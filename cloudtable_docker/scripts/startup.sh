# docker run -it --name cloud_table -v {ABSOLUTE PATH}/cloud_table:/cloud_table -p 9997-9999:9997-9999 cloud_table
# docker run -it --name cloud_table -v C:/Users/ytakzk/ml/cloud_table:/cloud_table -p 9997-9999:9997-9999 cloud_table

mkdir /cloud_table/data

# build pointcloud2mesh
cd cloud_table/pointcloud2mesh
mkdir build
cd build
cmake ..
make

# fetch data source
cd /cloud_table/data
curl -L -o ./04379243.zip https://www.dropbox.com/s/fpzchkh1zwvjkn6/04379243.zip?dl=0
unzip ./04379243.zip
rm -f 04379243.zip
mkdir 04379243_csv

cd /cloud_table/table_generator
python3 convert_ply_to_csv.py