from math import factorial

class ComponentsData:
    def __init__(self, mu, lam, real_mu, real_lam, busy_times, requests_wtimes, no_taken_requests):
        self.mu = mu
        self.lam = lam
        self.real_mu = real_mu
        self.real_lam = real_lam
        self.channel_count = len(busy_times)
        self.busy_times = busy_times
        self.requests_waiting_times = requests_wtimes
        self.no_taken_requests = no_taken_requests
        self.theoretical_metrics = self.calculate_metrics(self.channel_count, self.mu, self.lam)
        self.real_metrics = self.calculate_metrics(self.channel_count, self.real_mu, self.real_lam)

    def calculate_metrics(self, n, mu, lam):
        rho = lam / (n * mu)
        alpha = lam / mu

        P0 = 1 / (sum([alpha ** k / factorial(k) for k in range(n)]) +
                  (alpha ** n / (factorial(n) * (1 - rho))) if rho < 1 else float("inf"))

        probabilities = [P0] + [
            P0 * (alpha ** k) / factorial(k) for k in range(1, n)
        ]

        P_queue = (P0 * alpha ** n) / (factorial(n) * (1 - rho)) if rho < 1 else 1

        L_queue = (P_queue * rho) / (1 - rho) if rho < 1 else float("inf")
        L_system = L_queue + alpha
        W_queue = L_queue / lam if lam else 0
        W_system = L_system / lam if lam else 0

        return {
            "P0": P0,
            "P_queue": P_queue,
            "L_queue": L_queue,
            "L_system": L_system,
            "W_queue": W_queue,
            "W_system": W_system,
        }

    def __str__(self):
        output = []
        output.append("Theoretical Metrics:")
        for key, value in self.theoretical_metrics.items():
            output.append(f"  {key}: {value:.4f}")

        output.append("\nReal Metrics:")
        for key, value in self.real_metrics.items():
            output.append(f"  {key}: {value:.4f}")

        output.append("\nAdditional Data:")
        output.append(f"  Channel count: {self.channel_count}")
        output.append(f"  Set processing intensity: {self.mu}")
        output.append(f"  Real processing intensity: {self.real_mu}")
        output.append(f"  Set requests intensity: {self.lam}")
        output.append(f"  Real requests intensity: {self.real_lam}")
        output.append(f"  Set reduced intensity: {self.lam / self.mu}")
        output.append(f"  Real reduced intensity: {self.real_lam / self.real_mu}")
        output.append(f"  Total Busy Times: {sum(self.busy_times):.4f}")
        output.append(f"  Average Busy Time: {sum(self.busy_times) / len(self.busy_times) if self.busy_times else 0:.4f}")
        output.append(f"  Average Waiting Time: {sum(self.requests_waiting_times) / len(self.requests_waiting_times) if self.requests_waiting_times else 0:.4f}")
        output.append(f"  Number of unprocessed requests: {self.no_taken_requests}")

        return "\n".join(output)


    