# Privaty Key: secp256k1

Elliptic Curve Cryptography (ECC) is a public-key cryptographic algorithm that utilizes the discrete logarithm problem on elliptic curves to achieve secure communication and encryption.

In ECC, each participant has a public key and a private key. The public key is used for encryption and signature verification, while the private key is used for decryption and signing. The private key is a random number, and the public key is the product of the private key and a point on the elliptic curve. Here's a simple example:

Let's say we choose an elliptic curve, such as secp256k1, with the following parameters:



```go
p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
a = 0
b = 7
G = (x, y)
x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
h = 1
```



Here, `G` is a base point on the elliptic curve, also known as a generator point, and `n` is the order of the base point, which means adding the base point to itself `n` times will result in the identity element.

Now, let's generate a public-private key pair. First, we randomly choose a private key `d`, say `12345`. Then, we multiply the base point `G` by the private key `d` to obtain the public key `Q`:

```go
Q = d * G = (xq, yq)
(xq, yq) = d * (x, y) mod p
```



Plugging in `d=12345` and `G=(x,y)`, we get:

```
(xq, yq) = 12345 * (x, y) mod p
xq = 0xf00f92b4e8b4c4f9d4d4ce4ba77eaa18b49c3a41fa47eeeb79f42bb41dfedc18
yq = 0x58b41f8b62c44e79aafa5d0a6f9362965a5c6a5d0e56df186b35eb66691dcb21
```

Now, we have a public-private key pair, where the private key is `d=12345` and the public key is `(xq, yq)`.



### Ethereum

There is no particular reason why Ethereum uses the spec256k1 curve, mainly because the security of this curve has been verified by Bitcoin, and there are a large number of third-party libraries that already support this algorithm.

secp256k1:

- y² = x³ + 7
- R：2^256 - 2^32 - 977
- Base point：G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
- n：0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141



If k=2，the result should be 2G.

```
G = (0, 7)
2G = G + G = (x3, y3)
```



If we use addition calculation, then we directly calculate the address of the public key as (x3=0, y3=14), but unfortunately, the coordinates of the public key obtained by this method are not on the curve y² = x³ + 7. On elliptic curves, we will modify the definition of point plus.

The self-summation of points on the elliptic curve is the symmetric point along the y-axis to the intersection point of the tangent of the curve and the curve.

We will use mathematics to prove that the calculation of this point is not complicated.

for a point（x1, y1}，

```go
y' = (3 * x²) / (2 * y)

// use x1 and y1= sqrt(x³ + 7),
k = y' = (3 * x1²) /  (2 * y1)
```

Use y - y1 = k(x - x1)

```go
y - y1 = k * (x - x1)
k = (3 * x1²) / ( 2 * y1)

// remove y 
(k * (x - x1))^2 =  x³ + 7


x³ -  k² * x² + (2kx1 - 2ky1) * x + b -  (kx1 - y1)² = 0
```

A cubic equation whose solution corresponds to the abscissas x1 , x2 , x3 of the three intersection points of the straight line and the elliptic curve

According to Vieta's Formulas, the three roots x1 , x2 , x3  of the cubic equation have the following relationship:

```go
x1 + x2 + x3 = - b / a = k ^ 2

// x1 = x2
k = y' = (3 * x1²) /  (2 * y1)

// we get the result.
x3 = k^2 - 2x1
y3 = k(x1 - x3) - x1
```



In Ethereum, the base point is usually G=(0,1). The process for generating the public key is as follows:

1. Represent the private key as a 32-byte (256-bit) integer.
2. Use the private key to multiply the elliptic curve base point to get the public key point. Specifically, the public key point is the scalar product of the private key and the base point. The formula is: public key point = private key × G.
3. The public key point is another point on the elliptic curve, consisting of x and y coordinates. These coordinates are both 256-bit integers and can be represented as hexadecimal strings.

After generating the public key, Ethereum hashes it to produce a shorter address. This process is called the ripemd160 hash. Essentially, it uses a hashing function to convert the public key to a 20-byte address, which is typically represented as a hexadecimal string for an Ethereum address. The prefix for an Ethereum address is typically 0x, indicating it is a hexadecimal number.

It's important to note that the Ethereum address is actually a hash of the public key, not the public key itself. This hashing mechanism makes Ethereum addresses shorter and more convenient for transactions and storage.



### Address

In the elliptic curve algorithm, the public key is derived from the private key and the elliptic curve base point. Since the private key is a 256-bit random number, the probability of two different private keys generating the same public key is very low, even among all the possible private keys in the universe. Therefore, the uniqueness of the public key is generally guaranteed.

However, the public key does not necessarily correspond uniquely to an address. In Ethereum, the address is actually a hash of the public key. The hash function converts the public key into a 20-byte address, but different public keys may produce the same hash value, leading to address collisions.

To avoid this, Ethereum uses a very large address space, typically represented as 2 to the power of 160. This means that in theory, there can be approximately 1.46×10 to the power of 48 possible addresses, making the probability of address collisions very low. Additionally, Ethereum addresses typically check and reject new addresses that are the same as existing addresses, further reducing the likelihood of address collisions and ensuring the uniqueness of addresses.



### Summary

1. The private key of Ethereum can quickly calculate the public key.
2. It is almost impossible to deduce the private key from the public key.