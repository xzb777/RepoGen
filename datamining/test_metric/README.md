## Datamining

This directory contains modules and data used to mine and analyze repository-level metrics. Specifically, it focuses on two core aspects: the **test metric module** and the **processed `repo_metric` data**.

### 1. Test Metric Module

This folder is part of the **Reaper** project, which has recently undergone a major refactor to improve its modularity and scalability. In future releases, we plan to integrate and open-source the method we developed to calculate the proportion of test code within repositories. 

### 2. Processed `repo_metric` Data

The `datamining/test_metric/repo_code_metric_raw.json` file contains the **processed repository metrics**, which include the following:

#### Key Metrics Stored in `repo_code_metric_raw.json`:
1. **Lines of Code (LOC)**:
   - Total LOC broken down by programming language (e.g., Python, JavaScript, etc.).
2. **Comment Lines**:
   - Total number of lines dedicated to comments, helping to assess documentation practices.
3. **Test-Related Metrics**:
   - **Framework Test LOC (via package matching or keyword matching)**: LOC and file counts of test-related files identified by the use of test packages or keyword matching.


