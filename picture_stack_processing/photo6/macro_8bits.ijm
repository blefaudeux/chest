run("Window/Level...");
setMinAndMax(20, 300);
run("8-bit");
path = getInfo("image.directory")+File.separator+"8bits"+File.separator+getInfo("image.filename");
saveAs("Tiff", path);
close();
