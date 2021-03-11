# Probe Data Analysis for Road Slope  
Vincent Tran [A20396585]  

## Language

Python 3.7  


## Libraries

```
$ pip install pygeohash  
```


## Set up

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

The columns for MatchedPoints is the same as described on the project description.  
The columns for DerivedSlopes is linkPVID, derivedSlope.  
The columns for EvaluatedSlopes is linkPVID, derivedSlope, surveyedSlope.  