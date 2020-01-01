# input:
# two schedules for two persons
# two intervals of daily availability
# meeting necessary time
#
# output:
# a list with all the intervals in which the two person can take a meeting together

import pprint


def get_time_in_minutes(hour_string):
    hour, minutes = hour_string.split(":")
    return int(hour) * 60 + int(minutes)


def get_time_from_minutes(minutes):
    hour = int(minutes / 60)
    minutes_left = minutes % 60
    if minutes_left > 10:
        return f'{hour}:{minutes_left}'
    else:
        return f'{hour}:0{minutes_left}'


def get_common_availability(availability_one, availability_two):
    common_availability = list()
    if get_time_in_minutes(availability_one[0]) > get_time_in_minutes(availability_two[0]):
        common_availability.append(availability_one[0])
    else:
        common_availability.append(availability_two[0])
    if get_time_in_minutes(availability_one[1]) < get_time_in_minutes(availability_two[1]):
        common_availability.append(availability_one[1])
    else:
        common_availability.append(availability_two[1])
    return common_availability


def add_schedule_to_set(my_set, my_schedule):
    for interval in my_schedule:
        for number in range(get_time_in_minutes(interval[0]), get_time_in_minutes(interval[1]) + 1):
            my_set.add(number)


def find_meeting_interval(schedule_one, ava_one, schedule_two, ava_two, meeting_time_given):

    common_busy_time = set()
    add_schedule_to_set(common_busy_time, schedule_one)
    add_schedule_to_set(common_busy_time, schedule_two)

    common_availability = get_common_availability(ava_one, ava_two)

    start_time = get_time_in_minutes(common_availability[0])
    end_time = get_time_in_minutes(common_availability[1])
    free_time = list()
    while start_time + meeting_time_given <= end_time:
        if start_time + 1 not in common_busy_time and (start_time + meeting_time_given - 1) not in common_busy_time:
            new_list = list()
            new_list.append(get_time_from_minutes(start_time))
            new_list.append(get_time_from_minutes(start_time + meeting_time_given))
            free_time.append(new_list)
        start_time += meeting_time_given

    intervals_free_found_number = len(free_time)
    iterator = 0
    while iterator < intervals_free_found_number - 2:
        if get_time_in_minutes(free_time[iterator][1]) == get_time_in_minutes(free_time[iterator + 1][0]):
            free_time[iterator][1] = free_time[iterator + 1][1]
            free_time.remove(free_time[iterator + 1])
            intervals_free_found_number -= 1
        else:
            iterator += 1
    return free_time


# test input

first_program = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
first_availability = ['9:00', '20:00']
second_program = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
second_availability = ['10:00', '18:30']
time = 30

pprint.pprint(find_meeting_interval(first_program, first_availability, second_program, second_availability, time))
