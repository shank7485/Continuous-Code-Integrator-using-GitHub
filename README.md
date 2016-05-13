# Continuous Integration of files from GitHub using GitHub API:

The purpose of this script is to check for any new commits which are made to a GitHub Repository and if there are any new commits made, the program will download the files in which the commits were made. 

### My Usage:
I am currently using this program to fetch new blog files from my private GitHub Repository into an EC2 instance where my personal blogging website is hosted. The blog system on website renders [Markdown](https://en.wikipedia.org/wiki/Markdown) files present in a directory. This program gets newly commited Markdown files from my GitHub Repo and downloads it into the directory being watched by my blogging system. This way I get a seamless method to add my blog posts easily. 

### System Diagram:
![](add)

### Instruction to Run:
 * The program is be run as a [Cron](https://en.wikipedia.org/wiki/Cron) job (Linux) to check the GitHub repo periodically. Instruction can be found online on how to run programs periodically using Cron job.
 * 'cd' into the folder where the 'commit_checker_and_downloader.py' is present. From there run based on the following. 
 
    If Public Repo:
     ```
    python commit_checker_and_downloader.py <Repo_URL> <Destination Directory>
    ```
    If Private Repo:
    ```
    python commit_checker_and_downloader.py <Repo_URL> <Destination Directory> <username> <password>
    ```

### Example commands:
For public Repositories:
```
python commit_checker_and_downloader.py https://github.com/shank7485/Continuous-Code-Integrator-using-GitHub /home/shashank/Desktop/Recent_files/
```
For private Repositories:
```
python commit_checker_and_downloader.py https://github.com/shank7485/Blog_Files /home/shashank/Desktop/Recent_files/ 'shank7485' 'password'
```

### Note:    
* Make sure to point inside a directory while providing the final destination. Also include username and password inside single quotes to provide special characters. 
* Be sure to have the ['commit_tracker.json'](https://raw.githubusercontent.com/shank7485/Continuous-Code-Integrator-using-GitHub/master/commit_tracker.json) in the same folder as the program. This is needed to keep track of recently commited hash values. 
 
### Issues:
This tool is limited to files which are present at the root of your repository. If recently commited files are inside a folder, those will not be downloaded. Only those which are commited to the root of repository will be downloaded. 
