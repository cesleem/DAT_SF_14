# Lab 18: MapReduce & Hadoop

### Streaming MapReduce with Python

This example uses any text file as the data. Here are simple [mapper](mapper.py) and [reducer](reducer.py) scripts. 

#### cat command
Before running the above two scripts, take a few minutes to understand `cat` command in linux/unix:
[http://www.techonthenet.com/unix/basic/cat.php](http://www.techonthenet.com/unix/basic/cat.php)

In your terminal, navigate to the directory of this lab, something like this:

```
cd DAT_SF_14/labs/18_mapreduce/
```

Try the following in the terminal:

```
cat 4300.txt.utf-8.txt
```

#### head command
Read the first few lines of the given file:

```
head 4300.txt.utf-8.txt
```


#### pipe \|
Understand pipeline (\|) in linux/unix:

[http://www.westwind.com/reference/os-x/commandline/pipes.html](http://www.westwind.com/reference/os-x/commandline/pipes.html)

#### run streaming MapReduce with Python

In your terminal, navigate to the directory of this lab, something like this:

```
cd DAT_SF_14/labs/18_mapreduce/
```

Let's run MapReduce on a small sample by using `head`:

```
head 4300.txt.utf-8.txt | python mapper.py | sort | python reducer.py
```

Looks cool? Let's run using the complete file:

```
cat 4300.txt.utf-8.txt | python mapper.py | sort | python reducer.py
```

Alternatively, you can save the output to a file (e.g., `output.txt`):


```
cat 4300.txt.utf-8.txt | python mapper.py | sort | python reducer.py > output.txt
```

Change the filename to your faviroiate text file and check the results.

### In-class Discussions:
* How to implement groupby-then-sum using MapReduce?
* How to implement groupby-then-average using MapReduce?

### More exercises (optional):
* Retreive data via twitter API. Can you run MapReduce word count to get the most popular hashtags?


### More resources:
* Hadoop: [https://hadoop.apache.org/](https://hadoop.apache.org/)
* Google's MapReduce paper: [http://research.google.com/archive/mapreduce.html](http://research.google.com/archive/mapreduce.html)
* [Mahout](http://mahout.apache.org/) is a project for doing large scale machine learning. It was originally mostly map-reduce oriented, but in April 2014 announced a move toward Spark.
* [Pig](http://pig.apache.org/) lets you write [Pig Latin](http://pig.apache.org/docs/r0.7.0/piglatin_ref2.html) scripts for doing complex map-reduce tasks more easily. [Hortonworks](http://hortonworks.com/) has an introductory [tutorial](http://hortonworks.com/hadoop-tutorial/how-to-process-data-with-apache-pig/). [Mortar](http://www.mortardata.com/) has a [tutorial](http://help.mortardata.com/technologies/pig/learn_pig) as well. You can also run [Pig on Amazon EMR](http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-pig-launch.html).
* [Hive](http://hive.apache.org/) adds some more structure to data and let's you write [HiveQL](https://cwiki.apache.org/confluence/display/Hive/LanguageManual), which is very close to SQL. You can also run [Hive on Amazon EMR](http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-hive.html).
* There's also big graph processing as in [Giraph](http://giraph.apache.org/), which is inspired by Google's [Pregel](http://dl.acm.org/citation.cfm?id=1807184).

