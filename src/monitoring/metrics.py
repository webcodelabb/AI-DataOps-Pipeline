from prometheus_client import Counter, Histogram, Gauge


class _Metrics:
	def __init__(self) -> None:
		self.request_counter = Counter("api_requests_total", "Total API requests")
		self.request_latency = Histogram("api_request_latency_seconds", "API request latency")
		self.feedback_abs_error = Histogram("feedback_abs_error", "Absolute error from feedback")
		self.model_version = Gauge("model_version", "Model version as numeric epoch")

	def observe_feedback(self, prediction: float, label: float) -> None:
		self.feedback_abs_error.observe(abs(prediction - label))


metrics = _Metrics()
