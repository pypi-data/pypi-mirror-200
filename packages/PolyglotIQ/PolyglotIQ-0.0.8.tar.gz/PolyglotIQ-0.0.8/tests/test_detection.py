import time
from polyglotiq import DetectionModel, RuleFilter


detector = DetectionModel("cpu")


start = time.time()
print(detector.detect(["Hello",]).language_codes)
end = time.time()

print(end - start, "s")