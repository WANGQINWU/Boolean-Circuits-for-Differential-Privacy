# Boolean-Circuits-for-Differential-Privacy

The project develops a randomized response in boolean circuits solved via SAT problem solver engine, Z3.
## Structure
In BooleanCircuit folder, there are three core classes.
```
BC.py
BC_Stat.py
RRclass.py
```

BC.py contains functions for generation. 

### Example
```
from BC import BcSequence

bcSequence = BcSequence( seq ) // seq is array for boolean circuits info, like [0,0]
bcSequence.get_out_bc() // return representation of boolean circuit without any constrains.
bcSequence.getbc() // return representation of boolean circuit with output != input constrain.
bcSequence.get_t_bc() // return representation of boolean circuit with output != input, input == true constrains.
bcSequence.get_f_bc() // return representation of boolean circuit with output != input, input == false constrain.

output = bcSequence.get_output_with_random(input_of_bc, random) //input_of_bc = 0 or 1, random is arrary of random bits. here length of boolean circuit is 2 (length of seq), like [0, 1].

output = bcSequence.get_outputs(inputs_of_bc, randomizer) // randomizer is instance of Randomize class, inputs is like [0, 0, 0, 1]
```
BC_Stat is the father class for BC.py containing iteration models function and probability calculations. 

### Example
