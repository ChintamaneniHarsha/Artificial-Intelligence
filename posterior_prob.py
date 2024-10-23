import sys

def compute_a_posteriori(observations):
    # Define the prior probabilities for the hypotheses
    prior_prob = [0.10, 0.20, 0.40, 0.20, 0.10]
    
    # Define the probabilities for each hypothesis
    candy_likelihoods = [
        [1.0, 0.0],  # h1: 100% cherry
        [0.75, 0.25],  # h2: 75% cherry, 25% lime
        [0.50, 0.50],  # h3: 50% cherry, 50% lime
        [0.25, 0.75],  # h4: 25% cherry, 75% lime
        [0.0, 1.0]  # h5: 100% lime
    ]
    
    # Convert the observation sequence to a list of integers (0 for cherry, 1 for lime)
    ob_sequence = [0 if obs == 'C' else 1 for obs in observations]
    
    # Initialize the posteriors as the priors
    posterior_p = prior_prob.copy()
    
    # Initialize a list to store the posteriors after each observation
    new_posteriors = []
    
    for obs in ob_sequence:
        # Calculate the evidence for the current observation
        evidence = sum(posterior_p[j] * candy_likelihoods[j][obs] for j in range(len(prior_prob)))
        
        # Update the posterior probabilities for each hypothesis
        for i in range(len(prior_prob)):
            posterior_p[i] = (posterior_p[i] * candy_likelihoods[i][obs]) / evidence
        
        # Store the posteriors after this observation
        new_posteriors.append(posterior_p.copy())
    
    # Calculate the probability of the next observation
    next_cherry_prob = sum(posterior_p[i] * candy_likelihoods[i][0] for i in range(len(prior_prob)))
    next_lime_prob = sum(posterior_p[i] * candy_likelihoods[i][1] for i in range(len(prior_prob)))
    
    # Write the results to the "result.txt" file
    with open("result.txt", "w") as f:
        f.write(f"Observation sequence Q: {observations}\n")
        f.write(f"Length of Q: {len(observations)}\n")
        
        for i, obs in enumerate(ob_sequence):
            f.write(f"\nAfter Observation {i+1} = {observations[i]}:\n")
            f.write(f"P(h1 | Q) = {new_posteriors[i][0]:.5f}\n")
            f.write(f"P(h2 | Q) = {new_posteriors[i][1]:.5f}\n")
            f.write(f"P(h3 | Q) = {new_posteriors[i][2]:.5f}\n")
            f.write(f"P(h4 | Q) = {new_posteriors[i][3]:.5f}\n")
            f.write(f"P(h5 | Q) = {new_posteriors[i][4]:.5f}\n")
        
        f.write(f"Probability that the next candy we pick will be C, given Q: {next_cherry_prob:.5f}\n")
        f.write(f"Probability that the next candy we pick will be L, given Q: {next_lime_prob:.5f}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        observations = sys.argv[1]
        compute_a_posteriori(observations)
    else:
        print("Please provide a valid observation sequence.")

