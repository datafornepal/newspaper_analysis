## Time Tracking

### Present (11/11/2020)

#### Fetch data and perform analysis only on freshly fresher data (previously analyzed dataset is not touched)

```
fetch_data and compile_data 14.775455713272095
level_1_analysis 14.979163646697998
level_2_filter  15.038641929626465
level_2_analysis  15.236831188201904
level_3_analysis  15.414860725402832
```

#### Fetch data and perform analysis on all data (previously analyzed dataset is analyzed again). This is helpful if some parameter of testing is changed. (For example if another keyword were to be introduced in level 1 analysis)

Notes

- This was the pith of previous implementation. The analysis for the entire dataset was performed instead of just the new articles that were fetched. 
- Even when new keywords are introduced, it is better to perform this step in localhost and upload the datasets in production.

```
fetch_data and compile_data 10.52099084854126
reset_data 10.522985219955444
level_1_analysis 36.70826315879822
level_2_filter  36.76681447029114
level_2_analysis  53.337952613830566
level_3_analysis  55.175861835479736
```

#### Fetch data and conclude that there is nothing to analyze because all tasks have been completed previously. There are going to be instances when all fresh data has also already been fetched. If the request were to be run again, (this might happen for multiple reasons). 

```
fetch_data and compile_data 12.723800659179688
level_1_analysis 12.946254014968872
level_2_filter  13.002144575119019
level_2_analysis  13.193142414093018
level_3_analysis  13.365142345428467
```



#### Previously 

1. Read the latest news articles from the RSS source (fetch_data)
2. Convert the news articles into a pandas dataframe, open the previous stored dataset, convert that into another pandas dataframe, and merge them, remove duplicates.
3. Save the compiled file
4. Read the compiled file
5. Drop where url or content is null (for an extreme case)
6. Perform level 1 analysis by adding the supporting keywords into a column as list
7. Continue level 1 analysis by counting the rows with lists with len greater than 0
8. Check level 2 and level 3 continuation by validating if the articles have certain phrases
9. If condition met for level 2, for level 2 perform level 2 analysis by adding the supporting keywords into a column as list
10. Continue level 2 analysis by counting the rows with lists with len greater than 0
11. If condition met for level 3, for level 3 perform level 3 analysis by adding the supporting keywords into a column as list
12. Continue level 3 analysis by counting the rows with lists with len greater than 0
13. Store results (not here)

#### 

### Timings only for Himalayan times (for any implementation of previous model)

```
fetch_data 1.0984246730804443
compile_all_data 1.70798659324646
level_1_analysis 40.60980725288391
level_2_filter 40.75982451438904
level_2_analysis 47.8614776134491
level_3_analysis 52.45846652984619
```



-----

## Notes

** All times in seconds

** The times follow cumulative additions between process flows

** level1 analysis is the most expensive operation

** current implementation support scalability because the data analysis happens in constant process instead of a linear process

