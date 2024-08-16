import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives import serialization

# Generate key pair
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Display algorithm used
print("EC")

# Display the public and private keys (PEM format)
pem_priv = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
pem_pub = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("\n\n")
print("Public Key:\n", pem_pub.decode('utf-8'))
print("Private Key:\n", pem_priv.decode('utf-8'))

# Data to be signed
intent_url = (
    "upi://pay?ver=01&mode=05&orgId=700004&tid=TESTGST123456qazqwe12345hs29hnd1qa2&tr=MerRef123&tn=GST%20QR"
    "&category=02&url=https://www.test.com&pa=merchant@npci&pn=Test%20Merchant&mc=5411&am=100.00&cu=INR&mid=TST5432"
    "&msid=TSTABC123&mtid=TSTABC1234&gstBrkUp=CGST:08.45|SGST:08.45&qrMedium=02&invoiceNo=BillRef123&invoiceDate=2019-06-11T13:21:50+05:30"
    "&invoiceName=Dummy%20Customer&QRexpire=2019-06-11T13:21:50+05:30&QRts=2019-06-12T13:21:50+05:30&pinCode=400063"
    "&tier=TIER1&gstIn=GSTNUM1234567890"
)
print("\nintentURL:", intent_url)
intent_url_bytes = intent_url.encode('utf-8')

# Sign data
signature = private_key.sign(
    intent_url_bytes,
    ec.ECDSA(hashes.SHA256())
)

# Base64 encode the signature
encoded_signature = base64.b64encode(signature).decode('utf-8')

# Append the signature to the URL
final_bhim_url = intent_url + "&sign=" + encoded_signature
print("\nSignature:", signature.hex())
print("\nEncoded Signature:", encoded_signature)
print("\nFinal BHIM URL:", final_bhim_url)

# Decode the signed URL
bhim_received_url = final_bhim_url.split("&sign=")
decoded_signature = base64.b64decode(bhim_received_url[1])
print("\nDecoded Signature:", decoded_signature.hex())

# Verify the signature
verifier = public_key.verify(
    decoded_signature,
    bhim_received_url[0].encode('utf-8'),
    ec.ECDSA(hashes.SHA256()),
)
print(verifier)
#verifier.update(bhim_received_url[0].encode('utf-8'))
try:
    verifier.verify()
    verified = True
except:
    verified = False

print("\nSignature Verify Result:", verified)
