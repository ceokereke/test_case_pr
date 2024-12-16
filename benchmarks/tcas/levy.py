import numpy as np
import math

def levy_flight(n: int, beta: float = 1.5) -> np.ndarray:
    """
    Generates a series of steps following a Lévy flight distribution.

    Parameters:
    - n (int): Number of Lévy flight steps to generate. Must be positive.
    - beta (float): Stability parameter (default is 1.5). Determines the heavy-tailed nature of the distribution.

    Returns:
    - np.ndarray: Array of Lévy flight steps.
    
    Raises:
    - ValueError: If 'n' is not a positive integer or if 'beta' is less than 1.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Parameter 'n' must be a positive integer.")
    if beta <= 1:
        raise ValueError("Parameter 'beta' must be greater than 1 for stable Lévy flights.")

    # Calculate the scaling factor sigma
    sigma = (
        (math.gamma(1 + beta) * math.sin(math.pi * beta / 2)) /
        (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2))
    ) ** (1 / beta)

    # Generate Lévy flight steps
    u = np.random.normal(0, sigma, n)
    v = np.random.normal(0, 1, n)
    steps = u / np.abs(v) ** (1 / beta)

    return steps

# Example usage
if __name__ == "__main__":
    steps = levy_flight(100)
    step2 = max(1, int(abs(levy_flight(1)[0])))
    print(steps,step2,int(abs(levy_flight(1)[0])))