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

function processDirectory( dir, min, max ) {
 
  print("Processing directory " + dir);
  
  list = getFileList(dir);
    
  // Open all the pictures
  for (i=0; i<list.length; i++) {
    if (endsWith(list[i], "tif") && !startsWith(list[i], "8bits") && !startsWith(list[i], "fused"))
    {
      print("Opening picture : " + list[i]);
      open(dir + list[i]);
    }
  }
  
  
  // Bring all the pictures down to 8-bits, and save them :
  for (i = 1; i <= nImages; i++) {
    selectImage(i);
    
    setMinAndMax(min[i], max[i]);
    run("8-bit");
    title = getTitle();
    
    // Remove existing files if needed
    path = getInfo("image.directory") + File.separator + "8bits_" +getInfo("image.filename");
    
    if(File.exists(path))
    {
      File.delete(path);
    }    
    
    print("Writing picture : " + "8bits_" + getInfo("image.filename"));
    saveAs("Tiff", path);
  }
  
  // Convert the stack to RGB..
  colours = newArray("Red", "Green", "Blue", "Fire", "Cyan" );
  
  for (i = 1; i <= nImages; i++) {
    selectImage(i);
    
    // Give a colour cast
    run( colours[i] );
      
    // Make the picture RGB
    run("RGB Color");
  }
  
  projectionTypes = newArray("Max Intensity", "Min Intensity", "Average Intensity", "Sum Slices", "Standard Deviation", "Median"); 
  
  run("Images to Stack", "name=Coloured fuse");
  // run("Z Project...","start=1 stop="+nImages+" projection=Median");
  run("Z Project...");
  
  dirName = File.getName(dir); 
  path = dir + File.separator + "fused_" + dirName;
  
  // Remove existing file if needed
  if(File.exists(path))
  {
      File.delete(path);
  }
  
  print("Writing picture : " + "fused_" + dirName)
  saveAs("Tiff", path);
  
  run("Close All"); 
}


function processAll(root_dir)
{
  run("Close All");  
  setOption("display labels", true);
  setBatchMode(true);

  min = newArray(0,0,0)
  max = newArray(0,0,0)
  
  min[0] = getNumber("First channel : black level ? ", 100);
  max[0] = getNumber("First channel : white level ? ", 1000);
  
  min[1] = getNumber("Second channel : black level ? ", 100);
  max[1] = getNumber("Second channel : white level ? ", 1000);
  
  min[2] = getNumber("Third channel : black level ? ", 100);
  max[2] = getNumber("Third channel : white level ? ", 1000);
  
  keep_values = getString("Would you like to keep these values for all folders ? (yes/no)", "yes");
  
  list = getFileList(root_dir);
  
  for (i=0; i< list.length; i++)
  {
      if (File.isDirectory( root_dir + list[i]))
      {
	if (keep_values != "yes")
	{
	  min[0] = getNumber("First channel : black level ? ", 100);
	  max[0] = getNumber("First channel : white level ? ", 1000);
	  
	  min[1] = getNumber("Second channel : black level ? ", 100);
	  max[1] = getNumber("Second channel : white level ? ", 1000);
	  
	  min[2] = getNumber("Third channel : black level ? ", 100);
	  max[2] = getNumber("Third channel : white level ? ", 1000);
	}
      
         processDirectory( root_dir + list[i], min, max);
      }
  }
  
  setBatchMode(false);
}

root_dir = getDirectory("Please choose a root directory");
processAll(root_dir);
exit();
