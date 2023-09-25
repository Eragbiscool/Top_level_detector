# Top_level_detector
This is a project to make life easier for verification engineers to get the top-level module name, module count, and more(coming up next!) from a big RTL or Gate Level Netlist

## How to use it?

You can find a variable accepting your filepath naming **provide_filelist_path** and you can provide your filepath there. The report will give you the name of the top module of the given design file and the number of modules defined in the file.


You can put the path of all the design files in a single **.txt** file and provide that filepath of that **.txt** file to the variable **provide_filelist_path**. The rest is on the script!

You can have your library files separated now and the script will return you a list of probable top modules if there are multiple possible top modules.

We will have more features eventually in the future to make it even better.
