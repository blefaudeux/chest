function getMin(a, b) {
  if (a < b)
  {
    return a;
  }
  else
  {
    return b;
  }
}

function getMax(a, b) {
  if (a < b)
  {
    return b;
  }
  else
  {
    return a;
  }
}

function processDirectory( dir ) {

  run("Close All");  
  print("Processing directory " + dir);
  
  list = getFileList(root_dir + dir_list[i]);
    
  // Open all the pictures (if tiff ?)
  for (i=0; i<list.length; i++) {
    if (endsWidth(list[i], "tif")
    {
      open(list[i])
    }
  }
  
  // Get the min/max values of the opened pictures
  overallMin = 4096;
  overallMax = 0;
  
  for (i = 1; i <= nImages; i++) {
    selectImage(i);
    getRawStatistics(dummy, mean, min, max, dummy, dummy2);
    overallMin = getMin( overallMin, min);
    overallMax = getMax( overallMax, max);
  }
  
  print("Overall min/max : " + overallMin + " " + overallMax);
  
  // Bring all the pictures down to 8-bits, and save them :
  for (i = 1; i <= nImages; i++) {
    selectImage(i);
    
    setMinAndMax(overallMin, overallMax);
    run("8-bit");
    title = getTitle();
    path = getInfo("image.directory") + File.separator + "8bits_" +getInfo("image.filename");
    saveAs("Tiff", path);
  }
 
  setBatchMode(false);
}


function processAll(root_dir)
{
  run("Close All");  
  setOption("display labels", true);
  setBatchMode(true);
  
  dir_list = getDirectoryList(root_dir);
  processDirectory(dir_list);
  setBatchMode(false);
}

root_dir = getDirectory("Please choose a root directory");
processAll(root_dir);
exit();
