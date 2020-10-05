<h1> high_school_optics</h1>
<h2> SCRIPT: sogpy.py</h2>
<p>
  This script solves basic optical problems, considering the paraxial aproximation</p>
  
   --------------------------------------------------------------------------
<h4> FUNCTION: optic_system</h4>
<p>
  Function optic system takes the following arguments:

      - sys ---> Kind of eq system to solve acording the optical system we are working in
      - Vars---> SymPy symbolic variables to use with the eq system

  This function returns the SymPy system to solve acording sys value </p>

  --------------------------------------------------------------------------
<h4> CLASS: geometrical_optics</h4>
<p>Class geometrical_optics takes the following aguments:

      - f ---> focal distance
      - f'---> focal image distance
      - n ---> refractive index of the first medium
      - n'---> refractive index of the second medium (if exists)
      - y ---> object height
      - y'---> image height
      - s ---> distance between the object and the optical system (X axis)
      - s'---> distance between the image and the optical system (X axis)
      - P ---> power of the lsen (if exists)
      - Ml---> lateral raise

  For unknown arguments just don't pass them to the function 
  Using CMD set them blank (not yet)

  This class has 3 functions:

      - __init__ ---> initializes variables
      - generate ---> 
      - Plot     --->
 </p>
