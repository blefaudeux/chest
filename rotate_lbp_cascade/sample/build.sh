#!/bin/sh 


g++ `pkg-config --cflags opencv` facedetect.cpp -o facedetect `pkg-config --libs opencv`


