# Probe Data Analysis

Vincent Tran  

Project explanation can be found in the [presentation](docs/Probe%20Point%20Analysis%20for%20Road%20Slope.pdf).

## Language

Python 3.7  


## Libraries

```
$ pip install pygeohash  
```


## Set up

Download the [Partition6467LinkData.csv](https://drive.google.com/file/d/16swaw4P3NDRYbHDXhq1XepzjEZdzxIya/view?usp=sharing) file and the [Partition6467ProbePoints.csv](https://drive.google.com/file/d/1dnc0f53gwT15WhhRFeecQkzrBVflC92X/view?usp=sharing) file.  
Make sure the Partition6467LinkData.csv file and the Partition6467ProbePoints.csv file are in the src directory.  


## Execution

```
$ python MatchPoints.py  
$ python DeriveSlopes.py  
$ python EvaluateSlopes.py  
```

MatchPoints.py will take around 15-25 mins to finish running. After terminating, the output file is Partition6467MatchedPoints.csv.  
Run DeriveSlopes.py after MatchPoints.py finishes. After terminating, the output file is Partition6467DerivedSlopes.csv.  
Run EvaluateSlopes.py after DeriveSlopes.py finishes. After terminating, the output file is Partition6467EvaluatedSlopes.csv.  


## Output

Partition6467MatchedPoints.csv  
Partition6467DerivedSlopes.csv  
Partition6467EvaluatedSlopes.csv  

The columns for MatchedPoints is the same as described in the [MetaData.txt](src/MetaData.txt) file.  
The columns for DerivedSlopes is linkPVID, derivedSlope.  
The columns for EvaluatedSlopes is linkPVID, derivedSlope, surveyedSlope.  
