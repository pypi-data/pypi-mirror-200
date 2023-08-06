<h1>Data Analysis CheatSheet (everything you might need )</h1>
<p>
The project include four modules with functions to summarize and analysis dataset in order 
to understand properties and relationships.

  [more info read the documentation](docs/_build/html/index.html)
</p>
<h2>1. DESCRIPTIVE  MODULE</h2>
<h3>Answer the question (What Happen?)</h3>

Includes two modules:

            
- <i>pyeda.py</i><br>
Includes simple EDA functions that might be useful in general cases.<br><br>
  - <i>pydatapreprocessing.py</i><br> 
  Useful Functions for data preprocessing.<br>

          For Example:
          from descriptive import pyeda
          pyeda.distribution_of_numeric_column(data_frame, column_name: str)


          For Example:
          from descriptive import pydatapreprocessing
          pydatapreprocessing.standardization_numerical_columns(data, numerical_column: list)
  <h2>2. DIAGNOSTIC MODULE</h2>
  <h3>Answer the question (Why did it happen?)</h3>
  <i>pydiagnostic.py</i><br><br>
  Include functions to apply hypothesis testing 
          
          For Example:
          from diagnostic import pydiagnostic
          pydiagnostic.test_p_value(p_value:float)   


<h2>3. PREDICTIVE MODULE </h2>
<h3>Answer the question (What is likely to Happen?)</h3>
<i>pypredictive.py</i> <br><br>
The module include functions for:
*    Regression  
*    Forcasting 
*    Classification  
*    Clustering   


        For Example:
        from predictive import pypredictive
        pypredictive.chi_value_plot(data)
<h2>4. PRESCRIPTIVE MODULE</h2> 
<h3>Answer the question (What action should we take?)</h3>

<i>pyprescriptive.py</i><br>

Module include functions that might be useful for classification 

        For Example:
        from prescriptive import pyprescriptive
        pyprescriptive.visualize_confusion_matrix(actual, predicted)