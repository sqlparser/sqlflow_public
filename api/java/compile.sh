#!/bin/bash

cur_dir=$(pwd)

function compile(){
    src_dir=$cur_dir/src
    bin_dir=$cur_dir/lib
    class_dir=$cur_dir/class


    rm -rf $src_dir/sources.list
    find $src_dir -name "*.java" > $src_dir/sources.list
    cat  $src_dir/sources.list


    rm -rf $class_dir
    mkdir $class_dir
    cp $cur_dir/MANIFEST.MF $class_dir
    cp -r $cur_dir/lib $class_dir

    javac -d $class_dir  -cp .:$bin_dir/fastjson-1.2.47.jar:$bin_dir/commons-codec-1.10.jar:$bin_dir/commons-logging-1.2.jar:$bin_dir/slf4j-api-1.7.25.jar:$bin_dir/slf4j-log4j12-1.7.25.jar:$bin_dir/httpcore-4.4.9.jar:$bin_dir/httpclient-4.5.5.jar:$bin_dir/httpmime-4.5.6.jar -g -sourcepath $src_dir @$src_dir/sources.list

    cd $class_dir
    jar -cvfm $cur_dir/grabit-java.jar MANIFEST.MF *
}

compile
exit 0