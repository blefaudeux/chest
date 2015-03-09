run("Window/Level...");
setMinAndMax(120, 230);
run("8-bit");title = getTitle();path = getInfo("image.directory")+File.separator+"8bits"+File.separator+getInfo("image.filename");saveAs("Tiff", path);