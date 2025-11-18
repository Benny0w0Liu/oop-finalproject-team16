# Final Project of 114-1 CSE3002 Object-Oriented Programming
group member: 
* [B123245013 劉邦均](https://github.com/Benny0w0Liu) -> nick name: Benny
* [B123045009 陳予涵](https://github.com/Johnnnnnnnnnnnnnnnnnnn)
* [B123040027 林昱辰](https://github.com/ufirstfloor)

# set up the environment
1. add `pyproject.toml` to the `Gymnasium` folder.

    * `pyproject.toml`-> 
        ``` 
        [project]
        name = "gymnasium-project"
        version = "0.1.0"
        description = "OOP group project Gymnasium environment"
        authors = [
        { name = "Benny", email = "bennyliu9005@gmail.com" }
        ]

        [build-system]
        requires = ["setuptools","wheel"]
        build-backend = "setuptools.build_meta"
        ```

2. Create a virtual environment
    * ```python -m venv .venv```

3. Activate the virtual environment
    * ```.venv/bin/activate```

4. Navigate to the Gymnasium directory
    * ```cd group_project/Gymnasium```
5. Install Gymnasium in editable mode
    * ```pip install -e .```

6. Install additional dependencies
    * ```pip install "gymnasium[classic_control]"```
    * ```pip install matplotlib```
7. Verification
    * Run the following command to verify that the installation is successful:
    `pip list`

    * Sample Output of Benny's computer:
        ```
        Package              Version     Editable project location
        -------------------- ----------- -------------------------------------------
        cloudpickle          3.1.2
        contourpy            1.3.3
        cycler               0.12.1
        Farama-Notifications 0.0.4
        fonttools            4.60.1
        gymnasium            1.2.2
        gymnasium-project    0.1.0       D:\Github\114-1-OOP-group-project\Gymnasium
        kiwisolver           1.4.9
        matplotlib           3.10.7
        numpy                2.3.5
        packaging            25.0
        pillow               12.0.0
        pip                  24.0
        pygame               2.6.1
        pyparsing            3.2.5
        python-dateutil      2.9.0.post0
        six                  1.17.0
        typing_extensions    4.15.0
        ```
# run the virtual environment & the programs
1. enter virtual environment:  `.venv/bin/activate`
2. go to part you want, for example: `cd part1`
3. [!!! instruction to run the code !!!](https://github.com/ccslab1/Group-Project?tab=readme-ov-file#-running-the-project)
4. to leave virtual environment: `deactivate`

