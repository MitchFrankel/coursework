# Overview # 

This directory contains modules, classes, and functions that can be used 
across multiple projects. If this directory exists in anything except the
"common" repo, it is not to be edited in the current project/repo. To update 
any files in this directory:  
1. update and push code in whaterver branch of common repo.  
1. add & fetch common repo branch as remote branch in current repo/project.  
1. merge / cherry pick this remote branch into whatever branch of current repo.  
1. There will likely be a necessity to resolve conflicts on the main README.md 
from the common repo base directory and possibly the gitignore