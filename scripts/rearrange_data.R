# Try to rearrange data in a more useful way

x <- c("tidyverse", "stringr", "lubridate", "forcats", "magrittr", "feather")
lapply(x, library, character.only = TRUE)
rm(list = ls())

avail_rooms <- read_feather("data/avail_rooms.feather")

# For each day of the study rooms, I want to know what the total possible room-times are
# Basically for each room_date and location, I just need to know what the earliest and latest openings ever were

lib_times <- avail_rooms %>%
  group_by(room_date, location) %>%
  summarize(min_time = min(room_begin),
            max_time = max(room_begin))

# One observation per room/unit per block of available time
# I might be able to create this from scratch from the lib_times data
# For now I'll start on the 9th

all_times <- avail_rooms %>%
  arrange(room_begin, room_end, location, scrape_id) %>%
  group_by(room_begin, room_end, location) %>%
  filter(row_number() == 1,
         mday(room_begin) >= 9) %>%
  select(-c(scrape_time, scrape_id, room_name))

room_names <- avail_rooms %>%
  select(location, room_name) %>%
  group_by(location, room_name) %>%
  distinct()

all_times_all_rooms <- 
  full_join(all_times, room_names, by = "location") %>%
  arrange(room_begin, room_name)
rm(room_names, lib_times, all_times)
# all_times_all_rooms is every time slot in the data for every room


last_avail <- avail_rooms %>%
  arrange(room_name, room_begin, scrape_time) %>%
  group_by(room_name, room_begin) %>%
  filter(row_number() == n())

# All scrape times with their id
scrape_times <- avail_rooms %>%
  select(scrape_time, scrape_id) %>%
  distinct()

# Now merge the total possible room-times with when they were reserved
# Note that this is abstracting from possible cancellations
reserved_rooms <- 
  left_join(all_times_all_rooms, last_avail, 
            by = c("room_begin", "room_end", "room_date", "room_dow", "location", "room_name"))

# Any times when the scrape time is longer than 5 minutes?
scrape_times <- avail_rooms %>%
  group_by(scrape_time, scrape_id) %>%
  distinct() %>%
  ungroup() %>%
  arrange(scrape_time) %>%
  mutate(prev_scrape_time = lag(scrape_time),
         duration = scrape_time - prev_scrape_time) %>%
  arrange(desc(duration)) %>%
  View()
# Note: Basically missed a whole day on March 10, 2017

# Let's cut scrapes from before March 11 for now
# and rooms from before March 13

all_room_slots <- all_times_all_rooms %>%
  filter(room_begin >= mdy("March 13 2017"))















