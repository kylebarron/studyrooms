# Library Study Room Reservation Data

x <- c("tidyverse", "stringr", "lubridate", "forcats", "magrittr", "feather")
lapply(x, library, character.only = TRUE)
rm(list = ls())

# Import all csv files and append them into a list
data <- lapply(file.path("data", "rawdata", list.files(path = "data/rawdata/", pattern = "*.csv")),
               read_csv,
               col_types = cols(.default = col_character())) %>%
  bind_rows()


# Clean data into desired columns
data_clean <- data %>%
  mutate(scrape_time = ymd_hms(current_time, tz = "America/Los_Angeles"),
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
  # Make room_date
  mutate(room_date = as_date(room_begin)) %>%
  # Round scrape_time down to nearest minute
  mutate(scrape_time = floor_date(scrape_time, unit = "minute")) %>%
  # Make scrape_id
  # Instead, I should make the scrape_id as evenly spaced every 5 minutes
  #mutate(scrape_id = as.numeric(factor(scrape_time))) %>%
  # Make categorical variable for powell vs yrl_rooms vs yrl_pods
  mutate(type = ifelse(str_detect(room_name, "Group Study Room"), "powell", NA),
         type = ifelse(str_detect(room_name, "Pod"), "yrl_pod", type),
         type = ifelse(str_detect(room_name, "Room G[0-9]+"), "yrl_room", type)) %>%
  mutate(type = factor(type)) %>%
  rename(location = type) %>%
  select(room_name, room_begin, room_end, room_date, everything())

room_ids <- tibble(
  room_name = levels(factor(data_clean$room_name)),
  room_id = 1:41
)

data_clean <- data_clean %>%
  left_join(room_ids, by = "room_name")

# Take out any scrapings that were not multiples of 5
data_clean <- data_clean %>%
    filter(as.numeric(minute(scrape_time)) %% 5 == 0)

min_scrape_time <- min(data_clean$scrape_time)
max_scrape_time <- max(data_clean$scrape_time)
all_times <- seq.POSIXt(min_scrape_time, max_scrape_time, 300)

scrape_ids <- tibble(scrape_id = 1:length(all_times), 
                     scrape_time = all_times)

data_clean <- data_clean %>%
  left_join(scrape_ids, by = "scrape_time")



write_feather(data_clean, "data/avail_rooms.feather")

