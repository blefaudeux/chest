
#!/bin/sh

mkdir -p split

if [ "$1" != "" ]; then
    sizex=$1
else
    sizex=1280
fi

if [ "$2" != "" ]; then
    sizey=$2
else
    sizey=720
fi

mkdir -p split/0
mkdir -p split/1

for f in *.jpg
do
    filename="${f%.*}"
    echo "Splitting $f in $sizex x $sizey"
    convert -crop ${sizex}x$sizey $f split/%d/$filename.jpg
done

echo "Done"
