# Library Study Room Reservation Data

setwd("~/Dropbox/research/studyrooms/data")

library(tidyverse)
library(lubridate)
library(stringr)

# Import all csv files and append them into a list
data <-lapply(list.files(pattern = "*.csv"), read_csv, col_types = cols(.default = col_character())) %>%
  bind_rows()

# Clean data into desired columns
data <- data %>%
  mutate(scrape_time = ymd_hms(current_time),
         # Clean extra character symbols:
         room_name = str_sub(.$`1`, 2, -2),
         `2` = str_sub(.$`2`, 2, -1),
         `5` = str_sub(.$`5`, 1, -2),
         room_date = mdy(str_c(data$`4`, " ", data$`5`))) %>%
  separate(`2`, into = c("begin_time", "end_time"), sep = " - ") %>%
  # grep("America",OlsonNames(),value=TRUE) to find TZ
  mutate(room_begin = mdy_hm(str_c(data$`4`, " ", data$`5`, " ", .$begin_time), tz = "America/Los_Angeles"),
         room_end = mdy_hm(str_c(data$`4`, " ", data$`5`, " ", .$end_time), tz = "America/Los_Angeles")) %>%
  rename(room_dow = `3`) %>%
  select(room_name, room_begin, room_end, room_dow, scrape_time) %>%
  # Make scrape_id
  mutate(scrape_id = as.numeric(factor(scrape_time))) %>%
  # Make categorical variable for powell vs yrl_rooms vs yrl_pods
  mutate(type = ifelse(str_detect(room_name, "Group Study Room"), "powell", NA),
         type = ifelse(str_detect(room_name, "Pod"), "yrl_pod", type),
         type = ifelse(str_detect(room_name, "Room G[0-9]+"), "yrl_room", type)) %>%
  mutate(type = factor(type))

