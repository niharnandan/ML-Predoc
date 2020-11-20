if not exist "data" mkdir data

curl https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar > "data\imdb_crop.tar"

curl https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/wiki_crop.tar > "data\wiki_crop.tar"