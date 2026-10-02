# Generic Assembly Line Simulation & Capacity Optimization

##  Project Overview
This project simulates the workload distribution, operator utilization, and total cycle time for a generic multi-station assembly line. It is designed to model both sequential and parallel operations, optimizing the allocation of operators across dependent and independent tasks. 

By utilizing **Heuristic Task Assignment** and **Queue Modeling**, this simulation provides a direct approach to balancing assembly lines, identifying bottlenecks, and minimizing operator idle times without relying on expensive commercial simulation software.

##  Key Objectives
*   **Capacity Planning:** Calculate the total makespan for multiple production orders consisting of various product types.
*   **Workload Balancing:** Dynamically assign single-operator and joint-operator  tasks based on current operator availability.
*   **Idle Time Tracking:** Measure operator wait times caused by task dependencies.
*   **Automated Reporting:** Generate a comprehensive Excel report detailing every operation timestamp and cumulative summary metrics.

##  Features & Methodology
*   **Dynamic Task Allocation:**
    *   `assign_single_task`: Assigns a task to the operator with the minimum current load.
    *   `assign_joint_task_no_wait`: Distributes asynchronous collaborative tasks evenly among operators.
    *   `assign_joint_task_with_wait`: Models synchronous tasks where one operator must wait for another before starting.
*   **Scenario Modeling:** Simulates two distinct production workflows (`Assembly Line A` and `Assembly Line B`) with varying product configurations and constraints.
*   **Data Export:** Utilizes `pandas` and `openpyxl` to export detailed Gantt-style event logs and operator efficiency summaries.

##  How to Run
1. Ensure you have Python 3.14 installed along with the required libraries:
   ```bash
   pip install pandas openpyxl
   
##  Repository Structure
* generic_assembly_simulation.py: The main simulation script.
* README.md: Project documentation.

##  Author
Mustafa Cesmeli
Industrial Engineer
https://www.linkedin.com/in/mustafacesmeli/ | cesmelimustafa0@gmail.com
