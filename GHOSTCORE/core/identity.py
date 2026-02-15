import hashlib
import time

class IdentityKernel:
    def __init__(self, author="Šabad"):
        self.author = author

    def watermark(self, content):
        stamp = f"{self.author}-{int(time.time())}"
        digest = hashlib.sha256(stamp.encode()).hexdigest()
        return f"\n\n[GHOSTCORE-ID:{digest[:12]}]"
