# Description

Social network leaders detection & classification.

The project from [here](https://docs.google.com/spreadsheets/d/1Wmich78faSgrLE6UtKZ5IJPir7sM4vjnoxIMZj4uckM/edit#gid=564880975)

Trello - [here](https://youtu.be/dQw4w9WgXcQ)

Bonusly - [here](https://youtu.be/dQw4w9WgXcQ)

# Python ```venv```
Run the following script inside project root directory:

```python3 -m venv leadership && source leadership/bin/activate```
```pip install -r requirements.txt```

Run Jupyter Notebook.
You're awesome!


# Docker

### Explanation
Dockerfile in this repository allows to create a docker container with all required software to run all research stuff in /research. This container is using nvidia-docker stuff for CUDA.

# TODO
Добавить .sh скрипт для установки nvidia-container-toolkit.


### Pulling

Now you can simply pull already existing docker images from Docker Hub with 

```docker pull mrartemev/leadership```

If you want to build your own docker image proceed to the next step

### Building
To build an image run following code inside repo directory

``` docker build --rm -t <image_name> . ```

For example:

```docker build --rm -t mrartemev/leadership .```

### Usage
To run docker image run following code inside repo directory

```docker run --rm -v `pwd`:/home/leader --name <name> --runtime nvidia -it -p <port>:8888 <image_name>```

For example:

```docker run --rm -v `pwd`:/home/leader --name leader --runtime nvidia -it -p 7777:8888 mrartemev/leadership```

Running this command will mount docker to your repo directory and execute jupyter notebook command inside your docker.

Open this in your browser to work with repo http://localhost(or yours server-id):8888 (or other chosen <port>). After that, you'll be able to run ipython notebooks in /research

Once you finished just do usual `git add`, `git commit -m`, `git push` routine to commit changes to our repo

I recommend to run this docker image in something like tmux or screen just in case

If something goes wrong ping me @mrartemev



