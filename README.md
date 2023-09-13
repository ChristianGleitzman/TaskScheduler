# Task Scheduler

This project is a task scheduling application with a user-friendly interface that helps you plan your day efficiently. You can input tasks, update their start/end times, and specify your break time preferences. The application takes into account task priority and ensures that tasks do not overlap with your breaks.

## Features
- Task Input: Easily input your tasks, including their names, priorities, durations, and dependencies.
- Task Scheduling: The application schedules tasks based on priority and duration, ensuring efficient use of your available time.
- Break Management: Specify when you want to take breaks, and the scheduler will avoid scheduling tasks during these times.
- View Schedule: View your scheduled tasks in a table format to get a clear overview of your day.

## Screenshots

![Adding a task](https://github.com/ChristianGleitzman/TaskScheduler/blob/imgs/add_task.PNG)
![Saving Settings](https://github.com/ChristianGleitzman/TaskScheduler/blob/imgs/save_settings.PNG)
![Viewing Tasks](https://github.com/ChristianGleitzman/TaskScheduler/blob/imgs/view_task.PNG)

## Possible Improvements
- Efficient Scheduling Algorithm: The current scheduling algorithm is functional but might not always be the most efficient. Improving the algorithm to optimize task scheduling can be a complex task, but it could lead to better utilization of available time and resources.
- Task Dependencies: The current scheduler is more useful for tasks that are independent from each other. The algorithm could be further improved to consider tasks that may depend on one another, as to not schedule a task before one it depends on.
- Permanent Task Storage: All tasks are currently stored during run time so disappear after the program has finished running so the program could be improved to store tasks permanently in a text file for example.
  
### Prerequisites For Running
- Python 3.x
- PyQt5 (for the user interface)
