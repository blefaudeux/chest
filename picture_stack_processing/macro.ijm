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
 
  print("Processing directory " + dir);
  desiredMin = getNumber("Black level ? (-1 if automatic)", 50);
  desiredMax = getNumber("White level ? ", 1000);
  
  list = getFileList(dir);
    
  // Open all the pictures
  for (i=0; i<list.length; i++) {
    if (endsWith(list[i], "tif"))
    {
      open(dir + list[i]);
    }
  }
  
  // Get the min/max values of the opened pictures
   if (desiredMin > -1)
  {
     overallMin = 4096;
     overallMax = 0;
  
     for (i = 1; i <= nImages; i++) {
       selectImage(i);
       getRawStatistics(dummy, mean, min, max, dummy, dummy2);
       overallMin = getMin( overallMin, min);
       overallMax = getMax( overallMax, max);
     }
  
     print("Overall min/max : " + overallMin + " " + overallMax);
  }
  else
  {
   overallMin = desiredMin;
   overallMax = desiredMax;
  }
  
  // Bring all the pictures down to 8-bits, and save them :
  for (i = 1; i <= nImages; i++) {
    selectImage(i);
    
    setMinAndMax(overallMin, overallMax);
    run("8-bit");
    title = getTitle();
    path = getInfo("image.directory") + File.separator + "8bits_" +getInfo("image.filename");
    saveAs("Tiff", path);
  }
  
  run("Close All"); 
}


function processAll(root_dir)
{
  run("Close All");  
  setOption("display labels", true);
  // setBatchMode(true);
  
  list = getFileList(root_dir);
  
  for (i=0; i< list.length; i++)
  {

      if (File.isDirectory( root_dir + list[i]))
      {
         processDirectory( root_dir + list[i]);
      }
  }
   
  // setBatchMode(false);
}

root_dir = getDirectory("Please choose a root directory");
processAll(root_dir);
exit();
