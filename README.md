# photo-archiver 🗂️[🎞️]

<p align="center">
    <a href="#-getting-started">🚀 Getting Started</a> -
    <a href="#-usage">🧑‍💻 Usage</a> -
    <a href="./CHANGELOGS.md">📙Changelogs</a> -
    <a href="#-maintainers">👥 Maintainers</a> -
    <a href="#-contributing">🤝 Contributing</a> -
    <a href="#-license">📄 License</a>
</p>

<p align="center">
    <!-- Project maintenance status -->
    <img src="https://img.shields.io/badge/Build-Passed-gre">
    <img src="https://img.shields.io/badge/Unit Test-Passed-gre">
    <img src="https://img.shields.io/badge/Latest Release-no-red">
    </br>
    <!-- Project development environment -->
    <img src="https://img.shields.io/badge/OS-Windows 11-0079ba">
    <img src="https://img.shields.io/badge/VSC-1.100.2-23a9f2">
    <img src="https://img.shields.io/badge/Python-3.12.4-fee35d">
    </br>
    <!-- Documentation -->
    <img src="https://img.shields.io/badge/License-GPL3-238636">
    <img src="https://img.shields.io/badge/Readme Style-standard-gre">
    <img src="https://img.shields.io/badge/Changelog-Keep A Changelog-f25d30">
</p>


## 📦 About The Project

**photo-archiver** is a lightweight script toolkit designed to simplify the organization and archiving of **JPG** and **RAW** photo files.

It specifically supports automatic management of **RAW negatives** based on their corresponding **JPG** files, enabling photographers to efficiently extract and archive RAW files that match selected JPGs—**a powerful enhancement to modern photo archiving workflows**.

The diagram below illustrates the workflow from shooting to archiving for photographers. During the archiving phase, JPG files are usually selected and categorized first, followed by organizing RAW files according to the same folder structure. Manually sorting RAW files based on selected JPGs can be **extremely tedious and time-consuming**, especially when handling a large number of photos. However, **photo-archiver automates this part of the workflow**, allowing photographers to focus solely on organizing JPGs during the archiving process, thereby significantly simplifying the overall workflow.

```
+-----------------------------------------------------------------------+                      
|Step 01   +----------------+                                           |                      
|Take      |  Shoot photos  |    +--------------------+                 |                      
|Photos    |(Camera & Phone)+--->|Obtain JPGs and RAWs|                 |                      
|          +----------------+    +-------+------------+                 |                      
+----------------------------------------+------------------------------+                      
|Step 02                                 |                              |                      
|Archive         +-----------------------+                              |                      
|JPGs            |                                                      |                      
|          +-----v--------------------+   +---------------------------+ |                      
|          |Organize and archive files+-->|Store files in two folders:| |                      
|          +--------------------------+   |  /JPGs                    | |                      
|                +------------------------+  /RAWs                    | |                      
|                |                        +---------------------------+ |                      
|          +-----v---------------------------+                          |                      
|          |Filter JPGs folder:              |                          |                      
|          |- Delete unwanted                |                          |                      
|          |- Create subfolders to categorize|                          |                      
|          +-----+---------------------------+                          |                      
|                |                                                      |                      
+----------------+------------------------------------------------------+                      
|Step 03   +-----v-------------------------------------+                |                      
|Archive   |Mirror JPGs folder structure in RAWs folder|<---------------+-- photo-archiver     
|RAWs      |to keep corresponding RAWs organized       |                |   automates this task
|          +-------------------------------------------+                |                      
+-----------------------------------------------------------------------+                      
```


## 🚀 Getting Started

Create a Python 3.12.4 environment (either install directly or use conda), and install dependencies (see the list in <a href="./requirements.txt">./requirements.txt</a>):

```bash
pip install -r requirements.txt
```


## 🧑‍💻 Usage

Currently, **photo-archiver** offers two main features:
1. **Automatically organize the RAWs directory** based on a curated JPGs directory by deleting RAW files that do not have corresponding JPGs.
2. **Flatten all JPG files** from the curated JPGs directory into its root folder.

### 🪞 Filter RAWs By JPGs

Filter out unwanted RAW negatives from the RAWs directory based on the curated JPGs directory.

1. Configure the parameters in <a href="./config/filter_raw_by_jpg_config.yaml">./config/filter_raw_by_jpg_config.yaml</a>;
2. Run the following command: `python src.filter_raw_by_jpg`；

Example:
1. **Directory structure and photo-archiver configuration before using photo-archiver:**
    ```
    ### JPGs folder ###
    C:\Users\test\Download\JPGs\
        person\
            DSC_0001.jpg
            DSC_0003.jpg
            DSC_0005.jpg
        scenery\
            DSC_1001.jpg
            DSC_1010.jpg

    ### RAWs folder ###
    C:\Users\test\Download\RAWs\
        DSC_0001.nef
        DSC_0002.nef
        DSC_0003.nef
        ...     # All: from "DSC_0004.nef" to "DSC_1119.nef"
        DSC_1200.nef
    ```
    ```
    ### photo-archiver\config\filter_raw_by_jpg_config.yaml ###
    jpg_dir_abs_path: "C:\Users\test\Download\JPGs\"
    raw_dir_abs_path: "C:\Users\test\Download\RAWs\"
    jpg_exts: [".jpg", ".jpeg"]
    raw_exts: [".nef", ".cr2", ".dng"]
    camera_prefixes: ["dsc", "img"]
    log_file_abs_path: "C:\Users\test\Download\filter_raw_by_jpg.log"
    ```
2. **Directory structure after running photo-archiver:**
    ```
    ### JPGs folder ###
    C:\Users\test\Download\JPGs\
        person\
            DSC_0001.jpg
            DSC_0003.jpg
            DSC_0005.jpg
        scenery\
            DSC_1001.jpg
            DSC_1010.jpg

    ### RAWs folder ###
    C:\Users\test\Download\RAWs\
        DSC_0001.nef
        DSC_0003.nef
        DSC_0005.nef
        DSC_1001.nef
        DSC_1010.nef
    ```

### 👐Flatten JPGs

Flatten all JPG images from the curated JPGs directory into a single-level root directory.

1. Set parameters in <a href="./config/flatten_jpgs_config.yaml">./config/flatten_jpgs_config.yaml</a>;
2. Run the following command: `python src.flatten_jpgs`；

Example:
1. **Directory structure and photo-archiver configuration before using photo-archiver:**
    ```
    ### Input_JPGs folder ###
    C:\Users\test\Download\Input_JPGs\
        xx1\
            yy1\
                DSC_1001.jpg
                DSC_1009.jpg
            yy2\
                DSC_2001.jpg
        xx2\
            yyy1\
                DSC_2834.jpg

    ### Output_JPGs folder ###
    C:\Users\test\Download\Output_JPGs\
        Nothing
    ```

    ```
    ### photo-archiver\config\flatten_jpgs_config.yaml ###
    input_jpg_dir_abs_path: "C:\Users\test\Download\Input_JPGs\"
    output_jpg_dir_abs_path: "C:\Users\test\Download\Output_JPGs\"
    jpg_exts: [".jpg", ".jpeg"]
    number_of_digits: 2
    log_file_abs_path: "C:\Users\text\Download\flatten_jpgs.log"
    ```
2. **Directory structure after running photo-archiver:**
    ```
    ### Input_JPGs folder ###
    C:\Users\test\Download\Input_JPGs\
        xx1\
            yy1\
            yy2\
        xx2\
            yyy1\

    ### Output_JPGs folder ###
    C:\Users\test\Download\Output_JPGs\
        xx1-yy1-01.jpg
        xx1-yy1-02.jpg
        xx1-yy2-01.jpg
        xx2-yyy1-01.jpg
    ```


## 👥 Maintainers

[@OrangeByte42](https://github.com/OrangeByte42).


## 🤝 Contributing

<a href="https://github.com/OrangeByte42/photo-archiver/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=OrangeByte42/photo-archiver" alt="contrib.rocks image" />
</a>


## 📄 License

[GPL3](./LICENSE) © OrangeByte42


## 🔗 Related Efforts

### 💻️ Using Windows batch scripts (bat)

> https://forum.xitek.com/thread-1962205-1-1.html

1. Place the curated JPGs and RAWs to be organized all in one folder;
2. Run the following command, which deletes `.cr3` files in the specified folder `%1` that do not have corresponding `.jpg` files:
    ```bat
    for /f "delims=. tokens=1" %%N in ('dir /b %1\*.cr3') do if not exist %1\%%N.jpg del %1\%%N.cr3
    ```


## 🙏 Acknowledgments

Thanks to:
- [standard-readme](https://github.com/RichardLitt/standard-readme)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [keep-a-changelog](https://github.com/olivierlacan/keep-a-changelog)
- [shields](https://github.com/badges/shields)
- [contributors-img](https://github.com/lacolaco/contributors-img)





