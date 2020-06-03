library(data.table)
library(dplyr)

tweets_whitehouse_conference <- fread('../../gen/data-preparation/output/dataset.csv')

# filter tweets by English language 
tweets_whitehouse_conference <- tweets_whitehouse_conference %>%
  filter(language == "en") %>%
  select(-language)

# filter event specific tweets
# since want to analyse tweets specifically related Trump's whitehouse briefing 
# we set the constraint that the text of the tweets must include either on of 
# following words: 'donaldtrump', 'trump', 'presidenttrump', 'Whitehouse', 
# and / or 'WhitehouseBriefing' 
tweets_whitehouse_conference <- tweets_whitehouse_conference %>%
  mutate(contains_hashtag = grepl('donaldtrump', tolower(text)) + 
           grepl('trump', tolower(text)) + 
           grepl('presidenttrump', tolower(text)) +
           grepl('whitehouse', tolower(text)) +
           grepl('whitehousebriefing', tolower(text))) %>%  
  filter(contains_hashtag >= 1) %>% 
  select(-contains_hashtag)

# tag retweets
tweets_whitehouse_conference <- tweets_whitehouse_conference %>%
  mutate(retweet = ifelse(grepl('^RT', text), TRUE, FALSE))

# add categorized polarity
# we divide tweets into three categories: neutral (where polarity = 0), 
# positive (polarity > 0), and negative (polarity < 0)
tweets_whitehouse_conference <- tweets_whitehouse_conference %>%
  mutate(polarity_category = ifelse(polarity < 0, "negative", 
                                    ifelse(polarity == 0, "neutral", "positive")))

# the code below creates a new column in that takes the hh:mm format from the 
# created_at column and than divides time into ten minute intervals
tweets_whitehouse_conference <- tweets_whitehouse_conference %>%
  mutate(time = substr(created_at, 12, 16)) %>%
  mutate(hour = substr(time, 1, 2)) %>%
  mutate(part_of_hour = (floor(as.numeric(substr(time, 4, 5))/10)) +1) %>%
  mutate(part_of_hour = as.character(part_of_hour)) %>%
  mutate(nr_char = nchar(part_of_hour)) %>%
  mutate(time_interval = ifelse(nr_char == 1, 
                                paste(hour, part_of_hour, sep = '-0'),
                                paste(hour, part_of_hour, sep = '-'))) %>%
  select(-hour, -part_of_hour, -nr_char)

# code to get a cleaner version of the source variable into the dataframe
tweets_whitehouse_conference <- tweets_whitehouse_conference %>%
  mutate(source = sub(".*\\>(.*)\\<.*", "\\1", source, perl=TRUE))

dir.create('../../gen/analysis/temp/', recursive = TRUE)
dir.create('../../gen/analysis/output/', recursive = TRUE)
fwrite(tweets_whitehouse_conference, '../../gen/analysis/temp/preclean.csv')