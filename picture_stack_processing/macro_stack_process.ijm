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

function processDirectory( dir, min1, max1, min2, max2, min3, max3 ) {
 
  print("Processing directory " + dir);
  
  list = getFileList(dir);
    
  // Open all the pictures
  for (i=0; i<list.length; i++) {
    if (endsWith(list[i], "tif") && !startsWith(list[i], "8bits"))
    {
      open(dir + list[i]);
    }
  }
  
  min = newArray(min1, min2, min3);
  max = newArray(max1, max2, max3);
  
  
  // Bring all the pictures down to 8-bits, and save them :
  for (i = 1; i <= nImages; i++) {
    selectImage(i);
    
    setMinAndMax(min[i], max[i]);
    run("8-bit");
    title = getTitle();
    path = getInfo("image.directory") + File.separator + "8bits_" +getInfo("image.filename");
    saveAs("Tiff", path);
  }
  
  // Convert the stack to RGB..
  for (i = 1; i <= nImages; i++) {
    selectImage(i);
    if( i == 1)
    {
      run("Red");
    }
    
    if( i == 2)
    {
      run("Green");
    }
    
    if( i == 3)
    {
      run("Blue");
    }
    
    if( i == 4)
    {
      run("Fire");
    }

    if( i == 5)
    {
      run("Cyan");
    }
      
    run("RGB Color");
  }
  
  run("Images to Stack", "name=Coloured fuse");
  run("Z Project...");
  
  path = dir + File.separator + "fused";
  saveAs("Tiff", path);
  
  run("Close All"); 
}


function processAll(root_dir)
{
  run("Close All");  
  setOption("display labels", true);
  setBatchMode(true);

  min1 = getNumber("First channel : black level ? ", 100);
  max1 = getNumber("First channel : white level ? ", 1000);
  
  min2 = getNumber("Second channel : black level ? ", 100);
  max2 = getNumber("Second channel : white level ? ", 1000);
  
  min3 = getNumber("Third channel : black level ? ", 100);
  max3 = getNumber("Third channel : white level ? ", 1000);
  
  keep_values = getString("Would you like to keep these values for all folders ? (yes/no)", "yes");
  
  list = getFileList(root_dir);
  
  for (i=0; i< list.length; i++)
  {
      if (File.isDirectory( root_dir + list[i]))
      {
	if (keep_values != "yes")
	{
	  min1 = getNumber("First channel : black level ? ", 100);
	  max1 = getNumber("First channel : white level ? ", 1000);
	  
	  min2 = getNumber("Second channel : black level ? ", 100);
	  max2 = getNumber("Second channel : white level ? ", 1000);
	  
	  min3 = getNumber("Third channel : black level ? ", 100);
	  max3 = getNumber("Third channel : white level ? ", 1000);
	}
      
         processDirectory( root_dir + list[i], min1, max1, min2, max2, min3, max3);
      }
  }
   
  setBatchMode(false);
}

root_dir = getDirectory("Please choose a root directory");
processAll(root_dir);
exit();
