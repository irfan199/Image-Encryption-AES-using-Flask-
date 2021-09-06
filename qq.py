from Crypto.Hash import SHA256
hash = SHA256.new()
hash.update('message')
print(hash.digest())
print("yeess")
