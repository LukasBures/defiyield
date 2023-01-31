# DeFi Yield Demo

## Task
Here is our Rect Database: https://defiyield.app/rekt-database
Task: 
- prepare the visualization of risk vectors and how it evolves over time?
- share a jupyter notebook (or equivalent) in case of this task.

We expected just a few visualizations to highlight what are the most important insights from our database. 

The doc about the API: https://docs.defiyield.app/api/api
The API key: 

The test query:
```
query {
  rekts(
    pageNumber:1
    pageSize:10
    searchText: “terra”
    orderBy: {
      fundsLost: desc
    }
  ) {
    id
    projectName
    description
  }
}
```

## How to run
- Create .env file from .env.example file
- add API key to .env file
- execute main.py

## Results
Results (graphs in pdf format) are stored in ./graphs folder.

## Notes
- Total number of issues = 3167
- Total number of IDs = 3326
- Number of IDs deleted = 3326 - 3167 = 159
- The oldest incident: 2011-06-13 (Mt. Gox (2))
- The newest incident: 2023-01-26 (MutantNFTs)
- The most common issue is: Rugpull (started to increase around 2021), almost 600 issues
- The most money lost in: Rugpull issues
