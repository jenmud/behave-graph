# behave-graph
Keeping track of all the behave features, scenarios, and steps can be challenging. So this is a behave scraper creating a dependency graph of features, scenarios, and steps.


## TO DO

* Add in tests!!


# Installing and Developing

## Fork the project and clone it
```bash
# Assuming that you have forked the repo
$ git clone https://github.com/<username>/behave-graph.git
```

## Clone ruruki for examples
```bash
$ git clone https://github.com/optiver/ruruki.git
```

## Get it installed using a python virtualenv
```bash
$ virtualenv behave-graph-ve
$ behave-graph-ve/bin/pip install -U pip setuptools wheel
$ behave-graph-ve/bin/pip install behave-graph  # use -e to do a develop install.
```

## Running a scrape and starting a webserver
```bash
$ ansible-graph-ve/bin/behave-graph --runserver -b ruruki/ruruki/test_behave
INFO:root:Starting server 0.0.0.0:8000
INFO:ruruki_eye.server:Setting up db to <ruruki.graphs.Graph object at 0x10df1b150>
INFO:werkzeug: * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
```

Open a web browser and navigate to the running address provided in the output above.
```
http://0.0.0.0:8080
```

Example of interesting output (assuming that vertex with name="Graph features" has the id *74*)
```
http://localhost:8000/vertices/74?levels=1
```

![Screenshot](/behave-graph.png)
