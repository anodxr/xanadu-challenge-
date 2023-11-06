### DO NOT CHANGE ANYTHING BELOW THIS LINE

import pennylane as qml
from pennylane import numpy as np

WIRES = 2
LAYERS = 5
NUM_PARAMETERS = LAYERS * WIRES * 3

def variational_circuit(params,hamiltonian):
    """
    This is a template variational quantum circuit containing a fixed layout of gates with variable
    parameters. To be used as a QNode, it must either be wrapped with the @qml.qnode decorator or
    converted using the qml.QNode function.

    The output of this circuit is the expectation value of a Hamiltonian, somehow encoded in
    the hamiltonian argument

    Args:
        - params (np.ndarray): An array of optimizable parameters of shape (30,)
        - hamiltonian (np.ndarray): An array of real parameters encoding the Hamiltonian
        whose expectation value is returned.
    
    Returns:
        (float): The expectation value of the Hamiltonian
    """
    parameters = params.reshape((LAYERS, WIRES, 3))
    qml.templates.StronglyEntanglingLayers(parameters, wires=range(WIRES))
    return qml.expval(qml.Hermitian(hamiltonian, wires = [0,1]))

def optimize_circuit(hamiltonian):
    """Minimize the variational circuit and return its minimum value.
    You should create a device and convert the variational_circuit function 
    into an executable QNode. 
    Next, you should minimize the variational circuit using gradient-based 
    optimization to update the input params. 
    Return the optimized value of the QNode as a single floating-point number.

    Args:
        - params (np.ndarray): Input parameters to be optimized, of dimension 30
        - hamiltonian (np.ndarray): An array of real parameters encoding the Hamiltonian
        whose expectation value you should minimize.
    Returns:
        float: the value of the optimized QNode
    """
        
    hamiltonian = np.array(hamiltonian, requires_grad = False)

    hamiltonian = np.array(hamiltonian,float).reshape((2 ** WIRES), (2 ** WIRES))

    ### WRITE YOUR CODE BELOW THIS LINE
    
    ### Solution Template

    dev = qml.device("xanaduchallenge.QuantumSimulator", wires=WIRES) 

    circuit = qml.QNode(variational_circuit, dev)

    # Write your code to minimize the circuit

    # Initialize the parameters randomly
    params = np.random.uniform(0, 2*np.pi, size=NUM_PARAMETERS)

    # Define the cost function as the negative expectation value of the Hamiltonian
    def cost(params):
        return -circuit(params, hamiltonian)

    # Use a gradient-based optimizer to minimize the cost function
    opt = qml.GradientDescentOptimizer(stepsize=0.1)
    steps = 100 # Number of optimization steps
    for i in range(steps):
        params = opt.step(cost, params)
        print(f"Step {i+1}: Cost = {cost(params)}")

    # Return the optimized value of the QNode
    return circuit(params, hamiltonian)

