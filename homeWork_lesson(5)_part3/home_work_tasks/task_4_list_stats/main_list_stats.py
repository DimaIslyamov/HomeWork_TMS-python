from home_work_tasks.data import generate_random_list
from home_work_tasks.task_4_list_stats.list_stats import get_list_stats


value_list = generate_random_list()
total, minimum, maximum = get_list_stats(input_list=value_list)

task_4_result = (f"Total: {total}\n"
               f"Minimum: {minimum}\n"
               f"Maximum: {maximum}")

print(task_4_result)
